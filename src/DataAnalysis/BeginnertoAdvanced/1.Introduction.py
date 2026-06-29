#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第一章 数据分析入门
# Introduction to Data Analysis

import os
from scipy import stats
import pandas as pd
import statsmodels.formula.api as smf

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "Chapter_1_Data")
# 推断性统计分析


#  * t检验
# H0: 充电宝容量均值为5000mAh
# H1: 充电宝容量均值不为5000mAh
def inferential_statistical_analysis():
    # 读取充电宝容量数据
    volumns = [4988, 5006, 5021, 4923, 4947, 4896, 5104, 4922, 5070, 5009, 4892, 4997]
    # t检验

    # t 检验
    t_test_result = stats.ttest_1samp(volumns, popmean=5000)
    print(f"t检验结果: {t_test_result}")


#  * 卡方检验
# H0: 学生性别与其是否被录取相互独立
# H1: 学生性别与其是否被录取不相互独立
def chi_square_test():
    # 读入高三学生的数据
    students_data = pd.read_excel(f"{DATA_DIR}/卡方检验与Persion检验.xlsx")
    # print(students_data)
    # 构造两个离散型变量之间的频次统计表（或列联表）
    crosstable = pd.crosstab(students_data.Gender, students_data.Offer)
    print(crosstable)
    # 计算卡方值
    chi2, p, dof, expected = stats.chi2_contingency(crosstable)
    print(f"卡方值: {chi2}, p值: {p}, 自由度: {dof}, 期望频次: {expected}")
    # 判断是否拒绝原假设
    if p < 0.05:
        print("拒绝原假设，学生性别与其是否被录取相互独立")
    else:
        print("接受原假设，学生性别与其是否被录取相互独立")


#  * 对比概率P值
# H0: 汽车速度与刹车距离不相关
# H1: 汽车速度与刹车距离相关
def p_test():
    # 读入的数据
    cars = pd.read_excel(f"{DATA_DIR}/卡方检验与Persion检验.xlsx", sheet_name=1)
    # print(cars)
    # 构造两个离散型变量之间的频次统计表（或列联表）
    statistic, p = stats.pearsonr(cars.speed, cars.dist)
    print(f"statistic：{statistic}, p值：{p}")
    if p < 0.05:
        print("拒绝原假设")
    else:
        print("接受原假设")


#  * Shapiro正态性检验
# H0: 乘客的年龄数据服从正态分布
# H1: 乘客的年龄数据不服从正态分布
def normality_test():
    # 读入Titanic的数据
    titanic = pd.read_csv(f"{DATA_DIR}/Titanic.csv")
    # 提出年龄中的缺失值，再做Shapiro检查
    statistic, p = stats.shapiro(titanic.Age[~titanic.Age.isnull()])
    print(f"statistic：{statistic}, p值：{p}")
    if p < 0.05:
        print("拒绝原假设")
    else:
        print("接受原假设")


#  * 预测分析法中的线性回归模型，对数据进行建模，并基于模型实现商品销售利润的预测
def predictive_analysis():
    # 读取商品利润数据
    profit = pd.read_csv(f"{DATA_DIR}/Profit.csv")
    # 创建多远线性回归模型
    lm = smf.ols(
        "Profit ~ RD_Spend + Administration + Marketing_Spend", data=profit
    ).fit()
    # 返回模型概览
    lm.summary()
    print(lm.summary())
    """
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                 Profit   R-squared:                       0.951
Model:                            OLS   Adj. R-squared:                  0.948
Method:                 Least Squares   F-statistic:                     296.0
Date:                Mon, 08 Dec 2025   Prob (F-statistic):           4.53e-30
Time:                        10:58:23   Log-Likelihood:                -525.39
No. Observations:                  50   AIC:                             1059.
Df Residuals:                      46   BIC:                             1066.
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
===================================================================================
                      coef    std err          t      P>|t|      [0.025      0.975]
-----------------------------------------------------------------------------------
Intercept        5.012e+04   6572.353      7.626      0.000    3.69e+04    6.34e+04
RD_Spend            0.8057      0.045     17.846      0.000       0.715       0.897
Administration     -0.0268      0.051     -0.526      0.602      -0.130       0.076
Marketing_Spend     0.0272      0.016      1.655      0.105      -0.006       0.060
==============================================================================
Omnibus:                       14.838   Durbin-Watson:                   1.282
Prob(Omnibus):                  0.001   Jarque-Bera (JB):               21.442
Skew:                          -0.949   Prob(JB):                     2.21e-05
Kurtosis:                       5.586   Cond. No.                     1.40e+06
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.4e+06. This might indicate that there are
strong multicollinearity or other numerical problems.
    """
    # 不考虑模型的显著性和回归系数的显著性（仅看coef这列），得到的回归模型可表示为：
    # Profit = 5.012+0.81RD_Spend - 0.03Administration + 0.03Marketing_Spend


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        predictive_analysis()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
