#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第8章 数据规整：连接、联合与重塑
# ================================
from pathlib import Path

base_dir = Path(__file__).parent


from src.DataAnalysis.Data_Wrangling.debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


# 8.1 分层索引
def hierarchical_indexing():
    print(f"{speter*2}hierarchical_indexing{speter*2}")
    print(f"{speter*2}分层索引{speter*2}")


# 8.1.1 重排序和层级排序
def reordering_and_sorting_levels():
    print(f"{speter*2}reordering_and_sorting_levels{speter*2}")
    print(f"{speter*2}重排序和层级排序{speter*2}")


# 8.1.2 按层级进行汇总统计
def summary_statistics_by_level():
    print(f"{speter*2}summary_statistics_by_level{speter*2}")
    print(f"{speter*2}按层级进行汇总统计{speter*2}")


# 8.1.3 使用 DataFrame 的列进行索引
def indexing_with_dataframe_columns():
    print(f"{speter*2}indexing_with_dataframe_columns{speter*2}")
    print(f"{speter*2}使用 DataFrame 的列进行索引{speter*2}")


# 8.2 联合与合并数据集
def combining_and_merging_datasets():
    print(f"{speter*2}combining_and_merging_datasets{speter*2}")
    print(f"{speter*2}联合与合并数据集{speter*2}")


# 8.2.1 数据库风格的 DataFrame 连接
def database_style_dataframe_join():
    print(f"{speter*2}database_style_dataframe_join{speter*2}")
    print(f"{speter*2}数据库风格的 DataFrame 连接{speter*2}")


# 8.2.2 根据索引合并
def merging_on_index():
    print(f"{speter*2}merging_on_index{speter*2}")
    print(f"{speter*2}根据索引合并{speter*2}")


# 8.2.3 沿轴向连接
def concatenating_along_axis():
    print(f"{speter*2}concatenating_along_axis{speter*2}")
    print(f"{speter*2}沿轴向连接{speter*2}")


# 8.2.4 联合重叠数据
def combining_overlapping_data():
    print(f"{speter*2}combining_overlapping_data{speter*2}")
    print(f"{speter*2}联合重叠数据{speter*2}")


# 8.3 重塑和透视
def reshaping_and_pivoting():
    print(f"{speter*2}reshaping_and_pivoting{speter*2}")
    print(f"{speter*2}重塑和透视{speter*2}")


# 8.3.1 使用多层索引进行重塑
def reshaping_with_hierarchical_index():
    print(f"{speter*2}reshaping_with_hierarchical_index{speter*2}")
    print(f"{speter*2}使用多层索引进行重塑{speter*2}")


# 8.3.2 将“长”透视为“宽”
def pivot_long_to_wide():
    print(f"{speter*2}pivot_long_to_wide{speter*2}")
    print(f"{speter*2}将长透视为宽{speter*2}")


# 8.3.3 将“宽”透视为“长”
def pivot_wide_to_long():
    print(f"{speter*2}pivot_wide_to_long{speter*2}")
    print(f"{speter*2}将宽透视为长{speter*2}")


# 8.4 本章小结
def chapter_8_summary():
    print(f"{speter*2}chapter_8_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
