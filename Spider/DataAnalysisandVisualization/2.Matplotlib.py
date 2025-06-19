# !/usr/bin/python
# -*- coding: UTF-8 -*-

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import os
import numpy as np
from sympy.physics.quantum.tests.test_circuitplot import mpl


def is_chinese_font(font_path):
    """快速检查字体是否支持中文（通过Unicode范围判断）"""
    try:
        font = font_manager.FontProperties(fname=font_path)
        fontname = font.get_name()
        # 取代表性汉字“汉”的编码，查看字体是否包含该字符
        font_obj = font_manager.get_font(font_path)
        return font_obj.get_char_index(ord("汉")) != 0
    except Exception:
        return False


def set_chinese_font_preferably():
    """设置中文主字体 + fallback 英文数学字体"""
    fallback_font_name = font_manager.FontProperties(
        fname=font_manager.findfont("DejaVu Sans")
    ).get_name()
    preferred_fonts = [
        "PingFang SC",
        "Hiragino Sans GB",
        "Songti SC",
        "Heiti SC",
        "Arial Unicode MS",
        "Microsoft YaHei",
        "SimHei",
        "Source Han Sans SC",
        "Noto Sans CJK SC",
    ]

    # 尝试使用优选字体
    for font_name in preferred_fonts:
        try:
            font_path = font_manager.findfont(font_name, fallback_to_default=False)
            if is_chinese_font(font_path):
                chinese_font = font_manager.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams["font.family"] = [chinese_font, fallback_font_name]
                print(
                    f"[INFO] 设置默认中文字体为：{chinese_font}（fallback: {fallback_font_name}）"
                )
                return
        except Exception:
            continue

    # 没找到优选字体，扫描所有字体
    for f in font_manager.fontManager.ttflist:
        try:
            if is_chinese_font(f.fname):
                chinese_font = font_manager.FontProperties(fname=f.fname).get_name()
                matplotlib.rcParams["font.family"] = [chinese_font, fallback_font_name]
                print(
                    f"[INFO] 自动选择支持中文的字体为：{chinese_font}（fallback: {fallback_font_name}）"
                )
                return
        except Exception:
            continue

    # 无可用字体
    print(f"[WARNING] 未找到支持中文的字体，仅使用 fallback: {fallback_font_name}")
    matplotlib.rcParams["font.family"] = fallback_font_name


def base():
    print("-" * 30, "绘图基础", "-" * 30)

    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.plot(data)
    plt.title("示例图：数字序列")
    plt.ylabel(
        "数字序列",
    )
    plt.xlabel("索引")
    plt.show()


def GettingStartedExample():
    print("-" * 30, "Getting Started Example", "-" * 30)
    data_x = [1, 2, 3, 4, 5]
    data_y = [6, 7, 8, 9, 10]

    plt.plot(data_x, data_y)
    plt.ylabel("数字序列")
    plt.show()


def GettingStartedExample1():
    data_x = [1, 2, 3, 4, 5]
    data_y = [3, 5, 4, 7, 10]

    plt.ylabel("数字序列")
    plt.plot(data_x, data_y, "ro")
    plt.axis([0, 10, 2, 12])
    plt.show()


def numpy_array():

    data_x = np.array([1, 2, 3, 4, 5])
    data_y = np.array([3, 5, 4, 7, 10])

    plt.ylabel("数字序列")

    plt.plot(data_x * 2, data_y, "r--", data_x * 3, data_y, "bs")
    plt.show()


def plotting_using_keyword_arguments():
    print("-" * 30, "使用关键字参数绘图", "-" * 30)
    data = {"a": np.arange(20), "b": np.random.randint(0, 20, 20)}
    plt.scatter("a", "b", data=data)
    plt.xlabel("x 序列")
    plt.ylabel("y 序列")
    plt.show()


def group_drawing():
    print("-" * 30, "分组绘图", "-" * 30)
    group_name = ["A", "B", "C", "D", "E"]
    values = [1, 20, 30, 40, 50]

    plt.figure(1, figsize=(10, 5))

    plt.subplot(131)
    plt.bar(group_name, values)
    plt.subplot(132)
    plt.scatter(group_name, values)
    plt.subplot(133)
    plt.plot(group_name, values)
    plt.suptitle("分组绘制")
    plt.show()


def line_properties():
    print("-" * 30, "线条属性", "-" * 30)
    lines = plt.plot([1, 2, 3, 4], [1, 4, 9, 16], [1, 2, 3, 4] * 2, [1, 4, 9, 16] * 2)
    plt.axis([0, 6, 0, 20])
    lines[0].set_antialiased(False)

    plt.setp(lines, "color", "r", "linewidth", 2.0)
    plt.show()


