#!/usr/bin/env python3
"""Batch extract audio tracks from video files using ffmpeg.

Optionally convert the matching .srt subtitles into .lrc lyrics placed next to
the audio, and keep a copy of the .srt for players that prefer subtitles.
"""
from __future__ import annotations
import argparse, re, shutil, subprocess, sys
from pathlib import Path

# 改默认输出格式只改这一行：'m4a'（Apple 生态原生，源音轨是 AAC 时可无损直拷）/ 'mp3'（老设备通用）
DEFAULT_FORMAT = 'm4a'
DEFAULT_BITRATE = '192k'

VIDEO_EXTS = {'.mp4', '.m4v', '.mov', '.mkv', '.avi', '.webm'}
TIME_RE = re.compile(r'(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->')

def probe_audio_codec(video: Path) -> str:
    """Return the first audio stream's codec, or '' when ffprobe is unavailable."""
    if not shutil.which('ffprobe'):
        return ''
    try:
        r = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_name', '-of', 'default=nw=1:nk=1', str(video)],
            capture_output=True, text=True, timeout=20)
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

def write_lyrics(video: Path, audio: Path, lang: str):
    srt = video.with_suffix('.srt')
    if not srt.is_file():
        return '无字幕'
    cues = list(parse_srt(srt))
    if not cues:
        return '时间轴为空'
    lrc = audio.with_suffix('.lrc')
    lrc.write_text(make_lrc(cues, lang, video.stem), encoding='utf-8')
    srt_dest = audio.with_suffix('.srt')
    try:
        shutil.copy2(srt, srt_dest)
    except shutil.SameFileError:
        pass
    return f'{len(cues)} 条'

def main():
    ap = argparse.ArgumentParser(description='批量从视频提取音频，并把同名 SRT 转成 LRC 歌词')
    ap.add_argument('-i', '--input', required=True, help='视频文件或视频目录（递归扫描）')
    ap.add_argument('-o', '--output', default='', help='输出目录；默认在输入目录的父目录下创建 Audio')
    ap.add_argument('-f', '--format', choices=['m4a', 'mp3'], default=DEFAULT_FORMAT,
                    help=f'音频格式，默认 {DEFAULT_FORMAT}（可改脚本顶部 DEFAULT_FORMAT）')
    ap.add_argument('--bitrate', default=DEFAULT_BITRATE, help=f'重编码时的音频比特率，默认 {DEFAULT_BITRATE}')
    ap.add_argument('--reencode', action='store_true',
                    help='强制重编码；默认在源音轨为 AAC 且输出 m4a 时直接复制音轨（无损、更快）')
    ap.add_argument('--overwrite', action='store_true', help='覆盖已有音频文件')
    ap.add_argument('--keep-video', action='store_true', help='保留输入视频（默认本来就不删除）')
    ap.add_argument('--lyrics', dest='lyrics', action='store_true', default=True,
                    help='默认开启：同名 SRT 转 LRC，并复制一份 SRT 到音频旁')
    ap.add_argument('--no-lyrics', dest='lyrics', action='store_false', help='不生成歌词文件')
    ap.add_argument('--lyrics-only', action='store_true', help='只生成歌词文件，不转码音频')
    ap.add_argument('--lyrics-lang', choices=['all', 'en', 'zh'], default='all',
                    help='LRC 语言：all=双语合并（默认），en=仅英文，zh=仅中文')
    args = ap.parse_args()
    if not args.lyrics_only and not shutil.which('ffmpeg'):
        print('未找到 ffmpeg。请先执行：brew install ffmpeg', file=sys.stderr); return 2
    src = Path(args.input).expanduser().resolve()
    if not src.exists(): ap.error(f'输入路径不存在: {src}')
    if src.is_file():
        files = [src] if src.suffix.lower() in VIDEO_EXTS else []
        base = src.parent
    else:
        files = sorted(p for p in src.rglob('*') if p.is_file() and p.suffix.lower() in VIDEO_EXTS)
        base = src
    if not files:
        print('没有找到支持的视频文件。'); return 0
    dest_root = Path(args.output).expanduser().resolve() if args.output else base.parent / 'Audio'
    ok = skipped = failed = lyric_ok = lyric_skip = 0
    for video in files:
        rel = Path(video.name) if src.is_file() else video.relative_to(base)
        audio = (dest_root / rel).with_suffix('.' + args.format)
        audio.parent.mkdir(parents=True, exist_ok=True)
        if args.lyrics:
            result = write_lyrics(video, audio, args.lyrics_lang)
            if result.endswith('条'):
                print(f'[歌词] {video.name} -> {audio.stem}.lrc / .srt（{result}）')
                lyric_ok += 1
            else:
                print(f'[歌词] {video.name}: {result}，跳过')
                lyric_skip += 1
        if args.lyrics_only:
            continue
        if audio.exists() and not args.overwrite:
            print(f'[跳过] 已存在: {audio}'); skipped += 1; continue
        mode = '重编码'
        if args.format == 'm4a' and not args.reencode and probe_audio_codec(video) == 'aac':
            # 源音轨已是 AAC：直接换容器，不解码再编码，音质完全不变。
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(video),
                   '-vn', '-c:a', 'copy', '-movflags', '+faststart', str(audio)]
            mode = '无损复制'
        elif args.format == 'm4a':
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(video),
                   '-vn', '-c:a', 'aac', '-b:a', args.bitrate, '-movflags', '+faststart', str(audio)]
        else:
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(video),
                   '-vn', '-c:a', 'libmp3lame', '-b:a', args.bitrate, str(audio)]
        try:
            subprocess.run(cmd, check=True)
            print(f'[完成] {video.name} -> {audio}（{mode}）')
            ok += 1
        except subprocess.CalledProcessError:
            print(f'[失败] {video}', file=sys.stderr)
            audio.unlink(missing_ok=True); failed += 1
    if args.lyrics_only:
        print(f'\n歌词生成结束：成功 {lyric_ok}，无字幕/跳过 {lyric_skip}。输出目录：{dest_root}')
        return 0
    print(f'\n处理结束：成功 {ok}，跳过 {skipped}，失败 {failed}；歌词 {lyric_ok} 份。输出目录：{dest_root}')
    return 1 if failed else 0

if __name__ == '__main__':
    raise SystemExit(main())
