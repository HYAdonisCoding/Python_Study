#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8

import platform
import matplotlib.pyplot as plt
from matplotlib import font_manager


def _get_system_fonts():
    """收集系统可用字体"""
    return sorted(set(f.name for f in font_manager.fontManager.ttflist))


def _pick_chinese_font():
    """
    自动选择可用中文字体
    按优先级排序（macOS / Windows / Linux）
    """
    fonts = _get_system_fonts()

    candidates = [
        # macOS
        "PingFang SC",
        "Heiti SC",
        "Songti SC",
        "STSong",
        "STHeiti",
        "Kaiti SC",
        # Windows
        "Microsoft YaHei",
        "SimHei",
        # Linux / 通用
        "Noto Sans CJK SC",
        "WenQuanYi Zen Hei",
    ]

    for f in candidates:
        if f in fonts:
            return f

    # fallback：避免彻底崩
    return "DejaVu Sans"


def setup_matplotlib_chinese(font_size=12, figsize=(10, 6)):
    """
    一键配置 matplotlib 中文环境
    """

    font = _pick_chinese_font()

    print(f"[Matplotlib Font] Selected font: {font}")

    plt.rcParams.update(
        {
            "font.family": font,
            "font.size": font_size,
            "axes.unicode_minus": False,  # 解决负号乱码
            "figure.figsize": figsize,
        }
    )

    return font


def debug_fonts(keyword="SC"):
    """
    打印系统字体（调试用）
    """
    fonts = _get_system_fonts()
    return [f for f in fonts if keyword in f]


if __name__ == "__main__":
    setup_matplotlib_chinese()
    speter = "-" * 10
    print(f"{speter*2}Starting{speter*2}")
