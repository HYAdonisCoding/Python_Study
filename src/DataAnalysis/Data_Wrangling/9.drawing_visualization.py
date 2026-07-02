#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第9章 绘图与可视化
# ================================
from pathlib import Path
from matplotlib_font import setup_matplotlib_chinese

base_dir = Path(__file__).parent


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


def show_plot(seconds=8, save_path=None, title=None, dpi=400):
    if title:

        plt.title(title)
    if save_path:
        plt.savefig(f"{base_dir}/{save_path}", dpi=dpi, bbox_inches="tight")
        p_info(title="save successed", save_path=f"{base_dir}/{save_path}")

    plt.show(block=False)
    plt.pause(seconds)
    plt.close()


# 9.1 简明 matplotlib API 入门
def matplotlib_api_introduction():
    print(f"{speter*2}matplotlib_api_introduction{speter*2}")
    print(f"{speter*2}简明 matplotlib API 入门{speter*2}")
    data = np.arange(10)

    p_info(data=data)
    plt.plot(data)  # 绘制折线
    plt.show(block=False)  # 非阻塞显示窗口
    plt.pause(8)  # 等待 8 秒
    plt.close()  # 自动关闭窗口


# 9.1.1 图片与子图
def figures_and_subplots():
    print(f"{speter*2}figures_and_subplots{speter*2}")
    print(f"{speter*2}图片与子图{speter*2}")

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    # ax3.plot(np.random.standard_normal(50).cumsum(), color="black", linestyle="dashed")
    # plt.plot([1.5, 3.5, -2, 1.6])
    plt.plot(np.random.standard_normal(50).cumsum(), "k--")

    _ = ax1.hist(np.random.standard_normal(100), bins=20, color="black", alpha=0.3)
    ax2 = ax2.scatter(np.arange(30), np.arange(30) + 3 * np.random.standard_normal(30))

    # fig, axes = plt.subplots(2, 3)
    # p_info(
    #     axes=axes,
    # )

    # subplots_adjust(
    #     left=None, bottom=None, right=None, top=None, wspace=None, hspace=None
    # )
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
    for i in range(2):
        for j in range(2):
            axes[i, j].hist(
                np.random.standard_normal(500), bins=50, color="black", alpha=0.5
            )
    # fig.subplots_adjust(wspace=0, hspace=0)
    fig.tight_layout()
    show_plot()


from numpy.random import randn


# 9.1.2 颜色、标记和线类型
def colors_markers_and_line_styles():
    print(f"{speter*2}colors_markers_and_line_styles{speter*2}")
    print(f"{speter*2}颜色、标记和线类型{speter*2}")

    # plt.plot(randn(30).cumsum(), "ko--")
    # plt.plot(randn(30).cumsum(), color="k", linestyle="dashed", marker="o")
    data = np.random.randn(30).cumsum()
    plt.plot(data, "k--", label="Default")
    plt.plot(data, "k-", drawstyle="steps-post", label="steps-post")
    plt.legend(loc="best")
    show_plot()


# 9.1.3 刻度、标签和图例
def ticks_labels_and_legends():
    print(f"{speter*2}ticks_labels_and_legends{speter*2}")
    print(f"{speter*2}刻度、标签和图例{speter*2}")
    fig, ax = plt.subplots()
    # ax = fig.add_subplot(1, 1, 1)
    ax.plot(np.random.randn(1000).cumsum())
    ticks = ax.set_xticks([0, 250, 500, 750, 1000])
    labels = ax.set_xticklabels(
        ["one", "two", "three", "four", "five"], rotation=30, fontsize=8
    )
    # ax.set_xlabel("Stages")
    # ax.set_title("My first matplotlib plot")
    props = {
        "title": "My first matplotlib plot",
        "xlabel": "Stages",
        "ylabel": "Stages_y",
    }
    ax.set(**props)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax1 = ax.plot(randn(1000).cumsum(), "k", label="one")
    ax2 = ax.plot(randn(1000).cumsum(), "k--", label="two")
    ax3 = ax.plot(randn(1000).cumsum(), "k.", label="three")
    ax.legend(loc="best")
    p_info(
        ax1=ax1,
        ax2=ax2,
        ax3=ax3,
    )
    show_plot()


