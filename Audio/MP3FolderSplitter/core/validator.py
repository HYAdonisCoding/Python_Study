#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全校验。

两个入口：
- normalize_folders()：入参清洗。去重 + 拒绝父子目录同时入选。
  v1 没做这一步，`python mp3_splitter.py /a /a` 会生成一堆空文件夹，
  第二个 plan 的所有 move 全部失败。
- validate_plan()：执行前二次校验。预览到确认之间文件可能被改名、
  被删除、被同步盘替换，这里重新 stat 一遍，发现变化就拦下来。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from config import format_size
from core.grouper import GroupingResult
from core.scanner import ScanResult

__all__ = [
    "Issue",
    "Report",
    "normalize_folders",
    "validate_plan",
    "resolvable_path",
]


@dataclass(frozen=True)
class Issue:
    level: str          # "error" | "warning"
    code: str
    message: str
    path: Path | None = None

    def __str__(self) -> str:
        icon = "❌" if self.level == "error" else "⚠️"
        return f"{icon} [{self.code}] {self.message}"


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, path: Path | None = None) -> None:
        self.issues.append(Issue(level, code, message, path))

    def error(self, code: str, message: str, path: Path | None = None) -> None:
        self.add("error", code, message, path)

    def warning(self, code: str, message: str, path: Path | None = None) -> None:
        self.add("warning", code, message, path)

    def extend(self, other: "Report") -> None:
        self.issues.extend(other.issues)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def render(self) -> list[str]:
        return [str(i) for i in self.issues]


def resolvable_path(raw: str) -> Path:
    """展开 ~ 并 resolve；strict=False，路径不存在也不抛异常。"""
    return Path(raw).expanduser().resolve()


def _is_relative_to(child: Path, parent: Path) -> bool:
    if child == parent:
        return True
    return parent in child.parents


def normalize_folders(folders: list[Path]) -> tuple[list[Path], Report]:
    """
    去重 + 校验父子重叠，返回 (可处理列表, 报告)。

    重复和父子同时入选都会被丢弃（后者保留父目录），并记录 error，
    交由调用方决定是否继续。
    """
    report = Report()
    unique: list[Path] = []

    for f in folders:
        if f in unique:
            report.error("DUPLICATE_FOLDER", f"重复的目录已被忽略：{f}", f)
            continue
        unique.append(f)

    accepted: list[Path] = []
    for f in unique:
        shadowed = next(
            (a for a in accepted if _is_relative_to(f, a) and f != a),
            None,
        )
        if shadowed is not None:
            report.error(
                "NESTED_FOLDER",
                f"{f} 是 {shadowed} 的子目录，同时处理会互相搬乱，已跳过",
                f,
            )
            continue
        accepted.append(f)

    return accepted, report


def validate_plan(
    scan: ScanResult,
    grouped: GroupingResult,
    target_bytes: int,
    max_bytes: int,
    dest_paths: list[Path],
    strict: bool = True,
    overflow: bool = False,
) -> Report:
    """
    校验一份执行计划。

    strict=True 时，源文件在预览后发生的任何变化（消失、变大变小）都算 error，
    因为按旧快照装箱的结果已经不可信了。

    overflow=True 时，箱子允许填到 max_bytes，因此超过 target 不再告警；
    只有真正"单文件过大导致无法与他箱合并"的情况才提示。
    """
    report = Report()

    if scan.errors:
        for msg in scan.errors:
            report.error("SCAN", msg, scan.folder)

    if not scan.folder.is_dir():
        report.error("FOLDER_GONE", f"目录已不存在：{scan.folder}", scan.folder)
        return report

    if not os.access(scan.folder, os.W_OK):
        report.error("FOLDER_READONLY", f"目录不可写，无法移动文件：{scan.folder}", scan.folder)

    if len(dest_paths) != len(grouped.bins):
        report.error(
            "PLAN_MISMATCH",
            f"分组数（{len(grouped.bins)}）与目标目录数（{len(dest_paths)}）不一致",
            scan.folder,
        )

    # ---- 单个文件：仍然存在、体积未变
    names_in_bin: dict[int, set[str]] = {}
    for bin_idx, b in enumerate(grouped.bins):
        seen = names_in_bin.setdefault(bin_idx, set())
        if b.size > max_bytes:
            report.error(
                "BIN_OVER_MAX",
                f"分组 {b.index} 体积 {format_size(b.size)} 超过硬上限 {format_size(max_bytes)}",
                scan.folder,
            )
        # 超过目标容量：仅在非 overflow 模式下才值得提示。
        # overflow 模式本来就是允许填到 max 的，报"超目标"是误报。
        if b.size > target_bytes and not overflow:
            # 区分"单个文件本身过大"与"多文件合并后超目标"两种情况
            single_over = any(
                item.total_size > target_bytes for item in b.items
            )
            reason = "单文件过大" if single_over else "多文件合并后超出"
            report.warning(
                "BIN_OVER_TARGET",
                f"分组 {b.index} 体积 {format_size(b.size)} 超过目标容量，{reason}",
                scan.folder,
            )

        for item in b.items:
            for p, expected in [(item.path, item.audio_size)] + [
                (c.path, c.size) for c in item.companions
            ]:
                try:
                    actual = p.stat().st_size
                except FileNotFoundError:
                    report.error("SOURCE_GONE", f"源文件在预览后已消失：{p}", p)
                    continue
                except OSError as exc:
                    report.error("SOURCE_UNREADABLE", f"无法读取源文件：{p}（{exc}）", p)
                    continue

                if strict and actual != expected:
                    report.error(
                        "SOURCE_CHANGED",
                        f"源文件体积已变化：{p.name} "
                        f"{format_size(expected)} -> {format_size(actual)}",
                        p,
                    )

            if item.name in seen:
                report.warning(
                    "DUP_NAME",
                    f"分组 {b.index} 内有同名文件，执行时会自动改名：{item.name}",
                    item.path,
                )
            seen.add(item.name)

    # ---- 目标目录
    for dest in dest_paths:
        try:
            if dest.exists():
                if dest.is_dir():
                    if any(dest.iterdir()):
                        report.warning(
                            "DEST_NOT_EMPTY",
                            f"目标目录已存在且非空，将合并进去：{dest.name}",
                            dest,
                        )
                else:
                    report.error(
                        "DEST_IS_FILE",
                        f"目标路径已被同名文件占用，无法建目录：{dest}",
                        dest,
                    )
        except OSError as exc:
            report.error("DEST_UNREADABLE", f"无法访问目标路径：{dest}（{exc}）", dest)

    if grouped.oversized:
        for item in grouped.oversized:
            report.warning(
                "OVERSIZED",
                f"{item.name}（{format_size(item.total_size)}）超过硬上限 "
                f"{format_size(max_bytes)}，将留在原目录",
                item.path,
            )

    return report
