#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件移动 + JSON 操作日志。

可靠性要点：
- **先落盘计划，再动手**：plan.json 在任何 move 之前写盘并 fsync，
  进程被 kill 也能靠它恢复。
- **逐条追加状态**：每完成一个文件就往 state.jsonl 追加一行并 fsync，
  崩溃后能精确知道哪些搬完了。
- **原子移动**：同盘用 os.rename（原子，不占额外空间）；跨盘先写
  `<name>.part` 再 os.replace，目标路径永远不会出现半截文件。
- **冲突自动改名**：v1 遇到同名目标直接 continue，文件永远留在原地，
  下次运行又被扫到，形成死循环。这里改成 `name (2).mp3`。
"""

from __future__ import annotations

import json
import os
import shutil
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from config import (
    APP_NAME,
    APP_VERSION,
    FOLDER_NAME_TEMPLATE,
    KEEP_SESSIONS,
    format_size,
)
from core.grouper import Bin

__all__ = [
    "MoveOp",
    "Summary",
    "Session",
    "Organizer",
    "new_session",
    "dest_folder",
    "unique_path",
    "safe_move",
    "load_plan",
    "load_state",
    "list_sessions",
]


# --------------------------------------------------------------------------- 命名
def dest_folder(folder: Path, index: int, template: str = FOLDER_NAME_TEMPLATE) -> Path:
    """周杰伦 + 1 -> 周杰伦1"""
    return folder / template.format(name=folder.name, index=index)


def unique_path(dst: Path, limit: int = 999) -> Path:
    """目标已存在时追加 " (2)"、" (3)" …"""
    if not dst.exists():
        return dst
    stem, suffix = dst.stem, dst.suffix
    for n in range(2, limit + 1):
        candidate = dst.with_name(f"{stem} ({n}){suffix}")
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"同名文件过多，无法重命名：{dst}")


# --------------------------------------------------------------------------- 移动
def safe_move(src: Path, dst: Path) -> Path:
    """
    安全移动，返回实际落点（可能因冲突改名）。

    跨卷不直接 shutil.move：它会先 copy 再 unlink，中途失败会留下半个文件。
    这里写 .part 再 replace，保证目标路径要么是完整文件要么不存在。
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    final = unique_path(dst)

    try:
        same_device = src.stat().st_dev == dst.parent.stat().st_dev
    except OSError:
        same_device = False

    if same_device:
        os.rename(src, final)
        return final

    tmp = final.with_name(final.name + ".part")
    try:
        shutil.copy2(src, tmp)
        os.replace(tmp, final)
        src.unlink()
    except BaseException:
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return final


# --------------------------------------------------------------------------- 数据
@dataclass
class MoveOp:
    index: int
    src: str
    dst: str
    role: str = "audio"      # audio | companion | artwork
    size: int = 0
    op: str = "move"         # move | copy
    status: str = "planned"  # planned | done | failed | skipped
    error: str = ""
    final_dst: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def src_path(self) -> Path:
        return Path(self.src)

    @property
    def dst_path(self) -> Path:
        return Path(self.dst)


@dataclass
class Summary:
    session_id: str = ""
    dry_run: bool = False
    started_at: str = ""
    finished_at: str = ""
    planned: int = 0
    moved: int = 0
    copied: int = 0
    failed: int = 0
    skipped: int = 0
    bytes_moved: int = 0
    folders: list[str] = field(default_factory=list)
    bins: int = 0
    failures: list[dict] = field(default_factory=list)
    status: str = "completed"   # completed | interrupted | dry-run | error

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def ok(self) -> bool:
        return self.failed == 0


def _now() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------- 会话
@dataclass
class Session:
    id: str
    dir: Path
    dry_run: bool = False

    @property
    def plan_path(self) -> Path:
        return self.dir / "plan.json"

    @property
    def state_path(self) -> Path:
        return self.dir / "state.jsonl"

    @property
    def summary_path(self) -> Path:
        return self.dir / "summary.json"

    @property
    def log_path(self) -> Path:
        return self.dir / "session.log"


def new_session(log_dir: Path, dry_run: bool = False) -> Session:
    log_dir.mkdir(parents=True, exist_ok=True)
    base = time.strftime("%Y%m%d-%H%M%S")
    sid = base
    n = 2
    while (log_dir / sid).exists():
        sid = f"{base}-{n}"
        n += 1
    sdir = log_dir / sid
    sdir.mkdir(parents=True)
    _prune_sessions(log_dir)
    return Session(id=sid, dir=sdir, dry_run=dry_run)


