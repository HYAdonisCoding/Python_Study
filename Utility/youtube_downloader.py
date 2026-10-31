#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube 视频下载工具

功能：
1. 直接把链接写进 VIDEO_URLS 列表，运行即批量下载，无需交互输入
2. 支持单个视频 + 播放列表/系列（带 list= 的链接自动识别）
3. 自动读取 Chrome Cookie，访问登录后可见的视频
4. 指定清晰度（best / 2160 / 1440 / 1080 / 720 / 480）
5. 音视频自动合并为 MP4
6. 断点续传 + 下载归档（downloaded.txt 去重，重复运行自动跳过已完成）

用法：
    python3 youtube_downloader.py                    # 下载 VIDEO_URLS 里的链接
    python3 youtube_downloader.py "https://..."       # 临时快速下载单个视频
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# ============================================================
# 基础配置
# ============================================================

# 默认下载根目录
BASE_OUTPUT_DIR = Path("/Volumes/WorkSSD/03_Media/Videos/YouTube")
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 默认清晰度（每项也可单独指定）
DEFAULT_QUALITY = "1080"

# 清晰度 -> yt-dlp 视频格式选择器
QUALITY_MAP = {
    "best": "bestvideo+bestaudio/best",
    "2160": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    "1440": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
    "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
}

# ============================================================
# 下载任务清单
#
# 把要下载的链接填到 VIDEO_URLS，运行脚本即可。
# 每项可以是：
#   - 字符串 URL            -> 使用默认清晰度
#   - (URL, 清晰度) 元组    -> 单独指定清晰度
#
# 单个视频       -> 存到根目录
# 播放列表/系列  -> 自动按播放列表标题建子文件夹，文件名加集数前缀
# ============================================================

VIDEO_URLS = [
    # "https://www.youtube.com/watch?v=xxxxxxx",               # 单个视频
    # "https://www.youtube.com/watch?v=xxxxxxx&list=yyyyyyy",  # 播放列表/系列
    # ("https://www.youtube.com/watch?v=xxxxxxx", "2160"),     # 单独指定 4K
    "https://www.youtube.com/watch?v=zsVtaYl5Wsc&list=PLcoi1ufPPU8o5KxRbzQn37ZJgpIzYIBVn", # 沙盘战争：越南战争
    "https://www.youtube.com/watch?v=xzubvcKRx78&list=PLcoi1ufPPU8pDyylKp2VtFUjYUWLYFS0X", # 沙盘战争：名将传1 / 3
    "https://www.youtube.com/watch?v=VlWzjqygVcM&list=PLcoi1ufPPU8q1RuUB7KO-hBuPwelEw0ux", # 沙盘战争：从井冈山到古田会议1 / 9
    
    "https://www.youtube.com/watch?v=aPltSRVK7UA&list=PLcoi1ufPPU8r_GsBAvVUPhCoh6gSQm4zp", #沙盘战争：抗美援朝1 / 10
    "https://www.youtube.com/watch?v=Mdj7fy2OCJc&list=PLcoi1ufPPU8oSIUlFYqaxUWJWHSQA57nq", #沙盘战争：小型战役特辑1 / 7
    "https://www.youtube.com/watch?v=fgagClLOCdA&list=PLcoi1ufPPU8qlD0MTaGx1gnhep474vVlT", #沙盘上的战争1 / 6
    "https://www.youtube.com/watch?v=aPltSRVK7UA&list=PLcoi1ufPPU8r_GsBAvVUPhCoh6gSQm4zp", #沙盘战争：抗美援朝1 / 10
    "https://www.youtube.com/watch?v=IjjDzhiZII0&list=PLcoi1ufPPU8qk9jNm70Dp51TkQvo5Gc1t", #沙盘战争·红军创业沙盘上的战争1 / 16
    "https://www.youtube.com/watch?v=GvLwRG32Btc&list=PLcoi1ufPPU8rDt8no6_vnSDVV1FiODKoh", #沙盘战争：三国系列1 / 7
    "https://www.youtube.com/watch?v=iS9gsIy6qH0&list=PLcoi1ufPPU8pbGonqerxo20lan5FqYNYS", #沙盘战争：晚清风云1 / 6
    "https://www.youtube.com/watch?v=tece4J10cew&list=PLcoi1ufPPU8rKVoK4nZFw92A1D0Md5OxG", #沙盘战争：二战系列1 / 7
    "https://www.youtube.com/watch?v=mfQ2yVzWYFo&list=PLcoi1ufPPU8qZzL3pFkgqLXllFYdT8FHz", #沙盘战争：解放系列1 / 2
    "https://www.youtube.com/watch?v=UAlZFtPU4yE&list=PLcoi1ufPPU8rriqw7lcvK5aYFdLt_ib7V", #沙盘战争：长征系列1 / 30
    "https://www.youtube.com/watch?v=tLkoASz2UYA&list=PLcoi1ufPPU8qwF8jHX0X6lgbkWMQlelIH", #沙盘战争：抗日系列1 / 7
    "https://www.youtube.com/watch?v=z9r4wggKDXI&list=PLcoi1ufPPU8qAv3k-3LQP1aWaPWza8vCx", #沙盘战争：娱乐名场面系列1 / 5
]

