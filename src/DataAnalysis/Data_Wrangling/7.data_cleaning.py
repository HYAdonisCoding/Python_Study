#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第7章 数据清洗与准备
# ================================

from pathlib import Path

base_dir = Path(__file__).parent


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

np.set_printoptions(linewidth=200)


# 7.1 处理缺失值
def handling_missing_data():
    print(f"{speter*2}handling_missing_data{speter*2}")
    print(f"{speter*2}处理缺失值{speter*2}")
    string_data = pd.Series(["aardvark", np.nan, None, "avocado"])

    float_data = pd.Series([1, 2, None], dtype="float64")

    p_info(
        string_data=string_data,
        string_data_na=string_data.isna(),
        float_data=float_data,
        float_data_na=float_data.isna(),
    )


from numpy import nan as NA


# 7.1.1 过滤缺失值
def filtering_missing_data():
    print(f"{speter*2}filtering_missing_data{speter*2}")
    print(f"{speter*2}过滤缺失值{speter*2}")

    data = pd.Series([1, NA, 3.5, NA, 7])
    p_info(dropna=data.dropna(), dropna_1=data[data.notnull()])

    data = pd.DataFrame(
        [
            [1.0, 6.5, 3.0],
            [1.0, np.nan, np.nan],
            [np.nan, np.nan, np.nan],
            [np.nan, 6.5, 3.0],
        ]
    )

    cleaned = data.dropna()
    p_info(
        data=data,
        cleaned=cleaned,
        cleaned_1=data.dropna(how="all"),
        cleaned_2=data.dropna(how="any"),
    )
    data[4] = NA
    p_info(
        data=data,
        cleaned=data.dropna(),
        cleaned_1=data.dropna(axis=1, how="all"),
    )

    df = pd.DataFrame(np.random.standard_normal((7, 3)))
    df.iloc[:4, 1] = np.nan
    df.iloc[:2, 2] = np.nan
    p_info(
        df=df,
        dropna=df.dropna(),
        dropna_1=df.dropna(thresh=2),
    )


# 7.1.2 补全缺失值
def filling_missing_data():
    print(f"{speter*2}filling_missing_data{speter*2}")
    print(f"{speter*2}补全缺失值{speter*2}")

    df = pd.DataFrame(np.random.standard_normal((7, 3)))
    df.iloc[:4, 1] = NA
    df.iloc[:2, 2] = NA
    p_info(
        df=df,
        df_fill=df.fillna(0),
        df_fill_1=df.fillna({1: 0.5, 2: 0}),
        df_fill_2=df.fillna(0, inplace=True),
    )
    p_info(
        title="inplace",
        df=df,
    )
    df = pd.DataFrame(np.random.standard_normal((6, 3)))
    # df.iloc[:2, 1] = NA
    # df.iloc[:4, 2] = NA
    df.iloc[2:4, 1] = NA
    df.iloc[1:5, 2] = NA
    p_info(
        df=df,
        ffill=df.ffill(),
        ffill1=df.ffill(limit=2),
    )
    data = pd.Series([1.0, np.nan, 3.5, np.nan, 7])
    p_info(fill_mean=data.fillna(data.mean()))


# 7.2 数据转换


# 7.2.1 删除重复值
def removing_duplicates():
    print(f"{speter*2}removing_duplicates{speter*2}")
    print(f"{speter*2}删除重复值{speter*2}")
    data = pd.DataFrame(
        {"k1": ["one", "two"] * 3 + ["two"], "k2": [1, 1, 2, 3, 3, 4, 4]}
    )
    p_info(
        data=data, duplicated=data.duplicated(), drop_duplicates=data.drop_duplicates()
    )
    data["v1"] = range(7)
    p_info(
        data=data,
        drop_duplicates_k1=data.drop_duplicates(subset=["k1"]),
        drop_duplicates_k2=data.drop_duplicates(["k1", "k2"], keep="last"),
    )


# 7.2.2 使用函数或映射进行数据转换
def data_transformation_with_function_mapping():
    print(f"{speter*2}data_transformation_with_function_mapping{speter*2}")
    print(f"{speter*2}使用函数或映射进行数据转换{speter*2}")

    data = pd.DataFrame(
        {
            "food": [
                "bacon",
                "pulled pork",
                "bacon",
                "pastrami",
                "corned beef",
                "bacon",
                "pastrami",
                "honey ham",
                "nova lox",
            ],
            "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6],
        }
    )

    meat_to_animal = {
        "bacon": "pig",
        "pulled pork": "pig",
        "pastrami": "cow",
        "corned beef": "cow",
        "honey ham": "pig",
        "nova lox": "salmon",
    }
    lowercased = data["food"].str.lower()
    p_info(data=data, meat_to_animal=meat_to_animal, lowercased=lowercased)
    data["animal"] = data["food"].map(meat_to_animal)
    p_info(data1=data, data2=data["food"].map(lambda x: meat_to_animal[x.lower()]))

    def get_animal(x):
        return meat_to_animal[x]

    p_info(data=data, food=data["food"].map(get_animal))


