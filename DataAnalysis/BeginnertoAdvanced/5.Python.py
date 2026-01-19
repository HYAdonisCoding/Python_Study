#!/Users/adam/envs/py_arm64/bin/python 
# # #!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8

import matplotlib.font_manager as fm
import os
import statsmodels.api as sm
from scipy.stats import fit
from base_class import speter, BASE_DIR
import pandas as pd
import numpy as np

# 第五章 数据分析进阶 Python 数据分析
# Chapter 5 Advanced Data Analysis: Python Data Analysis


def read_txt_data():
    data1 = pd.read_table(
        filepath_or_buffer=f"{BASE_DIR}/Chapter_5_Data/datas/data1.txt",
        sep=",",
        header=None,
        names=["id", "name", "gender", "occupation"],
        skiprows=2,
        #   skipfooter=2,
        comment="#",
        #   converters={'id':str}
    )
    print(data1)


def read_excel_data():
    io = f"{BASE_DIR}/Chapter_5_Data/datas/data2.xlsx"
    data1 = pd.read_excel(
        io,
        sheet_name=0,
        header=0,
        names=["id", "date", "prod_name", "colour", "price"],
        converters={0: str},
        na_values="未知",
    )
    print(data1)


import pymysql


def read_sql_data():
    connect = pymysql.connect(
        host="localhost",
        user="root",
        passwd="chy123",
        database="train",
        charset="utf8",
    )
    # 读取数据
    data = pd.read_sql(
        "select * from sec_buildings where direction='朝南'", con=connect
    )

    # 关闭链接
    connect.close()

    print(data.head())


from sqlalchemy import create_engine


def read_sql_data_pro():
    engine = create_engine(
        "mysql+pymysql://root:chy123@localhost:3306/train?charset=utf8mb4"
    )
    data = pd.read_sql("select * from sec_buildings where direction='朝南'", con=engine)
    print(data.head())


# 数据类型的判断和转换
def data_type_identification_and_conversion():
    io = f"{BASE_DIR}/Chapter_5_Data/datas/data3.xlsx"
    data1 = pd.read_excel(
        io,
        sheet_name=0,
        header=0,
        # names=["id", "date", "prod_name", "colour", "price"],
        converters={0: str},
        na_values="未知",
    )
    print(data1.shape)
    print(data1.dtypes)
    # 数值类型转换
    data1["id"] = data1["id"].astype(str)
    # 数值类型转换
    data1["custom_amt"] = data1["custom_amt"].str[1:].astype(float)
    # 字符类型转换日期型
    data1["order_date"] = pd.to_datetime(data1["order_date"], format="%Y年%m月%d日")
    print(data1.shape)
    print(data1.dtypes)
    print(data1.head())
    # 冗余数据判断
    print(data1.duplicated().any())
    # 缺失数据的判断与处理
    print("判断各变量中是否存在缺失值：\n", data1.isnull().any(axis=0))
    print("各变量中缺失值的数量：\n", data1.isnull().sum(axis=0))
    print("各变量中缺失值的比例：\n", data1.isnull().sum(axis=0) / data1.shape[0])

    print("判断各数据行中是否存在缺失值：\n", data1.isnull().any(axis=1).any())
    print("缺失观察值的数量：\n", data1.isnull().any(axis=1).sum())
    print("缺失观察值的比例：\n", data1.isnull().any(axis=1).sum() / data1.shape[0])
    """判断各变量中是否存在缺失值：
    id            False
    gender         True
    age            True
    edu            True
    custom_amt    False
    order_date    False
    dtype: bool
    各变量中缺失值的数量：
    id               0
    gender         136
    age            100
    edu           1927
    custom_amt       0
    order_date       0
    dtype: int64
    各变量中缺失值的比例：
    id            0.000000
    gender        0.045333
    age           0.033333
    edu           0.642333
    custom_amt    0.000000
    order_date    0.000000
    dtype: float64
    判断各数据行中是否存在缺失值：
    True
    缺失观察值的数量：
    2024
    缺失观察值的比例：
    0.6746666666666666
    """
    # 删除观测值，如删除age变量中所对应的缺失观测值
    data1_new = data1.drop(labels=data1.index[data1["age"].isnull()], axis=0)
    print(data1_new.shape)

    # 替换法处理缺失值
    data1.fillna(
        value={
            "gender": data1["gender"].mode()[0],  # 使用性别的众数替换缺失性别
            "age": data1["age"].mean,  # 使用年龄的平均值替换缺失年龄
            "edu": "专科",
        },
        inplace=True,  # 原地修改数据
    )
    print("各变量中缺失值的数量：\n", data1.isnull().sum(axis=0))