# ============================================================
# 工具函数
# ============================================================


def get_playlist_id(url: str) -> str | None:
    """从 URL 提取 playlist id（带 list= 参数即为系列/播放列表）。"""
    values = parse_qs(urlparse(url).query).get("list")
    return values[0] if values else None


def check_dependencies() -> bool:
    """检查 yt-dlp 与 ffmpeg 是否可用。"""
    ok = True
    if shutil.which("yt-dlp") is None:
        print("错误：未安装 yt-dlp，执行：pip install -U yt-dlp")
        ok = False
    if shutil.which("ffmpeg") is None:
        print("错误：未安装 FFmpeg，执行：brew install ffmpeg")
        ok = False
    return ok


def parse_entry(entry) -> tuple[str, str]:
    """解析任务项，返回 (url, quality)。"""
    if isinstance(entry, (tuple, list)) and len(entry) >= 2:
        return str(entry[0]).strip(), str(entry[1]).strip()
    return str(entry).strip(), DEFAULT_QUALITY


def build_command(url: str, quality: str, is_playlist: bool) -> list[str]:
    """构造 yt-dlp 命令行参数。"""
    if is_playlist:
        # %(playlist)s 会自动按播放列表标题建子文件夹，
        # %(playlist_index) 加集数前缀，保证系列顺序。
        outtmpl = (
            BASE_OUTPUT_DIR
            / "%(playlist)s"
            / "%(playlist_index)03d - %(title)s [%(id)s].%(ext)s"
        )
    else:
        outtmpl = BASE_OUTPUT_DIR / "%(title)s [%(id)s].%(ext)s"

    # 全局归档：所有任务共用一个去重清单，重复运行自动跳过已完成条目。
    archive = BASE_OUTPUT_DIR / "downloaded.txt"

    format_selector = QUALITY_MAP.get(quality, QUALITY_MAP[DEFAULT_QUALITY])

    cmd = [
        "yt-dlp",
        "--cookies-from-browser", "chrome",
        "-f", format_selector,
        "--merge-output-format", "mp4",
        "-o", str(outtmpl),
        "--download-archive", str(archive),
        "--continue",
        "--ignore-errors",
        "--windows-filenames",
        "--progress",
    ]

    # 单视频不展开播放列表（即使链接里带了 list= 也只下这一集）。
    if not is_playlist:
        cmd.append("--no-playlist")

    cmd.append(url)
    return cmd


def download(url: str, quality: str) -> None:
    """下载单个链接（单视频或整个播放列表）。"""
    is_playlist = get_playlist_id(url) is not None

    print()
    print("=" * 70)
    print(f"类型：{'播放列表 / 系列' if is_playlist else '单个视频'}")
    print(f"清晰度：{quality}")
    print(f"链接：{url}")
    if is_playlist:
        print(f"保存目录：{BASE_OUTPUT_DIR / '<播放列表标题>'}")
    else:
        print(f"保存目录：{BASE_OUTPUT_DIR}")
    print("=" * 70)

    cmd = build_command(url, quality, is_playlist)

    try:
        result = subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n用户取消。下次运行会根据 downloaded.txt 跳过已完成条目。")
        return

    if result.returncode == 0:
        print("下载完成。")
    else:
        print(
            f"下载结束，返回码 {result.returncode}。"
            "部分条目可能因会员专享/下架被跳过，其余正常。"
        )


def main() -> None:
    if not check_dependencies():
        return

    # 任务来源：命令行参数（快速下载） + 文件里的 VIDEO_URLS
    cli_args = [a for a in sys.argv[1:] if a.strip() and not a.startswith("-")]
    entries = cli_args + [e for e in VIDEO_URLS if e]

    if not entries:
        print("没有待下载任务。")
        print("请把链接填到 VIDEO_URLS，或运行：")
        print('  python3 youtube_downloader.py "https://..."')
        return

    print()
    print("=" * 70)
    print("YouTube 视频下载工具")
    print(f"保存根目录：{BASE_OUTPUT_DIR}")
    print(f"任务数：{len(entries)}")
    print("=" * 70)

    seen: set[str] = set()
    for entry in entries:
        url, quality = parse_entry(entry)
        if not url:
            continue
        if url in seen:
            print(f"\n跳过重复任务：{url}")
            continue
        seen.add(url)
        try:
            download(url, quality)
        except Exception as e:
            print(f"\n[任务失败] {url}\n{e}")

    print()
    print("=" * 70)
    print("全部任务处理结束。")
    print("=" * 70)


if __name__ == "__main__":
    main()
