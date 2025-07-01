# !/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np


def series():
    print("-" * 30, "序列", "-" * 30)

    data = pd.Series()
    print("\n默认的空序列：", data)

    data = pd.Series(5, index=[0, 1, 2])
    print(f"\n通过数值创建序列data：\n{data}")
    data = pd.Series(5, index=["a", "b", "d"])
    print(f"\n通过数值创建序列data：\n{data}")

    init_data = np.array(["hello", "world", "python"])
    data = pd.Series(init_data)
    print(f"\n通过NumPy数组创建序列：\n{data}")

    # init_data = np.array(['hello', 'world', 'python'])
    # data = pd.Series(init_data, index=[1, 2])
    # print(f'\n通过NumPy数组创建序列2：\n{data}')

    init_data = {"name": "Ivy", "age": 10}
    data = pd.Series(init_data)
    print(f"\n通过字典创建序列：\n{data}")

    init_data = {"name": "Ivy", "age": 10}
    data = pd.Series(init_data, index=["name", "age1"])
    print(f"\n通过字典创建序列1：\n{data}")

    init_data = ["hello", "world", "python"]
    data = pd.Series(init_data, index=[12, 3, 4])
    print(f"\n通过列表创建序列：\n{data}")

    df = pd.DataFrame()
    print(f"\n创建空数据帧：\n{df}")

    data = [
        {"name": "Wilson", "age": 15, "gender": "man"},
        {"name": "Ivy", "age": 25, "gender": "woman"},
    ]
    df = pd.DataFrame(data)
    print(f"\n通过列表创建数据帧：\n{df}")

    data = ["Wilson", "Ivy"]
    df = pd.DataFrame(data)
    print(f"\n通过列表创建数据帧1：\n{df}")

    data = ["Wilson", "Ivy"]
    df = pd.DataFrame(data, columns=["name"])
    print(f"\n通过列表创建数据帧2：\n{df}")

    data = {
        "name": ["Wilson", "Bruce", "Chelsea"],
        "age": [15, 24, 19],
        "gender": ["man", "man", "woman"],
    }
    df = pd.DataFrame(data)
    print(f"\n通过字典创建数据帧：\n{df}")

    series = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "gender": pd.Series(["man", "man", "woman"]),
    }

    df = pd.DataFrame(series)
    print(f"\n通过序列创建数据帧：\n{df}")

    print("-" * 30, "行操作", "-" * 30)

    series = {
        "name": pd.Series(
            ["Wilson", "Bruce", "Chelsea"], index=["user1", "user2", "user3"]
        ),
        "age": pd.Series([15, 24, 19], index=["user1", "user2", "user3"]),
        "gender": pd.Series(["man", "man", "woman"], index=["user1", "user2", "user3"]),
    }

    df = pd.DataFrame(series)
    print(df)
    print("选取第1行数据：")
    print(df.loc["user1"])
    print("")
    print("选取第2行数据：")
    print(df.loc["user2"])

    print(f"\n行选择的切片：\n{df[0:2]}")

    df = pd.DataFrame(series)
    df1 = pd.DataFrame({"name": ["Lucy"], "age": [27], "gender": ["woman"]})
    df = pd.concat([df, df1])

    print(f"\n添加行：\n{df}")

    series = {
        "name": pd.Series(
            ["Wilson", "Bruce", "Chelsea"], index=["user1", "user2", "user2"]
        ),
        "age": pd.Series([15, 24, 19], index=["user1", "user2", "user2"]),
        "gender": pd.Series(["man", "man", "woman"], index=["user1", "user2", "user2"]),
    }

    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")

    print(f'\n删除user2：\n{df.drop("user2")}')

    print("-" * 30, "列操作", "-" * 30)

    series = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "gender": pd.Series(["man", "man", "woman"]),
    }

    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")
    df["height"] = pd.DataFrame(pd.Series(["180cm", "165cm", "172cm"]))
    print(f"\n添加列：\n{df}")
    print("当前列名：", df.columns.tolist())

    print(f'\n删除列：\n{df.drop("age", axis=1)}')

    print(f"\ninfo：\n{df.info()}")


