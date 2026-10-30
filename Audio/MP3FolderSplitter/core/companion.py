#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伴生文件识别。

v1 只搬 .mp3，同名歌词封面留在原地，整理完就是一地散件。
这里改为"音频 + 同 stem 伴生文件"一起入箱，伴生文件体积也计入箱子容量，
这样 600 MB 的硬上限才是真的上限。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config import (
    COMPANION_EXTS,
    IGNORE_NAMES,
    IGNORE_PREFIXES,
    SHARED_ARTWORK_EXTS,
    SHARED_ARTWORK_STEMS,
)


@dataclass(frozen=True)
class CompanionFile:
    path: Path
    size: int


def is_ignored(path: Path) -> bool:
    """过滤 macOS 资源叉 / 系统隐藏文件。"""
    name = path.name
    if name in IGNORE_NAMES:
        return True
    return any(name.startswith(p) for p in IGNORE_PREFIXES)


def build_index(
    folder: Path,
    exts: set[str] | None = None,
    audio_exts: set[str] | None = None,
) -> dict[str, list[Path]]:
    """
    扫一遍目录，建立 "小写 stem -> 候选伴生文件列表" 的索引。

    只遍历一次目录，避免对每个音频都 glob 一次造成 O(n^2) 系统调用。
    """
    exts = COMPANION_EXTS if exts is None else exts
    audio_exts = set() if audio_exts is None else audio_exts

    index: dict[str, list[Path]] = {}
    try:
        entries = list(folder.iterdir())
    except OSError:
        return index

    for p in entries:
        if is_ignored(p):
            continue
        try:
            if not p.is_file():
                continue
        except OSError:
            continue

        suffix = p.suffix.lower()
        if suffix not in exts or suffix in audio_exts:
            continue

        index.setdefault(p.stem.lower(), []).append(p)

    for lst in index.values():
        lst.sort()
    return index


def attach(
    audio_path: Path,
    index: dict[str, list[Path]],
    claimed: set[Path],
) -> list[CompanionFile]:
    """
    找出该音频的伴生文件。

    claimed 用来防止同一个 .lrc 被两个同名音频（如 a.mp3 与 a.flac）重复认领，
    否则第二个被搬走时源文件已经不存在。
    """
    result: list[CompanionFile] = []
    for p in index.get(audio_path.stem.lower(), []):
        if p in claimed or p == audio_path:
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        claimed.add(p)
        result.append(CompanionFile(path=p, size=size))
    return result


def find_shared_artwork(folder: Path) -> list[Path]:
    """目录级共享封面：cover.jpg / folder.png / front.jpg ..."""
    found: list[Path] = []
    try:
        entries = list(folder.iterdir())
    except OSError:
        return found

    for p in entries:
        if is_ignored(p):
            continue
        try:
            if not p.is_file():
                continue
        except OSError:
            continue
        if p.suffix.lower() in SHARED_ARTWORK_EXTS and p.stem.lower() in SHARED_ARTWORK_STEMS:
            found.append(p)
    return sorted(found)
