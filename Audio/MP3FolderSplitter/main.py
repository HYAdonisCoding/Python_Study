#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3 Folder Splitter v2.0 —— 程序入口

用法：
    python3 main.py                       # 打开文件夹选择器
    python3 main.py ~/Music/周杰伦         # 指定目录
    python3 main.py ~/Music/A ~/Music/B   # 批量
    python3 main.py ~/Music/A --dry-run   # 只预览
    python3 main.py --list                # 查看历史会话
    python3 main.py --resume              # 续跑最近一次中断的任务
    python3 main.py --undo <session>      # 回滚某次整理
    python3 main.py --gui                 # 图形界面
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:          # 保证 core / config 可导入
    sys.path.insert(0, str(ROOT))

import config
from config import (
    APP_NAME,
    APP_VERSION,
    AUDIO_EXTS,
    COMPANION_EXTS,
    DEFAULT_MAX_MB,
    DEFAULT_TARGET_MB,
    FOLDER_NAME_TEMPLATE,
    LOG_DIR,
    format_size,
    mb_to_bytes,
    unit_label,
)
from core import companion as companion_mod
from core import grouper, organizer, recovery, scanner, validator
from core.grouper import GroupingResult
from core.organizer import Organizer, Session, dest_folder, new_session
from core.scanner import ScanResult

QUIET = False


def say(*parts: object) -> None:
    """人类可读输出；--json 模式下改走 stderr，保持 stdout 干净。"""
    text = " ".join(str(p) for p in parts)
    print(text, file=sys.stderr if QUIET else sys.stdout)


# --------------------------------------------------------------------------- 参数
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="mp3-splitter",
        description=f"{APP_NAME} v{APP_VERSION} —— 按容量把音频整理进编号子文件夹",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  python3 main.py ~/Music/周杰伦 --dry-run\n"
            "  python3 main.py ~/Music/周杰伦 --target 500 --max 550 --yes\n"
            "  python3 main.py --resume\n"
        ),
    )
    p.add_argument("folders", nargs="*", help="要整理的目录；不传则打开文件夹选择器")
    p.add_argument("--target", type=float, default=DEFAULT_TARGET_MB,
                   help=f"目标容量 MB（软上限，单箱不会超过它），默认 {DEFAULT_TARGET_MB}")
    p.add_argument("--max", dest="max_mb", type=float, default=DEFAULT_MAX_MB,
                   help=f"硬上限 MB（判定超大单文件 / --overflow 上限），默认 {DEFAULT_MAX_MB}")
    p.add_argument("--binary", action="store_true",
                   help="使用二进制口径（1 MB = 1024*1024），默认十进制")
    p.add_argument("--overflow", action="store_true",
                   help="允许把箱子填到硬上限（箱子更少，但会贴 600 MB）")
    p.add_argument("--no-balance", action="store_true", help="关闭收尾再平衡")
    p.add_argument("--types", default="mp3",
                   help="音频扩展名，逗号分隔，默认 mp3（可写 flac,wav,m4a）")
    p.add_argument("--no-companions", action="store_true",
                   help="不搬同名伴生文件（.lrc/.jpg/.cue…）")
    p.add_argument("--copy-artwork", action="store_true",
                   help="把目录级 cover.jpg 复制进每个子文件夹")
    p.add_argument("--template", default=FOLDER_NAME_TEMPLATE,
                   help=f"子目录命名模板，可用 {{name}} {{index}}，默认 {FOLDER_NAME_TEMPLATE}")
    p.add_argument("--log-dir", default=str(LOG_DIR), help="日志目录")
    p.add_argument("--dry-run", action="store_true", help="只预览，不移动任何文件")
    p.add_argument("--yes", "-y", action="store_true", help="跳过确认")
    p.add_argument("--json", action="store_true", help="以 JSON 输出结果（stdout）")
    p.add_argument("--list", action="store_true", help="列出历史会话")
    p.add_argument("--resume", nargs="?", const="", default=None, metavar="SESSION",
                   help="续跑中断的会话；省略 ID 则取最近一次未完成的")
    p.add_argument("--undo", nargs="?", const="", default=None, metavar="SESSION",
                   help="回滚某次整理；省略 ID 则取最近一次")
    p.add_argument("--gui", action="store_true", help="启动图形界面")
    p.add_argument("--version", action="version", version=f"{APP_NAME} {APP_VERSION}")
    return p.parse_args(argv)


