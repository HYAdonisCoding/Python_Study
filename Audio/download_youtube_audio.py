from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yt_dlp
from yt_dlp.utils import sanitize_filename

# ============================================================
# 下载地址
#
# 支持：
# 1. 单个 YouTube 视频
# 2. YouTube 播放列表 / 系列
# 3. 一次填写多个 URL
#
# 如果 URL 中包含 list=，自动识别为系列，
# 并以播放列表标题创建独立文件夹。
# ============================================================

DOWNLOAD_URLS = [
    "https://www.youtube.com/watch?v=Zutmi_PmuPA&list=PLC5JP36mbqAG_B0DgqHRwFi9Tl1OcaKI7",  # 老梁故事汇58
    "https://www.youtube.com/watch?v=UYjJh3Mx7L0&list=PLC5JP36mbqAFFkA6KcUK_xXf3GcZRTXSP",  # 老梁故事汇 精选352
    "https://www.youtube.com/watch?v=Z0yLnwcgpdE&list=PLC5JP36mbqAFvC_a0at8g2N1bMxNHyY-B",  # 老梁观世界143
    "https://www.youtube.com/watch?v=hU39wfkIHRQ&list=PLlD7SeKBB31cI78XeR5k535TDjRRK-oAv",  # 王立群读史记251
    "https://www.youtube.com/watch?v=DNThQu4x2vQ&list=PLlD7SeKBB31f8Uh7-cfgCJnhZ4hyp7z3J",  # 资治通鉴3 7
]


# 所有下载内容的总目录
BASE_OUTPUT_DIR = Path.home() / "Downloads" / "youtube_audio"
BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_playlist_id(url):
    """
    从 YouTube URL 中获取 playlist ID。

    例如：
    https://www.youtube.com/watch?v=xxx&list=PL123

    返回：
    PL123
    """
    query = parse_qs(urlparse(url).query)

    values = query.get("list")

    if values:
        return values[0]

    return None


def get_playlist_info(url):
    """
    如果 URL 属于播放列表：
    1. 获取 playlist ID
    2. 获取播放列表标题
    3. 返回标准 playlist URL + 标题

    如果不是播放列表：
    返回 None, None
    """

    playlist_id = get_playlist_id(url)

    if not playlist_id:
        return None, None

    playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"

    options = {
        "quiet": True,
        "no_warnings": True,
        # 使用 Chrome 登录状态
        "cookiesfrombrowser": ("chrome",),
        # 这里只读取 playlist 元数据
        "extract_flat": True,
        "skip_download": True,
    }

    print()
    print("正在读取系列信息...")

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            playlist_url,
            download=False,
        )

    playlist_title = info.get("title") or playlist_id

    # 防止播放列表标题包含非法文件名字符
    safe_title = sanitize_filename(
        playlist_title,
        restricted=False,
    ).strip()

    if not safe_title:
        safe_title = playlist_id

    return playlist_url, safe_title


def resolve_target(url):
    """
    判断 URL 是：

    1. 单视频
    2. 系列 / playlist

    返回：

    download_url
    output_dir
    is_playlist
    """

    playlist_url, playlist_title = get_playlist_info(url)

    # -----------------------------
    # 系列
    # -----------------------------

    if playlist_url:

        output_dir = BASE_OUTPUT_DIR / playlist_title

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return (
            playlist_url,
            output_dir,
            True,
        )

    # -----------------------------
    # 单视频
    # -----------------------------

    return (
        url,
        BASE_OUTPUT_DIR,
        False,
    )


def build_options(
    output_dir,
    is_playlist,
):
    """
    构造 yt-dlp 下载参数。
    """

    # 每一个系列有自己独立的下载记录
    archive_file = output_dir / "downloaded.txt"

    # -----------------------------
    # 文件名
    # -----------------------------

    if is_playlist:

        # 系列：
        #
        # 01 - 视频标题 [YouTubeID].mp3
        # 02 - 视频标题 [YouTubeID].mp3

        outtmpl = output_dir / "%(playlist_index)02d - %(title)s [%(id)s].%(ext)s"

    else:

        # 单视频：
        #
        # 视频标题 [YouTubeID].mp3

        outtmpl = output_dir / "%(title)s [%(id)s].%(ext)s"

    return {
        # 优先下载最佳音频
        "format": "bestaudio/best",
        # 单视频时禁止展开 playlist
        # playlist 时允许完整下载
        "noplaylist": not is_playlist,
        # 输出文件名
        "outtmpl": str(outtmpl),
        # -----------------------------
        # 转 MP3
        # -----------------------------
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        # -----------------------------
        # 下载记录
        # -----------------------------
        #
        # 下载成功的视频 ID 会记录进去。
        #
        # 下次运行：
        #
        # 已完成 → 自动跳过
        # 未完成 → 继续下载
        #
        "download_archive": str(archive_file),
        # 一个视频失败不要终止整个系列
        "ignoreerrors": True,
        # 文件名兼容
        "windowsfilenames": True,
        # -----------------------------
        # 日志
        # -----------------------------
        "quiet": False,
        "no_warnings": False,
        # -----------------------------
        # 网络重试
        # -----------------------------
        "retries": 10,
        "fragment_retries": 10,
        "extractor_retries": 5,
        # -----------------------------
        # 断点续传
        # -----------------------------
        "continuedl": True,
        # -----------------------------
        # Chrome Cookies
        # -----------------------------
        "cookiesfrombrowser": ("chrome",),
        # FFmpeg 不输出版本 banner
        "postprocessor_args": {
            "ffmpeg": ["-hide_banner"],
        },
    }


def download_one(url):
    """
    下载一个 URL。
    """

    (
        download_url,
        output_dir,
        is_playlist,
    ) = resolve_target(url)

    archive_file = output_dir / "downloaded.txt"

    print()
    print("=" * 70)

    if is_playlist:
        print("下载类型：系列 / 播放列表")
    else:
        print("下载类型：单个视频")

    print()
    print(f"原始地址：{url}")
    print(f"保存目录：{output_dir}")
    print(f"下载记录：{archive_file}")

    print()
    print("已成功条目自动跳过，" "未完成文件支持断点续传。")

    print("=" * 70)
    print()

    options = build_options(
        output_dir,
        is_playlist,
    )

    with yt_dlp.YoutubeDL(options) as ydl:

        result = ydl.download([download_url])

    return result


def main():

    print()
    print("=" * 70)
    print("YouTube 音频下载器")
    print()
    print("Chrome Cookies：开启")
    print("格式：MP3 192kbps")
    print("断点续传：开启")
    print("下载记录：开启")
    print()
    print(f"总目录：{BASE_OUTPUT_DIR}")
    print("=" * 70)

    try:

        for url in DOWNLOAD_URLS:

            result = download_one(url)

            print()

            if result == 0:

                print("当前任务处理完成。")

            else:

                print("当前任务仍有部分条目无法下载。")

                print()

                print("如果看到：")

                print("  Private video")

                print("或者：")

                print("  Video unavailable")

                print()

                print("说明当前 Chrome 登录账号" "没有对应视频的访问权限。")

        print()
        print("=" * 70)
        print("全部任务处理结束。")
        print()
        print(f"总目录：{BASE_OUTPUT_DIR}")
        print("=" * 70)

    except KeyboardInterrupt:

        print()
        print("下载已停止。")
        print("下次运行会继续处理" "没有完成的条目。")

    except Exception as e:

        print()
        print("下载发生异常：")
        print(e)


if __name__ == "__main__":
    main()
