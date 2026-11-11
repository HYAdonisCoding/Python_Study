#!/usr/bin/env python3
"""Batch extract audio tracks from video files using ffmpeg.

给一个含多个子文件夹的课程根目录即可：递归扫描所有视频，输出保持完全相同的
子文件夹结构（Audio/<子文件夹>/<原名>.m4a），并按子文件夹分组打印进度与汇总。
同名 SRT 会转成 LRC 歌词，并复制一份 SRT 到音频旁供播放器加载。
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 改默认输出格式只改这一行：'m4a'（Apple 生态原生，源音轨是 AAC 时可无损直拷）/ 'mp3'（老设备通用）
DEFAULT_FORMAT = 'm4a'
DEFAULT_BITRATE = '192k'
# 不写 -o 时，在输入目录下创建的输出文件夹名
DEFAULT_OUTPUT_DIRNAME = 'Audio'

VIDEO_EXTS = {'.mp4', '.m4v', '.mov', '.mkv', '.avi', '.webm'}
TIME_RE = re.compile(r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->')
CN_DIGITS = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
             '六': 6, '七': 7, '八': 8, '九': 9}
# PATH 里没有 Homebrew 时（部分 GUI / 定时任务环境）仍要能找到 ffmpeg
BIN_DIRS = ('/usr/local/bin', '/opt/homebrew/bin', '/opt/local/bin', '/usr/bin')
_BIN_CACHE: dict[str, str] = {}


def find_bin(name: str) -> str:
    """Locate ffmpeg/ffprobe via PATH or common Homebrew/MacPorts prefixes."""
    if name not in _BIN_CACHE:
        hit = shutil.which(name) or ''
        if not hit:
            for folder in BIN_DIRS:
                cand = Path(folder) / name
                if cand.is_file() and os.access(cand, os.X_OK):
                    hit = str(cand)
                    break
        _BIN_CACHE[name] = hit
    return _BIN_CACHE[name]


def probe_audio_codec(video: Path, ffprobe: str) -> str:
    """Return the first audio stream's codec, or '' when ffprobe is unavailable."""
    if not ffprobe:
        return ''
    try:
        r = subprocess.run(
            [ffprobe, '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_name', '-of', 'default=nw=1:nk=1', str(video)],
            capture_output=True, text=True, errors='replace', timeout=20)
        lines = r.stdout.strip().splitlines()
        return lines[0].strip() if r.returncode == 0 and lines else ''
    except (subprocess.SubprocessError, OSError):
        return ''


def parse_srt(path: Path):
    """Yield (start_seconds, [text lines]) for each subtitle cue."""
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    for block in re.split(r'\r?\n\s*\r?\n', text.strip()):
        rows = [r.strip() for r in block.splitlines() if r.strip()]
        if not rows:
            continue
        start, text_at = None, 0
        for i, row in enumerate(rows[:3]):
            m = TIME_RE.match(row)
            if m:
                h, mm, ss, ms = m.groups()
                start = int(h) * 3600 + int(mm) * 60 + int(ss) + int(ms.ljust(3, '0')[:3]) / 1000
                text_at = i + 1
                break
        if start is not None:
            yield start, rows[text_at:]


def has_cjk(text: str) -> bool:
    return bool(re.search(r'[\u3400-\u9fff]', text))


