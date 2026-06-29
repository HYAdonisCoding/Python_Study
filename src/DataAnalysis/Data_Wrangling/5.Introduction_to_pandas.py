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


def p_info(**kwargs):
    for name, value in kwargs.items():
        print(f"{name}:")
        print(value)
    print(speter * 2)


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


# 5.1 pandas 数据结构介绍
def pandas_data_structures_introduction():
    print(f"{speter*2}pandas_data_structures_introduction{speter*2}")
    print(f"{speter*2}pandas 数据结构介绍{speter*2}")

    obj = pd.Series([4, 7, -5, 3])
    p_info(obj=obj, values=obj.values, idx=obj.index)

    obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])
    p_info(obj2=obj2, values2=obj2.values, idx2=obj2.index)

    obj2["d"] = 6
    p_info(
        obj2_a=obj2["a"],
        obj2_1=obj2[["c", "a", "d"]],
        obj2_0=obj2[obj2 > 2],
        obj2_2=obj2 * 2,
        obj2_b="b" in obj2,
        obj2_e="e" in obj2,
    )

    sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
    obj3 = pd.Series(sdata)
    p_info(obj3=obj3)

    states = ["California", "Ohio", "Oregon", "Texas"]
    obj4 = pd.Series(sdata, index=states)
    p_info(obj4=obj4, isnull=pd.isnull(obj4), notnull=pd.notnull(obj4))

    p_info(
        obj3_obj4=obj3 + obj4,
    )

    obj4.name = "population"
    obj4.index.name = "state"
    p_info(obj4=obj4, obj=obj)

    obj.index = ["Bob", "Steve", "Jeff", "Ryan"]
    p_info(按位置赋值obj=obj)
    # np.random.seed(12345)

    # plt.rc("figure", figsize=(10, 6))
    # PREVIOUS_MAX_ROWS = pd.options.display.max_rows
    # pd.options.display.max_rows = 20
    # pd.options.display.max_columns = 20
    # pd.options.display.max_colwidth = 80
    # np.set_printoptions(precision=4, suppress=True)
    # plt.show()


# 5.1.1 Series
def series():
    print(f"{speter*2}series{speter*2}")
    print(f"{speter*2}Series{speter*2}")


# 5.1.2 DataFrame
def dataframe():
    print(f"{speter*2}dataframe{speter*2}")
    print(f"{speter*2}DataFrame{speter*2}")

    data = {
        "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
        "year": [2000, 2001, 2002, 2001, 2002, 2003],
        "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2],
    }
    frame = pd.DataFrame(data)
    p_info(frame=frame, head=frame.head(), tail=frame.tail())

    p_info(
        指定顺序排列frame=pd.DataFrame(
            data,
            columns=[
                "pop",
                "year",
                "state",
            ],
        )
    )

    frame2 = pd.DataFrame(
        data,
        columns=["year", "state", "pop", "debt"],
        index=["one", "two", "three", "four", "five", "fix"],
    )
    p_info(
        frame2=frame2,
        columns=frame2.columns,
        state=frame2["state"],
        year=frame2.year,
        three=frame2.loc["three"],
    )

    frame2.debt = np.arange(6.0)
    p_info(
        frame2=frame2,
    )

    val = pd.Series([-1.2, -1.5, -1.7], index=["two", "four", "five"])
    frame2["debt"] = val

    p_info(
        frame2=frame2,
    )
    frame2["eastern"] = frame2["state"] == "Ohio"
    p_info(
        frame2=frame2,
    )

    del frame2["eastern"]
    p_info(frame2=frame2, columns=frame2.columns)

    populations = {
        "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
        "Nevada": {2001: 2.4, 2002: 2.9},
    }
    frame3 = pd.DataFrame(populations)
    p_info(
        frame3=frame3,
        t=frame3.T,
        df=pd.DataFrame(populations, index=[2001, 2002, 2003]),
    )

    pdata = {"Ohio": frame3["Ohio"][:-1], "Nevada": frame3["Nevada"][:2]}
    p_info(pdata=pd.DataFrame(pdata))

    frame3.index.name = "year"
    frame3.columns.name = "state"
    p_info(frame3=frame3, values=frame3.values)