def _prune_sessions(log_dir: Path, keep: int = KEEP_SESSIONS) -> None:
    """只保留最近 N 个会话目录，避免日志无限膨胀。"""
    try:
        sessions = sorted(p for p in log_dir.iterdir() if p.is_dir())
    except OSError:
        return
    for old in sessions[:-keep] if len(sessions) > keep else []:
        try:
            shutil.rmtree(old)
        except OSError:
            pass


def list_sessions(log_dir: Path) -> list[dict]:
    """列出所有会话，附带进度，供 --list 和恢复使用。"""
    if not log_dir.is_dir():
        return []

    result: list[dict] = []
    for d in sorted((p for p in log_dir.iterdir() if p.is_dir()), reverse=True):
        plan = d / "plan.json"
        summary = d / "summary.json"
        if not plan.exists():
            continue
        total = 0
        try:
            with plan.open(encoding="utf-8") as fh:
                total = len(json.load(fh).get("ops", []))
        except (OSError, json.JSONDecodeError):
            continue

        done = len(load_state(d))
        status = "incomplete"
        dry = False
        if summary.exists():
            try:
                with summary.open(encoding="utf-8") as fh:
                    data = json.load(fh)
                status = data.get("status", "completed")
                dry = bool(data.get("dry_run"))
            except (OSError, json.JSONDecodeError):
                pass
        if status != "dry-run" and done >= total and total > 0:
            status = "completed"

        result.append(
            {
                "id": d.name,
                "dir": str(d),
                "total": total,
                "done": done,
                "status": status,
                "dry_run": dry,
            }
        )
    return result


