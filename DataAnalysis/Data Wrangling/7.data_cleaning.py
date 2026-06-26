#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第7章 数据清洗与准备
# ================================

from pathlib import Path

base_dir = Path(__file__).parent


def p_info(**kwargs):
    for name, value in kwargs.items():
        print(f"{name}:")
        print(value)
    print()


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


# 7.1 处理缺失值
def handling_missing_data():
    print(f"{speter*2}handling_missing_data{speter*2}")
    print(f"{speter*2}处理缺失值{speter*2}")


# 7.1.1 过滤缺失值
def filtering_missing_data():
    print(f"{speter*2}filtering_missing_data{speter*2}")
    print(f"{speter*2}过滤缺失值{speter*2}")


# 7.1.2 补全缺失值
def filling_missing_data():
    print(f"{speter*2}filling_missing_data{speter*2}")
    print(f"{speter*2}补全缺失值{speter*2}")


# 7.2 数据转换
def data_transformation():
    print(f"{speter*2}data_transformation{speter*2}")
    print(f"{speter*2}数据转换{speter*2}")


# 7.2.1 删除重复值
def removing_duplicates():
    print(f"{speter*2}removing_duplicates{speter*2}")
    print(f"{speter*2}删除重复值{speter*2}")


# 7.2.2 使用函数或映射进行数据转换
def data_transformation_with_function_mapping():
    print(f"{speter*2}data_transformation_with_function_mapping{speter*2}")
    print(f"{speter*2}使用函数或映射进行数据转换{speter*2}")


# 7.2.3 替代值
def replacing_values():
    print(f"{speter*2}replacing_values{speter*2}")
    print(f"{speter*2}替代值{speter*2}")


# 7.2.4 重命名轴索引
def renaming_axis_indexes():
    print(f"{speter*2}renaming_axis_indexes{speter*2}")
    print(f"{speter*2}重命名轴索引{speter*2}")


# 7.2.5 离散化和分箱
def discretization_and_binning():
    print(f"{speter*2}discretization_and_binning{speter*2}")
    print(f"{speter*2}离散化和分箱{speter*2}")


# 7.2.6 检测和过滤异常值
def detecting_and_filtering_outliers():
    print(f"{speter*2}detecting_and_filtering_outliers{speter*2}")
    print(f"{speter*2}检测和过滤异常值{speter*2}")


# 7.2.7 置換和随机抽样
def permutation_and_random_sampling():
    print(f"{speter*2}permutation_and_random_sampling{speter*2}")
    print(f"{speter*2}置換和随机抽样{speter*2}")


# 7.2.8 计算指标/虚拟变量
def computing_indicators_dummy_variables():
    print(f"{speter*2}computing_indicators_dummy_variables{speter*2}")
    print(f"{speter*2}计算指标/虚拟变量{speter*2}")


# 7.3 字符串操作
def string_operations():
    print(f"{speter*2}string_operations{speter*2}")
    print(f"{speter*2}字符串操作{speter*2}")


# 7.3.1 字符串对象方法
def string_object_methods():
    print(f"{speter*2}string_object_methods{speter*2}")
    print(f"{speter*2}字符串对象方法{speter*2}")


# 7.3.2 正则表达式
def regular_expressions():
    print(f"{speter*2}regular_expressions{speter*2}")
    print(f"{speter*2}正则表达式{speter*2}")


# 7.3.3 pandas 中的向量化字符串函数
def pandas_vectorized_string_functions():
    print(f"{speter*2}pandas_vectorized_string_functions{speter*2}")
    print(f"{speter*2}pandas 中的向量化字符串函数{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        handling_missing_data()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
