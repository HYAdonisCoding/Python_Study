#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第13章 Python 建模库介绍
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


# 13.1 pandas 与建模代码的结合
def pandas_and_modeling_code_integration():
    print(f"{speter*2}pandas_and_modeling_code_integration{speter*2}")
    print(f"{speter*2}pandas 与建模代码的结合{speter*2}")


# 13.2 使用 Patsy 创建模型描述
def creating_model_descriptions_with_patsy():
    print(f"{speter*2}creating_model_descriptions_with_patsy{speter*2}")
    print(f"{speter*2}使用 Patsy 创建模型描述{speter*2}")


# 13.2.1 Patsy 公式中的数据转换
def data_transformations_in_patsy_formulas():
    print(f"{speter*2}data_transformations_in_patsy_formulas{speter*2}")
    print(f"{speter*2}Patsy 公式中的数据转换{speter*2}")


# 13.2.2 分类数据与 Patsy
def categorical_data_with_patsy():
    print(f"{speter*2}categorical_data_with_patsy{speter*2}")
    print(f"{speter*2}分类数据与 Patsy{speter*2}")


# 13.3 statsmodels 介绍
def statsmodels_introduction():
    print(f"{speter*2}statsmodels_introduction{speter*2}")
    print(f"{speter*2}statsmodels 介绍{speter*2}")


# 13.3.1 评估线性模型
def evaluating_linear_models():
    print(f"{speter*2}evaluating_linear_models{speter*2}")
    print(f"{speter*2}评估线性模型{speter*2}")


# 13.3.2 评估时间序列处理
def evaluating_time_series_processing():
    print(f"{speter*2}evaluating_time_series_processing{speter*2}")
    print(f"{speter*2}评估时间序列处理{speter*2}")


# 13.4 scikit-learn 介绍
def sklearn_introduction():
    print(f"{speter*2}sklearn_introduction{speter*2}")
    print(f"{speter*2}scikit-learn 介绍{speter*2}")


# 13.5 继续你的教育
def continue_your_education():
    print(f"{speter*2}continue_your_education{speter*2}")
    print(f"{speter*2}继续你的教育{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