# 5.1.3 索引对象
def index_objects():
    print(f"{speter*2}index_objects{speter*2}")
    print(f"{speter*2}索引对象{speter*2}")

    obj = pd.Series(np.arange(3), index=["a", "b", "c"])
    index = obj.index
    p_info(obj=obj, index=index, index_1=index[1:])
    # index[1] = 'd'
    labels = pd.Index(np.arange(3))
    obj2 = pd.Series([1.5, -2.5, 0], index=labels)

    p_info(labels=labels, obj2=obj2, is_in=obj2.index is labels)
    populations = {
        "Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
        "Nevada": {2001: 2.4, 2002: 2.9},
    }
    frame3 = pd.DataFrame(populations)
    p_info(
        frame3=frame3,
        columns=frame3.columns,
        is_in="Ohio" in frame3.columns,
        is_in1=2003 in frame3.index,
    )

    dup_labels = pd.Index(["foo", "foo", "bar", "bar"])
    p_info(dup_labels=dup_labels)


# 5.2 基本功能
def basic_functionality():
    print(f"{speter*2}basic_functionality{speter*2}")
    print(f"{speter*2}基本功能{speter*2}")


# 5.2.1 重建索引
def reindexing():
    print(f"{speter*2}reindexing{speter*2}")
    print(f"{speter*2}重建索引{speter*2}")

    obj = pd.Series([4.5, 7.2, -5.3, 3.6], index=["d", "b", "a", "c"])
    p_info(
        obj=obj,
    )

    obj2 = obj.reindex(["a", "b", "c", "d", "e"])
    p_info(
        obj2=obj2,
    )

    obj3 = pd.Series(["blue", "purple", "yellow"], index=[0, 2, 4])
    p_info(
        obj3=obj3,
    )

    obj4 = obj3.reindex(np.arange(6), method="ffill")
    p_info(
        obj4=obj4,
    )

    frame = pd.DataFrame(
        np.arange(9).reshape((3, 3)),
        index=["a", "c", "d"],
        columns=["Ohio", "Texas", "California"],
    )
    frame2 = frame.reindex(index=["a", "b", "c", "d"])
    p_info(frame=frame, frame2=frame2)

    states = ["Texas", "Utah", "California"]
    p_info(
        reindex=frame.reindex(columns=states),
        loc=frame.loc[["a", "d", "c"], ["California", "Texas"]],
    )


# 5.2.2 轴向上删除条目
def dropping_entries_from_axis():
    print(f"{speter*2}dropping_entries_from_axis{speter*2}")
    print(f"{speter*2}轴向上删除条目{speter*2}")

    obj = pd.Series(np.arange(5.0), index=["a", "b", "c", "d", "e"])
    p_info(obj=obj)
    new_obj = obj.drop("c")
    p_info(new_obj=new_obj)

    p_info(obj_drop=obj.drop(["d", "c"]))

    data = pd.DataFrame(
        np.arange(16).reshape((4, 4)),
        index=["Ohio", "Colorado", "Utah", "New York"],
        columns=["one", "two", "three", "four"],
    )
    p_info(
        data=data,
        drop=data.drop(index=["Colorado", "Ohio"]),
        d1=data.drop("two", axis=1),
        d2=data.drop(["two", "four"], axis="columns"),
    )
    obj.drop("c", inplace=True)
    p_info(obj=obj)


# 5.2.3 索引、选择与过滤
def indexing_selection_filtering():
    print(f"{speter*2}indexing_selection_filtering{speter*2}")
    print(f"{speter*2}索引、选择与过滤{speter*2}")

    obj = pd.Series(np.arange(4.0), index=["a", "b", "c", "d"])
    p_info(
        obj=obj,
        obj_b=obj["b"],
        obj_1=obj.iloc[1],
        obj_2_4=obj[2:4],
        obj_3=obj[["b", "a", "d"]],
        obj_1_3=obj.iloc[[1, 3]],
        obj_2=obj[obj < 2],
    )
    obj["b":"c"] = 5
    p_info(obj=obj)

    data = pd.DataFrame(
        np.arange(16).reshape((4, 4)),
        index=["Ohio", "Colorado", "Utah", "New York"],
        columns=["one", "two", "three", "four"],
    )
    p_info(
        data=data,
        data_two=data["two"],
        data_two_=data[["three", "one"]],
        data_2=data[:2],
        data_3_=data[data["three"] > 5],
        data_5=data < 5,
    )
    data[data < 5] = 0
    p_info(
        data=data,
        loc=data.loc["Colorado", ["two", "three"]],
        iloc=data.iloc[2, [3, 0, 1]],
        iloc_1=data.iloc[2],
        iloc_2=data.iloc[[1, 2], [3, 0, 1]],
        loc1=data.loc[:"Utah", "two"],
        iloc_3=data.iloc[:, :3][data.three > 5],
    )