def basic_function():
    print("-" * 30, "基础功能", "-" * 30)
    series = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "gender": pd.Series(["man", "man", "woman"]),
        "math_score": pd.Series([80, 88, 98]),
        "en_score": pd.Series([70, 68, 85]),
    }

    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")
    print(f"\n求和：{df.sum(axis=0, numeric_only=True)}")
    print(f"\n求和1：{df.sum(axis=1, numeric_only=True)}")

    print(f"\n求平均值：\n{df.mean(axis=0, numeric_only=True)}")
    print(f"\n求平均值1：\n{df.mean(axis=1, numeric_only=True)}")

    print(f"\n求最大值：\n{df.max(axis=0, numeric_only=False)}")
    print(f"\n求最大值1：\n{df.max(axis=1, numeric_only=True)}")

    print(f"\n求最小值：\n{df.min(axis=0, numeric_only=False)}")
    print(f"\n求最小值1：\n{df.min(axis=1, numeric_only=True)}")

    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")
    print(f"\n求标准偏差：\n{df.std(axis=0, numeric_only=True)}")
    print(f"\n求标准偏差1：\n{df.std(axis=1, numeric_only=True)}")

    print("-" * 30, "索引重置", "-" * 30)
    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")
    print("索引重命名：")
    print(
        df.rename(
            index={0: "第1行", 1: "第2行", 2: "第3行"},
            columns={
                "name": "姓名",
                "age": "年龄",
                "gender": "性别",
                "en_score": "英语",
                "math_score": "数学",
            },
        )
    )
    df = pd.DataFrame(series)
    print(f"\n源数据：\n{df}")
    print("重建索引：")
    print(df.reindex(index=[0, 1, 3], columns={"name", "age", "height"}))

    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([80, 88, 98]),
    }

    series2 = {
        "name": pd.Series(["Warren", "Leon", "Edith"]),
        "age": pd.Series([21, 18, 15]),
        "score": pd.Series([70, 68, 85]),
    }

    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    print(f"\n源数据1：\n{df1}")
    print(f"\n源数据2：\n{df2}")
    df1 = df1.reindex_like(df2)
    print(f"\nreindex_like数据：\n{df1}")

    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([80, 88, 98]),
        "en_score": pd.Series([70, 68, 85]),
    }

    df1 = pd.DataFrame(series1)
    print(f"\n源数据1：\n{df1}")

    df1 = df1.sort_index(axis=1)
    print(f"\nsort_index：\n{df1}")

    df1 = pd.DataFrame(series1)
    print(f"\n源数据1：\n{df1}")
    df1 = df1.sort_values(by=["math_score"], ascending=False)
    print(f"\nsort_values1：\n{df1}")

    print("-" * 30, "数据遍历", "-" * 30)

    df1 = pd.DataFrame(series1)
    print(f"\n源数据1：\n{df1}")
    for item in df1.itertuples():
        print(item)
    print("-" * 30, "以tuple方式遍历行", "-" * 30)
    for key, val in df1.iterrows():
        print("行索引：", key, "值：", val)
        print("-------------")

    print("-" * 30, "以tuple方式遍历列", "-" * 30)
    df1 = pd.DataFrame(series1)
    for key, val in df1.items():
        print("列名称：\n", key, "\n值：\n", val)
        print("-------------")


def custom_function():
    print("-" * 30, "自定义函数", "-" * 30)

    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
    }

    df1 = pd.DataFrame(series1)

    def f(item, p1, p2):
        item["math_score"] = item["math_score"] + p1
        item["en_score"] = item["en_score"] + p2
        return item

    df1 = df1.apply(f, axis=1, args=(10, 20))
    print(f"\n数据：\n{df1}")

    print("-" * 30, "针对元素", "-" * 30)
    df1 = pd.DataFrame(series1)

    def f(item):
        if isinstance(item, int):
            return item + 10
        elif isinstance(item, str):
            return "hello " + item

    # df1 = df1.applymap(f)
    df1 = df1.apply(lambda x: x.map(f))  # 对每列的每个元素应用 f
    print(f"\n数据：\n{df1}")

    print("-" * 30, "针对整个数据帧", "-" * 30)
    df1 = pd.DataFrame(series1)

    def f(df, p1, p2):
        df["math_score"] = df["math_score"] + p1
        df["en_score"] = df["en_score"] + p2
        return df

    df1 = df1.pipe(f, 10, 20)
    print(f"\n数据：\n{df1}")