def make_lrc(cues, lang: str, title: str) -> str:
    out = [f'[ti:{title}]']
    for seconds, rows in cues:
        if lang == 'zh':
            rows = [r for r in rows if has_cjk(r)]
        elif lang == 'en':
            rows = [r for r in rows if not has_cjk(r)]
        if not rows:
            continue
        minutes = int(seconds // 60)
        secs = seconds - minutes * 60
        out.append(f'[{minutes:02d}:{secs:05.2f}]' + ' / '.join(rows))
    return '\n'.join(out) + '\n'


def write_lyrics(video: Path, audio: Path, lang: str) -> tuple[int, str]:
    """Generate .lrc + copy .srt next to audio. Returns (cue count, state)."""
    srt = video.with_suffix('.srt')
    if not srt.is_file():
        return 0, '无字幕'
    cues = list(parse_srt(srt))
    if not cues:
        return 0, '时间轴为空'
    lrc = audio.with_suffix('.lrc')
    content = make_lrc(cues, lang, video.stem)
    changed = False
    if not lrc.is_file() or lrc.read_text(encoding='utf-8', errors='replace') != content:
        lrc.write_text(content, encoding='utf-8')
        changed = True
    srt_dest = audio.with_suffix('.srt')
    try:
        if not srt_dest.is_file() or srt.read_bytes() != srt_dest.read_bytes():
            shutil.copy2(srt, srt_dest)
            changed = True
    except shutil.SameFileError:
        pass
    return len(cues), ('已生成' if changed else '已存在')


def target_audio(rel: Path, dest_root: Path, fmt: str) -> Path:
    """Mirror the input relative path (including subfolders) under dest_root."""
    return (dest_root / rel).with_suffix('.' + fmt)


def collect(src: Path, dest_root: Path, only: list[str]) -> dict[str, list[tuple[Path, Path]]]:
    """Group videos by their first-level subfolder under src. '' = files at root."""
    if src.is_file():
        if src.suffix.lower() not in VIDEO_EXTS:
            return {}
        return {'': [(src, Path(src.name))]}
    groups: dict[str, list[tuple[Path, Path]]] = {}
    # 仅当输出目录位于输入目录「内部」时才需要排除；dest_root == src 时不能排除，
    # 否则会把所有输入都过滤掉。
    skip_dir = dest_root if src in dest_root.parents else None
    for path in sorted(src.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in VIDEO_EXTS:
            continue
        if skip_dir and skip_dir in path.parents:  # 别把输出目录里的东西再当输入
            continue
        rel = path.relative_to(src)
        group = rel.parts[0] if len(rel.parts) > 1 else ''
        groups.setdefault(group, []).append((path, rel))
    if only:
        keys = [k.lower() for k in only]
        groups = {g: fs for g, fs in groups.items()
                  if g and any(k in g.lower() for k in keys)}
    return groups


def cn_number(raw: str) -> int:
    if raw.isdigit():
        return int(raw)
    if raw == '十':
        return 10
    if '十' in raw:
        head, _, tail = raw.partition('十')
        return (CN_DIGITS.get(head, 1) if head else 1) * 10 + CN_DIGITS.get(tail, 0)
    return CN_DIGITS.get(raw, 999)


def group_sort_key(name: str):
    """按「一、二、三…」/「01、02…」的自然顺序排，而不是 Unicode 码点。"""
    if not name:
        return (0, -1, '')
    m = re.match(r'^\s*([0-9]+|[一二三四五六七八九十]+)\s*[、.．\-_]', name)
    if not m:
        return (1, 0, name)
    return (0, cn_number(m.group(1)), name)


def display_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in text)


def fit(text: str, width: int) -> str:
    """Truncate a CJK-aware string to a display width."""
    out, used = '', 0
    for c in text:
        w = 2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1
        if used + w > width:
            break
        out += c
        used += w
    return out


def pad(text: str, width: int, right: bool = False) -> str:
    text = str(text)
    gap = ' ' * max(1, width - display_width(text))
    return gap + text if right else text + gap


def dry_run(groups, dest_root: Path, args) -> int:
    totals = {'videos': 0, 'todo': 0, 'done': 0, 'srt': 0}
    names = sorted(groups, key=group_sort_key)
    for name in names:
        label = name or '(根目录直属文件)'
        todo = done = srt = 0
        for video, rel in groups[name]:
            audio = target_audio(rel, dest_root, args.format)
            exists = audio.is_file() and audio.stat().st_size > 0
            done += bool(exists) and not args.overwrite
            todo += not exists or args.overwrite
            srt += video.with_suffix('.srt').is_file()
        totals['videos'] += len(groups[name])
        totals['todo'] += todo
        totals['done'] += done
        totals['srt'] += srt
        print(f'  {label}  |  {len(groups[name])} 个视频  |  待处理 {todo}  |  '
              f'已有 {done}  |  字幕 {srt}')
        if args.verbose:
            for video, rel in groups[name]:
                audio = target_audio(rel, dest_root, args.format)
                print(f'      {rel}  ->  {audio.relative_to(dest_root)}')
    print(f"\n合计 {totals['videos']} 个视频，{len(names)} 个子文件夹；"
          f"待处理 {totals['todo']}，已有 {totals['done']}，配套字幕 {totals['srt']} 份。")
    print(f'输出目录：{dest_root} （保持子文件夹结构）')
    print('这是预览，未创建目录、未写入文件、未调用 ffmpeg。')
    return 0


def process_one(task, args, ffmpeg: str, ffprobe: str, dest_root: Path) -> dict:
    group, video, rel = task
    audio = target_audio(rel, dest_root, args.format)
    res = {'group': group, 'video': video, 'audio': audio, 'status': '',
           'mode': '', 'error': '', 'lyric_count': 0, 'lyric_state': ''}
    audio.parent.mkdir(parents=True, exist_ok=True)
    if args.lyrics:
        n, state = write_lyrics(video, audio, args.lyrics_lang)
        res['lyric_count'], res['lyric_state'] = n, state
    if args.lyrics_only:
        res['status'] = '仅歌词'
        return res
    # 0 字节多半是上次中断留下的残件，不能当成已完成
    if audio.is_file() and audio.stat().st_size > 0 and not args.overwrite:
        res['status'] = '跳过'
        return res

    tmp = audio.with_name(f'.{audio.stem}.tmp{audio.suffix}')
    common = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-y',
              '-i', str(video), '-vn']
    if args.format == 'm4a' and not args.reencode and probe_audio_codec(video, ffprobe) == 'aac':
        # 源音轨已是 AAC：直接换容器，不解码再编码，音质完全不变。
        cmd = common + ['-c:a', 'copy', '-movflags', '+faststart', str(tmp)]
        mode = '无损复制'
    elif args.format == 'm4a':
        cmd = common + ['-c:a', 'aac', '-b:a', args.bitrate,
                        '-movflags', '+faststart', str(tmp)]
        mode = '重编码'
    else:
        cmd = common + ['-c:a', 'libmp3lame', '-b:a', args.bitrate, str(tmp)]
        mode = '重编码'
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
        if r.returncode != 0:
            tail = (r.stderr or '').strip().splitlines()
            raise RuntimeError(tail[-1] if tail else f'ffmpeg 退出码 {r.returncode}')
        if not tmp.is_file() or tmp.stat().st_size == 0:
            raise RuntimeError('输出文件为空')
        os.replace(tmp, audio)  # 原子落盘，中断不会留下假完成的文件
        res['status'], res['mode'] = '成功', mode
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        tmp.unlink(missing_ok=True)
        res['status'], res['error'] = '失败', str(exc)
    return res


