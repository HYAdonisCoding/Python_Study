#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第8章 数据规整：连接、联合与重塑
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


# 8.1 分层索引
def hierarchical_indexing():
    print(f"{speter*2}hierarchical_indexing{speter*2}")
    print(f"{speter*2}分层索引{speter*2}")
    data = pd.Series(
        np.random.uniform(size=9),
        index=[
            ["a", "a", "a", "b", "b", "c", "c", "d", "d"],
            [1, 2, 3, 1, 3, 1, 2, 2, 3],
        ],
    )
    p_info(
        data=data,
        data_idx=data.index,
        data_b=data["b"],
        data_b_c=data["b":"c"],
        data_bd=data.loc[["b", "d"]],
        # 内部层级中
        data_inner=data.loc[:, 2],
        data_unstack=data.unstack(),
        data_stack=data.unstack().stack(),
    )
    frame = pd.DataFrame(
        np.arange(12).reshape((4, 3)),
        index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
        columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
    )
    p_info(frame=frame)
    frame.index.names = ["key1", "key2"]
    frame.columns.names = ["state", "color"]
    p_info(frame=frame, lev=frame.index.nlevels, f1=frame["Ohio"])

    print(f"{speter*2}重排序和层级排序{speter*2}")
    p_info(
        frame=frame.swaplevel("key1", "key2"),
        sort=frame.sort_index(level=1),
        swap=frame.swaplevel(0, 1).sort_index(level=0),
    )
    print(f"{speter*2}按层级进行汇总统计{speter*2}")
    p_info(sum=frame.groupby(level="key2").sum())


# 8.1.1 重排序和层级排序
def reordering_and_sorting_levels():
    print(f"{speter*2}reordering_and_sorting_levels{speter*2}")
    print(f"{speter*2}重排序和层级排序{speter*2}")
    hierarchical_indexing()


# 8.1.2 按层级进行汇总统计
def summary_statistics_by_level():
    print(f"{speter*2}summary_statistics_by_level{speter*2}")
    print(f"{speter*2}按层级进行汇总统计{speter*2}")
    hierarchical_indexing()


# 8.1.3 使用 DataFrame 的列进行索引
def indexing_with_dataframe_columns():
    print(f"{speter*2}indexing_with_dataframe_columns{speter*2}")
    print(f"{speter*2}使用 DataFrame 的列进行索引{speter*2}")
    frame = pd.DataFrame(
        {
            "a": range(7),
            "b": range(7, 0, -1),
            "c": ["one", "one", "one", "two", "two", "two", "two"],
            "d": [0, 1, 2, 0, 1, 2, 3],
        }
    )
    frame2 = frame.set_index(["c", "d"])
    p_info(
        frame=frame,
        frame2=frame2,
        set_idx=frame.set_index(["c", "d"], drop=False),
        reindex=frame2.reset_index(),
    )


# 8.2 联合与合并数据集


# 8.2.1 数据库风格的 DataFrame 连接
def database_style_dataframe_join():
    print(f"{speter*2}database_style_dataframe_join{speter*2}")
    print(f"{speter*2}数据库风格的 DataFrame 连接{speter*2}")

    df1 = pd.DataFrame(
        {
            "key": ["b", "b", "a", "c", "a", "a", "b"],
            "data1": pd.Series(range(7), dtype="Int64"),
        }
    )

    df2 = pd.DataFrame(
        {"key": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")}
    )
    m1 = pd.merge(df1, df2)
    m2 = pd.merge(df1, df2, on="key")
    df3 = pd.DataFrame(
        {
            "lkey": ["b", "b", "a", "c", "a", "a", "b"],
            "data1": pd.Series(range(7), dtype="Int64"),
        }
    )
    df4 = pd.DataFrame(
        {"rkey": ["a", "b", "d"], "data2": pd.Series(range(3), dtype="Int64")}
    )
    m3 = pd.merge(df3, df4, left_on="lkey", right_on="rkey")
    p_info(
        df1=df1,
        df2=df2,
        m1=m1,
        m2=m2,
        df3=df3,
        df4=df4,
        m3=m3,
        m4=pd.merge(df1, df2, how="outer"),
        m5=pd.merge(df3, df4, left_on="lkey", right_on="rkey", how="outer"),
    )
    df1 = pd.DataFrame(
        {
            "key": ["b", "b", "a", "c", "a", "b"],
            "data1": pd.Series(range(6), dtype="Int64"),
        }
    )
    df2 = pd.DataFrame(
        {"key": ["a", "b", "a", "b", "d"], "data2": pd.Series(range(5), dtype="Int64")}
    )

    m1 = pd.merge(df1, df2, on="key", how="left")

    p_info(df1=df1, df2=df2, m1=m1, m2=pd.merge(df1, df2, on="key", how="inner"))

    left = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar"],
            "key2": ["one", "two", "one"],
            "lval": pd.Series([1, 2, 3], dtype="Int64"),
        }
    )
    right = pd.DataFrame(
        {
            "key1": ["foo", "foo", "bar", "bar"],
            "key2": ["one", "one", "one", "two"],
            "rval": pd.Series([4, 5, 6, 7], dtype="Int64"),
        }
    )
    m1 = pd.merge(left, right, on=["key1", "key2"], how="outer")
    m2 = pd.merge(left, right, on="key1")
    m3 = pd.merge(left, right, on="key1", suffixes=("_left", "_right"))
    p_info(
        left=left,
        right=right,
        m1=m1,
        m2=m2,
        m3=m3,
    )


