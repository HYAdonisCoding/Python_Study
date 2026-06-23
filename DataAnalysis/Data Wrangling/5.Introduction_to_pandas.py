#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第5章 pandas入门
from pathlib import Path
base_dir = Path(__file__).parent
speter = "-" * 10


# 5.1 pandas 数据结构介绍
def pandas_data_structures_introduction():
    print(f"{speter*2}pandas_data_structures_introduction{speter*2}")
    print(f"{speter*2}pandas 数据结构介绍{speter*2}")


# 5.1.1 Series
def series():
    print(f"{speter*2}series{speter*2}")
    print(f"{speter*2}Series{speter*2}")


# 5.1.2 DataFrame
def dataframe():
    print(f"{speter*2}dataframe{speter*2}")
    print(f"{speter*2}DataFrame{speter*2}")


# 5.1.3 索引对象
def index_objects():
    print(f"{speter*2}index_objects{speter*2}")
    print(f"{speter*2}索引对象{speter*2}")


# 5.2 基本功能
def basic_functionality():
    print(f"{speter*2}basic_functionality{speter*2}")
    print(f"{speter*2}基本功能{speter*2}")


# 5.2.1 重建索引
def reindexing():
    print(f"{speter*2}reindexing{speter*2}")
    print(f"{speter*2}重建索引{speter*2}")


# 5.2.2 轴向上删除条目
def dropping_entries_from_axis():
    print(f"{speter*2}dropping_entries_from_axis{speter*2}")
    print(f"{speter*2}轴向上删除条目{speter*2}")


# 5.2.3 索引、选择与过滤
def indexing_selection_filtering():
    print(f"{speter*2}indexing_selection_filtering{speter*2}")
    print(f"{speter*2}索引、选择与过滤{speter*2}")


# 5.2.4 整数索引
def integer_indexing():
    print(f"{speter*2}integer_indexing{speter*2}")
    print(f"{speter*2}整数索引{speter*2}")


# 5.2.5 算术和数据对齐
def arithmetic_and_data_alignment():
    print(f"{speter*2}arithmetic_and_data_alignment{speter*2}")
    print(f"{speter*2}算术和数据对齐{speter*2}")


# 5.2.6 函数应用和映射
def function_application_and_mapping():
    print(f"{speter*2}function_application_and_mapping{speter*2}")
    print(f"{speter*2}函数应用和映射{speter*2}")


# 5.2.7 排序和排名
def sorting_and_ranking():
    print(f"{speter*2}sorting_and_ranking{speter*2}")
    print(f"{speter*2}排序和排名{speter*2}")


# 5.2.8 含有重复标签的轴索引
def duplicate_labels_axis_index():
    print(f"{speter*2}duplicate_labels_axis_index{speter*2}")
    print(f"{speter*2}含有重复标签的轴索引{speter*2}")


# 5.3 描述性统计的概述与计算
def descriptive_statistics():
    print(f"{speter*2}descriptive_statistics{speter*2}")
    print(f"{speter*2}描述性统计的概述与计算{speter*2}")


# 5.3.1 相关性和协方差
def correlation_and_covariance():
    print(f"{speter*2}correlation_and_covariance{speter*2}")
    print(f"{speter*2}相关性和协方差{speter*2}")


# 5.3.2 唯一值、计数和成员属性
def unique_values_counts_membership():
    print(f"{speter*2}unique_values_counts_membership{speter*2}")
    print(f"{speter*2}唯一值、计数和成员属性{speter*2}")



    
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        pandas_data_structures_introduction()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