from datetime import datetime


# 9.1.4 注释与子图加工
def annotations_and_subplot_adjustments():
    print(f"{speter*2}annotations_and_subplot_adjustments{speter*2}")
    print(f"{speter*2}注释与子图加工{speter*2}")
    fig, ax = plt.subplots()

    data = pd.read_csv(f"{base_dir}/examples/spx.csv", index_col=0, parse_dates=True)
    spx = data["SPX"]

    spx.plot(ax=ax, color="black")

    crisis_data = [
        (datetime(2007, 10, 11), "Peak of bull market"),
        (datetime(2008, 3, 12), "Bear Stearns Fails"),
        (datetime(2008, 9, 15), "Lehman Bankruptcy"),
    ]

    for date, label in crisis_data:
        ax.annotate(
            label,
            xy=(date, spx.asof(date) + 75),
            xytext=(date, spx.asof(date) + 225),
            arrowprops=dict(facecolor="black", headwidth=4, width=2, headlength=4),
            horizontalalignment="left",
            verticalalignment="top",
        )

    # Zoom in on 2007-2010
    ax.set_xlim(["1/1/2007", "1/1/2011"])
    ax.set_ylim([600, 1800])

    ax.set_title("Important dates in the 2008–2009 financial crisis")

    fig, ax = plt.subplots(figsize=(12, 6))
    rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color="black", alpha=0.3)
    circ = plt.Circle((0.7, 0.2), 0.15, color="blue", alpha=0.3)
    pgon = plt.Polygon(
        [[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]], color="green", alpha=0.5
    )
    ax.add_patch(rect)
    ax.add_patch(circ)
    ax.add_patch(pgon)
    # show_plot()
    show_plot(save_path="figpath.png")


from io import BytesIO


# 9.1.5 将图片保存到文件
def saving_figures_to_files():
    print(f"{speter*2}saving_figures_to_files{speter*2}")
    print(f"{speter*2}将图片保存到文件{speter*2}")

    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()

    show_plot(save_path="figpath.png")


# 9.1.6 matplotlib 设置
def matplotlib_configuration():
    print(f"{speter*2}matplotlib_configuration{speter*2}")
    print(f"{speter*2}matplotlib 设置{speter*2}")
    # from matplotlib import font_manager

    # fonts = sorted(set(f.name for f in font_manager.fontManager.ttflist))

    # for font in fonts:
    #     if "Ping" in font or "Hei" in font or "Song" in font or "Kai" in font:
    #         print(font)
    plt.rc("figure", figsize=(10, 10))

    font_options = {
        "family": "Heiti SC",
        "weight": "normal",
        "size": 12,
    }

    plt.rc("font", **font_options)
    plt.rcParams["axes.unicode_minus"] = False

    # 画一张测试图

    x = np.arange(10)

    plt.plot(x, x**2)

    plt.title("Test 标题")

    plt.xlabel("X 轴")

    plt.ylabel("Y 轴")
    show_plot()


# 9.2 使用 pandas 和 seaborn 绘图
def plotting_with_pandas_and_seaborn():
    print(f"{speter*2}plotting_with_pandas_and_seaborn{speter*2}")
    print(f"{speter*2}使用 pandas 和 seaborn 绘图{speter*2}")

    show_plot()


# 9.2.1 折线图
def line_plots():
    print(f"{speter*2}line_plots{speter*2}")
    print(f"{speter*2}折线图{speter*2}")
    s = pd.Series(np.random.standard_normal(10).cumsum(), index=np.arange(0, 100, 10))
    s.plot()
    df = pd.DataFrame(
        np.random.standard_normal((10, 4)).cumsum(0),
        columns=["A", "B", "C", "D"],
        index=np.arange(0, 100, 10),
    )
    plt.style.use("grayscale")
    df.plot()
    show_plot(title="折线图")


import seaborn as sns


