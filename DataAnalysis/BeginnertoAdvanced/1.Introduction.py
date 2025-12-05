#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第一章 数据分析入门
# Introduction to Data Analysis

from scipy import stats

# 推断性统计分析

#  * t检验
# H0: 充电宝容量均值为5000mAh
# H1: 充电宝容量均值不为5000mAh
def inferential_statistical_analysis():
    # 读取充电宝容量数据
    volumns = [4988,5006,5021,4923,4947,4896,5104,4922,5070,5009,4892,4997]
    # t检验
    
    # t 检验
    t_test_result = stats.ttest_1samp(volumns, popmean=5000)
    print(f"t检验结果: {t_test_result}")
    
#  * 卡方检验
# H0: 学生性别与其是否被录取相互独立
# H1: 学生性别与其是否被录取不相互独立
def chi_square_test():
    pass

#  * Shapiro正态性检验
# H0: 乘客的年龄数据服从正态分布
# H1: 乘客的年龄数据不服从正态分布
def normality_test():
    pass


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        inferential_statistical_analysis()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