def print_summary(stats: dict, args, dest_root: Path):
    lyrics_only = args.lyrics_only
    head = (('子文件夹', '视频', '歌词生成', '歌词已存在', '无字幕') if lyrics_only else
            ('子文件夹', '视频', '成功', '跳过', '失败', '歌词'))
    names = sorted(stats, key=group_sort_key)
    width = min(max([display_width(head[0])] +
                    [display_width(n or '(根目录直属文件)') for n in names] +
                    [display_width('合计')]), 44)
    widths = [max(6, display_width(h)) for h in head[1:]]
    line_width = width + sum(widths) + len(widths)
    print('\n' + '=' * line_width)
    print(pad(fit(head[0], width), width) +
          ''.join(pad(h, w, True) for h, w in zip(head[1:], widths)))
    print('-' * line_width)
    total = [0] * (len(head) - 1)
    for name in names:
        s = stats[name]
        if lyrics_only:
            cells = [s['videos'], s['lnew'], s['lold'], s['nosrt']]
        else:
            cells = [s['videos'], s['ok'], s['skip'], s['fail'], s['lyrics']]
        total = [a + b for a, b in zip(total, cells)]
        print(pad(fit(name or '(根目录直属文件)', width), width) +
              ''.join(pad(c, w, True) for c, w in zip(cells, widths)))
    print('-' * line_width)
    print(pad('合计', width) + ''.join(pad(c, w, True) for c, w in zip(total, widths)))
    print(f'输出目录：{dest_root}')


