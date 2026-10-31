#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能装箱。

v1 的致命问题：`distance = abs(new_size - target)` 是对称的，从下方接近
550 和从上方接近 550 打分相同，而"继续往里塞"永远是更优解，结果每个箱子
都被顶到 600 的硬上限（实测 14 个箱子里 13 个在 598~600 MB），既不是用户
要的 550，也会在十进制口径的存储设备上超限。

v2 的策略：
1. **目标容量是软上限**：默认 `cap = target`，任何箱子都不会超过 target。
   600 MB 只用于判定"放不下的超大单文件"和 --overflow 模式。
2. Best-Fit Decreasing：每个文件放进"放完之后剩余空间最小"的箱子，
   箱子利用率高且数量少。
3. 收尾再平衡：把最大箱子里的文件挪给最小的箱子，直到最小的箱子接近
   target、或没有再平衡空间。避免出现一个只有 100 MB 的尾巴箱。
4. 伴生文件体积计入箱子，所以 target / max 是真实占用上限。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from config import (
    BALANCE_FLOOR_RATIO,
    BALANCE_MAX_ROUNDS,
    BALANCE_TRIGGER_RATIO,
    format_size,
)
from core.scanner import Item

__all__ = ["Bin", "GroupingResult", "group", "rebalance", "natural_key"]


@dataclass
class Bin:
    index: int
    items: list[Item] = field(default_factory=list)

    @property
    def size(self) -> int:
        # 实时求和，杜绝 v1 里 size 字段与 items 不同步的问题
        return sum(i.total_size for i in self.items)

    @property
    def count(self) -> int:
        return len(self.items)

    @property
    def file_count(self) -> int:
        return sum(1 + len(i.companions) for i in self.items)


@dataclass
class GroupingResult:
    bins: list[Bin] = field(default_factory=list)
    oversized: list[Item] = field(default_factory=list)   # 单文件 > max，无法放入任何箱
    over_target: list[Item] = field(default_factory=list)  # 单文件 > target，独立成箱

    @property
    def total_size(self) -> int:
        return sum(b.size for b in self.bins)

    @property
    def placed_count(self) -> int:
        return sum(b.count for b in self.bins)


def natural_key(name: str) -> list:
    """自然排序键：'歌2.mp3' < '歌10.mp3'（数字按数值比较）。"""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def _best_fit(bins: list[Bin], size: int, cap: int) -> Bin | None:
    """返回放入后剩余空间最小的箱子；放不下则 None。"""
    best: Bin | None = None
    best_remain = -1
    for b in bins:
        new_size = b.size + size
        if new_size > cap:
            continue
        remain = cap - new_size
        if best is None or remain < best_remain:
            best, best_remain = b, remain
    return best


def rebalance(
    bins: list[Bin],
    cap: int,
    floor_ratio: float = BALANCE_FLOOR_RATIO,
    trigger_ratio: float = BALANCE_TRIGGER_RATIO,
) -> None:
    """
    原地"救尾巴"：把大箱子里的文件挪给过小的箱子。

    只在最小箱低于 cap * trigger_ratio 时才启动（否则不动，保持箱子贴近目标）；
    每轮结束重新判断，一旦最小箱回到 trigger 以上就停手。
    约束：
    - 挪完小箱子不超过 cap；
    - 挪完 donor 不低于 cap * floor_ratio，避免把所有箱子拉平成一片中等箱。
    """
    if len(bins) < 2:
        return

    floor = cap * floor_ratio

    for _ in range(BALANCE_MAX_ROUNDS):
        bins.sort(key=lambda b: b.size)
        smallest = bins[0]
        if smallest.size >= cap * trigger_ratio:
            return

        moved = False
        for donor in sorted(bins[1:], key=lambda b: b.size, reverse=True):
            candidates = [
                it
                for it in donor.items
                if smallest.size + it.total_size <= cap
                and donor.size - it.total_size >= floor
            ]
            if not candidates:
                continue
            candidates.sort(key=lambda i: i.total_size, reverse=True)
            item = candidates[0]
            donor.items.remove(item)
            smallest.items.append(item)
            moved = True
            break

        if not moved:
            return


def group(
    items: list[Item],
    target_bytes: int,
    max_bytes: int,
    overflow: bool = False,
    balance: bool = True,
    floor_ratio: float = BALANCE_FLOOR_RATIO,
    sort: str = "size",
) -> GroupingResult:
    """
    装箱主函数。

    overflow=False（默认）：每个箱子 <= target_bytes
    overflow=True：允许填到 max_bytes，箱子更少但更贴近硬上限

    sort="size"（默认）：按体积降序 Best-Fit，箱子数量最少。
    sort="name"：按文件名自然排序、顺序装箱，箱内与箱间都保持文件名
        顺序；不做再平衡（再平衡会把文件重新打散）。
    """
    cap = max_bytes if overflow else target_bytes
    result = GroupingResult()
    bins: list[Bin] = []

    if sort == "name":
        ordered = sorted(items, key=lambda i: natural_key(i.path.name))
    else:
        ordered = sorted(items, key=lambda i: i.total_size, reverse=True)

    for item in ordered:
        size = item.total_size

        if size > max_bytes:
            result.oversized.append(item)
            continue
        if size > target_bytes:
            result.over_target.append(item)

        if size > cap:
            # 单文件超过目标容量但没超硬上限：独立成箱，不与别人拼
            bins.append(Bin(index=len(bins) + 1, items=[item]))
            continue

        if sort == "name":
            # 顺序装箱：塞进当前最后一个箱子，放不下才开新箱，
            # 保证文件名连续、顺序不乱。
            if bins and bins[-1].size + size <= cap:
                bins[-1].items.append(item)
            else:
                bins.append(Bin(index=len(bins) + 1, items=[item]))
            continue

        target_bin = _best_fit(bins, size, cap)
        if target_bin is not None:
            target_bin.items.append(item)
        else:
            bins.append(Bin(index=len(bins) + 1, items=[item]))

    if balance and sort != "name":
        rebalance(bins, cap, floor_ratio)

    bins = [b for b in bins if b.items]
    if sort != "name":
        bins.sort(key=lambda b: b.size, reverse=True)
    for i, b in enumerate(bins, start=1):
        b.index = i

    result.bins = bins
    return result


def describe(result: GroupingResult, cap: int) -> str:
    """给 CLI / GUI 用的一行摘要。"""
    if not result.bins:
        return "没有可装箱的音频"
    sizes = [b.size for b in result.bins]
    return (
        f"{len(result.bins)} 箱，单箱 {format_size(min(sizes))} ~ "
        f"{format_size(max(sizes))}（上限 {format_size(cap)}）"
    )
