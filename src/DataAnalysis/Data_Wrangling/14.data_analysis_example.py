#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# ================================
# 第14章 数据分析示例
# ================================
from pathlib import Path

base_dir = Path(__file__).parent


from debug import p_info


import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import json

np.set_printoptions(linewidth=200)

path = f"{base_dir}/datasets/bitly_usagov/example.txt"


def test():
    print(f"{speter*2}test{speter*2}")
    path = f"{base_dir}/examples/segismundo.txt"


# 读取 Bitly USA.gov 访问日志数据
# 每一行是一个 JSON 对象，解析后得到 list[dict] 结构
# 将 Bitly 日志文件逐行读取
# 每一行都是一个 JSON 字符串，转换后成为 Python 字典
# 最终 records 的结构为 list[dict]，便于后续 pandas 分析
with open(path) as f:
    records = [json.loads(line) for line in f]


# 14.1 从 Bitly 获取 1.USA.gov 数据
def bitly_usagov_data():
    print(f"{speter*2}bitly_usagov_data{speter*2}")
    print(f"{speter*2}从 Bitly 获取 1.USA.gov 数据{speter*2}")

    p_info(readline=open(path).readline(), records=records[0])


# 14.1.1 纯 Python 时区计数
def timezone_counting_with_pure_python():
    print(f"{speter*2}timezone_counting_with_pure_python{speter*2}")
    print(f"{speter*2}纯 Python 时区计数{speter*2}")

    # 使用原生 Python 完成数据统计：
    # 1. 提取时区字段
    # 2. 统计每个时区出现次数
    # 3. 找出访问量最高的时区

    # time_zones = [rec["tz"] for rec in records]
    # p_info(time_zones=time_zones[:10])

    # 原始数据存在缺失字段，使用条件过滤避免 KeyError
    # tz 表示用户所在时区
    time_zones = [rec["tz"] for rec in records if "tz" in rec]

    p_info(time_zones1=time_zones[:10])

    # 使用普通 Python 字典统计每个元素出现次数
    # 这里展示手写计数逻辑，理解底层统计过程
    def get_counts(sequence):
        counts = {}
        for x in sequence:
            if x in counts:
                counts[x] += 1
            else:
                counts[x] = 1
        return counts

    from collections import defaultdict

    # defaultdict(int) 可以自动初始化不存在的 key
    # 相比普通 dict 写法更加简洁
    def get_counts2(sequence):
        counts = defaultdict(int)  # values will initialize to 0
        for x in sequence:
            counts[x] += 1
        return counts

    counts = get_counts(time_zones)

    p_info(
        counts=counts,
        ny=counts["America/New_York"],
        len=len(time_zones),
    )

    def top_counts(count_dict, n=10):
        value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
        value_key_pairs.sort()
        return value_key_pairs[-n:]

    p_info(top10=top_counts(counts, n=10))
    from collections import Counter

    # collections.Counter 是 Python 标准库提供的高级计数工具
    # 常用于词频、类别统计等场景
    counts = Counter(time_zones)
    p_info(most_common_10=counts.most_common(10))


