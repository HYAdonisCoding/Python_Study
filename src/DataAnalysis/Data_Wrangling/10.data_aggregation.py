#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第10章 数据聚合与分组操作
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


# 10.1 GroupBy 机制
def groupby_mechanism():
    print(f"{speter*2}groupby_mechanism{speter*2}")
    print(f"{speter*2}GroupBy 机制{speter*2}")

    df = pd.DataFrame(
        {
            "key1": ["a", "a", None, "b", "b", "a", None],
            "key2": pd.Series(["one", "two", "one", "two", "one", None, "one"]),
            "data1": np.random.standard_normal(7),
            "data2": np.random.standard_normal(7),
        }
    )
    grouped = df["data1"].groupby(df["key1"])
    means = df["data1"].groupby([df["key1"], df["key2"]]).mean()

    p_info(
        df=df,
        grouped=grouped,
        mean=grouped.mean(),
        means=means,
        means_unstack=means.unstack(),
    )

    states = np.array(["OH", "CA", "CA", "OH", "OH", "CA", "OH"])
    years = [2005, 2005, 2006, 2005, 2006, 2005, 2006]
    df1 = df["data1"].groupby([states, years])
    p_info(
        df1=df1,
        mean=df["data1"].groupby([states, years]).mean(),
        mean1=df.groupby("key1").mean(numeric_only=True),
        mean2=df.groupby("key2").mean(numeric_only=True),
        mean3=df.groupby(["key1", "key2"]).mean(),
        size=df.groupby(["key1", "key2"]).size(),
    )
    for name, group in df.groupby("key1"):
        print(name)
        print(group)
    for (k1, k2), group in df.groupby(["key1", "key2"]):
        print((k1, k2))
        print(group)

    pieces = {name: group for name, group in df.groupby("key1")}
    p_info(
        pieces_b=pieces["b"],
    )
    pieces = dict(list(df.groupby("key1")))
    p_info(
        pieces_b=pieces["b"],
        dtypes=df.dtypes,
    )
    grouped = {dtype: df.loc[:, df.dtypes == dtype] for dtype in df.dtypes.unique()}
    for group_key, group_values in grouped.items():
        print(group_key)
        print(group_values)
    print(f"{speter*2}选择一列或所有列的子集{speter*2}")
    p_info(
        mean=df.groupby(["key1", "key2"])[["data2"]].mean(),
    )


# 10.1.1 遍历各分组
def iterating_over_groups():
    print(f"{speter*2}iterating_over_groups{speter*2}")
    print(f"{speter*2}遍历各分组{speter*2}")
    groupby_mechanism()


# 10.1.2 选择一列或所有列的子集
def selecting_columns_or_subsets():
    print(f"{speter*2}selecting_columns_or_subsets{speter*2}")
    print(f"{speter*2}选择一列或所有列的子集{speter*2}")
    groupby_mechanism()


# 10.1.3 使用字典和 Series 分组
def grouping_with_dictionaries_and_series():
    print(f"{speter*2}grouping_with_dictionaries_and_series{speter*2}")
    print(f"{speter*2}使用字典和 Series 分组{speter*2}")

    people = pd.DataFrame(
        np.random.standard_normal((5, 5)),
        columns=["a", "b", "c", "d", "e"],
        index=["Joe", "Steve", "Wanda", "Jill", "Trey"],
    )
    p_info(people=people)
    people.iloc[2:3, [1, 2]] = np.nan  # Add a few NA values
    p_info(people_1=people)
    mapping = {
        "a": "red",
        "b": "red",
        "c": "blue",
        "d": "blue",
        "e": "red",
        "f": "orange",
    }
    # by_column = people.groupby(mapping, axis="columns")
    map_series = pd.Series(mapping)
    p_info(
        sum=people.T.groupby(mapping).sum().T,
        map_series=map_series,
        # cnt=people.groupby(map_series, axis="columns").count(),
        cnt=people.T.groupby(map_series).count().T,
    )
    print(f"{speter*2}使用函数分组{speter*2}")

    key_list = ["one", "one", "one", "two", "two"]
    columns = pd.MultiIndex.from_arrays(
        [["US", "US", "US", "JP", "JP"], [1, 3, 5, 1, 3]], names=["cty", "tenor"]
    )
    hier_df = pd.DataFrame(np.random.standard_normal((4, 5)), columns=columns)
    p_info(
        sum=people.groupby(len).sum(),
        min=people.groupby([len, key_list]).min(),
        columns=columns,
        hier_df=hier_df,
        cnt=hier_df.T.groupby(level="cty").count().T,
    )


