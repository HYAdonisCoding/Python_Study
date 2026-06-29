#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第11章 时间序列
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


# 11.1 日期和时间数据的类型及工具
def datetime_types_and_tools():
    print(f"{speter*2}datetime_types_and_tools{speter*2}")
    print(f"{speter*2}日期和时间数据的类型及工具{speter*2}")


# 11.1.1 字符串与 datetime 互相转换
def string_datetime_conversion():
    print(f"{speter*2}string_datetime_conversion{speter*2}")
    print(f"{speter*2}字符串与 datetime 互相转换{speter*2}")


# 11.2 时间序列基础
def time_series_basics():
    print(f"{speter*2}time_series_basics{speter*2}")
    print(f"{speter*2}时间序列基础{speter*2}")


# 11.2.1 索引、选择、子集
def time_series_indexing_selection_subset():
    print(f"{speter*2}time_series_indexing_selection_subset{speter*2}")
    print(f"{speter*2}索引、选择、子集{speter*2}")


# 11.2.2 含有重复索引的时间序列
def time_series_with_duplicate_indexes():
    print(f"{speter*2}time_series_with_duplicate_indexes{speter*2}")
    print(f"{speter*2}含有重复索引的时间序列{speter*2}")


# 11.3 日期范围、频率和移位
def date_ranges_frequencies_and_shifting():
    print(f"{speter*2}date_ranges_frequencies_and_shifting{speter*2}")
    print(f"{speter*2}日期范围、频率和移位{speter*2}")


# 11.3.1 生成日期范围
def generating_date_ranges():
    print(f"{speter*2}generating_date_ranges{speter*2}")
    print(f"{speter*2}生成日期范围{speter*2}")


# 11.3.2 频率和日期偏置
def frequencies_and_date_offsets():
    print(f"{speter*2}frequencies_and_date_offsets{speter*2}")
    print(f"{speter*2}频率和日期偏置{speter*2}")


# 11.3.3 移位（前向和后向）日期
def shifting_dates_forward_backward():
    print(f"{speter*2}shifting_dates_forward_backward{speter*2}")
    print(f"{speter*2}移位（前向和后向）日期{speter*2}")


# 11.4 时区处理
def timezone_handling():
    print(f"{speter*2}timezone_handling{speter*2}")
    print(f"{speter*2}时区处理{speter*2}")


# 11.4.1 时区的本地化和转换
def timezone_localization_and_conversion():
    print(f"{speter*2}timezone_localization_and_conversion{speter*2}")
    print(f"{speter*2}时区的本地化和转换{speter*2}")


# 11.4.2 时区感知时间戳对象的操作
def timezone_aware_timestamp_operations():
    print(f"{speter*2}timezone_aware_timestamp_operations{speter*2}")
    print(f"{speter*2}时区感知时间戳对象的操作{speter*2}")


# 11.4.3 不同时区间的操作
def operations_between_timezones():
    print(f"{speter*2}operations_between_timezones{speter*2}")
    print(f"{speter*2}不同时区间的操作{speter*2}")


# 11.5 时间区间和区间算术
def time_periods_and_period_arithmetic():
    print(f"{speter*2}time_periods_and_period_arithmetic{speter*2}")
    print(f"{speter*2}时间区间和区间算术{speter*2}")


# 11.5.1 区间频率转换
def period_frequency_conversion():
    print(f"{speter*2}period_frequency_conversion{speter*2}")
    print(f"{speter*2}区间频率转换{speter*2}")


# 11.5.2 季度区间频率
def quarterly_period_frequency():
    print(f"{speter*2}quarterly_period_frequency{speter*2}")
    print(f"{speter*2}季度区间频率{speter*2}")


# 11.5.3 将时间戳转换区间（以及逆转换）
def timestamp_period_conversion():
    print(f"{speter*2}timestamp_period_conversion{speter*2}")
    print(f"{speter*2}将时间戳转换区间（以及逆转换）{speter*2}")


# 11.5.4 从数组生成 PeriodIndex
def creating_periodindex_from_arrays():
    print(f"{speter*2}creating_periodindex_from_arrays{speter*2}")
    print(f"{speter*2}从数组生成 PeriodIndex{speter*2}")


# 11.6 重新采样与频率转换
def resampling_and_frequency_conversion():
    print(f"{speter*2}resampling_and_frequency_conversion{speter*2}")
    print(f"{speter*2}重新采样与频率转换{speter*2}")


# 11.6.1 向下采样
def downsampling():
    print(f"{speter*2}downsampling{speter*2}")
    print(f"{speter*2}向下采样{speter*2}")


# 11.6.2 向上采样与插值
def upsampling_and_interpolation():
    print(f"{speter*2}upsampling_and_interpolation{speter*2}")
    print(f"{speter*2}向上采样与插值{speter*2}")


# 11.6.3 使用区间进行重新采样
def resampling_with_periods():
    print(f"{speter*2}resampling_with_periods{speter*2}")
    print(f"{speter*2}使用区间进行重新采样{speter*2}")


# 11.7 移动窗口函数
def moving_window_functions():
    print(f"{speter*2}moving_window_functions{speter*2}")
    print(f"{speter*2}移动窗口函数{speter*2}")


# 11.7.1 指数加权函数
def exponentially_weighted_functions():
    print(f"{speter*2}exponentially_weighted_functions{speter*2}")
    print(f"{speter*2}指数加权函数{speter*2}")


# 11.7.2 二元移动窗口函数
def binary_moving_window_functions():
    print(f"{speter*2}binary_moving_window_functions{speter*2}")
    print(f"{speter*2}二元移动窗口函数{speter*2}")


# 11.7.3 用户自定义的移动窗口函数
def custom_moving_window_functions():
    print(f"{speter*2}custom_moving_window_functions{speter*2}")
    print(f"{speter*2}用户自定义的移动窗口函数{speter*2}")


# 11.8 本章小结
def chapter_11_summary():
    print(f"{speter*2}chapter_11_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