# 5.2.4 整数索引
def integer_indexing():
    print(f"{speter*2}integer_indexing{speter*2}")
    print(f"{speter*2}整数索引{speter*2}")

    ser = pd.Series(np.arange(3.0))
    p_info(ser=ser, ser1=ser.iloc[-1])

    ser2 = pd.Series(np.arange(3.0), index=["a", "b", "c"])
    p_info(
        ser2=ser2,
        ser21=ser2.iloc[-1],
        ser2_1=ser[:1],
        ser2_2=ser.loc[:1],
        ser2_3=ser.iloc[:1],
    )


# 5.2.5 算术和数据对齐
def arithmetic_and_data_alignment():
    print(f"{speter*2}arithmetic_and_data_alignment{speter*2}")
    print(f"{speter*2}算术和数据对齐{speter*2}")

    s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
    s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=["a", "c", "e", "f", "g"])
    p_info(s1=s1, s2=s2, s1_s2=s1 + s2)
    df1 = pd.DataFrame(
        np.arange(9.0).reshape((3, 3)),
        columns=list("bcd"),
        index=["Ohio", "Texas", "Colorado"],
    )
    df2 = pd.DataFrame(
        np.arange(12.0).reshape((4, 3)),
        columns=list("bde"),
        index=["Utah", "Ohio", "Texas", "Oregon"],
    )
    p_info(df1=df1, df2=df2, df1_df2=df1 + df2)

    df1 = pd.DataFrame({"A": [1, 2]})
    df2 = pd.DataFrame({"B": [3, 4]})
    p_info(df1=df1, df2=df2, df1_df2=df1 - df2)
    df1 = pd.DataFrame(np.arange(12.0).reshape((3, 4)), columns=list("abcd"))
    df2 = pd.DataFrame(np.arange(20.0).reshape((4, 5)), columns=list("abcde"))
    df2.loc[1, "b"] = np.nan
    p_info(
        df1=df1,
        df2=df2,
        df1_df2=df1 + df2,
        df1_df2_f=df1.add(df2, fill_value=0),
        rdiv=1 / df1,
        rdiv1=df1.rdiv(1),
        ridx=df1.reindex(columns=df2.columns, fill_value=0),
    )

    arr = np.arange(12.0).reshape((3, 4))
    p_info(arr=arr, arr_0=arr[0], arr_1=arr - arr[0])

    frame = pd.DataFrame(
        np.arange(12.0).reshape((4, 3)),
        columns=list("bde"),
        index=["Utah", "Ohio", "Texas", "Oregon"],
    )

    series = frame.iloc[0]
    series2 = pd.Series(np.arange(3), index=["b", "e", "f"])
    p_info(
        frame=frame,
        series=series,
        frame_series=frame - series,
        series2=series2,
        frame_add_series2=frame + series2,
    )

    series3 = frame["d"]
    p_info(frame=frame, series3=series3, sub=frame.sub(series3, axis="index"))


# 5.2.6 函数应用和映射
def function_application_and_mapping():
    print(f"{speter*2}function_application_and_mapping{speter*2}")
    print(f"{speter*2}函数应用和映射{speter*2}")

    frame = pd.DataFrame(
        np.random.standard_normal((4, 3)),
        columns=list("bde"),
        index=["Utah", "Ohio", "Texas", "Oregon"],
    )
    f = lambda x: x.max() - x.min()

    p_info(
        frame=frame,
        abs=np.abs(frame),
        l=frame.apply(f),
        l1=frame.apply(f, axis="columns"),
    )

    def f1(x):
        return x.max() - x.min()

    def f2(x):
        return pd.Series([x.min(), x.max()], index=["min", "max"])

    p_info(f1=frame.apply(f1), f2=frame.apply(f2))

    def my_format(x):
        return f"{x:.2f}"

    format = lambda x: "%.2f" % x
    p_info(my_format=frame.map(my_format), format=frame.map(format))


# 5.2.7 排序和排名
def sorting_and_ranking():
    print(f"{speter*2}sorting_and_ranking{speter*2}")
    print(f"{speter*2}排序和排名{speter*2}")

    obj = pd.Series(np.arange(4), index=["d", "a", "b", "c"])
    p_info(
        obj=obj,
        sort=obj.sort_index(),
    )

    frame = pd.DataFrame(
        np.arange(8).reshape((2, 4)),
        index=["three", "one"],
        columns=["d", "a", "b", "c"],
    )
    p_info(
        frame=frame,
        sort=frame.sort_index(),
        sort1=frame.sort_index(axis="columns"),
        sort2=frame.sort_index(axis="columns", ascending=False),
    )

    obj = pd.Series([4, 7, -3, 2])
    p_info(obj=obj, sort=obj.sort_values())

    obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
    p_info(obj=obj, sort=obj.sort_values())

    frame = pd.DataFrame({"b": [4, 7, -3, 2], "a": [0, 1, 0, 1]})
    p_info(
        frame=frame,
        sort=frame.sort_values("b"),
        sort1=frame.sort_values(by=["a", "b"]),
    )

    obj = pd.Series([7, -5, 7, 4, 2, 0, 4])
    p_info(
        obj=obj,
        rank=obj.rank(),
        rank1=obj.rank(method="first"),
        rank2=obj.rank(ascending=False),
        rank3=obj.rank(ascending=False, method="max"),
    )

    frame = pd.DataFrame(
        {"b": [4.3, 7, -3, 2], "a": [0, 1, 0, 1], "c": [-2, 5, 8, -2.5]}
    )
    p_info(frame=frame, rank=frame.rank(axis="columns"))