# 14.1.2 使用 pandas 进行时区计数
def timezone_counting_with_pandas():
    print(f"{speter*2}timezone_counting_with_pandas{speter*2}")
    print(f"{speter*2}使用 pandas 进行时区计数{speter*2}")

    # pandas 分析流程：
    # list[dict] -> DataFrame -> 数据清洗 -> 聚合统计 -> 可视化
    # 将 list[dict] 转换为 DataFrame
    # pandas 后续可以直接进行缺失值处理、分组统计和可视化
    frame = pd.DataFrame(records)
    p_info(
        frame_info=frame.info(),
        tz_head1=frame["tz"].head(),
    )
    tz_counts = frame["tz"].value_counts()

    p_info(tz_head2=tz_counts.head(10))
    # 处理缺失时区数据：
    # NaN 表示缺失，空字符串表示未知，需要统一处理
    clean_tz = frame["tz"].fillna("Missing")
    clean_tz[clean_tz == ""] = "Unknown"
    tz_counts = clean_tz.value_counts()
    p_info(tz_head3=tz_counts.head(10))

    plt.figure(figsize=(10, 4))
    import seaborn as sns

    subset = tz_counts.head(10)
    sns.barplot(y=subset.index, x=subset.to_numpy())
    # plt.show()
    p_info(
        frame1=frame["a"][1],
        frame50=frame["a"][50],
        frame51=frame["a"][51][:50],
    )

    # 从 User-Agent 字段提取浏览器信息
    # 通过字符串处理分析访问来源特征
    results = pd.Series([x.split()[0] for x in frame["a"].dropna()])
    p_info(
        results_head5=results.head(5),
        results_value_counts=results.value_counts().head(8),
    )

    cframe = frame[frame["a"].notna()].copy()
    # 根据 User-Agent 判断用户操作系统
    # np.where 类似 SQL 中的 CASE WHEN
    cframe["os"] = np.where(
        cframe["a"].str.contains("Windows"), "Windows", "Not Windows"
    )
    p_info(cframe_os_head5=cframe["os"].head(5))

    # 按时区和操作系统进行分组统计
    # groupby 是 pandas 数据分析中最核心的聚合操作之一
    # 按时区和操作系统两个维度分组
    # 用于分析不同地区用户访问来源的差异
    by_tz_os = cframe.groupby(["tz", "os"])
    # size() 统计每个分组数量
    # unstack() 将层级索引转换为二维表，方便分析和绘图
    agg_counts = by_tz_os.size().unstack().fillna(0)
    p_info(agg_counts_head=agg_counts.head(10))

    # 计算每个时区总访问量，并按照数量排序
    # argsort 返回排序后的索引位置
    # indexer = agg_counts.sum("columns").argsort()
    indexer = agg_counts.sum(axis="columns").argsort()
    p_info(indexer_values=indexer.values[:10])
    count_subset = agg_counts.take(indexer[-10:])
    p_info(
        count_subset=count_subset,
        top_tz=agg_counts.sum(axis="columns").nlargest(10),
    )
    count_subset = count_subset.stack()
    count_subset.name = "total"
    count_subset = count_subset.reset_index()
    p_info(
        count_subset=count_subset.head(10),
    )
    sns.barplot(x="total", y="tz", hue="os", data=count_subset)

    def norm_total(group):
        group["normed_total"] = group["total"] / group["total"].sum()
        return group

    results = count_subset.groupby("tz").apply(norm_total)
    plt.figure()

    sns.barplot(x="normed_total", y="tz", hue="os", data=results)

    g = count_subset.groupby("tz")
    results2 = count_subset["total"] / g["total"].transform("sum")
    plt.show()