# 数据的引用
def data_reference():
    # 构造数据框
    df1 = pd.DataFrame(
        {
            "name": ["张三", "李四", "王五", "赵六", "孙七"],
            "age": [20, 21, 22, 23, 24],
            "gender": ["男", "女", "女", "女", "男"],
            "edu": ["本科", "硕士", "专科", "本科", "硕士"],
        },
        columns=["name", "age", "gender", "edu"],
    )
    # 查看数据预览
    print(df1)
    # 取出数据集的中间三行(即所有女性)，并且返回姓名、年龄和受教育水平三列
    print("iloc方法：", df1.iloc[1:4, [0, 3, 2]])
    print("loc方法：", df1.loc[1:3, ["name", "age", "edu"]])
    # print('ix方法：', df1.ix[1:3, [0,3,2]])#ix 已经在新版本 Pandas 中移除了
    # 将员工的姓名用作行标签
    df2 = df1.set_index("name")
    print(df2)
    # 取出数据集的中间三行(即所有女性)，并且返回姓名、年龄和受教育水平三列
    print("iloc方法：", df2.iloc[1:4, :])
    print("loc方法：", df2.loc[["李四", "王五", "赵六"], :])
    # print('ix方法：', df2.ix[1:3, [0,3,2]])#ix 已经在新版本 Pandas 中移除了

    # 基于loc方法作筛选
    print("loc方法作筛选：", df2.loc[df2["gender"] == "男", ["age", "edu"]])
    # 删除观测，如删除age变量中所对应的缺失观测
    df2_new = df2.drop(labels=df2.index[df2["age"].isnull()], axis=0)
    print(df2_new)
    print(df2_new.shape)


# 多表合并与连接
def multi_table_connect():
    df1 = pd.DataFrame(
        {
            "name": ["张三", "李四", "王五"],
            "age": [20, 21, 22],
            "gender": ["男", "女", "女"],
            "edu": ["本科", "硕士", "专科"],
        },
        columns=["name", "age", "gender", "edu"],
    )
    df2 = pd.DataFrame(
        {
            "name": ["赵六", "孙七"],
            "age": [23, 24],
            "gender": ["女", "男"],
            "edu": ["本科", "硕士"],
        },
        columns=["name", "age", "gender", "edu"],
    )
    df3 = pd.concat([df1, df2], keys=["df1", "df2"])
    print(df3)
    print(df3.shape)
    df3.reset_index(level=0, inplace=True)
    df3.rename(columns={"level_0": "tab_name"}, inplace=True)
    df3.index = range(df3.shape[0])
    print(df3)
    print(df3.shape)
    # 数据横向合并
    df4 = pd.concat([df1, df2])
    print(df4)
    print(df4.shape)
    # 数据横向合并,仅保留与df2列索引值一致的数据，类似于交集
    # df5 = pd.concat([df1,df2], join_axes=[df2.index], axis=1)
    df5 = pd.concat([df1.reindex(df2.index), df2], axis=1)
    print(df5)
    print(df5.shape)


# 连接
def multi_table_connect():
    df3 = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "name": ["张三", "李四", "王二", "丁一", "赵武"],
            "age": [20, 21, 22, 23, 24],
            "gender": ["男", "男", "男", "女", "女"],
            "edu": ["本科", "硕士", "专科", "本科", "硕士"],
        },
        columns=["id", "name", "age", "gender", "edu"],
    )
    df4 = pd.DataFrame(
        {
            "id": [1, 2, 2, 4, 4, 4, 5],
            "score": [83, 81, 87, 75, 86, 74, 88],
            "kemu": ["科目1", "科目1", "科目2", "科目1", "科目2", "科目3", "科目1"],
        },
        columns=["id", "score", "kemu"],
    )
    df5 = pd.DataFrame(
        {
            "id": [1, 3, 5],
            "name": ["张三", "王二", "赵武"],
            "income": [13500, 18000, 15000],
        },
        columns=["id", "name", "income"],
    )
    print("df3:\n", df3)
    print("df4:\n", df4)
    print("df5:\n", df5)
    # 首先df3和df4连接
    merge1 = pd.merge(left=df3, right=df4, how="left", left_on="id", right_on="id")
    print("merge1:\n", merge1)
    print(merge1.shape)
    # 再将连接结果与df5连接
    merge2 = pd.merge(left=merge1, right=df5, how="left")
    print("merge2:\n", merge2)
    print(merge2.shape)


# 数据的汇总
def data_summary():
    diamonds = pd.read_table(f"{BASE_DIR}/Chapter_5_Data/datas/diamonds.csv", sep=",")
    # 单个分组变量的均值统计
    summary1 = pd.pivot_table(
        data=diamonds, index="color", values="price", margins=True, margins_name="总计"
    )
    print("summary1:\n", summary1)
    # # 多个分组变量的均值统计
    summary2 = pd.pivot_table(
        data=diamonds,
        index="clarity",
        columns="cut",
        values="carat",
        aggfunc=np.size,
        margins=True,
        margins_name="总计",
    )
    print("summary2:\n", summary2)


