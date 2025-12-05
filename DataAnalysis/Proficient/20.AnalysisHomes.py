#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd



speter = "-" * 10

# 第四篇
# 20 分析在售二手房数据 Analyzing data on existing homes for sale

# * 分析主页面
# 打开首页https://bj.lianjia.com/ershoufang/pg1/
# <li class="clear LOGCLICKDATA" data-lj_view_evtid="21625" data-lj_evtid="21624" data-lj_view_event="ItemExpo" data-lj_click_event="SearchClick" data-lj_action_source_type="链家_PC_二手列表页卡片" data-lj_action_click_position="0" data-lj_action_fb_expo_id="1045648294921654273" data-lj_action_fb_query_id="1045648294141513728" data-lj_action_resblock_id="1111027377528" data-lj_action_housedel_id="101133895297"><a class="noresultRecommend img LOGCLICKDATA" href="https://bj.lianjia.com/ershoufang/101133895297.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="101133895297" data-is_focus="" data-sl=""><!-- 热推标签、埋点 --><img src="https://s1.ljcdn.com/feroot/pc/asset/img/vr/vrlogo.png?_v=2025112415183059" class="vr_item"><img class="lj-lazy" src="https://image1.ljcdn.com/110000-inspection/pc1_oqXZjdJKI.jpg.296x216.jpg" data-original="https://image1.ljcdn.com/110000-inspection/pc1_oqXZjdJKI.jpg.296x216.jpg" alt="金隅丽港06年小区 人车分流 满五唯一、精致一居室" style="display: block;"></a><div class="info clear"><div class="title"><a class="" href="https://bj.lianjia.com/ershoufang/101133895297.html" target="_blank" data-log_index="1" data-el="ershoufang" data-housecode="101133895297" data-is_focus="" data-sl="">金隅丽港06年小区 人车分流 满五唯一、精致一居室</a><!-- 拆分标签 只留一个优先级最高的标签--><span class="goodhouse_tag tagBlock">必看好房</span></div><div class="flood"><div class="positionInfo"><span class="positionIcon"></span><a href="https://bj.lianjia.com/xiaoqu/1111027377528/" target="_blank" data-log_index="1" data-el="region">金隅丽港城 </a>   -  <a href="https://bj.lianjia.com/ershoufang/wangjing/" target="_blank">望京</a> </div></div><div class="address"><div class="houseInfo"><span class="houseIcon"></span>1室1厅 | 54.8平米 | 东 | 简装 | 低楼层(共26层) | 2004年 | 塔楼</div></div><div class="followInfo"><span class="starIcon"></span>11人关注 / 31天以前发布</div><div class="tag"><span class="subway">近地铁</span><span class="vr">VR房源</span><span class="five">房本满两年</span></div><div class="priceInfo"><div class="totalPrice totalPrice2"><i> </i><span class="">255</span><i>万</i></div><div class="unitPrice" data-hid="101133895297" data-rid="1111027377528" data-price="46533"><span>46,533元/平</span></div></div></div><div class="listButtonContainer"><div class="btn-follow followBtn" data-hid="101133895297"><span class="follow-text">关注</span></div><div class="compareBtn LOGCLICK" data-hid="101133895297" log-mod="101133895297" data-log_evtid="10230">加入对比</div></div></li>
# * 分析详情页
# 
# 筛选离地铁近的房源
def filter_listings_near_subway_stations():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )

    db_path = "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/lianjia_spider/db/lianjia.db"

    # 读取 house_details 表（包含 tags）
    df_detail = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "house_details")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )

    # 读取 houses 表（基础字段）
    df_houses = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "houses")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )

    # 1. 从 house_details 筛选出包含“地铁”的房源
    metro_ids = df_detail.filter(df_detail.tags.like("%地铁%")).select("house_id")

    # 2. 与 houses 表进行 JOIN
    metro_house = (
        metro_ids.join(df_houses, on="house_id", how="inner")
        .select(
            "house_id",
            "region",
            "community_name",
            "total_price",
            "unit_price"
        )
    )
    metro_house = metro_house.orderBy(
        col("region").asc(),
        col("unit_price").desc()
    )
    metro_house.show(50, truncate=False)
    
# 分析各区域在售房源占比
def analyze_the_percentage_of_listings_for_sale_in_each_area():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )

    db_path = "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/lianjia_spider/db/lianjia.db"


    # 读取 houses 表（基础字段）
    df_houses = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "houses")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )


    df_houses.createOrReplaceTempView("temp")

    some_fruit = spark.sql("SELECT region,count(1) as count FROM temp group by region ")
    result_pdf = some_fruit.toPandas()

    # 将数据转换为Pandas数据帧
    # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
    # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    plt.pie(result_pdf["count"], labels=result_pdf["region"], shadow=True, autopct='%1.1f%%')
    plt.legend()
    plt.show()
    
