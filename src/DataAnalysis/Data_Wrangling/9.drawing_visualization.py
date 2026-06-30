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


# 9.1 简明 matplotlib API 入门
def matplotlib_api_introduction():
    print(f"{speter*2}matplotlib_api_introduction{speter*2}")
    print(f"{speter*2}简明 matplotlib API 入门{speter*2}")


# 9.1.1 图片与子图
def figures_and_subplots():
    print(f"{speter*2}figures_and_subplots{speter*2}")
    print(f"{speter*2}图片与子图{speter*2}")


# 9.1.2 颜色、标记和线类型
def colors_markers_and_line_styles():
    print(f"{speter*2}colors_markers_and_line_styles{speter*2}")
    print(f"{speter*2}颜色、标记和线类型{speter*2}")


# 9.1.3 刻度、标签和图例
def ticks_labels_and_legends():
    print(f"{speter*2}ticks_labels_and_legends{speter*2}")
    print(f"{speter*2}刻度、标签和图例{speter*2}")


# 9.1.4 注释与子图加工
def annotations_and_subplot_adjustments():
    print(f"{speter*2}annotations_and_subplot_adjustments{speter*2}")
    print(f"{speter*2}注释与子图加工{speter*2}")


# 9.1.5 将图片保存到文件
def saving_figures_to_files():
    print(f"{speter*2}saving_figures_to_files{speter*2}")
    print(f"{speter*2}将图片保存到文件{speter*2}")


# 9.1.6 matplotlib 设置
def matplotlib_configuration():
    print(f"{speter*2}matplotlib_configuration{speter*2}")
    print(f"{speter*2}matplotlib 设置{speter*2}")


# 9.2 使用 pandas 和 seaborn 绘图
def plotting_with_pandas_and_seaborn():
    print(f"{speter*2}plotting_with_pandas_and_seaborn{speter*2}")
    print(f"{speter*2}使用 pandas 和 seaborn 绘图{speter*2}")


# 9.2.1 折线图
def line_plots():
    print(f"{speter*2}line_plots{speter*2}")
    print(f"{speter*2}折线图{speter*2}")


# 9.2.2 柱状图
def bar_plots():
    print(f"{speter*2}bar_plots{speter*2}")
    print(f"{speter*2}柱状图{speter*2}")


# 9.2.3 直方图和密度图
def histograms_and_density_plots():
    print(f"{speter*2}histograms_and_density_plots{speter*2}")
    print(f"{speter*2}直方图和密度图{speter*2}")


# 9.2.4 散点图或点图
def scatter_plots_or_point_plots():
    print(f"{speter*2}scatter_plots_or_point_plots{speter*2}")
    print(f"{speter*2}散点图或点图{speter*2}")


# 9.2.5 分面网格和分类数据
def facet_grids_and_categorical_data():
    print(f"{speter*2}facet_grids_and_categorical_data{speter*2}")
    print(f"{speter*2}分面网格和分类数据{speter*2}")


# 9.3 其他 Python 可视化工具
def other_python_visualization_tools():
    print(f"{speter*2}other_python_visualization_tools{speter*2}")
    print(f"{speter*2}其他 Python 可视化工具{speter*2}")


# 9.4 本章小结
def chapter_9_summary():
    print(f"{speter*2}chapter_9_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