# 分组聚合操作
def group_aggregate():
    diamonds = pd.read_table(f"{BASE_DIR}/Chapter_5_Data/datas/diamonds.csv", sep=",")
    grouped = diamonds.groupby(by=["color", "cut"])
    result = grouped.aggregate(
        {"color": np.size, "carat": np.min, "price": np.mean, "face_width": np.max}
    )
    result = pd.DataFrame(result, columns=["color", "carat", "price", "face_width"])
    print("result:\n", result)
    # 数据集重命名
    result.rename(
        columns={
            "color": "counts",
            "carat": "min_weight",
            "price": "avg_price",
            "face_width": "max_face_width",
        },
        inplace=True,
    )
    print("数据集重命名:\n", result)
    # 将行索引变量数据框的变量
    result.reset_index(inplace=True)
    print("将行索引变量数据框的变量:\n", result)


"""
箱线图（Box Plot），又称盒须图，是一种用于描述数据分布特征和异常情况的统计图形，常见于探索性数据分析中。

核心构成：
	1.	中位数（Median）：箱体中的一条线，反映数据的集中位置。
	2.	上下四分位数（Q1、Q3）：箱体的下边和上边，分别表示25%与75%分位点。
	3.	四分位距（IQR）：Q3 − Q1，衡量数据的离散程度，抗极端值能力强。
	4.	须（Whiskers）：通常延伸至 Q1 − 1.5×IQR, Q3 + 1.5×IQR 范围内的最小值和最大值。
	5.	异常值（Outliers）：落在须之外的点，提示可能的极端或异常观测。

主要作用：
	•	快速判断分布的集中趋势与离散程度
	•	识别偏态（对称/左偏/右偏）
	•	发现异常值，辅助数据清洗与风险识别
	•	便于多组数据对比（同一图中并列多个箱线图）

特点与局限：
	•	优点：直观、稳健、对异常值敏感
	•	局限：不展示具体分布形态（如多峰结构），通常需结合直方图或密度图使用

总体而言，箱线图是**“用最少元素概括数据整体结构”**的高效工具，尤其适合决策前的数据初步诊断。
"""
import matplotlib.pyplot as plt


# 基于箱线图的异常值检测
def outlier_detection():
    # 读取数据
    sunpots = pd.read_table(f"{BASE_DIR}/Chapter_5_Data/datas/sunspots.csv", sep=",")
    plt.boxplot(
        x=sunpots["counts"],
        whis=1.5,  # 1.5倍的四分位差
        widths=0.7,  # 指定箱线图的宽度
        patch_artist=True,  # 指定需要填充箱体颜色
        showmeans=True,  # 指定需要显示均值
        boxprops={"facecolor": "steelblue"},  # 指定箱体的填充色
        flierprops={
            "markerfacecolor": "red",
            "markeredgecolor": "red",
            "markersize": 4,
        },  # 指定异常点的填充色、边框色和大小
        meanprops={
            "marker": "D",
            "markerfacecolor": "black",
            "markersize": 4,
        },  # 指定均值点的标记符号（菱形）、填充色和大小
        medianprops={
            "linestyle": "--",
            "color": "orange",
        },  # 指定中位数的标记符号（虚线）和颜色
        labels=[""],
    )  # 绘制箱线图
    # 显示图形
    plt.show()

    # 计算下四分位数和上四分位数
    q1 = np.percentile(sunpots["counts"], 25)
    q3 = np.percentile(sunpots["counts"], 75)
    print("下四分位数:\n", q1)
    print("上四分位数:\n", q3)
    # 计算四分位距
    iqr = q3 - q1
    print("四分位距:\n", iqr)
    # 计算下限
    lower_limit = q1 - 1.5 * iqr
    print("下限:\n", lower_limit)
    # 计算上限
    upper_limit = q3 + 1.5 * iqr
    print("上限:\n", upper_limit)
    # 寻找异常点
    outliers = sunpots["counts"][
        (sunpots["counts"] > upper_limit) | (sunpots["counts"] < lower_limit)
    ]
    print("异常点:\n", outliers)


import matplotlib as mpl


# 基于正态分布的异常值检测
def normal_distribution_outlier_detection():
    # 读取数据
    pay_ratio = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/pay_ratio.xlsx")

    plt.plot(
        pay_ratio["date"],  # x轴数据
        pay_ratio["ratio"],  # y轴数据
        linestyle="-",
        linewidth=2,  # 折线宽度
        color="steelblue",
        marker="o",  # 折线图中添加圆点
        markersize=4,
        markeredgecolor="black",  # 点的边框色
        markerfacecolor="black",
    )

    # 添加上下界的水平参考线
    plt.axhline(
        y=pay_ratio["ratio"].mean() - 2 * pay_ratio["ratio"].std(),
        linestyle="--",
        color="gray",
    )
    plt.axhline(
        y=pay_ratio["ratio"].mean() + 2 * pay_ratio["ratio"].std(),
        linestyle="--",
        color="gray",
    )
    # 获取图的坐标信息
    ax = plt.gca()
    # 设置日期的显示格式
    date_format = mpl.dates.DateFormatter("%m-%d")
    ax.xaxis.set_major_formatter(date_format)

    # 设置x轴每个刻度的间隔天数
    xlocator = mpl.ticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(xlocator)
    # 为了避免x轴刻度标签的紧凑，将刻度标签旋转45度
    plt.xticks(rotation=45)

    # 计算判断异常点和极端异常点的临界值
    outlier_ll = pay_ratio["ratio"].mean() - 2 * pay_ratio["ratio"].std()
    outlier_ul = pay_ratio["ratio"].mean() + 2 * pay_ratio["ratio"].std()
    extreme_outlier_ll = pay_ratio["ratio"].mean() - 3 * pay_ratio["ratio"].std()
    extreme_outlier_ul = pay_ratio["ratio"].mean() + 3 * pay_ratio["ratio"].std()
    # 寻找异常点
    outliers = pay_ratio["ratio"][
        (pay_ratio["ratio"] > outlier_ul) | (pay_ratio["ratio"] < outlier_ll)
    ]
    extreme_outliers = pay_ratio["ratio"][
        (pay_ratio["ratio"] > extreme_outlier_ul)
        | (pay_ratio["ratio"] < extreme_outlier_ll)
    ]
    print("异常点:\n", outliers)
    print("极端异常点:\n", extreme_outliers)
    plt.show()


