#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第10章 数据聚合与分组操作
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


# 10.1 GroupBy 机制
def groupby_mechanism():
    print(f"{speter*2}groupby_mechanism{speter*2}")
    print(f"{speter*2}GroupBy 机制{speter*2}")


# 10.1.1 遍历各分组
def iterating_over_groups():
    print(f"{speter*2}iterating_over_groups{speter*2}")
    print(f"{speter*2}遍历各分组{speter*2}")


# 10.1.2 选择一列或所有列的子集
def selecting_columns_or_subsets():
    print(f"{speter*2}selecting_columns_or_subsets{speter*2}")
    print(f"{speter*2}选择一列或所有列的子集{speter*2}")


# 10.1.3 使用字典和 Series 分组
def grouping_with_dictionaries_and_series():
    print(f"{speter*2}grouping_with_dictionaries_and_series{speter*2}")
    print(f"{speter*2}使用字典和 Series 分组{speter*2}")


# 10.1.4 使用函数分组
def grouping_with_functions():
    print(f"{speter*2}grouping_with_functions{speter*2}")
    print(f"{speter*2}使用函数分组{speter*2}")


# 10.1.5 根据索引层级分组
def grouping_by_index_levels():
    print(f"{speter*2}grouping_by_index_levels{speter*2}")
    print(f"{speter*2}根据索引层级分组{speter*2}")


# 10.2 数据聚合
def data_aggregation():
    print(f"{speter*2}data_aggregation{speter*2}")
    print(f"{speter*2}数据聚合{speter*2}")


# 10.2.1 逐列及多函数应用
def column_wise_and_multiple_function_application():
    print(f"{speter*2}column_wise_and_multiple_function_application{speter*2}")
    print(f"{speter*2}逐列及多函数应用{speter*2}")


# 10.2.2 返回不含行索引的聚合数据
def aggregate_without_row_index():
    print(f"{speter*2}aggregate_without_row_index{speter*2}")
    print(f"{speter*2}返回不含行索引的聚合数据{speter*2}")


# 10.3 应用：通用拆分-应用-联合
def general_split_apply_combine():
    print(f"{speter*2}general_split_apply_combine{speter*2}")
    print(f"{speter*2}应用：通用拆分-应用-联合{speter*2}")


# 10.3.1 压缩分组键
def compressing_group_keys():
    print(f"{speter*2}compressing_group_keys{speter*2}")
    print(f"{speter*2}压缩分组键{speter*2}")


# 10.3.2 分位数与桶分析
def quantile_and_bucket_analysis():
    print(f"{speter*2}quantile_and_bucket_analysis{speter*2}")
    print(f"{speter*2}分位数与桶分析{speter*2}")


# 10.3.3 示例：使用指定分组值填充缺失值
def fill_missing_values_with_group_values():
    print(f"{speter*2}fill_missing_values_with_group_values{speter*2}")
    print(f"{speter*2}示例：使用指定分组值填充缺失值{speter*2}")


# 10.3.4 示例：随机采样与排列
def random_sampling_and_permutation():
    print(f"{speter*2}random_sampling_and_permutation{speter*2}")
    print(f"{speter*2}示例：随机采样与排列{speter*2}")


# 10.3.5 示例：分组加权平均和相关性
def grouped_weighted_average_and_correlation():
    print(f"{speter*2}grouped_weighted_average_and_correlation{speter*2}")
    print(f"{speter*2}示例：分组加权平均和相关性{speter*2}")


# 10.3.6 示例：逐组线性回归
def grouped_linear_regression():
    print(f"{speter*2}grouped_linear_regression{speter*2}")
    print(f"{speter*2}示例：逐组线性回归{speter*2}")


# 10.4 数据透视表与交叉表
def pivot_tables_and_cross_tabulation():
    print(f"{speter*2}pivot_tables_and_cross_tabulation{speter*2}")
    print(f"{speter*2}数据透视表与交叉表{speter*2}")


# 10.4.1 交叉表：crosstab
def cross_tabulation_crosstab():
    print(f"{speter*2}cross_tabulation_crosstab{speter*2}")
    print(f"{speter*2}交叉表：crosstab{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