def canvas_and_subgraphs():
    print("-" * 30, "画布与子图", "-" * 30)
    plt.figure(1)
    plt.subplot(211)
    plt.plot([1, 2, 3])
    plt.subplot(212)
    line = plt.plot([4, 5, 6])

    plt.figure(2)
    plt.plot([4, 5, 6])
    plt.show()

    plt.figure(1)
    plt.subplot(212)
    plt.title("第1张画图的第2个子图")
    plt.show()


def add_text():
    print("-" * 30, "添加文本", "-" * 30)
    lines = plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.axis([0, 6, 0, 20])
    lines[0].set_antialiased(False)
    plt.title("线性图")
    plt.xlabel("x轴", fontsize=14, color="red")
    plt.ylabel("y轴")
    plt.text(2, 10, r"数据走势", color="green")
    plt.show()


def add_text1():
    print("-" * 30, "添加文本1", "-" * 30)
    plt.plot([1, 5, 10, 15, 20, 25], [1, 5, 10, 15, 20, 25])

    plt.annotate(
        "中间值",
        xy=(12.5, 12.5),
        xytext=(15, 10),
        arrowprops=dict(facecolor="black", shrink=0.05),
    )
    plt.show()


def setting_the_style():
    print("-" * 30, "设置样式", "-" * 30)
    plt.style.use("tableau-colorblind10")
    data = np.random.randn(50)
    plt.plot(data)
    plt.show()
    print(plt.style.available)


def temporarily_style():
    print("-" * 30, "临时引入样式", "-" * 30)
    with plt.style.context(("dark_background")):
        data = np.linspace(0, 3 * np.pi)
        plt.plot(np.sin(data), "r-o")
        plt.title("临时引入样式")
        plt.show()


def rc_params():
    print("-" * 30, "rc参数", "-" * 30)

    mpl.rcParams["lines.linewidth"] = 2
    mpl.rcParams["lines.color"] = "r"
    plt.plot(np.sin(np.arange(0, 10)), "b-.")
    plt.show()


# *图形样例
def drawing_example():
    print("-" * 30, "绘图示例", "-" * 30)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(np.sin(np.arange(0, 10)), "b-.")
    plt.subplot(212)
    plt.plot(np.sin(np.arange(0, 10)), "r+")
    plt.show()


def histogram():
    print("-" * 30, "直方图", "-" * 30)

    data = np.array([0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 10])
    plt.hist(data, bins=10, color="red", edgecolor="black", alpha=1)
    plt.xlabel("范围")
    plt.ylabel("频数或者频率")
    plt.title("直方图")
    plt.show()


def bar_chart():
    print("-" * 30, "条形图", "-" * 30)
    names = ["Wilson", "Warren", "Leon", "Bruce", "Andrew", "Edith"]
    score = [69, 85, 98, 71, 82, 99]

    plt.barh(range(6), score, color="red")
    plt.yticks(range(6), names)

    for i in range(6):
        plt.text(score[i], i, score[i])

    plt.show()


def vertical_bar_chart():
    print("-" * 30, "垂直条形图", "-" * 30)
    names = ["Wilson", "Warren", "Leon", "Bruce", "Andrew", "Edith"]
    en_score = [69, 85, 72, 40, 55, 99]
    math_score = [79, 78, 100, 87, 81, 68]

    en_bar = plt.bar(
        range(6), height=en_score, width=0.3, alpha=0.8, color="red", label="英语成绩"
    )
    math_bar = plt.bar(
        [i + 0.3 for i in range(6)],
        height=math_score,
        width=0.3,
        color="green",
        label="数学成绩",
    )

    plt.xticks([i + 0.15 for i in range(6)], names)
    plt.xlabel("成绩统计图")

    plt.legend()
    plt.ylabel("成绩范围")

    for en in en_bar:
        height = en.get_height()
        plt.text(
            en.get_x() + en.get_width() / 2,
            height + 1,
            str(height),
            ha="center",
            va="bottom",
        )
    for math in math_bar:
        height = math.get_height()
        plt.text(
            math.get_x() + math.get_width() / 2,
            height + 1,
            str(height),
            ha="center",
            va="bottom",
        )

    plt.show()


def pie_chart():
    print("-" * 30, "饼状图", "-" * 30)
    leves = ["优", "良", "中", "差"]
    data = [10, 15, 20, 15]
    colors = ["red", "green", "purple", "royalblue"]
    explode = [0.1, 0, 0, 0]
    plt.pie(
        data,
        explode=explode,
        colors=colors,
        labels=leves,
        labeldistance=1.1,
        shadow=False,
        startangle=90,
        pctdistance=0.6,
    )

    plt.legend()
    plt.show()


