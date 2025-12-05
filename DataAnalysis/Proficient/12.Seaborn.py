#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
# 12.Seaborn 可视化 Seaborn visualization
import os
import platform
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats

speter = "-" * 10


def seabornBase():

    sns.set()
    tips = sns.load_dataset("tips")
    sns.relplot(
        x="total_bill",
        y="tip",
        col="time",
        hue="smoker",
        style="smoker",
        size="size",
        data=tips,
    )

    plt.show()


# 使用散点图观察数据分布
def seaborn_scatter_plots():
    sns.set()
    tips = sns.load_dataset("tips")
    # sns.relplot(x="total_bill", y="tip", data=tips)
    # sns.relplot(x="total_bill", y="tip", hue="smoker", data=tips)
    # sns.relplot(x="total_bill", y="tip", hue="smoker", style="smoker", data=tips)
    # sns.relplot(x="total_bill", y="tip", hue="smoker", style="time", data=tips)
    # sns.relplot(x="total_bill", y="tip", hue="size", data=tips)
    sns.relplot(
        x="total_bill", y="tip", hue="smoker", size="size", sizes=(15, 200), data=tips
    )
    plt.show()


# 使用线程图观察数据趋势
def seaborn_thread_graphs():
    sns.set()
    # df = pd.DataFrame(dict(time=np.arange(500),value=np.random.randn(500).cumsum()))
    # g = sns.relplot(x="time", y="value", kind="line", data=df)
    # 日期格式
    df = pd.DataFrame(
        dict(
            time=pd.date_range("2019-1-1", periods=500),
            value=np.random.randn(500).cumsum(),
        )
    )
    g = sns.relplot(x="time", y="value", kind="line", data=df)
    g.fig.autofmt_xdate()
    plt.show()


# 绘制多图
def seaborn_more_graphs():
    sns.set()
    # fmri = sns.load_dataset("fmri")
    # sns.relplot(x="timepoint", y="signal", hue="subject",
    #             col="region", row="event", height=3,
    #             kind="line", estimator=None, data=fmri)

    # 分类散点图
    tips = sns.load_dataset("tips")
    # sns.catplot(x="day", y="total_bill", kind="strip", data=tips)
    # sns.catplot(x="day", y="total_bill", kind="swarm", data=tips)
    # sns.catplot(x="total_bill", y="day", hue="time", kind="swarm", data=tips)

    # sns.catplot(x="day", y="total_bill", kind="box", data=tips)#箱型图
    diamonds = sns.load_dataset("diamonds")
    sns.catplot(
        x="color", y="price", kind="boxen", data=diamonds.sort_values("color")
    )  # 箱型图2
    # sns.catplot(x="day", y="total_bill", kind="violin",split=True,inner="stick",palette="pastel", data=tips)#小提琴图
    plt.show()


# 在类别内部观察趋势
def seaborn_observe_trends_within():
    sns.set()
    titanic = sns.load_dataset("titanic")
    # sns.catplot(x="sex", y="survived", hue="class", kind="bar", data=titanic)#条形图
    # sns.catplot(x="deck", kind="count", palette="ch:.25", data=titanic)
    sns.catplot(x="sex", y="survived", hue="class", kind="point", data=titanic)  # 点图
    plt.show()


