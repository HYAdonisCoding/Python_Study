#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
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
    data = pd.read_sql(
        "select * from sec_buildings where direction='朝南'",
        con=engine
    )
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
    data1['id'] = data1['id'].astype(str)
    # 数值类型转换
    data1['custom_amt'] = data1['custom_amt'].str[1:].astype(float)
    # 字符类型转换日期型
    data1['order_date'] = pd.to_datetime(data1['order_date'], format='%Y年%m月%d日') 
    print(data1.shape)
    print(data1.dtypes)
    print(data1.head())
    # 冗余数据判断
    print(data1.duplicated().any())
    # 缺失数据的判断与处理
    print('判断各变量中是否存在缺失值：\n', data1.isnull().any(axis=0))
    print('各变量中缺失值的数量：\n', data1.isnull().sum(axis=0))
    print('各变量中缺失值的比例：\n', data1.isnull().sum(axis=0)/data1.shape[0])
    
    print('判断各数据行中是否存在缺失值：\n', data1.isnull().any(axis=1).any())
    print('缺失观察值的数量：\n', data1.isnull().any(axis=1).sum())
    print('缺失观察值的比例：\n', data1.isnull().any(axis=1).sum()/data1.shape[0])
    '''判断各变量中是否存在缺失值：
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
    '''
    # 删除观测值，如删除age变量中所对应的缺失观测值
    data1_new = data1.drop(labels=data1.index[data1['age'].isnull()],axis=0)
    print(data1_new.shape)
    
    # 替换法处理缺失值
    data1.fillna(value={'gender':data1['gender'].mode()[0],#使用性别的众数替换缺失性别
                        'age':data1['age'].mean, # 使用年龄的平均值替换缺失年龄
                        'edu': '专科'
                        },
                 inplace=True#原地修改数据
                 )
    print('各变量中缺失值的数量：\n', data1.isnull().sum(axis=0))
# 数据的引用
def data_reference():
    # 构造数据框
    df1 = pd.DataFrame(
        {"name":["张三","李四","王五","赵六","孙七"],
         "age":[20,21,22,23,24],
         "gender":["男","女","女","女","男"],
         "edu":["本科","硕士","专科","本科","硕士"]
         },
         columns=["name","age","gender","edu"]
    )
    # 查看数据预览
    print(df1)
    # 取出数据集的中间三行(即所有女性)，并且返回姓名、年龄和受教育水平三列
    print('iloc方法：', df1.iloc[1:4, [0,3,2]])
    print('loc方法：', df1.loc[1:3, ['name','age','edu']])
    # print('ix方法：', df1.ix[1:3, [0,3,2]])#ix 已经在新版本 Pandas 中移除了
    # 将员工的姓名用作行标签
    df2 = df1.set_index('name')
    print(df2)
    # 取出数据集的中间三行(即所有女性)，并且返回姓名、年龄和受教育水平三列
    print('iloc方法：', df2.iloc[1:4,:])
    print('loc方法：', df2.loc[['李四','王五','赵六'],:])
    # print('ix方法：', df2.ix[1:3, [0,3,2]])#ix 已经在新版本 Pandas 中移除了
    
    # 基于loc方法作筛选
    print('loc方法作筛选：', df2.loc[df2['gender'] == '男', ['age','edu']])
    # 删除观测，如删除age变量中所对应的缺失观测
    df2_new = df2.drop(labels=df2.index[df2['age'].isnull()],axis=0)
    print(df2_new)
    print(df2_new.shape)
# 多表合并与连接
def multi_table_connect():
    df1 = pd.DataFrame(
        {"name":["张三","李四","王五"],
         "age":[20,21,22],
         "gender":["男","女","女"],
         "edu":["本科","硕士","专科"]
         },
         columns=["name","age","gender","edu"]
    )
    df2 = pd.DataFrame(
        {"name":["赵六","孙七"],
         "age":[23,24],
         "gender":["女","男"],
         "edu":["本科","硕士"]
         },
         columns=["name","age","gender","edu"]
    )
    df3 = pd.concat([df1,df2], keys=['df1','df2'])
    print(df3)
    print(df3.shape)
    df3.reset_index(level=0,inplace=True)
    df3.rename(columns={'level_0':'tab_name'},inplace=True)
    df3.index = range(df3.shape[0])
    print(df3)
    print(df3.shape)
    # 数据横向合并
    df4 = pd.concat([df1,df2])
    print(df4)
    print(df4.shape)
    # 数据横向合并,仅保留与df2列索引值一致的数据，类似于交集
    # df5 = pd.concat([df1,df2], join_axes=[df2.index], axis=1)
    df5 = pd.concat(
        [df1.reindex(df2.index), df2],
        axis=1
    )
    print(df5)
    print(df5.shape)
# 连接
def multi_table_connect():
    df3 = pd.DataFrame(
        {"id":[1,2,3,4,5], 
         "name":["张三","李四","王二","丁一","赵武"],
         "age":[20,21,22,23,24],
         "gender":["男","男","男","女","女"],
         "edu":["本科","硕士","专科","本科","硕士"]
         },
         columns=["id","name","age","gender","edu"]
    )
    df4 = pd.DataFrame(
        {"id":[1,2,2,4,4,4,5],
         "score":[83,81,87,75,86,74,88],
         "kemu":["科目1","科目1","科目2","科目1","科目2","科目3","科目1"]
         },
         columns=["id","score","kemu"]
    )
    df5 = pd.DataFrame(
        {"id":[1,3,5],
         "name":["张三","王二","赵武"],
         "income":[13500,18000,15000]
         },
         columns=["id","name","income"]
    )
    print('df3:\n',df3)
    print('df4:\n',df4)
    print('df5:\n',df5)
    # 首先df3和df4连接
    merge1 = pd.merge(left=df3, right=df4, how='left', left_on='id', right_on='id')
    print("merge1:\n",merge1)
    print(merge1.shape)
    # 再将连接结果与df5连接
    merge2 = pd.merge(left=merge1, right=df5, how='left')
    print("merge2:\n",merge2)
    print(merge2.shape)

# 数据的汇总
def data_summary():
    diamonds = pd.read_table(f"{BASE_DIR}/Chapter_5_Data/datas/diamonds.csv", sep=',')
    # 单个分组变量的均值统计
    summary1 = pd.pivot_table(data=diamonds, index='color', values='price', margins=True, margins_name='总计')
    print("summary1:\n",summary1)
    # # 多个分组变量的均值统计
    summary2 = pd.pivot_table(data=diamonds, index='clarity', columns='cut', values='carat', aggfunc=np.size, margins=True, margins_name='总计')
    print("summary2:\n",summary2)

# 分组聚合操作
def group_aggregate():
    diamonds = pd.read_table(f"{BASE_DIR}/Chapter_5_Data/datas/diamonds.csv", sep=',')
    grouped = diamonds.groupby(by=['color','cut'])
    result = grouped.aggregate({'color':np.size, 'carat':np.min, 'price':np.mean, 'face_width':np.max})
    result = pd.DataFrame(result, columns=['color','carat','price','face_width'])
    print("result:\n",result)
    # 数据集重命名
    result.rename(columns={'color':'counts','carat':'min_weight','price':'avg_price','face_width':'max_face_width'}, inplace=True)
    print("数据集重命名:\n",result)
    # 将行索引变量数据框的变量
    result.reset_index(inplace=True)
    print("将行索引变量数据框的变量:\n",result)
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        group_aggregate()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