def statistical_analysis():
    print("-" * 30, "统计分析", "-" * 30)

    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)

    data = df1["sum_score"].cov(df1["math_score"])

    print(f"\n协方差：\n{data}")

    df1 = pd.DataFrame(series1)

    data = df1["sum_score"].corr(df1["math_score"])
    print(f"\n相关性1：\n{data}")
    data = df1["sum_score"].corr(df1["en_score"], method="pearson")
    print(f"\n相关性2：\n{data}")

    print("-" * 30, "变化率", "-" * 30)
    series1 = {
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print(df1.pct_change(**{"axis": 1}))

    print("-" * 30, "排名", "-" * 30)
    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print(df1.rank(ascending=False))

    print("-" * 30, "扩展", "-" * 30)
    series1 = {
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print(df1.expanding(min_periods=2).sum())

    print("-" * 30, "窗口", "-" * 30)
    series1 = {
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print(df1.rolling(window=2).sum())


# 聚合统计
def aggregation():
    print("-" * 30, "聚合统计", "-" * 30)

    series1 = {
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print(df1.aggregate("sum"))
    # print(df1.aggregate(['sum', 'mean']))
    # print(df1.aggregate({'math_score': 'sum', 'en_score': 'mean'}))

    print("-" * 30, "对单个列进行聚合统计", "-" * 30)
    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
        "sum_score": pd.Series([168, 156, 165]),
    }

    df1 = pd.DataFrame(series1)
    print(df1)
    print("英语总成绩：", df1["en_score"].aggregate('sum'))
    print("数学总成绩：", df1["math_score"].aggregate('sum'))

    print("-" * 30, "对单个列进行多种聚合统计", "-" * 30)
    print("英语总成绩与平均成绩：", df1["en_score"].aggregate(['sum','mean']))
    print("数学总成绩与平均成绩：", df1["math_score"].aggregate(['sum','mean']))
    
    
    print("-" * 30, "对多个列进行聚合统计", "-" * 30)
    df1 = pd.DataFrame(series1)
    print("英语和数学总成绩：", df1[["en_score", "math_score"]].aggregate('sum'))

    print("-" * 30, "对多个列进行多种聚合统计", "-" * 30)
    print("英语和数学总成绩与平均成绩：", df1[["en_score", "math_score"]].aggregate(['sum','mean']))
    print("英语和数学最大成绩：", df1[["en_score", "math_score"]].aggregate('max'))
    print("英语和数学最小成绩：", df1[["en_score", "math_score"]].aggregate('min'))


# 分组统计
def groupby():
    print("-" * 30, "分组统计", "-" * 30)

    series1 = {"name": pd.Series(["Wilson", "Bruce", "Chelsea", "Wilson", "Bruce", "Chelsea"]),
           "math_score": pd.Series([98, 88, 80, 70, 68, 75]),
           "en_score": pd.Series([70, 68, 85, 61, 99, 82]),
           "term": pd.Series(["第一学期", "第一学期", "第一学期",
                              "第二学期", "第二学期", "第二学期"])}

    df1 = pd.DataFrame(series1)
    print(df1)
    print("按学期分组：", df1.groupby("term").groups)
    
    print("-" * 30, "遍历分组", "-" * 30)

    df1 = pd.DataFrame(series1)
    group_data = df1.groupby("term")

    for group_name, member in group_data:
        print(group_name)
        print(member)
    
    print("-" * 30, "获取指定分组", "-" * 30)
    df1 = pd.DataFrame(series1)
    group_data = df1.groupby("term")
    data = group_data.get_group("第二学期")
    print(data)
    
    print("-" * 30, "分组聚合", "-" * 30)
    df1 = pd.DataFrame(series1)
    group_data = df1.groupby(["name"])
    print(f"\n分组聚合数据1：\n{group_data.agg('sum')}")
    
    print("-" * 30, "数据转换", "-" * 30)
    
    df1 = pd.DataFrame(series1)
    group_data = df1.groupby(["name"])
    
    df1[["en_percent", "math_percent"]] = group_data[["en_score", "math_score"]].transform('sum')
    df1["en_percent"] = df1["en_score"] / df1["en_percent"]
    df1["math_percent"] = df1["math_score"] / df1["math_percent"]

    print(f"\n数据转换：\n{df1}")
    
    print("-" * 30, "数据过滤", "-" * 30)
    
    df1 = pd.DataFrame(series1)
    group_data = df1.groupby(["name"])

    # def f(item, a):
    #     if item["math_score"].sum() + item["en_score"].sum() >= a:
    #         return True
    #     else:
    #         return False
    # 定义过滤条件
    def f(item, a):
        print(f'\n分组数据：\n{item["math_score"]}, {item["en_score"]}')
        # 计算每个组的数学和英语成绩总和
        total_score = item["math_score"].sum() + item["en_score"].sum()
        # 如果总和大于等于a，则返回True
        return total_score >= a
    print(f"\n过滤条件：数学和英语成绩之和大于等于{180}分")
    print(f'\n过滤数据：\n{df1}')
    
    # 使用groupby().filter()进行筛选
    data = group_data.filter(lambda x: f(x, a=180))

    # 打印过滤后的数据
    print(f'\n过滤后的数据：\n{data}')
    
    print("-" * 30, "自定义过滤", "-" * 30)

    df1 = pd.DataFrame(series1)

    # 分组后计算总和
    group_data = df1.groupby("name").agg({"math_score": "sum", "en_score": "sum"})
    print(f"\n分组后数据：\n{group_data}")
    # 自定义过滤函数，检查分组总和是否满足条件
    def f(group):
        print(f'\n分组数据：\n{group["math_score"].sum()}, {group["en_score"].sum()}')
        total_score = group["math_score"].sum() + group["en_score"].sum()  # 计算分组内的总和
        return total_score >= 180  # 只保留符合总和大于等于 180 的分组

    # 使用 groupby.filter 过滤符合条件的分组
    filtered_data = df1.groupby("name").filter(f)               

    # 输出结果
    print(f"\n自定义过滤后的数据：\n{filtered_data}")

    
# 连接合并
def merge():
    print("-" * 30, "连接合并", "-" * 30)

    series1 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "math_score": pd.Series([98, 88, 80]),
        "en_score": pd.Series([70, 68, 85]),
    }

    series2 = {
        "name": pd.Series(["Wilson", "Bruce", "Chelsea"]),
        "age": pd.Series([15, 24, 19]),
        "sum_score": pd.Series([168, 156, 165]),
    }
    df1 = pd.DataFrame(series1)
    df2 = pd.DataFrame(series2)
    print(f"\n源数据1：\n{df1}")
    print(f"\n源数据2：\n{df2}")
    df3 = pd.merge(df1, df2, on="name", how="inner")
    print(f"\n合并数据：\n{df3}")
        

if __name__ == "__main__":
    groupby()