# 8.2.2 根据索引合并
def merging_on_index():
    print(f"{speter*2}merging_on_index{speter*2}")
    print(f"{speter*2}根据索引合并{speter*2}")
    left1 = pd.DataFrame(
        {
            "key": ["a", "b", "a", "a", "b", "c"],
            "value": pd.Series(range(6), dtype="Int64"),
        }
    )
    right1 = pd.DataFrame({"group_val": [3.5, 7]}, index=["a", "b"])

    m1 = pd.merge(left1, right1, left_on="key", right_index=True)
    m2 = pd.merge(left1, right1, left_on="key", right_index=True, how="outer")
    p_info(
        left1=left1,
        right1=right1,
        m1=m1,
        m2=m2,
    )
    lefth = pd.DataFrame(
        {
            "key1": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
            "key2": [2000, 2001, 2002, 2001, 2002],
            "data": pd.Series(range(5), dtype="Int64"),
        }
    )
    righth_index = pd.MultiIndex.from_arrays(
        [
            ["Nevada", "Nevada", "Ohio", "Ohio", "Ohio", "Ohio"],
            [2001, 2000, 2000, 2000, 2001, 2002],
        ]
    )
    righth = pd.DataFrame(
        {
            "event1": pd.Series([0, 2, 4, 6, 8, 10], dtype="Int64", index=righth_index),
            "event2": pd.Series([1, 3, 5, 7, 9, 11], dtype="Int64", index=righth_index),
        }
    )
    p_info(
        lefth=lefth,
        # righth_index=righth_index,
        righth=righth,
        m1=pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True),
        m2=pd.merge(
            lefth, righth, left_on=["key1", "key2"], right_index=True, how="outer"
        ),
    )

    left2 = pd.DataFrame(
        [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
        index=["a", "c", "e"],
        columns=["Ohio", "Nevada"],
    ).astype("Int64")
    right2 = pd.DataFrame(
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0], [13, 14]],
        index=["b", "c", "d", "e"],
        columns=["Missouri", "Alabama"],
    ).astype("Int64")
    p_info(
        left2=left2,
        right2=right2,
        m=pd.merge(left2, right2, how="outer", left_index=True, right_index=True),
        join=left2.join(right2, how="outer"),
        join1=left1.join(right1, on="key"),
    )
    another = pd.DataFrame(
        [[7.0, 8.0], [9.0, 10.0], [11.0, 12.0], [16.0, 17.0]],
        index=["a", "c", "e", "f"],
        columns=["New York", "Oregon"],
    )
    p_info(
        another=another,
        j1=left2.join([right2, another]),
        j2=left2.join([right2, another], how="outer"),
    )


# 8.2.3 沿轴向连接
def concatenating_along_axis():
    print(f"{speter*2}concatenating_along_axis{speter*2}")
    print(f"{speter*2}沿轴向连接{speter*2}")
    arr = np.arange(12).reshape((3, 4))

    s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")
    s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")
    s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")
    s4 = pd.concat([s1, s3])
    p_info(
        arr=arr,
        concatenate=np.concatenate([arr, arr], axis=1),
        concatenate1=np.concatenate([arr, arr], axis=0),
        s1=s1,
        s2=s2,
        s3=s3,
        concat=pd.concat([s1, s2, s3]),
        concat1=pd.concat([s1, s2, s3], axis=1),
        s4=s4,
        c1=pd.concat([s1, s4], axis="columns"),
        c2=pd.concat([s1, s4], axis="columns", join="inner"),
        c3=pd.concat([s1, s4], axis=1).reindex(["a", "c", "b", "e"]),
    )

    result = pd.concat([s1, s1, s3], keys=["one", "two", "three"])
    p_info(
        result=result,
        unstack=result.unstack(),
        c=pd.concat([s1, s2, s3], axis="columns", keys=["one", "two", "three"]),
    )

    df1 = pd.DataFrame(
        np.arange(6).reshape(3, 2), index=["a", "b", "c"], columns=["one", "two"]
    )

    df2 = pd.DataFrame(
        5 + np.arange(4).reshape(2, 2), index=["a", "c"], columns=["three", "four"]
    )
    p_info(
        df1=df1,
        df2=df2,
        c1=pd.concat([df1, df2], axis="columns", keys=["level1", "level2"]),
        c2=pd.concat({"level1": df1, "level2": df2}, axis="columns"),
        c3=pd.concat(
            [df1, df2],
            axis="columns",
            keys=["level1", "level2"],
            names=["upper", "lower"],
        ),
    )

    df1 = pd.DataFrame(np.random.standard_normal((3, 4)), columns=["a", "b", "c", "d"])
    df2 = pd.DataFrame(np.random.standard_normal((2, 3)), columns=["b", "d", "a"])
    p_info(
        df1=df1,
        df2=df2,
        c=pd.concat([df1, df2], ignore_index=True),
        c1=pd.concat([df1, df2]),
    )


