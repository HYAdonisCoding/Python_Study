#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3 Folder Splitter v2.0 —— 全局配置

设计约定（与 v1 的关键差异）：
1. 容量单位默认使用 **十进制 MB**（1 MB = 1,000,000 字节）。
   网盘、U 盘、车机、NAS 几乎都按十进制标注容量，v1 用 1024*1024 会让
   "600 MB"实际变成 629 MB，触发超限。需要二进制口径时用 --binary。
2. 目标容量是**软上限**：默认情况下所有子文件夹都不会超过 target。
   max 只在两种场景生效：标记放不下的超大单文件、以及 --overflow 模式。
"""

from __future__ import annotations

from pathlib import Path

APP_NAME = "MP3 Folder Splitter"
APP_VERSION = "2.0.0"

# ---------------------------------------------------------------- 容量
DEFAULT_TARGET_MB = 550
DEFAULT_MAX_MB = 600

DECIMAL_MB = 1_000_000          # 1 MB = 1000 * 1000
BINARY_MB = 1024 * 1024         # 1 MiB
USE_BINARY_UNITS = False        # 默认十进制

# ---------------------------------------------------------------- 文件类型
AUDIO_EXTS: set[str] = {".mp3"}

# 与音频同名的伴生文件（歌词、封面、说明、cue 等），会跟随音频一起移动。
COMPANION_EXTS: set[str] = {
    ".lrc", ".txt", ".cue", ".nfo", ".log", ".pdf",
    ".jpg", ".jpeg", ".png", ".webp", ".bmp",
}

# 目录级共享封面：默认不复制（每箱复制一份会让体积虚增），需要时 --copy-artwork。
SHARED_ARTWORK_STEMS = {"cover", "folder", "front", "albumart", "album", "artwork"}
SHARED_ARTWORK_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
COPY_SHARED_ARTWORK = False

# ---------------------------------------------------------------- 命名
FOLDER_NAME_TEMPLATE = "{name}{index}"   # 周杰伦 -> 周杰伦1 / 周杰伦2 ...
FOLDER_START_INDEX = 1

# ---------------------------------------------------------------- 扫描过滤
IGNORE_PREFIXES = ("._",)                 # macOS AppleDouble 资源叉，只有 4KB 噪音
IGNORE_NAMES = {".DS_Store", ".localized"}

# ---------------------------------------------------------------- 日志
LOG_DIR = Path(__file__).resolve().parent / "logs"
KEEP_SESSIONS = 200                       # 只保留最近 N 次会话目录

# ---------------------------------------------------------------- 装箱
# 再平衡只做"救尾巴"：仅当最小箱低于 target*0.40 时才动手，
# 且 donor 箱搬完后不得低于 target*0.85 —— 避免把所有箱子拉平成一片中等箱。
BALANCE_TRIGGER_RATIO = 0.40
BALANCE_FLOOR_RATIO = 0.85
BALANCE_MAX_ROUNDS = 500     # 再平衡迭代上限，防止病态数据卡死


def mb_to_bytes(mb: float, binary: bool | None = None) -> int:
    """MB -> 字节。binary=None 时跟随全局配置。"""
    unit = BINARY_MB if (USE_BINARY_UNITS if binary is None else binary) else DECIMAL_MB
    return int(round(mb * unit))


def bytes_to_mb(size: int, binary: bool | None = None) -> float:
    unit = BINARY_MB if (USE_BINARY_UNITS if binary is None else binary) else DECIMAL_MB
    return size / unit


def format_size(size: int, binary: bool | None = None) -> str:
    """1024 -> '0.0 MB'；548_200_000 -> '548.2 MB'"""
    binary = USE_BINARY_UNITS if binary is None else binary
    mb = bytes_to_mb(size, binary)
    if mb >= 1024:
        gb = mb / (1024 if binary else 1000)
        return f"{gb:.2f} GB"
    return f"{mb:.1f} MB"


def unit_label(binary: bool | None = None) -> str:
    return "MiB" if (USE_BINARY_UNITS if binary is None else binary) else "MB"
