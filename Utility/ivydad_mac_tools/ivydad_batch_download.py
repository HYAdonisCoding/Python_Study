#!/usr/bin/env python3
"""Organize and download IvyDad course media from saved API response JSON files.

Input: one or more .json/.jsonl files containing video-detail API response bodies.
No login automation or token handling is performed.

改下载位置：修改下面的 DEFAULT_OUTPUT_DIR，可写绝对路径。
"""
from __future__ import annotations
import argparse, csv, json, os, re, ssl, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPSHandler, ProxyHandler

DEFAULT_OUTPUT_DIR = '/Users/adam/Downloads/常青藤爸爸/中国名胜古迹与山水名片'
DEFAULT_LAYOUT = 'single'
DEFAULT_USE_PROXY = False
DEFAULT_NAMING_MAP = 'series.json'

VIDEO_EXTS = {'.mp4', '.m4v', '.mov'}

def safe_name(value: str, fallback: str = 'untitled') -> str:
    value = re.sub(r'[\\/:*?"<>|\x00-\x1f]', '_', str(value or '')).strip(' .')
    value = re.sub(r'\s+', ' ', value)
    return (value[:120] or fallback)

def iter_json_files(path: Path):
    if path.is_file():
        yield path
    else:
        yield from sorted(p for p in path.rglob('*') if p.is_file() and p.suffix.lower() in {'.json', '.jsonl'})

def load_records(file: Path):
    try:
        if file.suffix.lower() == '.jsonl':
            for line_no, line in enumerate(file.read_text(encoding='utf-8-sig').splitlines(), 1):
                if line.strip():
                    try: yield json.loads(line)
                    except json.JSONDecodeError as e: print(f'[跳过] {file}:{line_no}: {e}', file=sys.stderr)
        else:
            yield json.loads(file.read_text(encoding='utf-8-sig'))
    except (OSError, json.JSONDecodeError) as e:
        print(f'[跳过] 无法读取 {file}: {e}', file=sys.stderr)

def load_naming_map(path: Path):
    """读取 id -> {stem, episode} 的系列命名表；文件不存在则返回空表。"""
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        return {str(k): v for k, v in data.items()
                if not str(k).startswith('_') and isinstance(v, dict)}
    except (OSError, json.JSONDecodeError) as e:
        print(f'[跳过] 命名表读取失败 {path}: {e}', file=sys.stderr)
        return {}