def parse_exts(raw: str) -> set[str]:
    exts = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip().lower()
        if not part:
            continue
        exts.add(part if part.startswith(".") else f".{part}")
    return exts or set(AUDIO_EXTS)


# --------------------------------------------------------------------------- 预览
def bar(size: int, cap: int, width: int = 16) -> str:
    ratio = 0.0 if cap <= 0 else min(size / cap, 1.0)
    filled = int(round(ratio * width))
    return "█" * filled + "░" * (width - filled)


@dataclass
class FolderPlan:
    scan: ScanResult
    grouped: GroupingResult
    dest_paths: list[Path]
    report: validator.Report = field(default_factory=validator.Report)

    @property
    def has_work(self) -> bool:
        return bool(self.grouped.bins)


def build_folder_plan(
    folder: Path,
    args: argparse.Namespace,
    target_bytes: int,
    max_bytes: int,
    audio_exts: set[str],
) -> FolderPlan:
    scan = scanner.scan_folder(
        folder, audio_exts=audio_exts, with_companions=not args.no_companions
    )
    grouped = grouper.group(
        scan.items,
        target_bytes=target_bytes,
        max_bytes=max_bytes,
        overflow=args.overflow,
        balance=not args.no_balance,
    )
    dests = [
        dest_folder(folder, scan.next_index + i, args.template)
        for i in range(len(grouped.bins))
    ]
    report = validator.validate_plan(
        scan, grouped, target_bytes, max_bytes, dests,
        strict=True, overflow=args.overflow,
    )
    return FolderPlan(scan=scan, grouped=grouped, dest_paths=dests, report=report)


def render_preview(
    plan: FolderPlan,
    target_bytes: int,
    max_bytes: int,
    args: argparse.Namespace,
) -> None:
    scan, grouped = plan.scan, plan.grouped
    folder = scan.folder
    say("")
    say("═" * 74)
    say(f"📂 {folder}")
    say("═" * 74)

    if not scan.items:
        say("  没有发现待整理的音频，跳过。")
        return

    cap = max_bytes if args.overflow else target_bytes
    say(f"  音频 {len(scan.items)} 个 · 伴生文件 {scan.companion_count} 个 "
        f"· 合计 {format_size(scan.total_size, args.binary)}")
    say(f"  目标 {format_size(target_bytes, args.binary)} · "
        f"上限 {format_size(max_bytes, args.binary)} · "
        f"口径 {unit_label(args.binary)}"
        + ("（overflow：允许填到上限）" if args.overflow else "（单箱不超过目标）"))
    say(f"  预计 {len(grouped.bins)} 个子文件夹")

    if grouped.bins:
        say("")
        for i, b in enumerate(grouped.bins):
            name = dest_folder(folder, scan.next_index + i, args.template).name
            mark = "✓" if b.size >= target_bytes * 0.9 else "·"
            say(f"    {name:<26} {format_size(b.size, args.binary):>10}  "
                f"{bar(b.size, cap)}  {b.count:>4} 个  {mark}")

    for issue in plan.report.issues:
        say(f"  {issue}")
    if plan.report.ok and not plan.report.warnings:
        say("  ✅ 校验通过")


# --------------------------------------------------------------------------- 执行
def execute(
    plans: list[FolderPlan],
    args: argparse.Namespace,
    target_bytes: int,
    max_bytes: int,
    log_dir: Path,
) -> tuple[dict, Session, Organizer]:
    session = new_session(log_dir, dry_run=args.dry_run)
    org = Organizer(session, dry_run=args.dry_run)

    ops = []
    for plan in plans:
        if not plan.has_work:
            continue
        artwork = []
        if args.copy_artwork:
            artwork = companion_mod.find_shared_artwork(plan.scan.folder)
        ops.extend(
            org.build_ops(
                plan.scan.folder,
                plan.grouped.bins,
                plan.scan.next_index,
                template=args.template,
                artwork=artwork,
            )
        )

    org.write_plan(
        ops,
        meta={
            "target_mb": args.target,
            "max_mb": args.max_mb,
            "binary_units": args.binary,
            "overflow": args.overflow,
            "template": args.template,
            "folders": [str(p.scan.folder) for p in plans],
        },
    )
    summary = org.run(ops)
    return summary.to_dict(), session, org