def scatter_plot_chart():
    print("-" * 30, "散点图", "-" * 30)
    data_x = np.array([92, 68, 78, 69, 95, 99, 89, 72])
    data_y = np.array([46, 34, 39, 60, 74, 85, 59, 98])
    plt.figure(1)
    plt.scatter(data_x, data_y, marker="o", c="r")
    plt.show()


def box_plot_chart():
    print("-" * 30, "箱线图", "-" * 30)
    data = np.array([92, 68, 78, 69, 95, 99, 89, 72, 46, 34, 39, 60, 74, 85, 59, 98])
    plt.boxplot(data, meanline=True, notch=fal)
    plt.show()


def polar_plot_chart():
    print("-" * 30, "极坐标图", "-" * 30)
    data = np.arange(0, 100, 10)
    print(data)
    ax = plt.subplot(111, projection="polar")
    ax.set_xticklabels(["S1", "S2", "S3", "S4", "S5", "S6", "S7", "8"])
    ax.plot(data, data, "-.", lw=2)
    plt.show()


def line_plot_chart():
    print("-" * 30, "折线图", "-" * 30)
    mean_scores = np.array([94, 85, 75, 91, 69, 83, 89, 86])
    term = [
        "第一学习",
        "第二学习",
        "第三一学习",
        "第四学习",
        "第五学习",
        "第六学习",
        "第七学习",
        "第八学习",
    ]

    plt.plot(term, mean_scores, color="r", marker="o")

    plt.xlabel("成绩分析")
    plt.ylabel("成绩")
    plt.show()


def business_data_visualization():
    print("-" * 30, "营业数据可视化", "-" * 30)
    current_dir = os.path.dirname(__file__)
    file = os.path.join(current_dir, "..", "data", "销售数据.CSV")

    # 处理数据
    sales_info = np.loadtxt(file, dtype=str, delimiter=",")
    sales_info_1 = sales_info[0:15, :]
    sales_info_2 = sales_info[15:-1, :]

    plt.figure()
    # 绘制折线图
    plt.plot(sales_info_1[:, 0], sales_info_1[:, 2].astype(int), color="r", marker="o")
    plt.plot(sales_info_2[:, 0], sales_info_2[:, 2].astype(int), color="g", marker="o")
    plt.xticks(range(15), sales_info[range(15), 0], rotation=45)
    plt.title('折线图')
    plt.show()

    # 2.分别计算门店总营业额，绘制饼图
    sales_info_1_sum = sales_info_1[:, 2].astype(int).sum()
    sales_info_2_sum = sales_info_2[:, 2].astype(int).sum()

    pie_data = np.array([sales_info_1_sum, sales_info_2_sum])
    mendian = ["门店1", "门店2"]
    colors = ["red", "green"]
    explode = [0.05, 0]
    plt.pie(
        pie_data,
        explode=explode,
        colors=colors,
        labels=mendian,
        labeldistance=1.1,
        shadow=False,
        startangle=90,
        pctdistance=0.6,
    )
    plt.legend()
    plt.title('饼图')
    plt.show()

    # 3.绘制条形图
    date_list = sales_info_1[:, 0]
    count = date_list.size
    mendian_1 = sales_info_1[:, 2].astype(int)
    print(mendian_1)
    mendian_2 = sales_info_2[:, 2].astype(int)
    print(mendian_2)

    mendian_bar_1 = plt.bar(
        range(count),
        height=mendian_1,
        width=0.3,
        alpha=0.8,
        color="red",
        label="1店销售额",
    )
    mendian_bar_2 = plt.bar(
        [i + 0.3 for i in range(count)],
        height=mendian_2,
        width=0.3,
        color="green",
        label="2店销售额",
    )

    plt.xticks([i + 0.15 for i in range(count)], date_list, rotation=45)
    plt.xlabel("销售分析图")

    plt.legend()

    for m1 in mendian_bar_1:
        height = m1.get_height()
        plt.text(
            m1.get_x() + m1.get_width() / 2,
            height + 1,
            str(height),
            ha="center",
            va="bottom",
            rotation=90,
        )
    for m2 in mendian_bar_2:
        height = m2.get_height()
        plt.text(
            m2.get_x() + m2.get_width() / 2,
            height + 1,
            str(height),
            ha="center",
            va="bottom",
            rotation=90,
        )
    plt.title('条形图')
    plt.show()


# 调用函数设置字体
set_chinese_font_preferably()
if __name__ == "__main__":

    business_data_visualization()
