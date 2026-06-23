#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第14章 数据分析示例
# ================================
from pathlib import Path
base_dir = Path(__file__).parent
def test():
    print(f"{speter*2}test{speter*2}")
    path = f'{base_dir}/examples/segismundo.txt'



# 14.1 从 Bitly 获取 1.USA.gov 数据
def bitly_usagov_data():
    print(f"{speter*2}bitly_usagov_data{speter*2}")
    print(f"{speter*2}从 Bitly 获取 1.USA.gov 数据{speter*2}")


# 14.1.1 纯 Python 时区计数
def timezone_counting_with_pure_python():
    print(f"{speter*2}timezone_counting_with_pure_python{speter*2}")
    print(f"{speter*2}纯 Python 时区计数{speter*2}")


# 14.1.2 使用 pandas 进行时区计数
def timezone_counting_with_pandas():
    print(f"{speter*2}timezone_counting_with_pandas{speter*2}")
    print(f"{speter*2}使用 pandas 进行时区计数{speter*2}")


# 14.2 MovieLens 1M 数据集
def movielens_1m_dataset():
    print(f"{speter*2}movielens_1m_dataset{speter*2}")
    print(f"{speter*2}MovieLens 1M 数据集{speter*2}")


# 14.2.1 测量评价分歧
def measuring_rating_disagreement():
    print(f"{speter*2}measuring_rating_disagreement{speter*2}")
    print(f"{speter*2}测量评价分歧{speter*2}")


# 14.3 美国1880～2010年的婴儿名字
def us_baby_names_1880_2010():
    print(f"{speter*2}us_baby_names_1880_2010{speter*2}")
    print(f"{speter*2}美国1880～2010年的婴儿名字{speter*2}")


# 14.3.1 分析名字趋势
def analyzing_name_trends():
    print(f"{speter*2}analyzing_name_trends{speter*2}")
    print(f"{speter*2}分析名字趋势{speter*2}")


# 14.4 美国农业部食品数据库
def usda_food_database():
    print(f"{speter*2}usda_food_database{speter*2}")
    print(f"{speter*2}美国农业部食品数据库{speter*2}")


# 14.5 2012年联邦选举委员会数据库
def fec_2012_election_database():
    print(f"{speter*2}fec_2012_election_database{speter*2}")
    print(f"{speter*2}2012年联邦选举委员会数据库{speter*2}")


# 14.5.1 按职业和雇主的捐献统计
def donations_by_occupation_and_employer():
    print(f"{speter*2}donations_by_occupation_and_employer{speter*2}")
    print(f"{speter*2}按职业和雇主的捐献统计{speter*2}")


# 14.5.2 捐赠金额分桶
def donation_amount_binning():
    print(f"{speter*2}donation_amount_binning{speter*2}")
    print(f"{speter*2}捐赠金额分桶{speter*2}")


# 14.5.3 按州进行捐赠统计
def donation_statistics_by_state():
    print(f"{speter*2}donation_statistics_by_state{speter*2}")
    print(f"{speter*2}按州进行捐赠统计{speter*2}")


# 14.6 本章小结
def chapter_14_summary():
    print(f"{speter*2}chapter_14_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


