#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
# 11 Pandas统计分析
# 11.4 时间数据  2025-10-13 11:00:57
import os
import pandas as pd
import numpy as np
from datetime import datetime

from sqlalchemy import create_engine
# 导入机器学习库
from sklearn.cluster import KMeans
speter = '-'*10

def create_date():
    day = pd.date_range("2025-10-13", "2025-10-29", freq="D")
    print(f"按天创建：{day}")
    time = pd.date_range("01:00", "05:59", freq="h").time
    print(f"按小时创建：{time}")
    
    # time = pd.to_datetime(["2025-10-13", "2025.10.10", 1547516436],
    #                   errors='coerce', infer_datetime_format=True)
    
    # print("统一时间格式：", time)
    data = ["2025-10-13", "2025.10.10", 1547516436]
    parsed = []
    for v in data:
        if isinstance(v, (int, float, np.integer, np.floating)):
            parsed.append(pd.to_datetime(v, unit="s", errors="coerce"))
        else:
            # 字符串日期：尝试多种格式
            try:
                parsed.append(pd.to_datetime(v, format="%Y.%m.%d", errors="raise"))
            except Exception:
                try:
                    parsed.append(pd.to_datetime(v, format="%Y-%m-%d", errors="raise"))
                except Exception:
                    parsed.append(pd.to_datetime(v, errors="coerce"))

    time = pd.DatetimeIndex(parsed)
    print("统一时间格式：", time)
def timeOperation():
    
    time1 = pd.Timedelta(10, unit='h')
    print(time1)

    time2 = pd.Timedelta(days=5)
    print(time2)
    
    print(f"")
    date = pd.Series(pd.date_range(datetime.now().date(), periods=35, freq='D'))
    day = pd.Series([pd.Timedelta(days=i) for i in range(1, 36)])
    df = pd.DataFrame({"日期": date, "间隔时间": day})
    print(df)
    print(f"")
    
    date = pd.Series(pd.date_range(datetime.now().date(), periods=5, freq='D'))
    day = pd.Series([pd.Timedelta(days=i) for i in range(1, 6)])
    df = pd.DataFrame({"日期": date, "间隔时间": day})
    df["加上间隔时间"] = df["日期"] + df["间隔时间"]
    df["减去间隔时间"] = df["日期"] - df["间隔时间"]
    print(df)
# 11.5 数据整理
# 11.5.1 数据清洗
def dataCleaning():
    series1 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Warren", "Ivy"]),
           "math_score": pd.Series([98, 88, 91, 94, 74]),
           "en_score": pd.Series([92, 68, 94, 78, 69]),
           "term": pd.Series(["第一学期", "第一学期", "第一学期", "第一学期", "第一学期"])}

    series2 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Lucy", "Edith"]),
            "math_score": pd.Series([90, 68, 75, 83, 67]),
            "en_score": pd.Series([95, 99, 82, 89, 72]),
            "term": pd.Series(["第二学期", "第二学期", "第二学期", "第二学期", "第二学期"])}

    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    df3 = df1.merge(df2, on="name", how="outer")
    print(df3)
    print('-'*50)
    print(df3.fillna(0))
    print('-'*50)
    series1 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Warren", "Ivy"]),
           "math_score": pd.Series([198, 88, 91, 94, 74]),
           "en_score": pd.Series([92, 268, 94, 78, 69]),
           "term": pd.Series(["第一学期", "第一学期", "第一学期", "第一学期", "第一学期"])}

    series2 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Lucy", "Edith"]),
            "math_score": pd.Series([90, 68, 375, 83, 67]),
            "en_score": pd.Series([95, 99, 82, 89, 72]),
            "term": pd.Series(["第二学期", "第二学期", "第二学期", "第二学期", "第二学期"])}

    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    df3 = df1.merge(df2, on="name", how="outer")
    print(df3.fillna("缺考").replace({198: 98, 268: 68, 375: 75}))
    print('-'*50)
    print(df3.dropna())
    
    
    print(speter*5)
    print(f"{speter*2}稀疏数据{speter*2}")
    series1 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Warren", "Ivy"]),
           "math_score": pd.Series([198, np.nan, np.nan, np.nan, 74]),
           "en_score": pd.Series([92, np.nan, 94, np.nan, np.nan]),
           "term": pd.Series(["第一学期", "第一学期", "第一学期", "第一学期", "第一学期"])}
    df1 = pd.DataFrame(series1)
    # sparse = df1.to_sparse()
    print(f"稀疏数据密度（非空占比）：{df1.count().sum() / df1.size:.2%}")
    # df1 = sparse.to_dense()
    
    # 转为稀疏列
    for col in df1.columns:
        if df1[col].dtype.kind in "if":  
            df1[col] = df1[col].astype(pd.SparseDtype("float", np.nan))

    print(df1.dtypes)
    print("稀疏矩阵示例：")
    print(df1)
    print("稀疏矩阵内存占用：", df1.memory_usage(deep=True).sum())

    # 计算数据密度
    total = df1.size
    non_null = df1.count().sum()
    density = non_null / total
    print(f"数据密度（非空占比）：{density:.2%}")
    print(f"数据稀疏度（空值占比）：{1 - density:.2%}")