# 分析在售房源的户型
def analyze_the_unit_types_of_listings_for_sale():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )

    db_path = "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/lianjia_spider/db/lianjia.db"

    # 读取 house_details 表（包含 tags）
    df_detail = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "house_details")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )




    df_detail.createOrReplaceTempView("temp")

    mongodb_group_df = spark.sql("SELECT house_type,count(1) as counter  FROM temp group by house_type ")

    df = mongodb_group_df.toPandas()
    df.sort_values("counter", inplace=True, ascending=False)
    df.reset_index(inplace=True)

    # 将数据转换为Pandas数据帧
    # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
    # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    
    

    

    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    ax.vlines(x=df.index, ymin=0, ymax=df.counter, color="firebrick", alpha=0.7, linewidth=2)
    ax.scatter(x=df.index, y=df.counter, s=75, color="firebrick", alpha=0.7)

    ax.set_title("在售房源户型", fontdict={"size": 22})
    ax.set_ylabel("在售数量")
    ax.set_xticks(df.index)
    ax.set_xticklabels(df.house_type, rotation=60,
                    fontdict={"horizontalalignment": "right", "size": 12})
    for row in df.itertuples():
        ax.text(row.Index, row.counter + .5, s=round(row.counter, 2),
                horizontalalignment="center", verticalalignment="bottom",
                fontsize=14)

    plt.show()
# 分析房龄和平米单价的关系
def analyze_the_relationship_between_building_age_and_price_per_square_meter():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )

    db_path = "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/lianjia_spider/db/lianjia.db"


    # 读取 houses 表（基础字段）
    df_houses = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "houses")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )


    df_houses.createOrReplaceTempView("temp")

    current_year = 2025
    df_year_built = spark.sql(f"""
        SELECT
            CAST(REPLACE(year_built, '年', '') AS INT) AS year_built_clean,
            CAST({current_year} - CAST(REPLACE(year_built, '年', '') AS INT) AS INT) AS house_age,
            AVG(unit_price) AS avg_unit_price
        FROM temp
        WHERE 
            year_built IS NOT NULL
            AND REPLACE(year_built, '年', '') REGEXP '^[0-9]{{4}}$'
            AND CAST(REPLACE(year_built, '年', '') AS INT) BETWEEN 1900 AND {current_year}
        GROUP BY year_built_clean
        ORDER BY year_built_clean
    """)

    df_year_built = df_year_built.toPandas()

    # 添加房龄分组
    bins = [0, 5, 10, 20, 25, 30, 35, float('inf')]
    labels = ['0-5', '5-10', '10-20', '20-25', '25-30', '30-35', '35+']
    df_year_built['age_group'] = pd.cut(df_year_built['house_age'], bins=bins, labels=labels, right=False)

    # 计算每个房龄段的平均单价
    grouped = df_year_built.groupby('age_group')['avg_unit_price'].mean().reset_index()

    # 将数据转换为Pandas数据帧
    # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
    # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
    ax.plot(grouped['age_group'], grouped['avg_unit_price'], marker='o')

    ax.set_title("在售房源房龄分组与平均单价关系", fontdict={"size": 22})
    ax.set_xlabel("房龄分组（年）")
    ax.set_ylabel("平均单价（元/平）")
    for row in grouped.itertuples():
        ax.text(row.Index, row.avg_unit_price + .5, s=round(row.avg_unit_price, 2),
                horizontalalignment="center", verticalalignment="bottom",
                fontsize=14)

    plt.show()
# 分析在售房源小区的热度
def analyze_the_popularity_of_the_neighborhoods_where_listings_are_for_sale():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )

    db_path = "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/lianjia_spider/db/lianjia.db"

    # 读取 house_details 表（包含 tags）
    df_detail = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "house_details")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )

    # 读取 houses 表（基础字段）
    df_houses = (
        spark.read.format("jdbc")
        .option("url", db_path)
        .option("dbtable", "houses")
        .option("driver", "org.sqlite.JDBC")
        .load()
    )


  
    df_houses.createOrReplaceTempView("temp")

    df_community_popularity = spark.sql("""
        SELECT community_name, SUM(followers) as total_followers, COUNT(1) as count
        FROM temp
        GROUP BY community_name
    """)

    # Convert to pandas before sorting
    df_community_popularity = df_community_popularity.toPandas()
    df_community_popularity = df_community_popularity.sort_values("total_followers", ascending=False).head(20)
    df_community_popularity.reset_index(drop=True, inplace=True)

    names = df_community_popularity["community_name"]
    followers = df_community_popularity["total_followers"]

    plt.figure(figsize=(16,8))
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.bar(names, followers, color="red", alpha=0.8)
    
    plt.xticks(rotation=60)
    plt.xlabel("小区名称")
    plt.ylabel("关注人数")
    
    for i, v in enumerate(followers):
        plt.text(i, v + 1, str(v), ha="center", va="bottom")
    plt.show()
def test():
    pass
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        analyze_the_popularity_of_the_neighborhoods_where_listings_are_for_sale()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