# 8.2.4 联合重叠数据
def combining_overlapping_data():
    print(f"{speter*2}combining_overlapping_data{speter*2}")
    print(f"{speter*2}联合重叠数据{speter*2}")
    a = pd.Series(
        [np.nan, 2.5, 0.0, 3.5, 4.5, np.nan], index=["f", "e", "d", "c", "b", "a"]
    )
    b = pd.Series(
        [0.0, np.nan, 2.0, np.nan, np.nan, 5.0], index=["a", "b", "c", "d", "e", "f"]
    )
    p_info(
        a=a,
        b=b,
        isnull=np.where(pd.isna(a), b, a),
        c1=a.combine_first(b),
        c2=b.combine_first(a),
    )


# 8.3 重塑和透视


# 8.3.1 使用多层索引进行重塑
def reshaping_with_hierarchical_index():
    print(f"{speter*2}reshaping_with_hierarchical_index{speter*2}")
    print(f"{speter*2}使用多层索引进行重塑{speter*2}")

    data = pd.DataFrame(
        np.arange(6).reshape((2, 3)),
        index=pd.Index(["Ohio", "Colorado"], name="state"),
        columns=pd.Index(["one", "two", "three"], name="number"),
    )

    result = data.stack()
    p_info(
        data=data,
        result=result,
        unstack=result.unstack(),
        unstack1=result.unstack(level=0),
        unstack2=result.unstack(level="state"),
    )
    s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")

    s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")
    data2 = pd.concat([s1, s2], keys=["one", "two"])
    p_info(
        data2=data2,
        unstack1=data2.unstack(),
        unstack2=data2.unstack().stack(),
        # unstack3=data2.unstack().stack(dropna=False),
    )

    df = pd.DataFrame(
        {"left": result, "right": result + 5},
        columns=pd.Index(["left", "right"], name="side"),
    )
    p_info(
        df=df,
        unstack=df.unstack(level="state"),
        unstack1=df.unstack(level="state").stack(level="side"),
    )


# 8.3.2 将“长”透视为“宽”
def pivot_long_to_wide():
    print(f"{speter*2}pivot_long_to_wide{speter*2}")
    print(f"{speter*2}将长透视为宽{speter*2}")

    data = pd.read_csv(f"{base_dir}/examples/macrodata.csv")
    periods = pd.PeriodIndex(
        data.pop("year").astype(str) + "Q" + data.pop("quarter").astype(str),
        freq="Q",
        name="date",
    )
    columns = pd.Index(["realgdp", "infl", "unemp"], name="item")
    data = data.reindex(columns=columns)
    data.index = periods.to_timestamp("D")
    long_data = data.stack().reset_index().rename(columns={0: "value"})
    pivoted = long_data.pivot(index="date", columns="item", values="value")
    long_data["value2"] = np.random.standard_normal(len(long_data))
    pivoted = long_data.pivot(index="date", columns="item")
    unstacked = long_data.set_index(["date", "item"]).unstack(level="item")

    p_info(
        h=data.head(),
        periods=periods,
        long_data=long_data[:10],
        p=pivoted,
        ld=long_data[:10],
        ph1=pivoted.head(),
        ph2=pivoted["value"].head(),
        uh=unstacked.head(),
    )
    # data = data.loc[:, ["year", "quarter", "realgdp", "infl", "unemp"]]
    # p_info(
    #     h=data.head(),
    # )


# 8.3.3 将“宽”透视为“长”
def pivot_wide_to_long():
    print(f"{speter*2}pivot_wide_to_long{speter*2}")
    print(f"{speter*2}将宽透视为长{speter*2}")

    df = pd.DataFrame(
        {"key": ["foo", "bar", "baz"], "A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]}
    )

    melted = pd.melt(df, id_vars="key")
    reshaped = melted.pivot(index="key", columns="variable", values="value")
    p_info(
        df=df,
        melted=melted,
        reshaped=reshaped,
        reset_index=reshaped.reset_index(),
        melt=pd.melt(df, id_vars="key", value_vars=["A", "B"]),
        melt1=pd.melt(df, value_vars=["A", "B", "C"]),
        melt2=pd.melt(df, value_vars=["key", "A", "B"]),
    )


# 8.4 本章小结
def chapter_8_summary():
    print(f"{speter*2}chapter_8_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        pivot_wide_to_long()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