def print_summary_block(plans: list[FolderPlan], args: argparse.Namespace,
                        target_bytes: int) -> None:
    total_audio = sum(len(p.scan.items) for p in plans)
    total_size = sum(p.grouped.total_size for p in plans)
    total_bins = sum(len(p.grouped.bins) for p in plans)
    say("")
    say("═" * 74)
    say("📊 汇总")
    say("═" * 74)
    say(f"  文件夹 {len(plans)} 个 · 音频 {total_audio} 个 · "
        f"待整理 {format_size(total_size, args.binary)} · 生成 {total_bins} 个子文件夹")


def list_sessions_and_exit(log_dir: Path, as_json: bool) -> int:
    sessions = organizer.list_sessions(log_dir)
    if as_json:
        print(json.dumps(sessions, ensure_ascii=False, indent=2))
        return 0
    if not sessions:
        say(f"暂无历史会话（{log_dir}）")
        return 0
    say(f"历史会话（{log_dir}）：")
    say(f"  {'ID':<22}{'进度':<14}{'状态'}")
    for s in sessions:
        progress = f"{s['done']}/{s['total']}"
        say(f"  {s['id']:<22}{progress:<14}{s['status']}")
    say("\n续跑：python3 main.py --resume <ID>")
    say("回滚：python3 main.py --undo <ID>")
    return 0


def _pick_session(sessions: list[dict], want: str, statuses: tuple[str, ...]) -> str | None:
    if want:
        return want
    for s in sessions:
        if s["status"] in statuses and not s["dry_run"]:
            return s["id"]
    return None


def run_resume(log_dir: Path, sid: str, as_json: bool) -> int:
    sessions = organizer.list_sessions(log_dir)
    chosen = _pick_session(sessions, sid, ("incomplete",))
    if not chosen:
        say("没有找到可续跑的会话。用 --list 查看。")
        return 1

    info = recovery.inspect(log_dir, chosen)
    say(f"会话 {chosen}：共 {info.total} 个操作，已完成 {info.done}，"
        f"待处理 {len(info.pending)}，已就位 {len(info.already)}，冲突 {len(info.ambiguous)}")
    if not info.resumable:
        say("没有需要补做的操作。")
        return 0

    summary = recovery.resume(log_dir, chosen)
    if as_json:
        print(json.dumps(summary.to_dict(), ensure_ascii=False, indent=2))
    else:
        say(f"✅ 续跑完成：{organizer.summarize_line(summary)}")
        if summary.failed:
            for f in summary.failures[:10]:
                say(f"  ❌ {f.get('src')}：{f.get('error')}")
    return 0 if summary.failed == 0 else 1


def run_undo(log_dir: Path, sid: str, as_json: bool) -> int:
    sessions = organizer.list_sessions(log_dir)
    chosen = _pick_session(sessions, sid, ("completed", "interrupted"))
    if not chosen:
        say("没有找到可回滚的会话。用 --list 查看。")
        return 1

    result = recovery.undo(log_dir, chosen)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        say(f"↩️ 会话 {chosen} 回滚：还原 {result['restored']} 个文件，"
            f"失败 {result['failed']}，跳过 {result['skipped']}，"
            f"清理空目录 {result['removed_dirs']} 个")
    return 0 if result["failed"] == 0 else 1


# --------------------------------------------------------------------------- 选择器
def pick_folders() -> list[Path]:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        say("当前 Python 没有 tkinter，请用命令行参数传入目录。")
        return []

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.update()
    except Exception as exc:                       # noqa: BLE001 - 无显示环境
        say(f"无法打开选择器（{exc}），请用命令行参数传入目录。")
        return []

    folders: list[Path] = []
    say("请选择要整理的文件夹；取消即结束。")
    try:
        while True:
            selected = filedialog.askdirectory(title="选择要整理的音频文件夹（取消结束）")
            if not selected:
                break
            path = validator.resolvable_path(selected)
            if path not in folders:
                folders.append(path)
                say(f"  ✓ 已添加：{path}")
    finally:
        try:
            root.destroy()
        except Exception:                          # noqa: BLE001
            pass
    return folders