# 10.1.4 使用函数分组
def grouping_with_functions():
    print(f"{speter*2}grouping_with_functions{speter*2}")
    print(f"{speter*2}使用函数分组{speter*2}")


# 10.1.5 根据索引层级分组
def grouping_by_index_levels():
    print(f"{speter*2}grouping_by_index_levels{speter*2}")
    print(f"{speter*2}根据索引层级分组{speter*2}")


# 10.2 数据聚合
def data_aggregation():
    print(f"{speter*2}data_aggregation{speter*2}")
    print(f"{speter*2}数据聚合{speter*2}")
    df = pd.DataFrame(
        {
            "key1": ["a", "a", None, "b", "b", "a", None],
            "key2": pd.Series(["one", "two", "one", "two", "one", None, "one"]),
            "data1": np.random.standard_normal(7),
            "data2": np.random.standard_normal(7),
        }
    )
    grouped = df.groupby("key1")

    p_info(
        df=df,
        q=grouped["data1"].nsmallest(2),
        peak=grouped[["data1", "data2"]].agg(peak_to_peak),
        grouped_describe=grouped.describe(),
    )


def peak_to_peak(arr):
    return arr.max() - arr.min()


# 10.2.1 逐列及多函数应用
def column_wise_and_multiple_function_application():
    print(f"{speter*2}column_wise_and_multiple_function_application{speter*2}")
    print(f"{speter*2}逐列及多函数应用{speter*2}")
    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]

    grouped = tips.groupby(["day", "smoker"])
    grouped_pct = grouped["tip_pct"]

    functions = ["count", "mean", "max"]
    result = grouped[["tip_pct", "total_bill"]].agg(functions)

    ftuples = [("Average", "mean"), ("Variance", np.var)]

    p_info(
        head=tips.head(),
        top6=tips[:6],
        grouped=grouped,
        mean=grouped_pct.agg("mean"),
        agg=grouped_pct.agg(["mean", "std", peak_to_peak]),
        agg1=grouped_pct.agg([("average", "mean"), ("stdev", np.std)]),
        agg2=grouped_pct.agg([("average", "mean"), ("bar", np.std)]),
        result=result,
        tip_pct=result["tip_pct"],
        agg_ftuples=grouped[["tip_pct", "total_bill"]].agg(ftuples),
        grouped_agg1=grouped.agg({"tip": np.max, "size": "sum"}),
        grouped_agg2=grouped.agg(
            {"tip_pct": ["min", "max", "mean", "std"], "size": "sum"}
        ),
    )
    print(f"{speter*2}返回不含行索引的聚合数据{speter*2}")
    grouped = tips.groupby(["day", "smoker"], as_index=False)
    p_info(
        grouped_mean=grouped.mean(numeric_only=True),
    )


# 10.2.2 返回不含行索引的聚合数据
def aggregate_without_row_index():
    print(f"{speter*2}aggregate_without_row_index{speter*2}")
    print(f"{speter*2}返回不含行索引的聚合数据{speter*2}")


def top(df, n=5, column="tip_pct"):
    return df.sort_values(column, ascending=False)[:n]


