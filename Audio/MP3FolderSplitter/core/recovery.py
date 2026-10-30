#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中断恢复 + 回滚。

场景：搬到第 137 个文件时 Cmd+C / 断电 / 磁盘满。
- plan.json 已经完整落盘，state.jsonl 记了前 136 条；
- `--resume <session>` 只补齐剩下的，不会重复搬；
- `--undo <session>` 把已经搬走的文件原路退回，并清掉空目录。

判定规则（宁可不动，也不乱动）：
- src 在、dst 不在 -> 待搬（resume 处理）
- src 不在、dst 在 -> 已经搬完，只是状态没落盘，标记 done
- src 在、dst 也在 -> 目标有同名文件，不覆盖，按冲突改名
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from core.organizer import (
    MoveOp,
    Organizer,
    Session,
    Summary,
    list_sessions,
    load_plan,
    load_state,
    safe_move,
    unique_path,
)

__all__ = [
    "list_sessions",
    "resume",
    "undo",
    "inspect",
    "sweep_empty_dirs",
]


def _sdir(log_dir: Path, sid: str) -> Path:
    sdir = log_dir / sid
    if not sdir.is_dir():
        raise FileNotFoundError(f"找不到会话：{sid}")
    if not (sdir / "plan.json").exists():
        raise FileNotFoundError(f"会话缺少 plan.json：{sid}")
    return sdir


def _load_ops(sdir: Path) -> tuple[list[MoveOp], dict]:
    plan = load_plan(sdir)
    ops = [MoveOp(**o) for o in plan.get("ops", [])]
    return ops, plan


@dataclass
class InspectResult:
    id: str
    total: int
    done: int
    pending: list[MoveOp]
    already: list[MoveOp]
    ambiguous: list[MoveOp]

    @property
    def resumable(self) -> bool:
        return bool(self.pending or self.already)


def inspect(log_dir: Path, sid: str) -> InspectResult:
    """在不改动任何文件的前提下，判断该会话的真实进度。"""
    sdir = _sdir(log_dir, sid)
    ops, _ = _load_ops(sdir)
    state = load_state(sdir)

    pending: list[MoveOp] = []
    already: list[MoveOp] = []
    ambiguous: list[MoveOp] = []
    done = 0

    for op in ops:
        rec = state.get(op.index, {})
        if rec.get("status") == "done":
            done += 1
            continue
        src_exists = op.src_path.exists()
        fwd = Path(rec.get("dst") or op.dst)
        dst_exists = fwd.exists()
        if src_exists and not dst_exists:
            pending.append(op)
        elif not src_exists and dst_exists:
            already.append(op)
        elif src_exists and dst_exists:
            ambiguous.append(op)
        else:
            pending.append(op)   # 两边都没有：交给执行阶段报失败

    return InspectResult(
        id=sid, total=len(ops), done=done,
        pending=pending, already=already, ambiguous=ambiguous,
    )


def resume(log_dir: Path, sid: str, dry_run: bool = False) -> Summary:
    """续跑未完成的会话。"""
    sdir = _sdir(log_dir, sid)
    ops, plan = _load_ops(sdir)
    state = load_state(sdir)

    session = Session(id=sid, dir=sdir, dry_run=bool(plan.get("dry_run")))
    organizer = Organizer(session, dry_run=dry_run or session.dry_run)
    organizer.summary.folders = list(plan.get("folders", []))

    # 已完成的直接计入汇总，不重复搬
    skip: set[int] = set()
    for op in ops:
        if state.get(op.index, {}).get("status") == "done":
            skip.add(op.index)
            organizer.summary.moved += 1
            organizer.summary.bytes_moved += op.size

    return organizer.run(ops, skip=skip)


def undo(log_dir: Path, sid: str, dry_run: bool = False) -> dict:
    """
    把该会话已经搬动的文件原路退回。

    只回退 op=="move" 且状态为 done 的记录；artwork 是复制出来的，不动。
    """
    sdir = _sdir(log_dir, sid)
    ops, _ = _load_ops(sdir)
    state = load_state(sdir)

    index = {o.index: o for o in ops}
    restored = 0
    failed = 0
    skipped = 0
    touched_dirs: set[Path] = set()
    details: list[dict] = []

    for i in sorted(state):
        rec = state[i]
        if rec.get("status") != "done":
            continue
        op = index.get(i)
        if op is None or op.op != "move":
            skipped += 1
            continue

        current = Path(rec.get("dst") or op.dst)
        original = Path(op.src)

        if not current.exists():
            skipped += 1
            details.append({"src": str(current), "status": "missing"})
            continue

        if dry_run:
            restored += 1
            details.append({"from": str(current), "to": str(original), "status": "dry-run"})
            continue

        try:
            original.parent.mkdir(parents=True, exist_ok=True)
            target = unique_path(original)
            safe_move(current, target)
            restored += 1
            touched_dirs.add(current.parent)
            details.append({"from": str(current), "to": str(target), "status": "restored"})
        except OSError as exc:
            failed += 1
            details.append({"from": str(current), "error": str(exc), "status": "failed"})

    removed = sweep_empty_dirs(touched_dirs) if not dry_run else 0

    result = {
        "session": sid,
        "restored": restored,
        "failed": failed,
        "skipped": skipped,
        "removed_dirs": removed,
        "dry_run": dry_run,
        "at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "details": details,
    }
    try:
        with (sdir / f"undo-{time.strftime('%Y%m%d-%H%M%S')}.json").open(
            "w", encoding="utf-8"
        ) as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return result


def sweep_empty_dirs(dirs: set[Path]) -> int:
    """自底向上删掉空目录，返回删除数量。"""
    removed = 0
    for d in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            if d.is_dir() and not any(d.iterdir()):
                os.rmdir(d)
                removed += 1
        except OSError:
            pass
    return removed