# 7.2.3 替代值
def replacing_values():
    print(f"{speter*2}replacing_values{speter*2}")
    print(f"{speter*2}替代值{speter*2}")
    data = pd.Series([1.0, -999.0, 2.0, -999.0, -1000.0, 3.0])
    p_info(
        data=data,
        data1=data.replace(-999, NA),
        data2=data.replace([-999, -1000], NA),
        data3=data.replace([-999, -1000], [NA, 0]),
        data4=data.replace({-999: NA, -1000: 0}),
    )


# 7.2.4 重命名轴索引
def renaming_axis_indexes():
    print(f"{speter*2}renaming_axis_indexes{speter*2}")
    print(f"{speter*2}重命名轴索引{speter*2}")
    data = pd.DataFrame(
        np.arange(12).reshape((3, 4)),
        index=["Ohio", "Colorado", "New York"],
        columns=["one", "two", "three", "four"],
    )

    def transform(x):
        return x[:4].upper()

    p_info(
        data=data,
        data_transform=data.index.map(transform),
    )
    data.index = data.index.map(transform)
    p_info(
        data=data,
        data1=data.rename(index=str.title, columns=str.upper),
        data2=data.rename(index={"OHIO": "INDIANA"}, columns={"three": "peekaboo"}),
    )
    data.rename(index={"OHIO": "INDIANA"}, inplace=True)
    p_info(
        data=data,
    )


# 7.2.5 离散化和分箱
def discretization_and_binning():
    print(f"{speter*2}discretization_and_binning{speter*2}")
    print(f"{speter*2}离散化和分箱{speter*2}")
    ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
    bins = [18, 25, 35, 60, 100]
    cats = pd.cut(ages, bins)

    group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]

    p_info(
        cats=cats,
        cats_codes=cats.codes,
        cats_categories=cats.categories,
        cnt=cats.value_counts(),
        cut=pd.cut(ages, [18, 26, 36, 61, 100], right=False),
        cut1=pd.cut(ages, bins, labels=group_names),
    )

    data = np.random.rand(20)
    p_info(data=data, cut=pd.cut(data, 4, precision=2))

    # 正态分布
    data = np.random.standard_normal(1000)
    quartiles = pd.qcut(data, 4, precision=2)
    p_info(
        正态分布data=data,
        quartiles=quartiles,
        cnt=quartiles.value_counts(),
        qcut=pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.0]),
    )


# 7.2.6 检测和过滤异常值
def detecting_and_filtering_outliers():
    print(f"{speter*2}detecting_and_filtering_outliers{speter*2}")
    print(f"{speter*2}检测和过滤异常值{speter*2}")
    data = pd.DataFrame(np.random.standard_normal((1000, 4)))
    col = data[2]
    p_info(
        data=data.describe(),
        _3=col[np.abs(col) > 3],
        all_3=data[(np.abs(data) > 3).any(axis=1)],
    )

    data[data.abs() > 3] = np.sign(data) * 3
    p_info(describe=data.describe(), sign=np.sign(data).head())


# 7.2.7 置換和随机抽样
def permutation_and_random_sampling():
    print(f"{speter*2}permutation_and_random_sampling{speter*2}")
    print(f"{speter*2}置換和随机抽样{speter*2}")
    df = pd.DataFrame(np.arange(5 * 4).reshape((5, 4)))

    sampler = np.random.permutation(5)
    p_info(df=df, sampler=sampler, take=df.take(sampler), s1=df.sample(n=3))

    choices = pd.Series([5, 7, -1, 6, 4])
    draws = choices.sample(n=10, replace=True)
    p_info(choices=choices, draws=draws)