def load_plan(session_dir: Path) -> dict:
    with (session_dir / "plan.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def load_state(session_dir: Path) -> dict[int, dict]:
    """读取 state.jsonl，返回 {op_index: {status, dst, error}}。"""
    state: dict[int, dict] = {}
    path = session_dir / "state.jsonl"
    if not path.exists():
        return state
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue   # 崩溃时可能写了半行，跳过
                state[int(rec["i"])] = rec
    except OSError:
        pass
    return state


# --------------------------------------------------------------------------- 执行器
class Organizer:
    def __init__(self, session: Session, dry_run: bool = False, fsync: bool = True):
        self.session = session
        self.dry_run = dry_run or session.dry_run
        self.fsync = fsync
        self.summary = Summary(
            session_id=session.id,
            dry_run=self.dry_run,
            started_at=_now(),
        )
        self._state_fh = None
        self._log_fh = None

    # ---------------------------------------------------------------- 计划
    def build_ops(
        self,
        folder: Path,
        bins: list[Bin],
        start_index: int,
        template: str = FOLDER_NAME_TEMPLATE,
        artwork: list[Path] | None = None,
    ) -> list[MoveOp]:
        """
        把一个目录的装箱结果展开成文件级操作清单。

        artwork：目录级共享封面。用 copy 而不是 move，否则只有第一个箱子有。
        """
        ops: list[MoveOp] = []
        idx = 0
        for offset, b in enumerate(bins):
            target_dir = dest_folder(folder, start_index + offset, template)
            for item in b.items:
                idx += 1
                ops.append(
                    MoveOp(
                        index=idx,
                        src=str(item.path),
                        dst=str(target_dir / item.path.name),
                        role="audio",
                        size=item.audio_size,
                    )
                )
                for c in item.companions:
                    idx += 1
                    ops.append(
                        MoveOp(
                            index=idx,
                            src=str(c.path),
                            dst=str(target_dir / c.path.name),
                            role="companion",
                            size=c.size,
                        )
                    )
            for art in artwork or []:
                idx += 1
                ops.append(
                    MoveOp(
                        index=idx,
                        src=str(art),
                        dst=str(target_dir / art.name),
                        role="artwork",
                        size=0,
                        op="copy",
                    )
                )
        self.summary.bins += len(bins)
        return ops

    def write_plan(self, ops: list[MoveOp], meta: dict) -> None:
        """先把计划落盘并 fsync —— 崩溃恢复的唯一依据。"""
        payload = {
            "app": "MP3 Folder Splitter",
            "version": APP_VERSION,
            "session": self.session.id,
            "created_at": _now(),
            "dry_run": self.dry_run,
            **meta,
            "ops": [o.to_dict() for o in ops],
        }
        self.session.dir.mkdir(parents=True, exist_ok=True)
        with self.session.plan_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.flush()
            if self.fsync:
                os.fsync(fh.fileno())

        if meta.get("folders"):
            self.summary.folders = list(meta["folders"])

    # ---------------------------------------------------------------- 执行
    def run(self, ops: list[MoveOp], skip: set[int] | None = None) -> Summary:
        skip = skip or set()
        self.summary.planned = len(ops)
        created_dirs: set[Path] = set()
        self._open_io()

        try:
            for op in ops:
                if op.index in skip:
                    self.summary.skipped += 1
                    continue
                self._exec_one(op, created_dirs)
        except KeyboardInterrupt:
            self.summary.status = "interrupted"
            raise
        finally:
            self._close_io()
            if self.summary.status != "interrupted":
                self.summary.status = "dry-run" if self.dry_run else "completed"
            self.summary.finished_at = _now()
            self._cleanup_empty(created_dirs)
            self._write_summary()

        return self.summary

    def _exec_one(self, op: MoveOp, created_dirs: set[Path]) -> None:
        src = op.src_path
        dst = op.dst_path

        if not src.exists():
            # 恢复场景：上一次其实搬成功了，只是状态行没来得及落盘
            landed = op.final_dst or op.dst
            if Path(landed).exists():
                op.status = "done"
                op.final_dst = landed
                self._record(op, "done", dst=landed)
                self.summary.moved += 1
                self.summary.bytes_moved += op.size
                return
            op.status = "failed"
            op.error = "源文件不存在"
            self.summary.failed += 1
            self.summary.failures.append({"src": op.src, "error": op.error})
            self._record(op, "failed")
            self._write_log(f"✗ 源文件不存在 {op.src}")
            return

        if self.dry_run:
            op.status = "planned"
            self.summary.skipped += 1
            return

        target_dir = dst.parent
        if not target_dir.exists():
            created_dirs.add(target_dir)

        try:
            if op.op == "copy":
                target_dir.mkdir(parents=True, exist_ok=True)
                final = unique_path(dst)
                shutil.copy2(src, final)
                self.summary.copied += 1
            else:
                final = safe_move(src, dst)
                self.summary.moved += 1
                self.summary.bytes_moved += op.size
        except OSError as exc:
            op.status = "failed"
            op.error = str(exc)
            self.summary.failed += 1
            self.summary.failures.append({"src": op.src, "dst": op.dst, "error": op.error})
            self._record(op, "failed")
            self._write_log(f"✗ 失败 {op.src} -> {op.dst} ({exc})")
            return

        op.status = "done"
        op.final_dst = str(final)
        self._record(op, "done", dst=str(final))
        verb = "复制" if op.op == "copy" else "移动"
        self._write_log(f"✓ {verb} {src.name} -> {final.parent.name}/{final.name}")

    # ---------------------------------------------------------------- IO
    def _open_io(self) -> None:
        if self.dry_run:
            return
        self._state_fh = self.session.state_path.open("a", encoding="utf-8")
        self._log_fh = self.session.log_path.open("a", encoding="utf-8")
        self._write_log(
            f"=== {APP_NAME} {APP_VERSION} session {self.session.id} "
            f"@ {self.summary.started_at} ==="
        )

    def _close_io(self) -> None:
        for fh in (self._state_fh, self._log_fh):
            if fh:
                try:
                    fh.flush()
                    fh.close()
                except OSError:
                    pass
        self._state_fh = None
        self._log_fh = None

    def _record(self, op: MoveOp, status: str, dst: str = "") -> None:
        if not self._state_fh:
            return
        rec = {"i": op.index, "status": status, "src": op.src, "dst": dst or op.dst, "size": op.size}
        if op.error:
            rec["error"] = op.error
        self._state_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self._state_fh.flush()
        if self.fsync:
            os.fsync(self._state_fh.fileno())

    def _write_log(self, line: str) -> None:
        if self._log_fh:
            self._log_fh.write(line + "\n")
            self._log_fh.flush()

    def _cleanup_empty(self, created: set[Path]) -> None:
        """失败的箱子会留下空目录，这里清掉；只碰本次自己创建的。"""
        for d in sorted(created, key=lambda p: len(p.parts), reverse=True):
            try:
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
            except OSError:
                pass

    def _write_summary(self) -> None:
        try:
            self.session.dir.mkdir(parents=True, exist_ok=True)
            with self.session.summary_path.open("w", encoding="utf-8") as fh:
                json.dump(self.summary.to_dict(), fh, ensure_ascii=False, indent=2)
        except OSError:
            pass


def summarize_line(s: Summary) -> str:
    parts = [f"移动 {s.moved}"]
    if s.copied:
        parts.append(f"复制 {s.copied}")
    if s.failed:
        parts.append(f"失败 {s.failed}")
    if s.skipped:
        parts.append(f"跳过 {s.skipped}")
    parts.append(format_size(s.bytes_moved))
    return "，".join(parts)
