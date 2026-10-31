#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MP3 Folder Splitter v2.0 冒烟测试

不依赖任何第三方库：
    python3 tests/smoke_test.py

覆盖：基本分箱 / 伴生文件 / 冲突改名 / 去重与嵌套目录 / 崩溃续跑 /
回滚 / overflow / JSON 输出 / 只读目录不崩。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "main.py"
MB = 1_000_000

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def mk(path: Path, mb: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        fh.truncate(int(mb * MB))


def dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.iterdir() if f.is_file())


def count_audio(path: Path) -> int:
    return len([f for f in path.iterdir() if f.suffix.lower() == ".mp3" and not f.name.startswith("._")])


# --------------------------------------------------------------------------- A
def case_basic(tmp: Path) -> None:
    src = tmp / "周杰伦"
    src.mkdir()
    for i in range(40):
        mk(src / f"歌{i:02d}.mp3", 20)
        if i % 2 == 0:
            mk(src / f"歌{i:02d}.lrc", 0.004)
        if i % 5 == 0:
            mk(src / f"歌{i:02d}.jpg", 0.05)
    mk(src / "超长.mp3", 700)
    mk(src / "._噪音.mp3", 0.004)
    mk(src / "cover.jpg", 0.3)
    (src / "周杰伦1").mkdir()
    mk(src / "周杰伦1" / "旧文件.mp3", 5)

    log = tmp / "logs"
    r = run(str(src), "--yes", "--log-dir", str(log))
    check("A1 退出码 0", r.returncode == 0, r.stdout[-400:] + r.stderr[-400:])

    bins = sorted(d for d in src.iterdir() if d.is_dir() and d.name != "周杰伦1")
    check("A2 生成子目录", len(bins) >= 2, str([b.name for b in bins]))
    check("A3 编号从 2 开始", bins and bins[0].name == "周杰伦2", str(bins[0].name if bins else None))

    over = [b for b in bins if dir_size(b) > 550 * MB]
    check("A4 每箱 <= 550 MB", not over, str([(b.name, dir_size(b) / MB) for b in over]))

    total_in_bins = sum(count_audio(b) for b in bins)
    check("A5 音频数量守恒", total_in_bins == 40, f"{total_in_bins} vs 40")

    # 伴生文件跟随
    lrc_in_root = [f for f in src.iterdir() if f.suffix == ".lrc"]
    check("A6 伴生文件全部跟随", not lrc_in_root, str(lrc_in_root[:3]))
    paired = all(
        (b / f"歌{i:02d}.lrc").exists()
        for b in bins
        for i in range(40)
        if i % 2 == 0 and (b / f"歌{i:02d}.mp3").exists()
    )
    check("A7 歌词与音频同箱", paired)

    check("A8 超大文件留在原地", (src / "超长.mp3").exists())
    check("A9 共享封面未被搬走", (src / "cover.jpg").exists())
    check("A10 已存在编号目录未被处理", (src / "周杰伦1" / "旧文件.mp3").exists())
    check("A11 AppleDouble 未被动过", (src / "._噪音.mp3").exists())

    sessions = [d for d in log.iterdir() if (d / "plan.json").exists()]
    check("A12 日志四件套齐全", sessions and all(
        (sessions[0] / n).exists() for n in ("plan.json", "state.jsonl", "summary.json", "session.log")
    ), str(sessions))


# --------------------------------------------------------------------------- B
def case_conflict(tmp: Path) -> None:
    src = tmp / "冲突"
    src.mkdir()
    mk(src / "同名.mp3", 10)
    bins = src / "冲突1"
    bins.mkdir()
    mk(bins / "同名.mp3", 1)   # 目标已存在

    sys.path.insert(0, str(ROOT))
    from core.organizer import safe_move, unique_path

    p = unique_path(bins / "同名.mp3")
    check("B1 unique_path 追加 (2)", p.name == "同名 (2).mp3", p.name)

    final = safe_move(src / "同名.mp3", bins / "同名.mp3")
    check("B2 冲突不覆盖原文件", (bins / "同名.mp3").stat().st_size == 1 * MB)
    check("B3 新文件落到 (2)", final.name == "同名 (2).mp3" and final.exists(), final.name)
    check("B4 源文件已移走", not (src / "同名.mp3").exists())


# --------------------------------------------------------------------------- C
def case_guard(tmp: Path) -> None:
    src = tmp / "保护"
    src.mkdir()
    mk(src / "a.mp3", 10)
    (src / "保护1").mkdir()
    mk(src / "保护1" / "b.mp3", 10)

    r = run(str(src), str(src), str(src / "保护1"), "--dry-run", "--log-dir", str(tmp / "logs"))
    out = r.stdout + r.stderr
    check("C1 重复目录被拦截", "DUPLICATE_FOLDER" in out, out[:300])
    check("C2 嵌套目录被拦截", "NESTED_FOLDER" in out, out[:300])


