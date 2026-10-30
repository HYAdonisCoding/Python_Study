#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MP3 Folder Splitter
按“目标 550 MB / 上限 600 MB”智能整理 MP3。

特点：
- 支持一个或多个目录
- 只处理当前目录下的 .mp3（默认不递归）
- 目标 550 MB，硬上限 600 MB
- 尽量让每个子文件夹接近 550 MB
- 自动创建：原文件夹1、原文件夹2、原文件夹3...
- 已存在的编号文件夹不会被重复处理
- 默认先预览，确认后才移动
- 支持 --dry-run
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_TARGET_MB = 550
DEFAULT_MAX_MB = 600
MB = 1024 * 1024


@dataclass
class MP3File:
    path: Path
    size: int


@dataclass
class Bin:
    index: int
    files: list[MP3File]
    size: int = 0

    @property
    def mb(self) -> float:
        return self.size / MB

    @property
    def count(self) -> int:
        return len(self.files)


def format_mb(size: int) -> str:
    return f"{size / MB:.1f} MB"


def is_mp3(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".mp3"


def collect_mp3s(folder: Path) -> list[MP3File]:
    # 只扫描当前目录，不进入已经创建的子目录。
    result = []
    for p in folder.iterdir():
        if is_mp3(p):
            try:
                result.append(MP3File(p, p.stat().st_size))
            except OSError as exc:
                print(f"⚠️ 无法读取：{p.name} ({exc})")

    # 大文件优先，有利于装箱效果。
    result.sort(key=lambda x: x.size, reverse=True)
    return result


def existing_numbered_folders(folder: Path) -> list[tuple[int, Path]]:
    """
    识别：
      原文件夹1
      原文件夹2
      ...
    返回 [(编号, 路径), ...]
    """
    prefix = folder.name
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    result = []

    for p in folder.iterdir():
        if not p.is_dir():
            continue
        m = pattern.match(p.name)
        if m:
            result.append((int(m.group(1)), p))

    return sorted(result)


def next_folder_number(folder: Path) -> int:
    existing = existing_numbered_folders(folder)
    return (max((n for n, _ in existing), default=0) + 1)


def split_files(
    files: list[MP3File],
    target_bytes: int,
    max_bytes: int,
) -> tuple[list[Bin], list[MP3File]]:
    """
    启发式装箱：
    1. 文件从大到小处理
    2. 对每个文件，优先放进“放进去以后最接近目标值”的已有箱子
    3. 不能超过 max_bytes 才允许放入
    4. 放不进去就新建箱子

    这是实际文件整理场景下速度和效果比较均衡的方案。
    """
    bins: list[Bin] = []
    oversized: list[MP3File] = []

    for f in files:
        if f.size > max_bytes:
            oversized.append(f)
            continue

        candidates = []
        for b in bins:
            new_size = b.size + f.size
            if new_size <= max_bytes:
                # 第一目标：接近 550 MB
                distance = abs(new_size - target_bytes)
                # 第二目标：尽量利用容量
                candidates.append((distance, -new_size, b))

        if candidates:
            candidates.sort(key=lambda x: (x[0], x[1]))
            chosen = candidates[0][2]
            chosen.files.append(f)
            chosen.size += f.size
        else:
            bins.append(Bin(index=len(bins) + 1, files=[f], size=f.size))

    return bins, oversized


def safe_destination(folder: Path, number: int) -> Path:
    return folder / f"{folder.name}{number}"


def preview_folder(
    folder: Path,
    target_mb: int,
    max_mb: int,
) -> tuple[list[Bin], list[MP3File], int]:
    files = collect_mp3s(folder)
    target_bytes = target_mb * MB
    max_bytes = max_mb * MB

    bins, oversized = split_files(files, target_bytes, max_bytes)

    print()
    print("=" * 72)
    print(f"📂 {folder}")
    print("=" * 72)

    if not files:
        print("  没有发现当前目录下的 MP3，跳过。")
        return [], [], 0

    print(f"  MP3 数量：{len(files)}")
    print(f"  总大小：  {format_mb(sum(f.size for f in files))}")
    print(f"  目标：    {target_mb} MB")
    print(f"  上限：    {max_mb} MB")
    print(f"  预计：    {len(bins)} 个子文件夹")

    if bins:
        print()
        print("  分组预览：")
        start_number = next_folder_number(folder)
        for i, b in enumerate(bins):
            dest_name = f"{folder.name}{start_number + i}"
            status = "✓"
            if b.mb < target_mb * 0.75:
                status = "·"
            print(
                f"    {dest_name:<30} "
                f"{b.mb:>7.1f} MB   "
                f"{b.count:>4} 个 MP3   {status}"
            )

    if oversized:
        print()
        print("  ⚠️ 以下文件超过 600 MB，无法放入任何子文件夹：")
        for f in oversized:
            print(f"    - {f.path.name} ({format_mb(f.size)})")

    return bins, oversized, len(files)


def move_bins(
    folder: Path,
    bins: list[Bin],
    start_number: int,
) -> tuple[int, int]:
    moved = 0
    failed = 0

    for i, b in enumerate(bins):
        dest = safe_destination(folder, start_number + i)
        dest.mkdir(exist_ok=True)

        for f in b.files:
            target = dest / f.path.name

            if target.exists():
                print(f"  ⚠️ 目标已存在，跳过：{target}")
                failed += 1
                continue

            try:
                shutil.move(str(f.path), str(target))
                moved += 1
            except OSError as exc:
                print(f"  ❌ 移动失败：{f.path.name} -> {dest.name} ({exc})")
                failed += 1

    return moved, failed


def choose_folders_with_gui() -> list[Path]:
    """
    简单 macOS 文件夹选择器。
    可以连续选择多个目录；选择“取消”结束。
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("当前 Python 没有 tkinter，请使用命令行参数传入目录。")
        return []

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folders: list[Path] = []
    print("请在 Finder 选择要整理的文件夹；取消选择即可结束。")

    while True:
        selected = filedialog.askdirectory(
            title="选择要整理的 MP3 文件夹（取消结束）"
        )
        if not selected:
            break

        path = Path(selected).expanduser().resolve()
        if path not in folders:
            folders.append(path)
            print(f"  ✓ 已添加：{path}")

    root.destroy()
    return folders


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="按 550 MB 目标 / 600 MB 上限智能整理 MP3。"
    )
    parser.add_argument(
        "folders",
        nargs="*",
        help="要处理的文件夹；不传则打开 macOS 文件夹选择器。",
    )
    parser.add_argument(
        "--target",
        type=int,
        default=DEFAULT_TARGET_MB,
        help=f"目标大小 MB，默认 {DEFAULT_TARGET_MB}",
    )
    parser.add_argument(
        "--max",
        dest="max_mb",
        type=int,
        default=DEFAULT_MAX_MB,
        help=f"硬上限 MB，默认 {DEFAULT_MAX_MB}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不移动任何文件。",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="跳过最终确认，直接移动。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.target <= 0 or args.max_mb <= 0:
        print("❌ target/max 必须大于 0。")
        return 1

    if args.target > args.max_mb:
        print("❌ target 不能大于 max。")
        return 1

    if args.folders:
        folders = [Path(x).expanduser().resolve() for x in args.folders]
    else:
        folders = choose_folders_with_gui()

    if not folders:
        print("没有选择任何文件夹。")
        return 0

    valid_folders = []
    for folder in folders:
        if not folder.is_dir():
            print(f"⚠️ 不是有效文件夹，跳过：{folder}")
            continue
        valid_folders.append(folder)

    if not valid_folders:
        print("没有可处理的文件夹。")
        return 1

    all_plans: list[tuple[Path, list[Bin]]] = []
    total_mp3 = 0
    total_size = 0

    for folder in valid_folders:
        bins, oversized, count = preview_folder(
            folder, args.target, args.max_mb
        )
        all_plans.append((folder, bins))

        total_mp3 += count
        for b in bins:
            total_size += b.size

    if not any(bins for _, bins in all_plans):
        print("\n没有需要整理的 MP3。")
        return 0

    print()
    print("=" * 72)
    print("📊 汇总")
    print("=" * 72)
    print(f"文件夹数量：{len(valid_folders)}")
    print(f"MP3 数量：  {total_mp3}")
    print(f"预计整理：  {format_mb(total_size)}")

    if args.dry_run:
        print("\n🟡 DRY RUN：仅预览，没有移动任何文件。")
        return 0

    if not args.yes:
        print()
        answer = input("确认开始移动 MP3？输入 YES 执行： ").strip()
        if answer != "YES":
            print("已取消，没有移动任何文件。")
            return 0

    print()
    print("🚀 开始整理...")
    total_moved = 0
    total_failed = 0

    for folder, bins in all_plans:
        if not bins:
            continue

        start_number = next_folder_number(folder)
        print(f"\n📂 {folder.name}")

        moved, failed = move_bins(folder, bins, start_number)
        total_moved += moved
        total_failed += failed

        print(f"  ✓ 移动 {moved} 个")
        if failed:
            print(f"  ⚠️ 失败/跳过 {failed} 个")

    print()
    print("=" * 72)
    print("✅ 整理完成")
    print("=" * 72)
    print(f"成功移动：{total_moved} 个 MP3")
    print(f"失败/跳过：{total_failed} 个")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
