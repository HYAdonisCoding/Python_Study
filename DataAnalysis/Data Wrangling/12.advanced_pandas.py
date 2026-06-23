#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第12章 高阶 pandas
# ================================

from pathlib import Path
base_dir = Path(__file__).parent
def test():
    print(f"{speter*2}test{speter*2}")
    path = f'{base_dir}/examples/segismundo.txt'






# 12.1 分类数据
def categorical_data():
    print(f"{speter*2}categorical_data{speter*2}")
    print(f"{speter*2}分类数据{speter*2}")


# 12.1.1 背景和目标
def categorical_background_and_goals():
    print(f"{speter*2}categorical_background_and_goals{speter*2}")
    print(f"{speter*2}背景和目标{speter*2}")


# 12.1.2 pandas 中的 Categorical类型
def pandas_categorical_type():
    print(f"{speter*2}pandas_categorical_type{speter*2}")
    print(f"{speter*2}pandas 中的 Categorical类型{speter*2}")


# 12.1.3 使用Categorical 对象进行计算
def computations_with_categorical_objects():
    print(f"{speter*2}computations_with_categorical_objects{speter*2}")
    print(f"{speter*2}使用Categorical 对象进行计算{speter*2}")


# 12.1.4 分类方法
def categorical_methods():
    print(f"{speter*2}categorical_methods{speter*2}")
    print(f"{speter*2}分类方法{speter*2}")


# 12.2 高阶 GroupBy 应用
def advanced_groupby_applications():
    print(f"{speter*2}advanced_groupby_applications{speter*2}")
    print(f"{speter*2}高阶 GroupBy 应用{speter*2}")


# 12.2.1 分组转换和“展开”GroupBy
def group_transformations_and_unstack_groupby():
    print(f"{speter*2}group_transformations_and_unstack_groupby{speter*2}")
    print(f"{speter*2}分组转换和“展开”GroupBy{speter*2}")


# 12.2.2 分组的时间重新采样
def grouped_time_resampling():
    print(f"{speter*2}grouped_time_resampling{speter*2}")
    print(f"{speter*2}分组的时间重新采样{speter*2}")


# 12.3 方法链技术
def method_chaining_techniques():
    print(f"{speter*2}method_chaining_techniques{speter*2}")
    print(f"{speter*2}方法链技术{speter*2}")


# 12.3.1 pipe 方法
def pipe_method():
    print(f"{speter*2}pipe_method{speter*2}")
    print(f"{speter*2}pipe 方法{speter*2}")


# 12.4 本章小结
def chapter_12_summary():
    print(f"{speter*2}chapter_12_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")

if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