# --------------------------------------------------------------------------- D
def case_resume(tmp: Path) -> None:
    src = tmp / "续跑"
    src.mkdir()
    for i in range(20):
        mk(src / f"r{i:02d}.mp3", 10)

    log = tmp / "logs"
    r = run(str(src), "--yes", "--skip-under", "0", "--log-dir", str(log))
    check("D1 首次执行成功", r.returncode == 0, r.stderr[-300:])

    session = sorted(d for d in log.iterdir() if (d / "state.jsonl").exists())[-1]
    state = session / "state.jsonl"
    lines = state.read_text(encoding="utf-8").splitlines()
    # 模拟"搬完了但状态只写了几行"的崩溃
    state.write_text("\n".join(lines[:3]) + "\n", encoding="utf-8")

    before = sum(count_audio(d) for d in src.iterdir() if d.is_dir())
    r2 = run("--resume", str(session.name), "--log-dir", str(log))
    out = r2.stdout + r2.stderr
    check("D2 续跑不报错", r2.returncode == 0, out[-400:])

    after = sum(count_audio(d) for d in src.iterdir() if d.is_dir())
    check("D3 续跑不产生重复文件", before == after == 20, f"{before} -> {after}")
    root_left = count_audio(src)
    check("D4 根目录无残留", root_left == 0, str(root_left))

    summary = json.loads((session / "summary.json").read_text(encoding="utf-8"))
    check("D5 会话标记完成", summary.get("status") == "completed", str(summary.get("status")))


# --------------------------------------------------------------------------- E
def case_undo(tmp: Path) -> None:
    src = tmp / "回滚"
    src.mkdir()
    for i in range(12):
        mk(src / f"u{i:02d}.mp3", 30)
        mk(src / f"u{i:02d}.lrc", 0.003)

    log = tmp / "logs"
    run(str(src), "--yes", "--skip-under", "0", "--log-dir", str(log))
    session = sorted(d for d in log.iterdir() if (d / "summary.json").exists())[-1]

    moved_out = count_audio(src)
    check("E1 已全部搬走", moved_out == 0, str(moved_out))

    r = run("--undo", str(session.name), "--log-dir", str(log))
    check("E2 回滚成功", r.returncode == 0, r.stderr[-300:])
    check("E3 音频回到原位", count_audio(src) == 12, str(count_audio(src)))
    check("E4 歌词回到原位", len(list(src.glob("*.lrc"))) == 12, str(len(list(src.glob("*.lrc")))))
    empty = [d.name for d in src.iterdir() if d.is_dir()]
    check("E5 空目录已清理", not empty, str(empty))


# --------------------------------------------------------------------------- F
def case_overflow(tmp: Path) -> None:
    src = tmp / "溢出"
    src.mkdir()
    for i in range(30):
        mk(src / f"o{i:02d}.mp3", 20)

    r = run(str(src), "--dry-run", "--overflow", "--log-dir", str(tmp / "logs"))
    out = r.stdout
    check("F1 overflow 允许接近上限", "overflow" in out, out[:200])
    sizes = [
        float(line.split("MB")[0].split()[-1])
        for line in out.splitlines()
        if line.strip().startswith("溢出") and "MB" in line
    ]
    check("F2 overflow 箱体 <= 600", sizes and max(sizes) <= 600.5, str(sizes))
    check("F3 overflow 不误报超目标", "BIN_OVER_TARGET" not in out, out[:400])


# --------------------------------------------------------------------------- F2
def case_over_target(tmp: Path) -> None:
    """单文件 > target 但 < max，应独立成箱并告警（非 overflow）。"""
    src = tmp / "超目标"
    src.mkdir()
    mk(src / "big.mp3", 580)     # target(550) < 580 < max(600)
    mk(src / "small.mp3", 10)

    r = run(str(src), "--dry-run", "--skip-under", "0", "--log-dir", str(tmp / "logs"))
    out = r.stdout + r.stderr
    check("F2a 单文件超目标被识别", "BIN_OVER_TARGET" in out, out[:400])
    check("F2b 独立成箱（2 箱）", "预计 2 个子文件夹" in out, out[:400])
    check("F2c 不报超硬上限", "BIN_OVER_MAX" not in out, out[:400])


# --------------------------------------------------------------------------- G
def case_json(tmp: Path) -> None:
    src = tmp / "json"
    src.mkdir()
    for i in range(5):
        mk(src / f"j{i}.mp3", 100)

    r = run(str(src), "--dry-run", "--json", "--skip-under", "0", "--log-dir", str(tmp / "logs"))
    try:
        data = json.loads(r.stdout)
        ok = data.get("dry_run") is True and data["folders"][0]["bins"]
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        ok = False
        data = str(exc)
    check("G1 JSON 输出可解析", ok, str(data)[:300])


