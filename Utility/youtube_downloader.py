
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YouTube 视频下载工具
功能：
1. 自动读取 Chrome Cookie
2. 支持登录后访问的视频
3. 支持指定视频清晰度
4. 自动合并音视频
5. 默认保存到 Downloads/YouTube
"""

import os
import subprocess
import shutil
from pathlib import Path


class YouTubeDownloader:

    def __init__(self):
        # 默认下载目录
        self.download_dir = Path("/Volumes/WorkSSD/03_Media/Videos/YouTube")
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def check_dependencies(self):
        """检查运行环境"""

        if shutil.which("yt-dlp") is None:
            print("错误：未安装 yt-dlp")
            print("执行：pip install -U yt-dlp")
            return False

        if shutil.which("ffmpeg") is None:
            print("错误：未安装 FFmpeg")
            print("执行：brew install ffmpeg")
            return False

        return True

    def download(self, url, quality="1080"):
        """下载 YouTube 视频"""

        # 视频清晰度选择
        quality_map = {
            "best": "bestvideo+bestaudio/best",
            "2160": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
            "1440": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
            "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        }

        format_option = quality_map.get(
            quality, quality_map["1080"]
        )

        # 下载参数
        command = [
            "yt-dlp",

            # 从 Chrome 自动读取 Cookie
            "--cookies-from-browser", "chrome",

            # 视频格式
            "-f", format_option,

            # 合并为 MP4
            "--merge-output-format", "mp4",

            # 文件输出路径
            "-o", str(
                self.download_dir / "%(title)s.%(ext)s"
            ),

            # 显示下载进度
            "--progress",

            # 避免覆盖已有文件
            "--no-overwrites",

            url
        ]

        print("\n开始下载 YouTube 视频...")
        print(f"视频链接：{url}")
        print(f"清晰度：{quality}")
        print(f"保存目录：{self.download_dir}")
        print("-" * 50)

        try:
            result = subprocess.run(command)

            if result.returncode == 0:
                print("\n下载完成！")
            else:
                print("\n下载失败，请检查错误信息。")

        except KeyboardInterrupt:
            print("\n用户取消下载。")

        except Exception as error:
            print(f"\n发生异常：{error}")


def main():
    downloader = YouTubeDownloader()

    if not downloader.check_dependencies():
        return

    print("=" * 45)
    print("          YouTube 视频下载工具")
    print("=" * 45)

    url = input("\n请输入 YouTube 视频链接：").strip()

    if not url:
        print("视频链接不能为空！")
        return

    print("\n请选择视频清晰度：")
    print("1. 最高画质")
    print("2. 2160P")
    print("3. 1440P")
    print("4. 1080P")
    print("5. 720P")
    print("6. 480P")

    options = {
        "1": "best",
        "2": "2160",
        "3": "1440",
        "4": "1080",
        "5": "720",
        "6": "480"
    }

    choice = input("\n请输入选项（默认 1080P）：").strip()
    quality = options.get(choice, "1080")

    downloader.download(url, quality)


if __name__ == "__main__":
    main()