def main() -> int:
    ap = argparse.ArgumentParser(
        description='批量从视频提取音频（按子文件夹分组输出），并把同名 SRT 转成 LRC 歌词')
    ap.add_argument('-i', '--input', required=True,
                    help='视频根目录（递归扫描所有子文件夹）或单个视频文件')
    ap.add_argument('-o', '--output', default='',
                    help=f'输出目录；默认在输入目录下创建 {DEFAULT_OUTPUT_DIRNAME}/，并保持子文件夹结构')
    ap.add_argument('-f', '--format', choices=['m4a', 'mp3'], default=DEFAULT_FORMAT,
                    help=f'音频格式，默认 {DEFAULT_FORMAT}（可改脚本顶部 DEFAULT_FORMAT）')
    ap.add_argument('--bitrate', default=DEFAULT_BITRATE,
                    help=f'重编码时的音频比特率，默认 {DEFAULT_BITRATE}')
    ap.add_argument('--reencode', action='store_true',
                    help='强制重编码；默认在源音轨为 AAC 且输出 m4a 时直接复制音轨（无损、更快）')
    ap.add_argument('--overwrite', action='store_true', help='覆盖已有音频文件')
    ap.add_argument('--keep-video', action='store_true',
                    help='兼容参数；脚本从不删除源视频')
    ap.add_argument('--lyrics', dest='lyrics', action='store_true', default=True,
                    help='默认开启：同名 SRT 转 LRC，并复制一份 SRT 到音频旁')
    ap.add_argument('--no-lyrics', dest='lyrics', action='store_false', help='不生成歌词文件')
    ap.add_argument('--lyrics-only', action='store_true', help='只生成歌词文件，不转码音频')
    ap.add_argument('--lyrics-lang', choices=['all', 'en', 'zh'], default='all',
                    help='LRC 语言：all=双语合并（默认），en=仅英文，zh=仅中文')
    ap.add_argument('--only', action='append', default=[], metavar='关键词',
                    help='只处理名称含该关键词的一级子文件夹，可重复；如 --only 三、 --only 五、')
    ap.add_argument('-j', '--jobs', type=int, default=1,
                    help='并行转换数，默认 1（串行）；外置 SSD 可试 2~4')
    ap.add_argument('--dry-run', action='store_true', help='只预览分组和将要生成的文件，不写任何文件')
    ap.add_argument('-v', '--verbose', action='store_true', help='预览时逐条列出源文件与目标路径')
    args = ap.parse_args()
    if args.jobs < 1:
        ap.error('--jobs 必须 >= 1')

    src = Path(args.input).expanduser().resolve()
    if not src.exists():
        ap.error(f'输入路径不存在: {src}')
    root = src if src.is_dir() else src.parent
    dest_root = Path(args.output).expanduser().resolve() if args.output else root / DEFAULT_OUTPUT_DIRNAME

    ffmpeg = ffprobe = ''
    if not (args.dry_run or args.lyrics_only):
        ffmpeg = find_bin('ffmpeg')
        if not ffmpeg:
            print('未找到 ffmpeg。请先执行：brew install ffmpeg', file=sys.stderr)
            return 2
        ffprobe = find_bin('ffprobe')

    groups = collect(src, dest_root, args.only)
    if not groups:
        hint = '（--only 没匹配到任何子文件夹）' if args.only else ''
        print(f'没有找到支持的视频文件。{hint}')
        return 0
    ordered = sorted(groups, key=group_sort_key)
    total_videos = sum(len(groups[g]) for g in ordered)

    unit = '个分组' if '' in groups else '个子文件夹'
    print(f'[扫描] 输入：{src}')
    print(f'[扫描] 输出：{dest_root} （保持子文件夹结构）')
    print(f'[扫描] {len(ordered)} {unit} / {total_videos} 个视频，格式 {args.format}')
    if ffmpeg:
        print(f'[环境] ffmpeg: {ffmpeg} | ffprobe: {ffprobe or "未找到（将走重编码）"}')
    if args.only:
        print(f'[筛选] 只处理：{", ".join(args.only)}')
    if args.dry_run:
        return dry_run(groups, dest_root, args)

    tasks = [(g, v, rel) for g in ordered for v, rel in groups[g]]
    stats = {g: dict(videos=0, ok=0, skip=0, fail=0, lyrics=0, lnew=0, lold=0, nosrt=0)
             for g in ordered}
    work = lambda t: process_one(t, args, ffmpeg, ffprobe, dest_root)
    if args.jobs > 1:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(work, tasks))  # map 保序，日志仍按分组顺序输出
    else:
        results = [work(t) for t in tasks]

    current = None
    idx = 0
    for res in results:
        group = res['group']
        if group != current:
            current = group
            idx += 1
            print(f'\n[{idx}/{len(ordered)}] {group or "(根目录直属文件)"} — '
                  f'{len(groups[group])} 个视频')
        s = stats[group]
        s['videos'] += 1
        rel_out = res['audio'].relative_to(dest_root)
        if res['status'] == '成功':
            s['ok'] += 1
            print(f'  [完成] {res["video"].name} -> {rel_out}（{res["mode"]}）')
        elif res['status'] == '跳过':
            s['skip'] += 1
            print(f'  [跳过] 已存在: {rel_out}')
        elif res['status'] == '失败':
            s['fail'] += 1
            print(f'  [失败] {res["video"]}：{res["error"]}', file=sys.stderr)
        if args.lyrics:
            if res['lyric_count']:
                s['lyrics'] += 1
                s['lnew' if res['lyric_state'] == '已生成' else 'lold'] += 1
                if args.lyrics_only:
                    print(f'  [歌词] {res["video"].name} -> {rel_out.with_suffix(".lrc")}'
                          f'（{res["lyric_count"]} 条，{res["lyric_state"]}）')
            else:
                s['nosrt'] += 1
                if args.lyrics_only:
                    print(f'  [歌词] {res["video"].name}: {res["lyric_state"]}，跳过')

    print_summary(stats, args, dest_root)
    failed = sum(s['fail'] for s in stats.values())
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