# 14.2 MovieLens 1M 数据集
def movielens_1m_dataset():
    print(f"{speter*2}movielens_1m_dataset{speter*2}")
    print(f"{speter*2}MovieLens 1M 数据集{speter*2}")

    unames = ["user_id", "gender", "age", "occupation", "zip"]
    users = pd.read_table(
        f"{base_dir}/datasets/movielens/users.dat",
        sep="::",
        header=None,
        names=unames,
        engine="python",
    )

    rnames = ["user_id", "movie_id", "rating", "timestamp"]
    ratings = pd.read_table(
        f"{base_dir}/datasets/movielens/ratings.dat",
        sep="::",
        header=None,
        names=rnames,
        engine="python",
    )

    mnames = ["movie_id", "title", "genres"]
    movies = pd.read_table(
        f"{base_dir}/datasets/movielens/movies.dat",
        sep="::",
        header=None,
        names=mnames,
        engine="python",
    )
    p_info(users=users.head(5), ratings=ratings.head(5), movies=movies.head(5))
    data = pd.merge(pd.merge(ratings, users), movies)
    p_info(
        data=data,
        data_iloc_0=data.iloc[0],
    )
    mean_ratings = data.pivot_table(
        "rating", index="title", columns="gender", aggfunc="mean"
    )

    ratings_by_title = data.groupby("title").size()

    active_titles = ratings_by_title.index[ratings_by_title >= 250]

    p_info(
        mean_ratings=mean_ratings.head(5),
        ratings_by_title=ratings_by_title.head(10),
        active_titles=active_titles,
    )
    mean_ratings = mean_ratings.loc[active_titles]
    p_info(mean_ratings1=mean_ratings)
    top_female_ratings = mean_ratings.sort_values("F", ascending=False)
    p_info(top_female_ratings=top_female_ratings.head())

    # 14.2.1 测量评价分歧
    print(f"{speter*2}measurement_of_rating_disagreement{speter*2}")
    print(f"{speter*2}测量评价分歧{speter*2}")
    mean_ratings["diff"] = mean_ratings["M"] - mean_ratings["F"]
    p_info(mean_ratings_with_diff=mean_ratings)
    sorted_by_diff = mean_ratings.sort_values("diff")
    p_info(
        sorted_by_diff=sorted_by_diff.head(10),
        sort_values1=sorted_by_diff[::-1][:10],
    )

    rating_std_by_title = data.groupby("title")["rating"].std()
    rating_std_by_title = rating_std_by_title.loc[active_titles]
    p_info(
        rating_std_by_title=rating_std_by_title.head(),
        rating_std_by_title1=rating_std_by_title.sort_values(ascending=False)[:10],
    )