# 5.2.8 含有重复标签的轴索引
def duplicate_labels_axis_index():
    print(f"{speter*2}duplicate_labels_axis_index{speter*2}")
    print(f"{speter*2}含有重复标签的轴索引{speter*2}")

    df = pd.DataFrame(range(5), index=["a", "a", "b", "b", "c"])
    p_info(
        df=df,
        loc_b=df.loc["b"],
        loc_c=df.loc["c"],
        is_unique=df.index.is_unique,
        df_a=df.loc["a"],
        df_c_=df.loc["c"],
    )

    df = pd.DataFrame(
        np.random.standard_normal((5, 3)), index=["a", "a", "b", "b", "c"]
    )
    p_info(
        df=df,
        loc_b=df.loc["b"],
        loc_c=df.loc["c"],
    )


# 5.3 描述性统计的概述与计算
def descriptive_statistics():
    print(f"{speter*2}descriptive_statistics{speter*2}")
    print(f"{speter*2}描述性统计的概述与计算{speter*2}")

    df = pd.DataFrame(
        [[1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], [0.75, -1.3]],
        index=["a", "b", "c", "d"],
        columns=["one", "two"],
    )
    p_info(
        df=df,
        sum=df.sum(),
        sum1=df.sum(axis="columns"),
        sum2=df.sum(axis="index", skipna=False),
        sum3=df.sum(axis="columns", skipna=False),
        mean=df.mean(axis="columns"),
        idxmax=df.idxmax(),
        cumsum=df.cumsum(),
        describe=df.describe(),
    )
    obj = pd.Series(["a", "a", "b", "c"] * 4)
    p_info(obj=obj, describe=obj.describe())


# 5.3.1 相关性和协方差
def correlation_and_covariance():
    print(f"{speter*2}correlation_and_covariance{speter*2}")
    print(f"{speter*2}相关性和协方差{speter*2}")

    price = pd.read_pickle(f"{base_dir}/examples/yahoo_price_new.pkl")
    volume = pd.read_pickle(f"{base_dir}/examples/yahoo_volume_new.pkl")
    returns = price.pct_change()
    corr1 = returns["MSFT"].corr(returns.IBM)
    p_info(
        tail=returns.tail(),
        corr=returns["MSFT"].corr(returns["IBM"]),
        cov=returns["MSFT"].cov(returns["IBM"]),
        corr1=corr1,
        coor2=returns.corr(),
        cov1=returns.cov(),
        ibm=returns.corrwith(returns["IBM"]),
        ibm1=returns.corrwith(returns.IBM),
        corrw=returns.corrwith(volume),
    )


# 5.3.2 唯一值、计数和成员属性
def unique_values_counts_membership():
    print(f"{speter*2}unique_values_counts_membership{speter*2}")
    print(f"{speter*2}唯一值、计数和成员属性{speter*2}")

    obj = pd.Series(["c", "a", "d", "a", "a", "b", "b", "c", "c"])
    uniques = obj.unique()
    p_info(
        uniques=uniques,
        sort=np.sort(uniques),
        cnt=obj.value_counts(),
        cnt_sort=obj.value_counts(sort=False),
        cnt_sort1=obj.value_counts(sort=True),
        obj=obj,
    )
    mask = obj.isin(["b", "c"])
    p_info(
        mask=mask,
        m1=obj[mask],
    )
    to_match = pd.Series(["c", "a", "b", "b", "c", "a"])
    unique_vals = pd.Series(["c", "b", "a"])
    indices = pd.Index(unique_vals).get_indexer(to_match)
    p_info(indices=indices)

    data = pd.DataFrame(
        {"Qu1": [1, 3, 4, 3, 4], "Qu2": [2, 3, 1, 2, 3], "Qu3": [1, 5, 2, 4, 4]}
    )
    result = data.apply(pd.Series.value_counts).fillna(0)

    p_info(data=data, result=result)


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        unique_values_counts_membership()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