# * 数据的描述
# * 数据的集中趋势
# * 均值（Mean）
# * 算术平均数：
# 特点：利用全部数据，数学性质好，适合进一步统计分析。
def mean_calculation():
    cars_score = pd.read_table(
        f"{BASE_DIR}/Chapter_5_Data/datas/cars_score.csv", sep=","
    )

    # 计算均值
    print("均值:\n", cars_score.mean(axis=0))
    # 计算加权平均数
    print("加权平均数:\n", cars_score.mean(axis=0))
    # 计算几何平均数
    print("几何平均数:\n", cars_score.mean(axis=0))


# * 加权平均数：
# 特点：加权平均数是以各观测值出现的频数、比重或重要性作为权数，通过“值与权数乘积之和”除以“权数之和”所得到的集中趋势指标。
def weighted_mean_calculation():
    # 读取数据RFM数据
    RFM = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/RFM.xlsx")
    print("RFM:\n", RFM.head())
    # 计算每个用户在R、F、M三个指标上的加权平均得分
    RFM["Weight_Mean"] = (
        0.2 * RFM["R_score"] + 0.5 * RFM["F_score"] + 0.3 * RFM["M_score"]
    )
    print("加权平均得分:\n", RFM.head())


# * 几何平均数：
# 对一组正数数据，将各观测值连乘后，再开与数据个数相同次数方所得的平均水平，称为几何平均数。
def geometric_mean_calculation():
    # 读取数据GDP数据
    GDP = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/G_D_P.xlsx")
    print("GDP:\n", GDP.head())
    # 利用cumprod“方法”实现所有元素的累计乘积
    cum_prod = GDP.Grouth.cumprod()
    # 基于cum_prod结果，利用索引将最后一个累积元素取出来
    res = cum_prod[GDP.shape[0]-1]
    # 计算几何平均数
    print("几何平均数:\n", pow(res, 1/len(cum_prod)))


# * 中位数（Median）
# 特点：将数据按大小排序后处于中间位置的值。
# * 分位数（Quantile）
# 将一组数据按从小到大排序后，把总体划分为若干个等份，使得有相同比例的数据落在各区间内的分割点，称为分位数。
def median_calculation():
    tips = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/tips.csv")
    # 基于pandas模块中的hist方法绘制直方图
    tips.tip.hist(grid=False, facecolor='steelblue', edgecolor='black')
    # 计算小费数据的中位数
    print('中位数为：', tips.tip.median())
    
    # 计算小费数据的均值
    print('均值为：', tips.tip.mean()) 
    # 计算小费数据的上下四分位数
    print('上四分位数为：', tips.tip.quantile(q=0.25))
    print('下四分位数为：', tips.tip.quantile(q=0.75))
    # 显示图形
    plt.show()
# * 众数（Mode）
# 特点：出现频率最高的数值。
def mode_calculation():
    titanic = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/Titanic.xlsx")
    # 计算登船地址的众数
    print('众数：',titanic.Embarked.mode())
    
    # 读入用户收入数据
    income = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/Income.xlsx")
    # 返回众数所在组的索引
    index = income.Counts.argmax()
    # 返回众数所在组的下限
    L = int(income.Income[index].split(',')[0][1:])
    # 返回众数所在组的上限
    U = int(income.Income[index].split(',')[1][:-1])
    # 返回左邻与右邻组所对应的频次
    LF = income.Counts[index-1]
    RF = income.Counts[index+1]
    # 计算众数
    print('众数：', L+LF/(LF+RF)*(U-L))


# * 数据的分散趋势
# * 方差与标准差
def std_calculation():
    tips = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/tips.csv")
    # 计算小费的方差
    Var = tips.tip.var()
    # 计算小费的标准差
    Std = tips.tip.std()
    print('小费的方差：', Var)
    print('小费的标准差：', Std)