def find_video_objects(obj):
    """Find response objects containing a title and a media URL."""
    if isinstance(obj, dict):
        url = obj.get('url') or obj.get('backup_url')
        title = obj.get('title')
        if isinstance(url, str) and url.startswith(('https://', 'http://')) and title:
            yield obj
        for value in obj.values():
            yield from find_video_objects(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from find_video_objects(value)

def make_opener(use_proxy: bool, ca_bundle: str, insecure: bool):
    """默认直连并保留 TLS 校验；抓包代理会重签证书，Python 不认其自签 CA。"""
    ctx = ssl.create_default_context()
    if ca_bundle:
        ctx.load_verify_locations(cafile=ca_bundle)
    if insecure:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    handlers = [HTTPSHandler(context=ctx)]
    if not use_proxy:
        handlers.append(ProxyHandler({}))
    return build_opener(*handlers)

def download(url: str, target: Path, net_opts: dict, retries: int = 3):
    opener = make_opener(**net_opts)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return '已存在'
    part = target.with_suffix(target.suffix + '.part')
    for attempt in range(1, retries + 1):
        try:
            offset = part.stat().st_size if part.exists() else 0
            headers = {'User-Agent': 'IvyDadMediaOrganizer/1.0'}
            if offset:
                headers['Range'] = f'bytes={offset}-'
            req = Request(url, headers=headers)
            with opener.open(req, timeout=45) as response:
                status = getattr(response, 'status', 200)
                if offset and status != 206:
                    offset = 0
                    part.unlink(missing_ok=True)
                mode = 'ab' if offset and status == 206 else 'wb'
                content_type = response.headers.get('Content-Type', '').lower()
                if 'text/html' in content_type:
                    raise RuntimeError('服务器返回了 HTML，而不是媒体文件（可能需要官方授权访问）')
                with part.open(mode) as out:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk: break
                        out.write(chunk)
            if part.stat().st_size == 0:
                raise RuntimeError('下载结果为空')
            part.replace(target)
            return '下载完成'
        except Exception as e:
            if attempt == retries:
                part.unlink(missing_ok=True)
                raise RuntimeError(str(e))
            time.sleep(attempt * 2)

def main():
    ap = argparse.ArgumentParser(description='从已保存的课程视频 API JSON 中整理并下载媒体')
    ap.add_argument('-i', '--input', required=True, help='JSON 文件或包含 JSON/JSONL 的目录')
    ap.add_argument('-o', '--output', default=DEFAULT_OUTPUT_DIR, help='输出目录；命令行优先，默认取脚本顶部 DEFAULT_OUTPUT_DIR')
    ap.add_argument('-w', '--workers', type=int, default=3, help='并发数，默认 3')
    ap.add_argument('--layout', choices=['single', 'by-episode', 'per-video'], default=DEFAULT_LAYOUT,
                    help='single=全部平铺（默认）；by-episode=按集分文件夹；per-video=每个视频一个子文件夹')
    ap.add_argument('--naming-map', default='', help='系列命名表 JSON；默认读脚本同目录的 series.json')
    ap.add_argument('--adopt', action='store_true', help='把已下载的旧命名文件改名复用，避免重新下载')
    ap.add_argument('--dry-run', action='store_true', help='只预览将要下载的路径，不联网、不写文件')
    ap.add_argument('--use-proxy', action='store_true', default=DEFAULT_USE_PROXY,
                    help='走系统/环境代理；默认直连，避开 Proxyman 等抓包代理的自签证书')
    ap.add_argument('--ca-bundle', default='', help='追加信任的 CA 证书 PEM，配合 --use-proxy 使用')
    ap.add_argument('--insecure', action='store_true', help='跳过 TLS 证书校验（不推荐，仅确认代理可信时用）')
    args = ap.parse_args()
    source, outdir = Path(args.input).expanduser(), Path(args.output).expanduser()
    if not source.exists(): ap.error(f'输入路径不存在: {source}')
    if args.ca_bundle and not Path(args.ca_bundle).expanduser().is_file():
        ap.error(f'CA 证书文件不存在: {args.ca_bundle}')
    naming_path = Path(args.naming_map).expanduser() if args.naming_map else Path(__file__).resolve().parent / DEFAULT_NAMING_MAP
    naming_map = load_naming_map(naming_path)
    items, seen = [], set()
    for file in iter_json_files(source):
        for root in load_records(file):
            for obj in find_video_objects(root):
                key = (str(obj.get('id', '')), obj.get('url'))
                if key in seen: continue
                seen.add(key)
                rule = naming_map.get(str(obj.get('id', '')), {})
                raw_stem = obj.get('local_stem') or rule.get('stem') or obj.get('title') or 'untitled'
                raw_episode = obj.get('episode') or rule.get('episode') or ''
                items.append({
                    '_idx': len(items),
                    'id': obj.get('id', ''), 'title': str(obj.get('title') or 'untitled'),
                    'stem': safe_name(raw_stem),
                    'episode': safe_name(raw_episode) if raw_episode else '',
                    'duration': obj.get('duration', ''), 'url': obj.get('url') or obj.get('backup_url'),
                    'backup_url': obj.get('backup_url', ''), 'subtitle': obj.get('subtitle', ''),
                    'subtitle_type': obj.get('subtitle_type', ''), 'source_json': str(file)
                })
    if not items:
        print('没有找到同时包含 title 和 url/backup_url 的视频对象。请确认输入是课程 video 接口的 JSON 响应正文。')
        return 2
    jobs = []
    stem_counts = {}
    for item in items:
        s = item['stem']
        stem_counts[s] = stem_counts.get(s, 0) + 1
    for item in items:
        stem = item['stem']
        if stem_counts[stem] > 1 and args.layout != 'per-video':
            stem = f"{stem} [{safe_name(str(item['id']), 'no-id')}]"
        if args.layout == 'per-video':
            folder = outdir / f"{stem} [{safe_name(str(item['id']), 'no-id')}]"
        elif args.layout == 'by-episode':
            folder = outdir / (item['episode'] or '未分集')
        else:
            folder = outdir
        item['local_video'] = str(folder / f'{stem}.mp4')
        item['local_subtitle'] = str(folder / f'{stem}.srt') if item['subtitle'] else ''
        jobs.append((item, 'video', item['url'], Path(item['local_video'])))
        if item['subtitle']:
            jobs.append((item, 'subtitle', item['subtitle'], Path(item['local_subtitle'])))
    adoptions = []
    for item in items:
        old_stem = safe_name(item['title'])
        if old_stem == item['stem']:
            continue
        for kind in ('video', 'subtitle'):
            raw_new = item['local_video'] if kind == 'video' else item['local_subtitle']
            if not raw_new:
                continue
            new = Path(raw_new)
            old = outdir / f"{old_stem}{new.suffix}"
            if old == new or not old.is_file() or old.stat().st_size == 0 or new.exists():
                continue
            adoptions.append((old, new))
    if adoptions:
        print(f'[发现] {len(adoptions)} 个已下载文件可改名复用，不用重新下载：')
        for old, new in adoptions:
            print(f'  {old.name}  ->  {new.relative_to(outdir)}')
        if args.dry_run:
            print('  （预览模式，不改动文件）')
        elif args.adopt:
            for old, new in adoptions:
                new.parent.mkdir(parents=True, exist_ok=True)
                old.rename(new)
                print(f'[改名] {old.name} -> {new.name}')
        else:
            print('  加 --adopt 才实际改名；不加则会按新名字重新下载')
    if args.dry_run:
        print(f'[预览] 输出目录：{outdir.resolve()}')
        for item in items:
            print(f"  {item['stem']}  <-  {item['title']}")
            print(f"    视频 -> {Path(item['local_video']).resolve()}")
            if item['local_subtitle']:
                print(f"    字幕 -> {Path(item['local_subtitle']).resolve()}")
        print(f"  清单 -> {(outdir / '课程清单.csv').resolve()}")
        return 0
    if args.insecure:
        print('[警告] 已跳过 TLS 证书校验，仅在你确认代理可信时使用', file=sys.stderr)
    net_opts = {'use_proxy': args.use_proxy,
                'ca_bundle': str(Path(args.ca_bundle).expanduser()) if args.ca_bundle else '',
                'insecure': args.insecure}
    outdir.mkdir(parents=True, exist_ok=True)
    results = {}
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as pool:
        future_map = {pool.submit(download, url, target, net_opts): (item, kind) for item, kind, url, target in jobs}
        for future in as_completed(future_map):
            item, kind = future_map[future]
            key = (item['_idx'], kind)
            try:
                status = future.result()
                print(f'[完成] {item["stem"]} / {kind}: {status}')
                results[key] = status
            except Exception as e:
                print(f'[失败] {item["stem"]} / {kind}: {e}', file=sys.stderr)
                results[key] = f'失败: {e}'
    manifest = outdir / '课程清单.csv'
    fields = ['id', 'stem', 'episode', 'title', 'duration', 'url', 'backup_url', 'subtitle', 'subtitle_type', 'local_video', 'local_subtitle', 'video_status', 'subtitle_status', 'source_json']
    with manifest.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader()
        for item in items:
            row = dict(item)
            row['video_status'] = results.get((item['_idx'], 'video'), '未处理')
            row['subtitle_status'] = results.get((item['_idx'], 'subtitle'), '无字幕') if item['subtitle'] else '无字幕'
            writer.writerow({k: row.get(k, '') for k in fields})
    print(f'\n共识别 {len(items)} 个视频。清单：{manifest.resolve()}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