# 14.3 美国1880～2010年的婴儿名字
def us_baby_names_1880_2010():
    print(f"{speter*2}us_baby_names_1880_2010{speter*2}")
    print(f"{speter*2}美国1880～2010年的婴儿名字{speter*2}")

    names1880 = pd.read_csv(
        f"{base_dir}/datasets/babynames/yob1880.txt", names=["name", "sex", "births"]
    )
    p_info(
        names1880=names1880,
        total_births_by_sex=names1880.groupby("sex")["births"].sum(),
    )

    pieces = []
    for year in range(1880, 2011):
        path = f"{base_dir}/datasets/babynames/yob{year}.txt"
        frame = pd.read_csv(path, names=["name", "sex", "births"])

        # Add a column for the year
        frame["year"] = year
        pieces.append(frame)

    # Concatenate all the frames
    # 合并 1880-2010 年所有婴儿名字数据
    # ignore_index=True 会重新生成连续整数索引
    names = pd.concat(pieces, ignore_index=True)
    p_info(names=names)
    total_births = names.pivot_table("births", index="year", columns="sex", aggfunc=sum)
    p_info(total_births__tail=total_births.tail())
    total_births.plot(title="Total births by sex and year")
    # plt.show()

    def add_prop(group):
        group["prop"] = group["births"] / group["births"].sum()
        return group

    # names = names.groupby(["year", "sex"], group_keys=False).apply(add_prop)
    # 计算名字占同年份同性别出生人口的比例
    # prop 越大，说明该名字在该年份越流行
    # transform 保持原 DataFrame 行数，方便新增列
    names["prop"] = names["births"] / names.groupby(["year", "sex"])[
        "births"
    ].transform("sum")
    p_info(names_columns=names.columns)
    p_info(
        names1=names,
        groupby=names.groupby(["year", "sex"])["prop"].sum(),
    )

    def get_top1000(group):
        return group.sort_values("births", ascending=False)[:1000]

    grouped = names.groupby(["year", "sex"])
    top1000 = grouped.apply(get_top1000)
    # top1000.reset_index(inplace=True, drop=True)
    top1000.reset_index(drop=True)
    top1000 = top1000.reset_index()
    pieces = []
    for year, group in top1000.groupby(["year", "sex"]):
        pieces.append(group.sort_values("births", ascending=False)[:1000])
    top1000 = pd.concat(pieces, ignore_index=True)
    p_info(top1000=top1000)

    # 14.3.1 分析名字趋势
    print(f"{speter*2}analyzing_name_trends{speter*2}")
    print(f"{speter*2}分析名字趋势{speter*2}")

    boys = top1000[top1000["sex"] == "M"]
    girls = top1000[top1000["sex"] == "F"]

    total_births = top1000.pivot_table(
        "births", index="year", columns="name", aggfunc=sum
    )

    total_births.info()
    subset = total_births[["John", "Harry", "Mary", "Marilyn"]]
    subset.plot(subplots=True, figsize=(12, 10), title="Number of births per year")

    # plt.show()

    table = top1000.pivot_table("prop", index="year", columns="sex", aggfunc=sum)
    table.plot(
        title="Sum of table1000.prop by year and sex", yticks=np.linspace(0, 1.2, 13)
    )
    # plt.show()
    df = boys[boys["year"] == 2010]
    p_info(df=df)
    prop_cumsum = df["prop"].sort_values(ascending=False).cumsum()
    p_info(
        prop_cumsum=prop_cumsum[:10],
        prop_cumsum_searchsorted=prop_cumsum.searchsorted(0.5),
    )

    df = boys[boys.year == 1900]
    in1900 = df.sort_values("prop", ascending=False).prop.cumsum()
    p_info(searchsorted=in1900.searchsorted(0.5) + 1)

    def get_quantile_count(group, q=0.5):
        group = group.sort_values("prop", ascending=False)
        return group.prop.cumsum().searchsorted(q) + 1

    diversity = top1000.groupby(["year", "sex"]).apply(get_quantile_count)
    diversity = diversity.unstack()
    fig = plt.figure()

    p_info(diversity_head=diversity.head())
    diversity.plot(title="Number of popular names in top 50%")
    # plt.show()

    def get_last_letter(x):
        return x[-1]

    last_letters = names["name"].map(get_last_letter)
    last_letters.name = "last_letter"

    table = names.pivot_table(
        "births", index=last_letters, columns=["sex", "year"], aggfunc=sum
    )

    subtable = table.reindex(columns=[1910, 1960, 2010], level="year")

    p_info(
        subtable_head=subtable.head(),
        sum=subtable.sum(),
    )
    letter_prop = subtable / subtable.sum()
    p_info(letter_prop=letter_prop)

    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    letter_prop["M"].plot(kind="bar", rot=0, ax=axes[0], title="Male")
    letter_prop["F"].plot(kind="bar", rot=0, ax=axes[1], title="Female", legend=False)
    plt.subplots_adjust(hspace=0.25)
    plt.show()
    letter_prop = table / table.sum()

    dny_ts = letter_prop.loc[["d", "n", "y"], "M"].T
    p_info(dny_ts=dny_ts.head())
    # plt.close("all")
    fig = plt.figure()
    dny_ts.plot()
    # plt.show()

    all_names = pd.Series(top1000["name"].unique())
    lesley_like = all_names[all_names.str.contains("Lesl")]
    p_info(lesley_like=lesley_like)

    filtered = top1000[top1000["name"].isin(lesley_like)]
    p_info(filtered_sum=filtered.groupby("name")["births"].sum())
    table = filtered.pivot_table("births", index="year", columns="sex", aggfunc="sum")
    table = table.div(table.sum(axis="columns"), axis="index")
    p_info(table_tail=table.tail())

    fig = plt.figure()
    table.plot(style={"M": "k-", "F": "k--"})
    plt.show()