# 高级功能
def advancedFeatures():   
    # 多维度分析
    
    print(f"{speter*2}透视表{speter*2}")
    series1 = {"name": pd.Series(["Wilson", "Bruce", "Wilson", "Bruce"]),
           "math_score": pd.Series([98, 88, 94, 74]),
           "en_score": pd.Series([92, 68, 78, 69]),
           "school_year": pd.Series(["第一学年", "第一学年", "第一学年", "第一学年"]),
           "term": pd.Series(["第一学期", "第一学期", "第二学期", "第二学期"])}

    series2 = {"name": pd.Series(["Wilson", "Bruce", "Wilson", "Bruce"]),
            "math_score": pd.Series([90, 68, 83, 67]),
            "en_score": pd.Series([95, 99, 89, 72]),
            "school_year": pd.Series(["第二学年", "第二学年", "第二学年", "第二学年"]),
            "term": pd.Series(["第一学期", "第一学期", "第二学期", "第二学期"])}

    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    print(df1)
    print(speter*5)
    print(df2)
    print(speter*5)
    # df3 = df1.append(df2, ignore_index=True) # Pandas 新版本（>=2.0）中 DataFrame.append() 被彻底移除
    df3 = pd.concat([df1, df2], ignore_index=True)
    df3 = df3.pivot_table(['math_score'], index='name', columns='school_year', aggfunc='sum')
    print(df3)
    
    print(f"{speter*2}交叉表{speter*2}")
    series1 = {"name": pd.Series(["Wilson", "Bruce", "Wilson", "Bruce"]),
           "math_score": pd.Series([98, 88, 94, 74]),
           "en_score": pd.Series([92, 68, 78, 69]),
           "school_year": pd.Series(["第一学年", "第一学年", "第一学年", "第一学年"]),
           "term": pd.Series(["第一学期", "第一学期", "第二学期", "第二学期"])}

    series2 = {"name": pd.Series(["Wilson", "Bruce", "Wilson", "Bruce"]),
            "math_score": pd.Series([90, 68, 83, 67]),
            "en_score": pd.Series([95, 99, 89, 72]),
            "school_year": pd.Series(["第二学年", "第二学年", "第二学年", "第二学年"]),
            "term": pd.Series(["第一学期", "第一学期", "第二学期", "第二学期"])}

    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    # df3 = df1.append(df2, ignore_index=True)
    df3 = pd.concat([df1, df2], ignore_index=True)
    df3 = pd.crosstab(df3.name, df3.school_year,normalize=True)
    print(df3)
    print(f"{speter*2}查看不同组合出现次数{speter*2}")
    df_all = pd.concat([df1, df2], ignore_index=True)
    # 查看不同组合出现次数
    print(df_all.groupby(["name", "school_year"]).size())
    # 计算整体归一化的交叉表
    print(pd.crosstab(df_all["name"], df_all["school_year"], normalize="all"))
    
    # 选取数据
    print(f"{speter*2}在单列上进行切片{speter*2}")
    df3 = pd.concat([df1, df2], ignore_index=True)
    print(df3)
    print(df3["math_score"][1:7:2])

    print(f"{speter*2}在多列上进行切片{speter*2}")
    print(df3[["name", "math_score"]][2:5:3])
    
    print(f"{speter*2}使用loc与iloc选取数据{speter*2}")
    print(df3.loc[5:, ["math_score", "en_score"]])
    print(df3.iloc[6:, [1, 3]])
    print(f"{speter*2}读写MySQL数据库{speter*2}")
    # engine = create_engine("mysql+pymysql://root:root@localhost:3306/test", encoding="utf8")
    # engine = create_engine("mysql+pymysql://root:root@localhost:3306/test?charset=utf8")
    engine = create_engine(
        "mysql+pymysql://eason:chy123@127.0.0.1:3306/example?charset=utf8mb4"
    )

    sql = "SELECT * from iris limit 100"
    df = pd.read_sql(sql, engine)
    df = df.groupby("Species", as_index=True).sum()
    print(df)
    df.to_sql("iris1", engine, index=False, if_exists="replace")
    
    print(f"{speter*2}布尔值索引{speter*2}")
    series = {"Wilson": pd.Series([98, 92]),
          "Bruce": pd.Series([88, 68]),
          "Chelsea": pd.Series([91, 94]),
          "Warren": pd.Series([96, 78]),
          "Ivy": pd.Series([74, 95])}

    df1 = pd.DataFrame(series)
    df2 = df1.rename(index={0: "math_score", 1: "en_score"})
    print("原始数据：")
    print(df2)
    print("筛选后的数据：")
    print(df2.loc[:, (df2.iloc[0] > 95) & (df2.iloc[1] > 90)])