# * 极差与四分位差
# * 变异系数
def cv_calculation():
    tips = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/tips.csv")
    # 筛选男性与女性的小费数据
    tip_man = tips.tip[tips.sex == 'Male']
    tip_woman = tips.tip[tips.sex == 'Female']
    print(f'男性的样本量为{len(tip_man)}个')
    print(f'女性的样本量为{len(tip_woman)}个')
    # 计算男性顾客与女性顾客所支付小费的变异系数
    cv_man = tip_man.mean()/tip_man.std()
    cv_woman = tip_woman.mean()/tip_woman.std()
    print(f'男性顾客所支付小费的变异系数: {cv_man} .')
    print(f'女性顾客所支付小费的变异系数: {cv_woman} .')
    
# * describe方法
def describe_calculation():
    tips = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/tips.csv")
    # 通过describe方法默认对所有数值型变量做统计汇总
    print(f'统计汇总:\n{tips.describe()}')
    # 通过指定参数实现离散型变量的统计汇总
    print(f"离散型变量的统计汇总:\n{tips.describe(include=['object'])}")
    '''
    统计汇总:
        total_bill         tip        size
    count  244.000000  244.000000  244.000000 # 样本数 非缺失值的观测数量，用于判断是否存在缺失数据
    mean    19.785943    2.998279    2.569672 # 均值（算术平均数） 反映总体的平均水平，对极端值敏感 
    std      8.902412    1.383638    0.951100 # 标准差 衡量数据围绕均值的离散程度，越大说明波动越大
    min      3.070000    1.000000    1.000000 # 最小值 数据中最小的观测值
    25%     13.347500    2.000000    2.000000 # 下四分位数（Q1） 有 25% 的数据小于等于该值 
    50%     17.795000    2.900000    2.000000 # 中位数（Median） 将数据一分为二的位置，抗极端值能力强 
    75%     24.127500    3.562500    3.000000 # 上四分位数（Q3）有 75% 的数据小于等于该值
    max     50.810000   10.000000    6.000000 # 最大值 数据中最大的观测值
    离散型变量的统计汇总:
            sex smoker  day    time
    count    244    244  244     244 # 样本数 非缺失值数量 
    unique     2      2    4       2 # 不同取值个数 用于衡量类别数量 
    top     Male     No  Sat  Dinner # 众数 出现频率最高的类别 
    freq     157    151   87     176 # 众数出现次数 众数对应的样本数 
    '''
# * 数据的分布形态
def distribution_shape():
    forestfires = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/forest fires.csv")
    print(forestfires.head())
    # 计算受灾面积的偏度
    print('受灾面积的偏度：', forestfires.area.skew())
    # 计算受灾面积的峰度
    print('受灾面积的峰度：', forestfires.area.kurt())
    # 绘制直方图
    plt.hist(x = forestfires.area, 
             bins=50,
             color='steelblue',
             edgecolor='black')
    # 显示图形
    plt.show()
import seaborn as sns
# * 数据的相关关系
def correlation_analysis():
    ccpp = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/C_C_P_P.xlsx")
    # 使用corrwith方法计算PE变量与其余变量之间的相关系数
    print(ccpp.corrwith(ccpp.PE))
    # 绘制PE与AT之间的散点图
    plt.scatter(x=ccpp.AT, y = ccpp.PE,
                c = 'steelblue',
                alpha=0.7,
                edgecolors='black')
    plt.xlabel('AT')
    plt.ylabel('PE')
    plt.show()
    
    # 绘制ccpp数据集中两两变量之间的散点图
    sns.pairplot(ccpp)
    plt.show()
import scipy.stats as stats
# * 数据的波动趋势
def trend_analysis():
    sales = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/trans_amt.xlsx")
    # 将date变量转换为日期型变量
    sales.month = pd.to_datetime(sales.month, format='%Y年%m月')
    
    # 绘制每月的销售额
    plt.plot(sales.month, sales.trans_amt, linestyle='-', linewidth=2, color='steelblue', marker='o', markersize=4, markerfacecolor='black')
    
    # 获取坐标信息
    ax = plt.gca()
    # 设置日期显示格式
    date_format = mpl.dates.DateFormatter("%y/%m")
    ax.xaxis.set_major_formatter(date_format)
    
    # 设置x轴显示多少个日期刻度
    xlocator = mpl.ticker.LinearLocator(18)
    ax.xaxis.set_major_locator(xlocator)
    
    # 将刻度标签旋转45°
    plt.xticks(rotation=45)
    
    plt.show()
    
# * 数据的推断
# * 正态性检验
def normality_test():
    sec_buildings = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/sec_buildings.xlsx")
    print(sec_buildings.head())
    # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
    # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    
    # 基于直方图判断数据是否服从正太分布
    sns.distplot(a=sec_buildings.price,
                 fit=stats.norm,
                 norm_hist=True,
                 hist_kws={'color': 'steelblue', 'edgecolor': 'black'},
                 kde_kws={'color':'black', 'linestyle':'--','label':'核密度曲线'},
                 fit_kws={'color':'red', 'linestyle':':', 'label':'正太密度曲线'})
    # 显示图例
    plt.legend()
    plt.show()
    