# 14.4 美国农业部食品数据库
def usda_food_database():
    print(f"{speter*2}usda_food_database{speter*2}")
    print(f"{speter*2}美国农业部食品数据库{speter*2}")
    # 分析美国农业部食品数据库 USDA Food Database
    # 包含食品分类、营养成分、生产商等结构化信息
    db = json.load(open(f"{base_dir}/datasets/usda_food/database.json"))
    p_info(
        len_db=len(db),
        keys=db[0].keys(),
        nutrients=db[0]["nutrients"][0],
    )
    nutrients = pd.DataFrame(db[0]["nutrients"])
    p_info(nutrients_head=nutrients.head(7))
    info_keys = ["description", "group", "id", "manufacturer"]
    info = pd.DataFrame(db, columns=info_keys)
    info.info()
    p_info(
        info_head=info.head(),
        info_description=info.describe(),
        group=info["group"].value_counts()[:10],
    )
    nutrients = []

    for rec in db:
        fnuts = pd.DataFrame(rec["nutrients"])
        fnuts["id"] = rec["id"]
        nutrients.append(fnuts)

    nutrients = pd.concat(nutrients, ignore_index=True)
    p_info(nutrients=nutrients)
    p_info(nutrients_sum=nutrients.duplicated().sum())  # number of duplicates
    nutrients = nutrients.drop_duplicates()
    p_info(nutrients1=nutrients)
    col_mapping = {"description": "food", "group": "fgroup"}
    info = info.rename(columns=col_mapping, copy=False)
    info.info()
    col_mapping = {"description": "nutrient", "group": "nutgroup"}
    nutrients = nutrients.rename(columns=col_mapping, copy=False)
    p_info(nutrients2=nutrients)
    # 将营养成分表和食品基本信息按照食品 id 合并
    # 形成完整的数据分析表
    ndata = pd.merge(nutrients, info, on="id", how="outer")
    ndata.info()
    p_info(ndata_describe=ndata.describe(), ndata_30000=ndata.iloc[30000])

    fig = plt.figure()
    result = ndata.groupby(["nutrient", "fgroup"])["value"].quantile(0.5)
    result["Zinc, Zn"].sort_values().plot(kind="barh")
    # plt.show()
    by_nutrient = ndata.groupby(["nutgroup", "nutrient"])

    def get_maximum(x):
        return x.loc[x.value.idxmax()]

    max_foods = by_nutrient.apply(get_maximum)[["value", "food"]]

    # make the food a little smaller
    max_foods["food"] = max_foods["food"].str[:50]
    p_info(max_foods=max_foods.loc["Amino Acids"]["food"])


