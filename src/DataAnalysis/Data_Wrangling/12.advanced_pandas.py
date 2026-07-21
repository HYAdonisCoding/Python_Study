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


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


# 12.1 分类数据
def categorical_data():
    print(f"{speter*2}categorical_data{speter*2}")
    print(f"{speter*2}分类数据{speter*2}")


# 12.1.1 背景和目标
def categorical_background_and_goals():
    print(f"{speter*2}categorical_background_and_goals{speter*2}")
    print(f"{speter*2}背景和目标{speter*2}")

    values = pd.Series(["apple", "orange", "apple", "apple"] * 2)
    p_info(
        values=values,
        unique=pd.unique(values),
        value_counts=values.value_counts(),
    )

    values = pd.Series([0, 1, 0, 0] * 2)
    dim = pd.Series(["apple", "orange"])
    p_info(
        values=values,
        dim=dim,
        take=dim.take(values),
    )


# 12.1.2 pandas 中的 Categorical类型
def pandas_categorical_type():
    print(f"{speter*2}pandas_categorical_type{speter*2}")
    print(f"{speter*2}pandas 中的 Categorical类型{speter*2}")

    fruits = ["apple", "orange", "apple", "apple"] * 2
    N = len(fruits)
    df = pd.DataFrame(
        {
            "fruit": fruits,
            "basket_id": np.arange(N),
            "count": np.random.randint(3, 15, size=N),
            "weight": np.random.uniform(0, 4, size=N),
        },
        columns=["basket_id", "fruit", "count", "weight"],
    )
    fruit_cat = df["fruit"].astype("category")
    c = fruit_cat.values

    p_info(
        df=df,
        fruit_cat=fruit_cat,
        c=c,
        c_t=type(c),
    )
    df["fruit"] = df["fruit"].astype("category")
    p_info(
        df=df,
        dff=df["fruit"],
    )

    my_categories = pd.Categorical(["foo", "bar", "baz", "foo", "bar"])
    categories = [
        "foo",
        "bar",
        "baz",
    ]
    codes = [0, 1, 2, 0, 0, 1]
    my_cats = pd.Categorical.from_codes(codes, categories)
    order_cats = pd.Categorical.from_codes(codes, categories, ordered=True)
    p_info(
        my_categories=my_categories,
        my_cats=my_cats,
        order_cats=order_cats,
        my=my_cats.as_ordered(),
    )


import time


# 12.1.3 使用Categorical 对象进行计算
def computations_with_categorical_objects():
    print(f"{speter*2}computations_with_categorical_objects{speter*2}")
    print(f"{speter*2}使用Categorical 对象进行计算{speter*2}")

    np.random.seed(12345)
    draws = np.random.randn(1000)
    bins = pd.qcut(draws, 4)
    bins1 = pd.qcut(draws, 4, labels=["Q1", "Q2", "Q3", "Q4"])
    bins2 = pd.Series(bins1, name="quartile")
    results = pd.Series(draws).groupby(bins2).agg(["count", "min", "max"]).reset_index()

    N = 10000000
    draws1 = pd.Series(np.random.randn(N))
    labels = pd.Series(["foo", "bar", "baz", "qux"] * (N // 4))
    categories = labels.astype("category")
    start = time.time()

    _ = labels.astype("category")

    end = time.time()

    print(f"耗时: {end - start:.6f}s")
    p_info(
        draws=draws[:5],
        bins=bins,
        bins1=bins1,
        bins1_=bins1.codes[:10],
        bins2=bins2,
        results=results,
        results_q=results["quartile"],
        labels_m=labels.memory_usage(),
        categories_m=categories.memory_usage(),
    )


# 12.1.4 分类方法
def categorical_methods():
    print(f"{speter*2}categorical_methods{speter*2}")
    print(f"{speter*2}分类方法{speter*2}")

    s = pd.Series(["a", "b", "c", "d"] * 2)
    cat_s = s.astype("category")
    p_info(s=s, cat_s=cat_s, codes=cat_s.cat.codes, categories=cat_s.cat.categories)

    actual_categories = ["a", "b", "c", "d", "e"]
    cat_s2 = cat_s.cat.set_categories(actual_categories)
    cat_s3 = cat_s[cat_s.isin(["a", "b"])]
    p_info(
        cat_s2=cat_s2,
        value_counts=cat_s.value_counts(),
        value_counts2=cat_s2.value_counts(),
        cat_s3=cat_s3,
        remove_unused_categories=cat_s3.cat.remove_unused_categories(),
        get_dummies=pd.get_dummies(cat_s),
    )


# 12.2 高阶 GroupBy 应用
def advanced_groupby_applications():
    print(f"{speter*2}advanced_groupby_applications{speter*2}")
    print(f"{speter*2}高阶 GroupBy 应用{speter*2}")

    df = pd.DataFrame({"key": ["a", "b", "c"] * 4, "value": np.arange(12.0)})
    g = df.groupby("key").value

    def normalize(x):
        return (x - x.mean()) / x.std()

    p_info(
        df=df,
        g=g,
        mean=g.mean(),
        transform=g.transform(lambda x: x.mean()),
        transform1=g.transform("mean"),
        transform2=g.transform(lambda x: x * 2),
        transform3=g.transform(lambda x: x.rank(ascending=False)),
        transform4=g.transform(normalize),
        apple=g.apply(normalize),
    )

    normalized = (df["value"] - g.transform("mean")) / g.transform("std")
    p_info(normalized=normalized)


# 12.2.1 分组转换和“展开”GroupBy
def group_transformations_and_unstack_groupby():
    print(f"{speter*2}group_transformations_and_unstack_groupby{speter*2}")
    print(f"{speter*2}分组转换和“展开”GroupBy{speter*2}")


# 12.2.2 分组的时间重新采样
def grouped_time_resampling():
    print(f"{speter*2}grouped_time_resampling{speter*2}")
    print(f"{speter*2}分组的时间重新采样{speter*2}")
    N = 15
    times = pd.date_range("2017-05-20 00:00", freq="1min", periods=N)
    df = pd.DataFrame({"time": times, "value": np.arange(N)})
    df2 = pd.DataFrame(
        {
            "time": times.repeat(3),
            "key": np.tile(["a", "b", "c"], N),
            "value": np.arange(N * 3.0),
        }
    )

    time_key = pd.Grouper(freq="5min")
    resampled = df2.set_index("time").groupby(["key", time_key]).sum()
    p_info(
        df=df,
        cnt=df.set_index("time").resample("5min").count(),
        df2=df2,
        resampled=resampled,
        reset_index=resampled.reset_index(),
    )


# 12.3 方法链技术
def method_chaining_techniques():
    print(f"{speter*2}method_chaining_techniques{speter*2}")
    print(f"{speter*2}方法链技术{speter*2}")

    df = load_data()
    df2 = df[df["col2"] < 0]
    df2["col1_demeaned"] = df2["col1"] - df2["col1"].mean()
    result = df2.groupby("key").col1_demeaned.std()
    result1 = (
        df2.assign(col1_demeaned=df2.col1 - df2.col2.mean())
        .groupby("key")
        .col1_demeaned.std()
    )
    df3 = load_data()[lambda x: x["col2"] < 0]

    result2 = (
        load_data()[lambda x: x.col2 < 0]
        .assign(col1_demeaned=lambda x: x.col1 - x.xol1.mean())
        .groupby("key")
        .col1_demeaned.std()
    )


def load_data():
    pass


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
        pipe_method()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