# * PP图与QQ图
def PP_QQ_plot():
    sec_buildings = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/sec_buildings.xlsx")

    probplot = sm.ProbPlot(sec_buildings.price)

    # 绘制 P-P 图
    fig, ax = plt.subplots()
    probplot.ppplot(line='45', ax=ax)
    ax.set_title('P–P Plot')

    # 绘制 Q-Q 图
    fig, ax = plt.subplots()
    probplot.qqplot(line='q', ax=ax)
    ax.set_title('Q–Q Plot')

    plt.show()
def PP_QQ_plot():
    sec_buildings = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/sec_buildings.xlsx")
    data = sec_buildings["price"].dropna()
    x = np.sort(data)
    n = len(x)

    # 经验分布概率
    p_emp = np.arange(1, n+1) / n

    # 理论分布概率（正态）
    mu, sigma = np.mean(x), np.std(x, ddof=1)
    p_the = stats.norm.cdf(x, mu, sigma)

    plt.scatter(p_the, p_emp)
    plt.plot([0,1], [0,1], '--')
    plt.xlabel('Theoretical CDF')
    plt.ylabel('Empirical CDF')
    plt.title('P–P Plot (Textbook Style)')
    plt.show()
# * Shapiro检验和ts检验
# 样本量高于5000时用ts检验，低于5000时用Shapiro检验
def ks_test():
    sec_buildings = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/sec_buildings.xlsx")
    result = stats.kstest(rvs=sec_buildings.price,
                          args=(sec_buildings.price.mean(), sec_buildings.price.std()),
                          cdf='norm'# 指定累计分布函数为正态分布函数
                          )
    print('kstest result:', result)
        
def shapiro_test():
    # 生成正太分布和均匀分布随机数
    x1 = np.random.normal(loc=5, scale=2, size=3500)
    x2 = np.random.uniform(low=1, high=100, size=400)
    # 正态性检验
    shapiro_test1 = stats.shapiro(x=x1)
    shapiro_test2 = stats.shapiro(x=x2)
    
    print('shapiro_test1', shapiro_test1)
    print('shapiro_test2', shapiro_test2)
from scipy.stats import chi2_contingency
# * 卡方检验
def chi_square_test():
    mushrooms = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/mushroom.csv")
    # 构造两个变量之间的频次统计表
    crosstable = pd.crosstab(mushrooms['cap-shape'], mushrooms['class'])
    print('列联表结果\n', crosstable)
    
    print('卡方检验\n', chi2_contingency(crosstable))
    '''
    卡方检验
    Chi2ContingencyResult(
        statistic=np.float64(487.948342301851), 卡方统计量
        pvalue=np.float64(3.1872101369079138e-103), 概率（远远小于0.05，拒绝原假设）
        dof=5, 自由度
        expected_freq=array([[2.41038023e+02, 2.10961977e+02],理论频数表
        [2.13307985e+00, 1.86692015e+00],
        [2.02429278e+03, 1.77170722e+03],
        [1.75552471e+03, 1.53647529e+03],
        [4.47946768e+02, 3.92053232e+02],
        [1.70646388e+01, 1.49353612e+01]]))
    '''
# * t检验
def t_test():
    # 饮料净含量数据
    data = [558,551,542,557,552,547,551,549,548,551,553,557,548,550,546,552]
    # 单样本t检验
    print('t-test', stats.ttest_1samp(a=data, popmean=550, nan_policy='propagate'))
# * 独立样本t检验
def independent_samples_t_test():
    tips = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/tips.csv")
    male_tips = tips.loc[tips.sex == 'Male', 'tip']
    female_tips = tips.loc[tips.sex == 'Female', 'tip']
    
    print('检验两样本之间的方差是否相等', stats.levene(male_tips, female_tips))
    print('独立样本t检验', stats.ttest_ind(a=male_tips, 
                                     b=female_tips,
                                     equal_var=True#指定样本方差相等
                                     ))
# * 配对样本t检验
def paired_samples_t_test():
    ppgnp = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/PPGNP.xlsx")
    # 计算两年人均可支配收入之间的差值
    diff = ppgnp.PPGNP_2017-ppgnp.PPGNP_2016
    # 使用ttest_1samp函数计算配对样本的t统计量
    print('配对样本的t统计量', stats.ttest_1samp(a=diff, popmean=0))
    
# * 5.6 线性回归模型的应用
def application_of_linear_regression():
    # 读取汽车刹车速度与距离的数据
    speed_dist = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/cars.csv")
    
    # 绘制散点数据，并添加拟合线
    sns.lmplot(x='speed',
               y='dist',
               data=speed_dist,
               legend_out=False,#将图例呈现在图框内
               truncate=True#根据实际的数据范围，对拟合线做截断操作
               )
    plt.show()
def application_ols_of_linear_regression():
    # 读取汽车刹车速度与距离的数据
    speed_dist = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/cars.csv")    
    # 利用汽车刹车数据，构建回归模型
    fit = sm.formula.ols('dist ~ speed', data=speed_dist).fit()
    print('模型的参数值：', fit.params)
    '''
    Intercept   -17.579095
    speed         3.932409
    '''