# --------------------------------------------------------------------------- H
def case_readonly(tmp: Path) -> None:
    src = tmp / "只读"
    src.mkdir()
    mk(src / "ro.mp3", 10)
    os.chmod(src, 0o500)
    try:
        r = run(str(src), "--yes", "--skip-under", "0", "--log-dir", str(tmp / "logs"))
        out = r.stdout + r.stderr
        check("H1 只读目录被拦截", r.returncode == 2, f"exit={r.returncode}")
        check("H2 无 traceback", "Traceback" not in out, out[-300:])
        check("H3 文件未被移动", (src / "ro.mp3").exists())
    finally:
        os.chmod(src, 0o755)


# --------------------------------------------------------------------------- I
def case_skip_under(tmp: Path) -> None:
    """内容小于 600 MB 时默认跳过；--skip-under 0 关闭跳过。"""
    src = tmp / "小目录"
    src.mkdir()
    for i in range(3):
        mk(src / f"s{i}.mp3", 100)   # 300 MB < 600 MB

    log = tmp / "logs"
    r = run(str(src), "--dry-run", "--log-dir", str(log))
    out = r.stdout + r.stderr
    check("I1 小于阈值默认跳过", r.returncode == 0 and "无需分箱" in out, out[:300])
    subs = [d for d in src.iterdir() if d.is_dir()]
    check("I2 跳过时不生成子目录", not subs, str(subs))

    r2 = run(str(src), "--dry-run", "--skip-under", "0", "--log-dir", str(log))
    check("I3 --skip-under 0 关闭跳过", "预计 1 个子文件夹" in r2.stdout, r2.stdout[:300])


# --------------------------------------------------------------------------- J
def case_sort_name(tmp: Path) -> None:
    """--sort name 按文件名自然排序、顺序装箱。"""
    src = tmp / "排序"
    src.mkdir()
    # 名字自然序 1 < 2 < 10 < 11；体积故意乱序，避免“按大小排”碰巧一致
    for name, mb in {"1.mp3": 4, "2.mp3": 1, "10.mp3": 3, "11.mp3": 2}.items():
        mk(src / name, mb)

    log = tmp / "logs"
    r = run(str(src), "--yes", "--skip-under", "0", "--target", "5", "--max", "5",
            "--sort", "name", "--log-dir", str(log))
    check("J1 --sort name 退出码 0", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])

    b1, b2 = src / "排序1", src / "排序2"
    n1 = sorted(p.name for p in b1.iterdir()) if b1.is_dir() else []
    n2 = sorted(p.name for p in b2.iterdir()) if b2.is_dir() else []
    check("J2 第1箱是 1/2", n1 == ["1.mp3", "2.mp3"], str(n1))
    check("J3 第2箱是 10/11", n2 == ["10.mp3", "11.mp3"], str(n2))


# --------------------------------------------------------------------------- K
def case_multi_index(tmp: Path) -> None:
    """多文件夹批量整理时，操作序号必须全局唯一（否则 undo/resume 序号冲突）。"""
    a = tmp / "甲"; b = tmp / "乙"
    a.mkdir(); b.mkdir()
    for d in (a, b):
        for i in range(3):
            mk(d / f"{i:02d}.mp3", 300)   # 每目录 900 MB > 跳过阈值

    log = tmp / "logs"
    r = run(str(a), str(b), "--yes", "--log-dir", str(log))
    check("K1 多目录执行成功", r.returncode == 0, r.stdout[-300:] + r.stderr[-300:])

    session = sorted(d for d in log.iterdir() if (d / "plan.json").exists())[-1]
    plan = json.loads((session / "plan.json").read_text(encoding="utf-8"))
    idxs = [o["index"] for o in plan["ops"]]
    check("K2 操作序号全局唯一", len(idxs) == len(set(idxs)), f"{len(idxs)} vs {len(set(idxs))}")


# --------------------------------------------------------------------------- main
def main() -> int:
    print(f"测试目标：{MAIN}")
    with tempfile.TemporaryDirectory(prefix="mps-test-") as td:
        tmp = Path(td)
        for name, fn in [
            ("基本分箱", case_basic),
            ("冲突改名", case_conflict),
            ("入参保护", case_guard),
            ("崩溃续跑", case_resume),
            ("回滚", case_undo),
            ("overflow", case_overflow),
            ("超目标单文件", case_over_target),
            ("JSON", case_json),
            ("只读目录", case_readonly),
            ("小于阈值跳过", case_skip_under),
            ("按文件名排序", case_sort_name),
            ("多目录序号唯一", case_multi_index),
        ]:
            work = tmp / name
            work.mkdir()
            try:
                fn(work)
            except Exception as exc:                     # noqa: BLE001
                check(f"{name} 用例未崩溃", False, repr(exc))

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    for name, ok, detail in RESULTS:
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}" + (f"  <- {detail}" if not ok and detail else ""))
    print(f"\n{passed}/{len(RESULTS)} 通过")
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