# 9.2.2 柱状图
def bar_plots():
    print(f"{speter*2}bar_plots{speter*2}")
    print(f"{speter*2}柱状图{speter*2}")
    # fig, axes = plt.subplots(2, 1)
    # data = pd.Series(np.random.uniform(size=16), index=list("abcdefghijklmnop"))
    # data.plot.bar(ax=axes[0], color="black", alpha=0.7)
    # data.plot.barh(ax=axes[1], color="black", alpha=0.7)

    df = pd.DataFrame(
        np.random.uniform(size=(6, 4)),
        index=["one", "two", "three", "four", "five", "six"],
        columns=pd.Index(["A", "B", "C", "D"], name="Genus"),
    )
    p_info(df=df)
    # df.plot.bar()
    # df.plot.barh(stacked=True, alpha=0.5)

    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")

    party_counts = pd.crosstab(tips["day"], tips["size"])
    party_counts = party_counts.reindex(index=["Thur", "Fri", "Sat", "Sun"])
    party_counts = party_counts.loc[:, 2:5]
    party_pcts = party_counts.div(party_counts.sum(axis="columns"), axis="index")

    # party_pcts.plot.bar(stacked=False)
    p_info(
        head=tips.head(),
        cnt=party_counts,
        party_pcts=party_pcts,
    )

    tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])

    sns.barplot(x="tip_pct", y="day", data=tips, orient="h")
    sns.barplot(x="tip_pct", y="day", hue="time", data=tips, orient="h")
    sns.set_style("whitegrid")
    p_info(
        head=tips.head(),
    )
    show_plot()


# 9.2.3 直方图和密度图
def histograms_and_density_plots():
    print(f"{speter*2}histograms_and_density_plots{speter*2}")
    print(f"{speter*2}直方图和密度图{speter*2}")
    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])
    tips["tip_pct"].plot.hist(bins=50)
    plt.figure()
    tips["tip_pct"].plot.density()
    comp1 = np.random.standard_normal(200)
    comp2 = 10 + 2 * np.random.standard_normal(200)
    values = pd.Series(np.concatenate([comp1, comp2]))

    # sns.histplot(values, bins=100, color="black")
    sns.distplot(values, bins=100, color="k")
    show_plot()


# 9.2.4 散点图或点图
def scatter_plots_or_point_plots():
    print(f"{speter*2}scatter_plots_or_point_plots{speter*2}")
    print(f"{speter*2}散点图或点图{speter*2}")
    macro = pd.read_csv(f"{base_dir}/examples/macrodata.csv")
    data = macro[["cpi", "m1", "tbilrate", "unemp"]]
    trans_data = np.log(data).diff().dropna()

    plt.figure()
    ax = sns.regplot(x="m1", y="unemp", data=trans_data)
    ax.set_title("Changes in log(m1) versus log(unemp)")
    sns.pairplot(trans_data, diag_kind="kde", plot_kws={"alpha": 0.2})

    p_info(
        data=trans_data.tail(),
    )
    show_plot()


# 9.2.5 分面网格和分类数据
def facet_grids_and_categorical_data():
    print(f"{speter*2}facet_grids_and_categorical_data{speter*2}")
    print(f"{speter*2}分面网格和分类数据{speter*2}")
    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / (tips["total_bill"] - tips["tip"])
    sns.catplot(
        x="day",
        y="tip_pct",
        hue="time",
        col="smoker",
        kind="bar",
        data=tips[tips.tip_pct < 1],
    )
    sns.catplot(
        x="day",
        y="tip_pct",
        row="time",
        col="smoker",
        kind="bar",
        data=tips[tips.tip_pct < 1],
    )
    sns.catplot(x="tip_pct", y="day", kind="box", data=tips[tips.tip_pct < 0.5])
    show_plot()


# 9.3 其他 Python 可视化工具
def other_python_visualization_tools():
    print(f"{speter*2}other_python_visualization_tools{speter*2}")
    print(f"{speter*2}其他 Python 可视化工具{speter*2}")
    show_plot()


# 9.4 本章小结
def chapter_9_summary():
    print(f"{speter*2}chapter_9_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    setup_matplotlib_chinese()
    try:
        facet_grids_and_categorical_data()

    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