# * 多远线性回归模型的参数求解
def parameter_estimation_for_multiple_linear_regression_models():
    # 读取销售额与成本的数据
    sales = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/Advertising.csv")  
    # 1️⃣ 看一眼列名（调试用）
    print(sales.columns)

    # 2️⃣ 删除多余索引列（安全操作）
    sales = sales.drop(columns=['Unnamed: 0'], errors='ignore')

    # 3️⃣ 统一列名（强烈建议）
    sales.columns = [c.strip().lower() for c in sales.columns]

    # 4️⃣ 再建模（注意列名已变）
    fit = sm.formula.ols(
        'sales ~ tv + radio + newspaper',
        data=sales
    ).fit()
    print('模型的参数值：\n', fit.params)
    
def scatter_plot():
    # 读取销售额与成本的数据
    sales = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/Advertising.csv")  
    # 1️⃣ 看一眼列名（调试用）
    print(sales.columns)

    # 2️⃣ 删除多余索引列（安全操作）
    sales = sales.drop(columns=['Unnamed: 0'], errors='ignore')

    # 3️⃣ 统一列名（强烈建议）
    sales.columns = [c.strip().lower() for c in sales.columns]

    # 4️⃣ 绘制散点图
    sns.lmplot(x='newspaper',
               y='sales',
               data=sales,
               truncate=True,
               fit_reg=False#不显示拟合曲线
               )
    plt.show()
# * 剔除newspaper变量，重新构造多元回归模型
def no_newspaper_for_multiple_linear_regression_models():
    # 读取销售额与成本的数据
    sales = pd.read_csv(f"{BASE_DIR}/Chapter_5_Data/datas/Advertising.csv")  
    # 1️⃣ 看一眼列名（调试用）
    print(sales.columns)

    # 2️⃣ 删除多余索引列（安全操作）
    sales = sales.drop(columns=['Unnamed: 0'], errors='ignore')

    # 3️⃣ 统一列名（强烈建议）
    sales.columns = [c.strip().lower() for c in sales.columns]

    # 4️⃣ 再建模（注意列名已变）
    fit = sm.formula.ols(
        'sales ~ tv + radio',
        data=sales
    ).fit()
    print('模型的参数值：\n', fit.params)
    print('模型的概览：\n', fit.summary())
    '''
    Index(['Unnamed: 0', 'TV', 'Radio', 'Newspaper', 'Sales'], dtype='object')
    模型的参数值：
    Intercept    2.921100
    tv           0.045755
    radio        0.187994
    dtype: float64
    模型的概览：
                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                  sales   R-squared:                       0.897
    Model:                            OLS   Adj. R-squared:                  0.896
    Method:                 Least Squares   F-statistic:                     859.6
    Date:                Fri, 16 Jan 2026   Prob (F-statistic):           4.83e-98
    Time:                        10:49:54   Log-Likelihood:                -386.20
    No. Observations:                 200   AIC:                             778.4
    Df Residuals:                     197   BIC:                             788.3
    Df Model:                           2                                         
    Covariance Type:            nonrobust                                         
    ==============================================================================
                    coef    std err          t      P>|t|      [0.025      0.975]
    ------------------------------------------------------------------------------
    Intercept      2.9211      0.294      9.919      0.000       2.340       3.502
    tv             0.0458      0.001     32.909      0.000       0.043       0.048
    radio          0.1880      0.008     23.382      0.000       0.172       0.204
    ==============================================================================
    Omnibus:                       60.022   Durbin-Watson:                   2.081
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):              148.679
    Skew:                          -1.323   Prob(JB):                     5.19e-33
    Kurtosis:                       6.292   Cond. No.                         425.
    ==============================================================================

    Notes:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    最终模型是：
    Sales= 2.9211 + 0.0458 * TV + 0.1880 * Radio
    
    截距 Intercept = 2.9211

    含义：

    当 TV 和 Radio 广告投入都为 0 时，模型预测的销售额约为 2.92。

    专业解读：
        •	这是一个基准销量（baseline sales）
        •	并不强调“现实意义”，而是保证模型数学成立
        •	在广告投放模型中，截距主要是技术项，不必过度解读

    ⸻

    2️⃣ TV 系数 = 0.0458

    含义（关键）：

    在 Radio 投入不变 的情况下，
    TV 广告投入每增加 1 个单位，销售额平均增加 0.0458 个单位。
    
    Radio 系数 = 0.1880
    含义：

    在 TV 投入不变 的情况下，
    Radio 广告投入每增加 1 个单位，销售额平均增加 0.188 个单位。
    '''
