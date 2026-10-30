#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件扫描：把目录里待整理的音频变成 Item 列表。

与 v1 的差异：
- iterdir 的 PermissionError / OSError 全部捕获，不再 traceback；
- 跳过 ._xxx.mp3 这类 4KB 的 AppleDouble 资源叉（v1 会把它们当真 MP3）；
- 每个 Item 带上伴生文件，体积合并计算；
- 预先算好下一个可用编号，避免预览和执行两次计算不一致。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from config import (
    AUDIO_EXTS,
    COMPANION_EXTS,
    FOLDER_START_INDEX,
)
from core import companion
from core.companion import CompanionFile

__all__ = [
    "CompanionFile",
    "Item",
    "ScanResult",
    "scan_folder",
    "find_numbered_dirs",
    "next_folder_number",
    "is_audio",
]


@dataclass
class Item:
    """一个整理单元：音频 + 它的伴生文件。"""

    path: Path
    audio_size: int
    companions: list[CompanionFile] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def total_size(self) -> int:
        return self.audio_size + sum(c.size for c in self.companions)

    @property
    def all_paths(self) -> list[Path]:
        return [self.path] + [c.path for c in self.companions]


@dataclass
class ScanResult:
    folder: Path
    items: list[Item] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    numbered_dirs: list[Path] = field(default_factory=list)
    next_index: int = FOLDER_START_INDEX

    @property
    def total_size(self) -> int:
        return sum(i.total_size for i in self.items)

    @property
    def companion_count(self) -> int:
        return sum(len(i.companions) for i in self.items)


def is_audio(path: Path, exts: set[str]) -> bool:
    if companion.is_ignored(path):
        return False
    try:
        if not path.is_file():
            return False
    except OSError:
        return False
    return path.suffix.lower() in exts


def _number_pattern(folder_name: str) -> re.Pattern[str]:
    return re.compile(rf"^{re.escape(folder_name)}(\d+)$")


def find_numbered_dirs(folder: Path) -> list[tuple[int, Path]]:
    """识别本工具创建的编号子目录：<folder.name><数字>。"""
    pattern = _number_pattern(folder.name)
    result: list[tuple[int, Path]] = []
    try:
        entries = list(folder.iterdir())
    except OSError:
        return result

    for p in entries:
        try:
            if not p.is_dir():
                continue
        except OSError:
            continue
        m = pattern.match(p.name)
        if m:
            result.append((int(m.group(1)), p))
    return sorted(result)


def next_folder_number(folder: Path) -> int:
    numbered = find_numbered_dirs(folder)
    return max((n for n, _ in numbered), default=FOLDER_START_INDEX - 1) + 1


def scan_folder(
    folder: Path,
    audio_exts: set[str] | None = None,
    with_companions: bool = True,
) -> ScanResult:
    """
    扫描单个目录（不递归）。

    返回值里的 items 已按体积降序排列，装箱阶段直接可用。
    """
    audio_exts = AUDIO_EXTS if audio_exts is None else audio_exts
    result = ScanResult(folder=folder, next_index=FOLDER_START_INDEX)

    if not folder.exists():
        result.errors.append(f"目录不存在：{folder}")
        return result
    if not folder.is_dir():
        result.errors.append(f"不是目录：{folder}")
        return result

    try:
        entries = list(folder.iterdir())
    except PermissionError:
        result.errors.append(f"没有权限读取目录：{folder}")
        return result
    except OSError as exc:
        result.errors.append(f"读取目录失败：{folder}（{exc}）")
        return result

    numbered = find_numbered_dirs(folder)
    result.numbered_dirs = [p for _, p in numbered]
    result.next_index = max((n for n, _ in numbered), default=FOLDER_START_INDEX - 1) + 1

    index = (
        companion.build_index(folder, COMPANION_EXTS, audio_exts)
        if with_companions
        else {}
    )
    claimed: set[Path] = set()

    for p in entries:
        if not is_audio(p, audio_exts):
            continue
        try:
            size = p.stat().st_size
        except OSError as exc:
            result.errors.append(f"无法读取文件大小：{p.name}（{exc}）")
            continue

        comps = companion.attach(p, index, claimed) if with_companions else []
        result.items.append(Item(path=p, audio_size=size, companions=comps))

    result.items.sort(key=lambda i: i.total_size, reverse=True)
    return result
