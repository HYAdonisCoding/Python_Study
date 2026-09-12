#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MP4 / M4A 批量转换为高质量 MP3

要求：
    1. 安装 FFmpeg
    2. Python 3.8+

用法：
    python convert_to_mp3.py "/path/to/file.m4a"
    python convert_to_mp3.py "/path/to/folder"

默认输出：
    与原文件放在同一目录
    example.m4a -> example.mp3
"""

import sys
import shutil
import subprocess
from pathlib import Path


# 支持的输入格式
SUPPORTED_EXTENSIONS = {".mp4", ".m4a"}

# MP3 音质参数
# libmp3lame:
#   -q:a 0 = 最高质量 VBR，通常约 220~260 kbps
#   -q:a 2 = 很高质量 VBR，通常约 170~210 kbps
MP3_QUALITY = "0"


def check_ffmpeg():
    """检查系统是否安装 FFmpeg"""
    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg is None:
        print("错误：没有找到 FFmpeg。")
        print()
        print("macOS 可使用 Homebrew 安装：")
        print("    brew install ffmpeg")
        print()
        print("安装完成后重新运行脚本。")
        sys.exit(1)

    return ffmpeg


def convert_to_mp3(ffmpeg, input_file: Path):
    """将一个 MP4/M4A 文件转换为高质量 MP3"""

    output_file = input_file.with_suffix(".mp3")

    # 防止把已有 MP3 覆盖掉
    if output_file.exists():
        print(f"跳过：MP3 已存在 -> {output_file.name}")
        return

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel", "error",

        "-i", str(input_file),

        # 不处理视频流
        "-vn",

        # 使用 LAME MP3 编码器
        "-c:a", "libmp3lame",

        # 高质量 VBR
        "-q:a", MP3_QUALITY,

        # 保留常见元数据
        "-map_metadata", "0",

        # 自动覆盖可改成 -y
        "-n",

        str(output_file),
    ]

    print(f"正在转换：{input_file.name}")

    try:
        subprocess.run(command, check=True)

        print(f"转换完成：{output_file.name}")

    except subprocess.CalledProcessError:
        print(f"转换失败：{input_file.name}")

        # 删除可能产生的不完整文件
        if output_file.exists():
            output_file.unlink()


def main():
    if len(sys.argv) < 2:
        print("请指定 MP4/M4A 文件或文件夹。")
        print()
        print("例如：")
        print('    python convert_to_mp3.py "/Users/eason/Music/test.m4a"')
        print('    python convert_to_mp3.py "/Users/eason/Music"')
        sys.exit(1)

    ffmpeg = check_ffmpeg()

    target = Path(sys.argv[1]).expanduser().resolve()

    if not target.exists():
        print(f"路径不存在：{target}")
        sys.exit(1)

    # 单个文件
    if target.is_file():

        if target.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print("只支持 MP4 和 M4A 文件。")
            sys.exit(1)

        convert_to_mp3(ffmpeg, target)

    # 文件夹
    elif target.is_dir():

        files = [
            f for f in target.iterdir()
            if f.is_file()
            and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        files.sort()

        if not files:
            print("该文件夹中没有找到 MP4/M4A 文件。")
            return

        print(f"共找到 {len(files)} 个文件。\n")

        for index, file in enumerate(files, 1):
            print(f"[{index}/{len(files)}]")
            convert_to_mp3(ffmpeg, file)
            print()

        print("全部处理完成。")


if __name__ == "__main__":
    main()