# 成绩分析
def performanceAnalysis():
    print(f"{speter*2}统计成绩{speter*2}")
    # 获取当前脚本所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 拼接文件完整路径
    file = os.path.join(base_dir, "成绩明细表.xlsx")
    # file = "成绩明细表.xlsx"
    df = pd.read_excel(file, sheet_name='成绩表')
    df["总成绩"] = df.iloc[:, 1:13].apply(lambda x: x.sum(), axis=1)
    df["平均成绩"] = df.iloc[:, 1:13].apply(lambda x: x.mean(), axis=1)
    df.loc["各科目平均成绩"] = df.iloc[0:, 1:13].apply(lambda x: x.mean(), axis=0)
    df.loc["各科目平均成绩", "总成绩"] = df.iloc[:-1, -2].mean()   # 总成绩列平均
    df.loc["各科目平均成绩", "平均成绩"] = df.iloc[:-1, -1].mean()  # 平均成绩列平均
    # print(df.fillna("0")) 
    # print(df)
    result = get_actegory(df["平均成绩"], 4)
    print(result.value_counts())
def get_actegory(data, k):
    print(data)
    means_model = KMeans(n_clusters=k)
    train_data = data.values.reshape((len(data), 1))
    means_model.fit(train_data)
    center = pd.DataFrame(means_model.cluster_centers_).sort_values(0)
    mean_data = center.rolling(2).mean().iloc[1:]
    mean_data = [0] + list(mean_data[0]) + [data.max()]
    data = pd.cut(data, mean_data, labels=["差", "中", "良", "优"])
    return data
if __name__ == "__main__":
    print(f"{speter*2}Started{speter*2}")
    performanceAnalysis()
    print(f"{speter*2}Finished{speter*2}")