# 7.2.8 计算指标/虚拟变量
def computing_indicators_dummy_variables():
    print(f"{speter*2}computing_indicators_dummy_variables{speter*2}")
    print(f"{speter*2}计算指标/虚拟变量{speter*2}")
    df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"], "data1": range(6)})
    dummies = pd.get_dummies(df["key"], prefix="key", dtype=float)
    df_with_dummy = df[["data1"]].join(dummies)
    p_info(
        df=df,
        get_dummies=pd.get_dummies(df["key"], dtype=float),
        get_dummies1=pd.get_dummies(df["key"]),
        df_with_dummy=df_with_dummy,
    )
    mnames = ["movie_id", "title", "genres"]
    movies = pd.read_table(
        f"{base_dir}/datasets/movielens/movies.dat",
        sep="::",
        header=None,
        names=mnames,
        engine="python",
    )
    p_info(movies=movies, movies1=movies[:10])

    all_genres = []
    for x in movies.genres:
        all_genres.extend(x.split("|"))
    genres = pd.unique(pd.Series(all_genres))
    p_info(genres=genres)

    zero_matrix = np.zeros((len(movies), len(genres)))
    dummies = pd.DataFrame(zero_matrix, columns=genres)
    gen = movies.genres[0]
    p_info(
        zero_matrix=zero_matrix,
        dummies=dummies,
        gen=gen,
        gen1=gen.split("|"),
        idx=dummies.columns.get_indexer(gen.split("|")),
    )
    for i, gen in enumerate(movies.genres):
        indices = dummies.columns.get_indexer(gen.split("|"))
        dummies.iloc[i, indices] = 1
    movies_windic = movies.join(dummies.add_prefix("Genre_"))
    p_info(
        movies_windic=movies_windic.iloc[0],
        type=type(movies_windic),
        shape=movies_windic.shape,
        data=movies_windic.head().to_string(),
    )

    np.random.rand(12345)
    values = np.random.rand(10)
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1]

    p_info(values=values, b=pd.get_dummies(pd.cut(values, bins)))


# 7.3 字符串操作


# 7.3.1 字符串对象方法
def string_object_methods():
    print(f"{speter*2}string_object_methods{speter*2}")
    print(f"{speter*2}字符串对象方法{speter*2}")

    val = "a,b,  guido"
    pieces = [x.strip() for x in val.split(",")]
    first, second, third = pieces
    result = first + "::" + second + "::" + third
    result1 = "::".join(pieces)
    p_info(
        val=val,
        val1=val.split(","),
        pieces=pieces,
        result=result,
        result1=result1,
        in_="guido" in val,
        idx=val.index(","),
        find=val.find(":"),
        # index=val.index(":"),
        cnt=val.count(","),
        replace=val.replace(",", "::"),
        replace1=val.replace(",", ""),
    )


import re


# 7.3.2 正则表达式
def regular_expressions():
    print(f"{speter*2}regular_expressions{speter*2}")
    print(f"{speter*2}正则表达式{speter*2}")

    text = "foo    bar\t baz  \tqux"
    regex = re.compile(r"\s+")

    p_info(
        text=text,
        spl=re.split(
            r"\s+",
            text,
        ),
        reg=regex.split(text),
        reg_all=regex.findall(text),
    )
    text = """Dave dave@google.com
    Steve steve@gmail.com
    Rob rob@gmail.com
    Ryan ryan@yahoo.com"""
    pattern = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"

    # re.IGNORECASE makes the regex case insensitive
    regex = re.compile(pattern, flags=re.IGNORECASE)

    m = regex.search(text)

    p_info(
        text=text,
        regex=regex,
        regex_all=regex.findall(text),
        m=m,
        m_1=text[m.start() : m.end()],
        reg=regex.match(text),
        sub=regex.sub("REDACTED", text),
    )
    pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"
    regex = re.compile(pattern, flags=re.IGNORECASE)
    m = regex.match("wesm@bright.net")
    p_info(
        m=m,
        m1=m.groups(),
        all=regex.findall(text),
        reg=regex.sub(r"Username: \1, Domain: \2, Suffix: \3", text),
    )


# 7.3.3 pandas 中的向量化字符串函数
def pandas_vectorized_string_functions():
    print(f"{speter*2}pandas_vectorized_string_functions{speter*2}")
    print(f"{speter*2}pandas 中的向量化字符串函数{speter*2}")
    data = {
        "Dave": "dave@google.com",
        "Steve": "steve@gmail.com",
        "Rob": "rob@gmail.com",
        "Wes": NA,
    }
    data1 = pd.Series(data)
    pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"

    matches = data1.str.findall(pattern, flags=re.IGNORECASE).str[0]

    p_info(
        data=data,
        data1=data1,
        is_null=data1.isnull(),
        contains=data1.str.contains("gmail"),
        pattern=pattern,
        find_all=data1.str.findall(pattern, flags=re.IGNORECASE),
        matches=matches,
        matches1=matches.str.get(1),
        matches0=matches.str.get(0),
        data5=data1.str[:5],
    )


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        pandas_vectorized_string_functions()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