# 14.5 2012年联邦选举委员会数据库
def fec_2012_election_database():
    print(f"{speter*2}fec_2012_election_database{speter*2}")
    print(f"{speter*2}2012年联邦选举委员会数据库{speter*2}")

    fec = pd.read_csv(f"{base_dir}/datasets/fec/P00000001-ALL.csv", low_memory=False)
    fec.info()
    p_info(fec_iloc=fec.iloc[123456])
    unique_cands = fec["cand_nm"].unique()
    p_info(unique_cands=unique_cands, unique_cands_2=unique_cands[2])
    parties = {
        "Bachmann, Michelle": "Republican",
        "Cain, Herman": "Republican",
        "Gingrich, Newt": "Republican",
        "Huntsman, Jon": "Republican",
        "Johnson, Gary Earl": "Republican",
        "McCotter, Thaddeus G": "Republican",
        "Obama, Barack": "Democrat",
        "Paul, Ron": "Republican",
        "Pawlenty, Timothy": "Republican",
        "Perry, Rick": "Republican",
        "Roemer, Charles E. 'Buddy' III": "Republican",
        "Romney, Mitt": "Republican",
        "Santorum, Rick": "Republican",
    }
    p_info(
        cand_nm_123456_123460=fec["cand_nm"][123456:123461],
        party_123456_123460=fec["cand_nm"][123456:123461].map(parties),
    )
    # Add it as a column
    fec["party"] = fec["cand_nm"].map(parties)
    p_info(
        fec_party=fec["party"].value_counts(),
        fec_contb_receipt_amt_positive=(fec["contb_receipt_amt"] > 0).value_counts(),
    )

    fec = fec[fec["contb_receipt_amt"] > 0]
    fec_mrbo = fec[fec["cand_nm"].isin(["Obama, Barack", "Romney, Mitt"])]

    # 14.5.1 按职业和雇主的捐献统计
    print(f"{speter*2}donations_by_occupation_and_employer{speter*2}")
    print(f"{speter*2}按职业和雇主的捐献统计{speter*2}")
    p_info(fec_contbr_occupation=fec["contbr_occupation"].value_counts()[:10])

    occ_mapping = {
        "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
        "INFORMATION REQUESTED": "NOT PROVIDED",
        "INFORMATION REQUESTED (BEST EFFORTS)": "NOT PROVIDED",
        "C.E.O.": "CEO",
    }

    def get_occ(x):
        # If no mapping provided, return x
        return occ_mapping.get(x, x)

    fec["contbr_occupation"] = fec["contbr_occupation"].map(get_occ)
    emp_mapping = {
        "INFORMATION REQUESTED PER BEST EFFORTS": "NOT PROVIDED",
        "INFORMATION REQUESTED": "NOT PROVIDED",
        "SELF": "SELF-EMPLOYED",
        "SELF EMPLOYED": "SELF-EMPLOYED",
    }

    def get_emp(x):
        # If no mapping provided, return x
        return emp_mapping.get(x, x)

    fec["contbr_employer"] = fec["contbr_employer"].map(get_emp)

    by_occupation = fec.pivot_table(
        "contb_receipt_amt", index="contbr_occupation", columns="party", aggfunc="sum"
    )
    over_2mm = by_occupation[by_occupation.sum(axis="columns") > 2000000]
    p_info(over_2mm=over_2mm)
    plt.figure()
    over_2mm.plot(kind="barh")
    plt.title("Donations by Occupation")
    plt.xlabel("Total Donations")
    plt.ylabel("Occupation")

    # plt.show()
    def get_top_amounts(group, key, n=5):
        totals = group.groupby(key)["contb_receipt_amt"].sum()
        return totals.nlargest(n)

    grouped = fec_mrbo.groupby("cand_nm")
    p_info(
        contbr_occupation=grouped.apply(get_top_amounts, "contbr_occupation", n=7),
        contbr_employer=grouped.apply(get_top_amounts, "contbr_employer", n=10),
    )

    # 14.5.2 捐赠金额分桶
    print(f"{speter*2}donation_amount_binning{speter*2}")
    print(f"{speter*2}捐赠金额分桶{speter*2}")
    bins = np.array([0, 1, 10, 100, 1000, 10000, 100_000, 1_000_000, 10_000_000])
    labels = pd.cut(fec_mrbo["contb_receipt_amt"], bins)
    p_info(labels=labels)
    grouped = fec_mrbo.groupby(["cand_nm", labels])
    p_info(grouped=grouped.size().unstack(level=0))
    plt.figure()
    bucket_sums = grouped["contb_receipt_amt"].sum().unstack(level=0)
    normed_sums = bucket_sums.div(bucket_sums.sum(axis="columns"), axis="index")
    p_info(normed_sums=normed_sums)
    normed_sums[:-2].plot(kind="barh")
    plt.title("Normalized Donations by Bucket")
    plt.xlabel("Total Donations")
    plt.ylabel("Bucket")
    # plt.show()

    # 14.5.3 按州进行捐赠统计
    print(f"{speter*2}donation_statistics_by_state{speter*2}")
    print(f"{speter*2}按州进行捐赠统计{speter*2}")
    # Get donation statistics by state
    grouped = fec_mrbo.groupby(["cand_nm", "contbr_st"])
    totals = grouped["contb_receipt_amt"].sum().unstack(level=0).fillna(0)
    totals = totals[totals.sum(axis="columns") > 100000]
    p_info(totals=totals.head(10))
    percent = totals.div(totals.sum(axis="columns"), axis="index")
    p_info(percent=percent.head(10))


# 14.6 本章小结
def chapter_14_summary():
    print(f"{speter*2}chapter_14_summary{speter*2}")
    print(f"{speter*2}本章小结{speter*2}")


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        fec_2012_election_database()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