# 单变量与双变量
def univariate_bivariate():
    # 绘制单变量分布
    sns.set()
    # x = np.random.normal(size=100)
    # sns.distplot(x, bins=20, kde=False, rug=True)
    # plt.show()

    # 单变量核密度估计
    # x = np.random.normal(size=100)
    # sns.kdeplot(x)
    # sns.kdeplot(x, bw=.2, label="bw: 0.2")
    # sns.kdeplot(x, bw=2, label="bw: 2")
    # plt.legend()
    # plt.show()

    # 拟合参数分布
    # x = np.random.gamma(6, size=200)
    # sns.distplot(x, kde=False, fit=stats.gamma)
    # plt.show()

    # 散点图
    # mean, cov = [0, 1], [(1, .5), (.5, 1)]
    # data = np.random.multivariate_normal(mean, cov, 200)
    # df = pd.DataFrame(data, columns=["x", "y"])
    # sns.jointplot(x="x", y="y", data=df)
    # plt.show()

    # Hexbin图
    # mean, cov = [0, 1], [(1, .5), (.5, 1)]
    # x, y = np.random.multivariate_normal(mean, cov, 1000).T
    # with sns.axes_style("white"):
    #     sns.jointplot(x=x, y=y, kind="hex", color="k")
    # plt.show()

    # 双变量核密度估计
    # mean, cov = [0, 1], [(1, .5), (.5, 1)]
    # data = np.random.multivariate_normal(mean, cov, 200)
    # df = pd.DataFrame(data, columns=["x", "y"])
    # sns.jointplot(x="x", y="y", data=df, kind="kde")

    # 绘制二维核密度图
    # mean, cov = [0, 1], [(1, .5), (.5, 1)]
    # data = np.random.multivariate_normal(mean, cov, 200)
    # df = pd.DataFrame(data, columns=["x", "y"])
    # f, ax = plt.subplots(figsize=(6, 6))
    # sns.kdeplot(x=df.x, y=df.y, ax=ax)
    # sns.rugplot(df.x, color="g", ax=ax)
    # sns.rugplot(df.y, vertical=True, ax=ax)

    # 数据集中的对应关系
    # iris = sns.load_dataset("iris")
    # sns.pairplot(iris)

    # 线性回归函数
    # tips = sns.load_dataset("tips")
    # sns.lmplot(x="total_bill", y="tip", data=tips)

    # 多项式回归
    anscombe = sns.load_dataset("anscombe")
    sns.lmplot(
        x="x",
        y="y",
        data=anscombe.query("dataset == 'II'"),
        order=2,
        ci=None,
        scatter_kws={"s": 80},
    )

    # 非阻塞显示
    plt.show(block=False)
    plt.pause(10)  # 暂停10秒（保持图像显示）
    plt.close()  # 自动关闭图像窗口


# 成绩分析可视化
def performanceAnalysis():
    # 获取当前脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 拼接文件完整路径
    file = os.path.join(base_dir, "成绩统计表.xlsx")

    # 1 获取成绩分部信息
    sns.set()
    # plt.rcParams["font.sans-serif"] = ["SimHei"]
    # 解决字体问题
    system = platform.system()
    if system == "Darwin":  # macOS
        plt.rcParams["font.sans-serif"] = ["Heiti TC", "Arial Unicode MS"]
    elif system == "Windows":
        plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
    else:  # Linux
        plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC"]

    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

    df = pd.read_excel(file, sheet_name="成绩表")

    # 过滤掉 “总分” 列中无法转换为数字的行
    df = df[pd.to_numeric(df["总分"], errors="coerce").notnull()]
    df["总分"] = pd.to_numeric(df["总分"], errors="coerce")

    sns.relplot(x="学号", y="总分", data=df)
    plt.xticks(rotation=45)
    # plt.show()

    # 各等级成绩分布箱线图
    sns.catplot(x="等级", y="平均分", kind="boxen", data=df)
    sns.catplot(x="等级", y="平均分", kind="box", data=df)
    sns.catplot(
        x="等级",
        y="平均分",
        kind="box",
        data=df,
        notch=True,  # 添加凹口（显示置信区间）
        fliersize=4,  # 离群点大小
        palette="Set3",  # 调色方案
    )
    # plt.show()

    # 各科目成绩排名
    course = df.columns.values[1:13]
    means = df.iloc[-1, 1:13]
    df = pd.DataFrame({"科目名称": course, "各科成绩": means})
    sns.catplot(
        x="各科成绩",
        y="科目名称",
        kind="bar",
        data=df.sort_values("各科成绩", ascending=False),
    )

    plt.title("各科平均成绩排名")
    # 非阻塞显示
    plt.show(block=False)
    plt.pause(100)  # 暂停10秒（保持图像显示）
    plt.close()  # 自动关闭图像窗口


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        performanceAnalysis()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
