#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图形界面（tkinter，零第三方依赖）。

- 多文件夹：按钮选择；装了 tkinterdnd2 还支持直接把文件夹拖进窗口
- 预览：先算装箱，确认后才动手
- 执行：后台线程跑，界面不假死
- 所有危险操作都走 core 里的同一套校验与日志，和 CLI 完全一致
"""

from __future__ import annotations

import queue
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import config
from config import DEFAULT_MAX_MB, DEFAULT_TARGET_MB, LOG_DIR, format_size, mb_to_bytes
from core import grouper, scanner, validator
from core.organizer import Organizer, dest_folder, new_session

try:                                    # 可选：拖拽支持
    from tkinterdnd2 import DND_FILES, TkinterDnD  # type: ignore
    HAS_DND = True
except Exception:                        # noqa: BLE001
    HAS_DND = False


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.root.geometry("900x660")
        self.root.minsize(780, 560)

        self.folders: list[Path] = []
        self.plans: list = []
        self.queue: queue.Queue[tuple[str, object]] = queue.Queue()
        self.running = False

        self._build()
        if not HAS_DND:
            self._log("提示：安装 tkinterdnd2 后可直接把文件夹拖进窗口（pip install tkinterdnd2）")

    # ------------------------------------------------------------------ UI
    def _build(self) -> None:
        pad = {"padx": 10, "pady": 6}

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, **pad)

        # --- 左：文件夹列表
        left = ttk.LabelFrame(main, text="待整理目录")
        left.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(left, selectmode="extended", height=12,
                                  activestyle="none", exportselection=False)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=8)

        btns = ttk.Frame(left)
        btns.pack(fill="x", padx=8, pady=(0, 8))
        ttk.Button(btns, text="添加文件夹", command=self.add_folders).pack(side="left")
        ttk.Button(btns, text="移除选中", command=self.remove_selected).pack(side="left", padx=6)
        ttk.Button(btns, text="清空", command=self.clear_folders).pack(side="left")

        # --- 右：参数
        right = ttk.LabelFrame(main, text="参数")
        right.pack(side="right", fill="y", padx=(10, 0))

        self.target_var = tk.StringVar(value=str(DEFAULT_TARGET_MB))
        self.max_var = tk.StringVar(value=str(DEFAULT_MAX_MB))
        self.binary_var = tk.BooleanVar(value=config.USE_BINARY_UNITS)
        self.overflow_var = tk.BooleanVar(value=False)
        self.companion_var = tk.BooleanVar(value=True)
        self.artwork_var = tk.BooleanVar(value=False)

        rows = [
            ("目标容量 (MB)", ttk.Entry(right, textvariable=self.target_var, width=12)),
            ("硬上限 (MB)", ttk.Entry(right, textvariable=self.max_var, width=12)),
        ]
        for r, (label, widget) in enumerate(rows):
            ttk.Label(right, text=label).grid(row=r, column=0, sticky="w", padx=8, pady=4)
            widget.grid(row=r, column=1, sticky="w", padx=8, pady=4)

        ttk.Checkbutton(right, text="二进制口径 (MiB)", variable=self.binary_var).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=8, pady=2)
        ttk.Checkbutton(right, text="允许填到硬上限", variable=self.overflow_var).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=8, pady=2)
        ttk.Checkbutton(right, text="搬同名伴生文件", variable=self.companion_var).grid(
            row=4, column=0, columnspan=2, sticky="w", padx=8, pady=2)
        ttk.Checkbutton(right, text="复制共享封面", variable=self.artwork_var).grid(
            row=5, column=0, columnspan=2, sticky="w", padx=8, pady=2)

        ttk.Separator(right, orient="horizontal").grid(
            row=6, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        self.preview_btn = ttk.Button(right, text="① 预览分组", command=self.preview)
        self.preview_btn.grid(row=7, column=0, columnspan=2, sticky="ew", padx=8, pady=4)
        self.start_btn = ttk.Button(right, text="② 执行整理", command=self.start,
                                    state="disabled")
        self.start_btn.grid(row=8, column=0, columnspan=2, sticky="ew", padx=8, pady=4)

        self.stat_var = tk.StringVar(value="就绪")
        ttk.Label(right, textvariable=self.stat_var, foreground="#666").grid(
            row=9, column=0, columnspan=2, sticky="w", padx=8, pady=(12, 4))

        # --- 预览表
        mid = ttk.LabelFrame(self.root, text="分组预览")
        mid.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        cols = ("dest", "size", "count", "state")
        self.tree = ttk.Treeview(mid, columns=cols, show="headings", height=9)
        for key, title, width in (
            ("dest", "目标子文件夹", 420),
            ("size", "容量", 110),
            ("count", "文件数", 80),
            ("state", "状态", 200),
        ):
            self.tree.heading(key, text=title)
            self.tree.column(key, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        # --- 日志
        logbox = ttk.LabelFrame(self.root, text="日志")
        logbox.pack(fill="both", expand=False, padx=10, pady=(0, 10))
        self.log_text = tk.Text(logbox, height=7, wrap="none")
        self.log_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.log_text.configure(state="disabled")

        if HAS_DND:
            for widget in (self.root, self.listbox):
                widget.drop_target_register(DND_FILES)          # type: ignore[attr-defined]
                widget.dnd_bind("<<Drop>>", self._on_drop)      # type: ignore[attr-defined]

    # ------------------------------------------------------------------ 文件夹
    def add_folders(self) -> None:
        selected = filedialog.askdirectory(title="选择要整理的音频文件夹")
        if not selected:
            return
        self._add_path(validator.resolvable_path(selected))

    def _on_drop(self, event) -> None:
        try:
            raw = self.root.tk.splitlist(event.data)
        except Exception:                                        # noqa: BLE001
            raw = str(event.data).split()
        for item in raw:
            self._add_path(validator.resolvable_path(item))

    def _add_path(self, path: Path) -> None:
        if not path.is_dir():
            messagebox.showwarning("无效目录", f"不是文件夹：\n{path}")
            return
        if path in self.folders:
            return
        self.folders.append(path)
        self.listbox.insert("end", str(path))
        self.stat_var.set(f"已添加 {len(self.folders)} 个目录")

    def remove_selected(self) -> None:
        for idx in sorted(self.listbox.curselection(), reverse=True):
            self.listbox.delete(idx)
            del self.folders[idx]
        self.stat_var.set(f"已添加 {len(self.folders)} 个目录")

    def clear_folders(self) -> None:
        self.listbox.delete(0, "end")
        self.folders.clear()
        self.plans.clear()
        self.tree.delete(*self.tree.get_children())
        self.start_btn.configure(state="disabled")
        self.stat_var.set("就绪")

    # ------------------------------------------------------------------ 预览
    def _params(self) -> tuple[int, int] | None:
        try:
            target = float(self.target_var.get())
            max_mb = float(self.max_var.get())
        except ValueError:
            messagebox.showerror("参数错误", "容量必须是数字")
            return None
        if target <= 0 or max_mb <= 0:
            messagebox.showerror("参数错误", "容量必须大于 0")
            return None
        if target > max_mb:
            messagebox.showerror("参数错误", "目标容量不能大于硬上限")
            return None
        return mb_to_bytes(target, self.binary_var.get()), mb_to_bytes(max_mb, self.binary_var.get())

    def preview(self) -> None:
        if not self.folders:
            messagebox.showinfo("没有目录", "先添加要整理的文件夹")
            return
        params = self._params()
        if not params:
            return
        target, max_bytes = params

        self.tree.delete(*self.tree.get_children())
        self.plans = []
        problems: list[str] = []

        for folder in self.folders:
            scan = scanner.scan_folder(folder, with_companions=self.companion_var.get())
            grouped = grouper.group(scan.items, target, max_bytes,
                                    overflow=self.overflow_var.get())
            dests = [dest_folder(folder, scan.next_index + i) for i in range(len(grouped.bins))]
            report = validator.validate_plan(
                scan, grouped, target, max_bytes, dests,
                overflow=self.overflow_var.get(),
            )
            self.plans.append((scan, grouped, dests, report))

            if not grouped.bins:
                self._row(f"{folder.name}：无待整理音频", "", "", "跳过")
            for dest, b in zip(dests, grouped.bins):
                state = "✓"
                if b.size > target:
                    state = "超出目标"
                if any(i.path == dest for i in report.errors):
                    state = "目标被占用"
                self._row(dest.name, format_size(b.size, self.binary_var.get()),
                          f"{b.count} 个", state)
            for issue in report.issues:
                if issue.level == "error":
                    problems.append(str(issue))
                    self._row("", "", "", str(issue))

        total_bins = sum(len(g.bins) for _, g, _, _ in self.plans)
        total_size = sum(g.total_size for _, g, _, _ in self.plans)
        self.stat_var.set(f"预览：{total_bins} 个子文件夹，{format_size(total_size)}")
        self._log(f"预览完成：{total_bins} 个子文件夹，共 {format_size(total_size)}")

        blocking = problems or any(not r.ok for *_, r in self.plans)
        self.start_btn.configure(state="disabled" if blocking else "normal")

    def _row(self, dest: str, size: str, count: str, state: str) -> None:
        self.tree.insert("", "end", values=(dest, size, count, state))

    # ------------------------------------------------------------------ 执行
    def start(self) -> None:
        if self.running or not self.plans:
            return
        params = self._params()
        if not params:
            return
        target, max_bytes = params

        if not messagebox.askyesno(
            "确认整理",
            "将按预览结果移动文件（同目录内移动，可回滚）。\n\n继续吗？",
        ):
            return

        self.running = True
        self.start_btn.configure(state="disabled")
        self.preview_btn.configure(state="disabled")
        self.stat_var.set("正在整理…")
        threading.Thread(
            target=self._worker, args=(target, max_bytes), daemon=True
        ).start()
        self.root.after(120, self._poll)

    def _worker(self, target: int, max_bytes: int) -> None:
        try:
            session = new_session(LOG_DIR)
            org = Organizer(session)
            ops = []
            for scan, grouped, dests, report in self.plans:
                if not grouped.bins:
                    continue
                if not report.ok:
                    self.queue.put(("log", f"跳过 {scan.folder.name}：校验未通过"))
                    continue
                artwork = []
                if self.artwork_var.get():
                    from core.companion import find_shared_artwork
                    artwork = find_shared_artwork(scan.folder)
                ops.extend(org.build_ops(scan.folder, grouped.bins, scan.next_index,
                                         artwork=artwork))

            org.write_plan(ops, meta={"target_mb": target, "max_mb": max_bytes,
                                      "source": "gui"})
            summary = org.run(ops)
            self.queue.put(("done", (summary, session)))
        except Exception as exc:                                 # noqa: BLE001
            self.queue.put(("error", exc))

    def _poll(self) -> None:
        try:
            while True:
                kind, payload = self.queue.get_nowait()
                if kind == "log":
                    self._log(str(payload))
                elif kind == "error":
                    self.running = False
                    self._enable()
                    self.stat_var.set("执行失败")
                    messagebox.showerror("执行失败", str(payload))
                elif kind == "done":
                    summary, session = payload
                    self.running = False
                    self._enable()
                    msg = (f"移动 {summary.moved} 个，失败 {summary.failed} 个，"
                           f"{format_size(summary.bytes_moved)}")
                    self.stat_var.set(msg)
                    self._log("完成：" + msg)
                    self._log(f"日志：{session.dir}")
                    if summary.failed:
                        messagebox.showwarning("部分失败", msg + "\n详情见日志目录")
                    else:
                        messagebox.showinfo("整理完成", msg + f"\n\n日志：\n{session.dir}")
                    return
        except queue.Empty:
            pass
        if self.running:
            self.root.after(120, self._poll)

    def _enable(self) -> None:
        self.preview_btn.configure(state="normal")
        self.start_btn.configure(state="normal" if self.plans else "disabled")

    def _log(self, text: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")


def main() -> int:
    try:
        root = TkinterDnD.Tk() if HAS_DND else tk.Tk()
    except tk.TclError as exc:
        print(f"无法启动图形界面：{exc}\n请改用命令行：python3 main.py <目录>", file=sys.stderr)
        return 1
    App(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