# 10.3 应用：通用拆分-应用-联合
def general_split_apply_combine():
    print(f"{speter*2}general_split_apply_combine{speter*2}")
    print(f"{speter*2}应用：通用拆分-应用-联合{speter*2}")
    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]
    result = tips.groupby("smoker")["tip_pct"].describe()

    p_info(
        top=top(tips, n=6),
        smoker=tips.groupby("smoker").apply(top),
        apply=tips.groupby(["smoker", "day"]).apply(top, n=1, column="total_bill"),
        result=result,
        unstack=result.unstack("smoker"),
    )
    print(f"{speter*2}压缩分组键{speter*2}")
    p_info(
        smoker=tips.groupby("smoker", group_keys=False).apply(top),
    )


# 10.3.1 压缩分组键
def compressing_group_keys():
    print(f"{speter*2}compressing_group_keys{speter*2}")
    print(f"{speter*2}压缩分组键{speter*2}")


# 10.3.2 分位数与桶分析
def quantile_and_bucket_analysis():
    print(f"{speter*2}quantile_and_bucket_analysis{speter*2}")
    print(f"{speter*2}分位数与桶分析{speter*2}")
    frame = pd.DataFrame(
        {
            "data1": np.random.standard_normal(1000),
            "data2": np.random.standard_normal(1000),
        }
    )
    p_info(head=frame.head())
    quartiles = pd.cut(frame["data1"], 4)
    grouped = frame.groupby(quartiles)
    grouping = pd.cut(frame.data1, 10, labels=False)
    grouped1 = frame.data2.groupby(grouping)
    p_info(
        head=quartiles.head(10),
        g=grouped.apply(get_stats),
        g1=grouped.apply(get_stats).unstack(),
        g2=grouped1.apply(get_stats).unstack(),
    )


def get_stats(group):
    return pd.Series(
        {
            "min": group.min(),
            "max": group.max(),
            "count": group.count(),
            "mean": group.mean(),
        }
    )


# 10.3.3 示例：使用指定分组值填充缺失值
def fill_missing_values_with_group_values():
    print(f"{speter*2}fill_missing_values_with_group_values{speter*2}")
    print(f"{speter*2}示例：使用指定分组值填充缺失值{speter*2}")
    s = pd.Series(np.random.standard_normal(6))
    s[::2] = np.nan
    p_info(
        s=s,
        fillna=s.fillna(s.mean()),
    )
    states = [
        "Ohio",
        "New York",
        "Vermont",
        "Florida",
        "Oregon",
        "Nevada",
        "California",
        "Idaho",
    ]
    group_key = ["East", "East", "East", "East", "West", "West", "West", "West"]
    data = pd.Series(np.random.standard_normal(8), index=states)
    p_info(
        data=data,
    )
    data[["Vermont", "Nevada", "Idaho"]] = np.nan

    p_info(
        data_na=data,
        size=data.groupby(group_key).size(),
        count=data.groupby(group_key).count(),
        mean=data.groupby(group_key).mean(),
    )

    def fill_mean(group):
        return group.fillna(group.mean())

    data.groupby(group_key).apply(fill_mean)


# 10.3.4 示例：随机采样与排列
def random_sampling_and_permutation():
    print(f"{speter*2}random_sampling_and_permutation{speter*2}")
    print(f"{speter*2}示例：随机采样与排列{speter*2}")

    suits = ["H", "S", "C", "D"]  # Hearts, Spades, Clubs, Diamonds
    card_val = (list(range(1, 11)) + [10] * 3) * 4
    base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
    cards = []
    for suit in suits:
        cards.extend(str(num) + suit for num in base_names)

    deck = pd.Series(card_val, index=cards)

    def draw(deck, n=5):
        return deck.sample(n)

    p_info(
        deck=deck[:13],
        draw=draw(deck),
    )

    def get_suit(card):
        # last letter is suit
        return card[-1]

    p_info(
        deck1=deck.groupby(get_suit).apply(draw, n=2),
        deck2=deck.groupby(get_suit, group_keys=False).apply(draw, n=2),
    )