# * 模型的预测
def predictions_models():
    # 读取销售额与成本的数据
    titanic = pd.read_csv(f"{BASE_DIR}/Chapter_1_Data/Titanic.csv")  
    # 数据预览
    print(titanic.head())
    # 查看数据类型
    print('查看数据类型:\n', titanic.dtypes)
    # 查看各变量的缺失比例
    print('查看各变量的缺失比例:\n', titanic.isnull().mean())
    # 删除无意义的变量
    titanic.drop(labels=['PassengerId', 'Name', 'Ticket', 'Cabin', 'Embarked'], axis=1, inplace=True)
    print(titanic.head())
    # 哑变量转换
    # 将Pclass变量转换为字符型变量
    titanic['Pclass'] = titanic['Pclass'].astype(str)
    # 将Pclass变量和Sex变量做哑变量处理
    dummies = pd.get_dummies(data=titanic[['Pclass', 'Sex']])
    # 将titanic数据集与dummies数据集进行合并
    titanic_new = pd.concat([titanic, dummies], axis=1)
    print(titanic_new.head())
    # 删除原始的分类变量
    titanic_new.drop(labels=['Pclass', 'Sex', 'Pclass_3', 'Sex_male'], axis=1, inplace=True)
    print(titanic_new.head())
    
    # 取出年龄为缺失的数据子集
    missing = titanic_new[titanic_new['Age'].isnull()]
    print('缺失数据子集:\n', missing)
    # 取出年龄不为缺失的数据子集
    no_missing = titanic_new[titanic_new['Age'].notnull()]
    print('非缺失数据子集:\n', no_missing)
    
    # 构建逻辑回归模型
    
    # 提取出所有的自变量名称
    predictors = no_missing.columns[~no_missing.columns.isin(['Age'])]
    # 构造多元线性回归模型的“类”
    # lm_Class = sm.formula.ols(formula='Age ~ ' + ' + '.join(predictors), data=no_missing)
    # lm_Class = sm.formula.OLS(endog=no_missing.Age, # 指定模型中的因变量
                            #   exog=no_missing[predictors]) # 指定模型中的自变量
    lm_Class = sm.formula.ols(
        "Age ~ " + " + ".join(predictors),
        data=no_missing
    )
    # 拟合多元线性回归模型
    lm = lm_Class.fit()
    print('多元线性回归模型的参数值:\n', lm.summary())
    
    # 绘制其余变量与年龄之间的散点图
    sns.pairplot(no_missing[['Survived', 'SibSp', 'Parch', 'Fare', 'Age']])
    plt.show()
    # 选定新的自变量
    predictors_new = ['SibSp', 'Pclass_1', 'Pclass_2', 'Sex_female']
    # 构造新的多元线性回归模型的“类”
    lm_Class_new = sm.formula.ols(
        "Age ~ " + " + ".join(predictors_new),
        data=no_missing
    )
    # 拟合新的多元线性回归模型
    lm_new = lm_Class_new.fit()
    print('新的多元线性回归模型的参数值:\n', lm_new.summary())
    
    # 基于PP图和QQ图判断残差的正态性
    PP_QQ_plot = sm.ProbPlot(lm_new.resid)
    # 绘制 P-P 图
    fig, ax = plt.subplots()
    PP_QQ_plot.ppplot(line='45', ax=ax)
    ax.set_title('P–P Plot of Residuals')
    # 绘制 Q-Q 图
    fig, ax = plt.subplots()
    PP_QQ_plot.qqplot(line='q', ax=ax)
    ax.set_title('Q–Q Plot of Residuals')
    plt.show()
    
    # 使用新模型对缺失的年龄进行预测
    pred_age = lm_new.predict(missing[predictors_new])
    # 将年龄的预测结果填补到原始数据集中
    missing.loc[:, 'Age'] = pred_age
    print('填补缺失值后的数据集:\n', missing.head())
    
    # 预测结果插补带原始数据中
    titanic.loc[:, 'Age'] = pd.concat([no_missing['Age'], pred_age], axis=0)
    print('最终数据集:\n', titanic.head())

# * 数据的聚类分析
# * 数据的分类分析
# * 数据的降维分析
# * 数据的关联分析
# * 数据的异常值检测
# * 数据的描述性统计
# * 数据的假设检验
# * 数据的方差分析
# * 数据的回归分析
# * 数据的聚类分析
# * 数据的分类分析

def data_description():
    sec_buildings = pd.read_excel(f"{BASE_DIR}/Chapter_5_Data/datas/sec_buildings.xlsx")
    print("sec_buildings:\n", sec_buildings)
    # 计算各指标的平均得分
    print("各指标的平均得分:\n", sec_buildings.mean(axis=0))
    # 计算各指标的标准差
    print("各指标的标准差:\n", sec_buildings.std(axis=0))
    # 计算各指标的变异系数
    print("各指标的变异系数:\n", sec_buildings.var(axis=0))

import sys
print("解释器路径:", sys.executable)
if __name__ == "__main__":
    if 1:
        # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
        # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
        font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
        fm.fontManager.addfont(font_path)

        # 设置 Matplotlib 使用该字体
        plt.rcParams['font.family'] = 'Source Han Sans HW SC'
        plt.rcParams['axes.unicode_minus'] = False
        print(f"{speter*2}Starting{speter*2}")
    
    
    try:
        predictions_models()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