# --------------------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> int:
    global QUIET
    args = parse_args(argv)
    QUIET = args.json

    log_dir = Path(args.log_dir).expanduser().resolve()

    if args.list:
        return list_sessions_and_exit(log_dir, args.json)
    if args.resume is not None:
        return run_resume(log_dir, args.resume, args.json)
    if args.undo is not None:
        return run_undo(log_dir, args.undo, args.json)
    if args.gui:
        from gui.app import main as gui_main
        return gui_main()

    if args.target <= 0 or args.max_mb <= 0:
        say("❌ target / max 必须大于 0。")
        return 2
    if args.target > args.max_mb:
        say("❌ target 不能大于 max。")
        return 2
    if "{index}" not in args.template:
        say("❌ 模板必须包含 {index}，否则所有子文件夹会重名。")
        return 2

    target_bytes = mb_to_bytes(args.target, args.binary)
    max_bytes = mb_to_bytes(args.max_mb, args.binary)
    audio_exts = parse_exts(args.types)

    raw = [validator.resolvable_path(x) for x in args.folders] if args.folders else pick_folders()
    if not raw:
        say("没有选择任何文件夹。")
        return 0

    folders, folder_report = validator.normalize_folders(raw)
    for issue in folder_report.issues:
        say(f"{issue}")

    existing: list[Path] = []
    for f in folders:
        if not f.is_dir():
            say(f"⚠️ 不是有效文件夹，跳过：{f}")
            continue
        existing.append(f)
    if not existing:
        say("没有可处理的文件夹。")
        return 2

    plans = [
        build_folder_plan(f, args, target_bytes, max_bytes, audio_exts)
        for f in existing
    ]
    for plan in plans:
        render_preview(plan, target_bytes, max_bytes, args)

    if not any(p.has_work for p in plans):
        say("")
        say("没有需要整理的音频。")
        return 0

    print_summary_block(plans, args, target_bytes)

    blocking = [i for p in plans for i in p.report.errors]
    if blocking:
        say("")
        say("❌ 存在阻断性问题，未执行任何操作：")
        for issue in blocking:
            say(f"   {issue}")
        return 2

    if args.dry_run:
        say("")
        say("🟡 DRY RUN：仅预览，没有移动任何文件。")
        if args.json:
            print(json.dumps(
                {
                    "dry_run": True,
                    "folders": [
                        {
                            "folder": str(p.scan.folder),
                            "bins": [
                                {"dest": str(d), "size": b.size, "count": b.count}
                                for d, b in zip(p.dest_paths, p.grouped.bins)
                            ],
                        }
                        for p in plans
                    ],
                },
                ensure_ascii=False, indent=2,
            ))
        return 0

    if not args.yes:
        say("")
        try:
            answer = input("确认开始整理？输入 YES 执行（其它任意输入取消）： ").strip()
        except (EOFError, KeyboardInterrupt):
            say("\n已取消，没有移动任何文件。")
            return 0
        if answer.upper() != "YES":
            say("已取消，没有移动任何文件。")
            return 0

    # ---- 执行前二次校验：确认期间文件可能已经变了
    say("")
    say("🔍 二次校验…")
    stale = 0
    for plan in plans:
        if not plan.has_work:
            continue
        recheck = validator.validate_plan(
            plan.scan, plan.grouped, target_bytes, max_bytes, plan.dest_paths,
            strict=True, overflow=args.overflow,
        )
        for issue in recheck.errors:
            say(f"   {issue}")
            stale += 1
    if stale:
        say("❌ 文件在确认期间发生变化，已中止。请重新运行。")
        return 2

    say("🚀 开始整理…")
    try:
        payload, session, _org = execute(plans, args, target_bytes, max_bytes, log_dir)
    except KeyboardInterrupt:
        say("")
        say("⛔️ 已中断。已完成的文件有日志记录，可以这样续跑：")
        say("   python3 main.py --resume")
        return 130
    except OSError as exc:
        say(f"❌ 执行失败：{exc}")
        return 1

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        say("")
        say("═" * 74)
        say("✅ 整理完成" if payload["failed"] == 0 else "⚠️ 整理完成（有失败项）")
        say("═" * 74)
        say(f"  移动 {payload['moved']} 个 · 复制 {payload['copied']} 个 · "
            f"失败 {payload['failed']} 个 · {format_size(payload['bytes_moved'], args.binary)}")
        say(f"  日志：{session.dir}")
        say(f"  回滚：python3 main.py --undo {session.id}")
        for failure in payload["failures"][:10]:
            say(f"  ❌ {failure.get('src')}：{failure.get('error')}")

    return 0 if payload["failed"] == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