# 10.3.5 示例：分组加权平均和相关性
def grouped_weighted_average_and_correlation():
    print(f"{speter*2}grouped_weighted_average_and_correlation{speter*2}")
    print(f"{speter*2}示例：分组加权平均和相关性{speter*2}")
    df = pd.DataFrame(
        {
            "category": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "data": np.random.standard_normal(8),
            "weights": np.random.uniform(size=8),
        }
    )
    p_info(
        df=df,
    )
    grouped = df.groupby("category")

    def get_wavg(group):
        return np.average(group["data"], weights=group["weights"])

    p_info(
        apply=grouped.apply(get_wavg),
    )

    close_px = pd.read_csv(
        f"{base_dir}/examples/stock_px.csv", parse_dates=True, index_col=0
    )
    close_px.info()
    p_info(
        tail=close_px.tail(4),
    )
    spx_corr = lambda x: x.corrwith(x[["SPX"]])
    rets = close_px.pct_change().dropna()

    def spx_corr(group):
        return group.corrwith(group["SPX"])

    get_year = lambda x: x.year
    by_year = rets.groupby(get_year)
    p_info(
        by_year=by_year,
        by_year1=by_year.apply(spx_corr),
        by_year2=by_year.apply(lambda g: g["AAPL"].corr(g["MSFT"])),
    )
    print(f"{speter*2}示例：逐组线性回归{speter*2}")

    def regress(data, yvar=None, xvars=None):
        Y = data[yvar]
        X = data[xvars]
        X["intercept"] = 1.0
        result = sm.OLS(Y, X).fit()
        return result.params

    p_info(
        apply=by_year.apply(regress, yvar="AAPL", xvars=["SPX"]),
    )


import statsmodels.api as sm


# 10.3.6 示例：逐组线性回归
def grouped_linear_regression():
    print(f"{speter*2}grouped_linear_regression{speter*2}")
    grouped_weighted_average_and_correlation()


# 10.4 数据透视表与交叉表
def pivot_tables_and_cross_tabulation():
    print(f"{speter*2}pivot_tables_and_cross_tabulation{speter*2}")
    print(f"{speter*2}数据透视表与交叉表{speter*2}")
    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]

    piv = tips.pivot_table(
        values=["tip", "total_bill", "size", "tip_pct"],
        index=["day", "smoker"],
        aggfunc="mean",
    )

    p_info(
        head=tips.head(),
        piv=piv,
        piv1=tips.pivot_table(
            index=["time", "day"], columns="smoker", values=["tip_pct", "size"]
        ),
        piv2=tips.pivot_table(
            index=["time", "day"],
            columns="smoker",
            values=["tip_pct", "size"],
            margins=True,
        ),
        piv3=tips.pivot_table(
            index=["time", "smoker"],
            columns="day",
            values="tip_pct",
            aggfunc=len,
            margins=True,
        ),
        piv4=tips.pivot_table(
            index=["time", "size", "smoker"],
            columns="day",
            values="tip_pct",
            fill_value=0,
        ),
    )


# 10.4.1 交叉表：crosstab
def cross_tabulation_crosstab():
    print(f"{speter*2}cross_tabulation_crosstab{speter*2}")
    print(f"{speter*2}交叉表：crosstab{speter*2}")
    from io import StringIO

    tips = pd.read_csv(f"{base_dir}/examples/tips.csv")
    tips["tip_pct"] = tips["tip"] / tips["total_bill"]
    data = """Sample  Nationality  Handedness
    1   USA  Right-handed
    2   Japan    Left-handed
    3   USA  Right-handed
    4   Japan    Right-handed
    5   Japan    Left-handed
    6   Japan    Right-handed
    7   USA  Right-handed
    8   USA  Left-handed
    9   Japan    Right-handed
    10  USA  Right-handed"""
    data = pd.read_table(StringIO(data), sep="\s+")
    p_info(
        data=data,
        crosstab1=pd.crosstab(data["Nationality"], data["Handedness"], margins=True),
        crosstab2=pd.crosstab(
            [tips["time"], tips["day"]], tips["smoker"], margins=True
        ),
    )


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        cross_tabulation_crosstab()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
