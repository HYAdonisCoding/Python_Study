#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 18 分析电商网站销售数据 Analyzing sales data from e-commerce websites
# * 分析主页面
# 1.打开点评网北京首页
# https://www.dianping.com/beijing/ch10
# 2.检查html元素 数据实际存放位置 <div class="shop-list J_shop-list shop-all-list" id="shop-all-list">下的<ul>
# 3.每页有15条数据,一共50页数据
# 4.分别点击2、3、4页
# https://www.dianping.com/beijing/ch10/p2
# https://www.dianping.com/beijing/ch10/p3
# https://www.dianping.com/beijing/ch10/p4

# * 分享商家商品列表
# 1.商品名称
# <div class="tit">
#     <a onclick="LXAnalytics('moduleClick', 'shopname');document.hippo.ext({cl_i:1,query_id:'559167c7-2c2a-4021-978a-15108f960e2d'}).mv('cl_to_s','G9B5lBAWimhGRPnh');" data-click-name="shop_title_click" data-shopid="G9B5lBAWimhGRPnh" data-hippo-type="shop" title="北京宜宾招待所(南翠花街店)" target="_blank" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh">
#         <h4>北京宜宾招待所(南翠花街店)</h4>
#     </a>
#     <div class="promo-icon J_promo_icon">
#           <a rel="nofollow" data-click-name="shop_group_icon_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank" href="http://t.dianping.com/deal/1447305194" title="北京宜宾招待所!仅售95元！价值100元的代金券1张，可叠加使用。" class="igroup" data-hippo-dealgrp_type="" data-hippo-dealgrp_id="1447305194">
#           </a>
#     </div>
#   </div>
# 2.获取每个商品名称所在链接，href 为：https://www.dianping.com/shop/+data-shopid+#comment
# *列表页获取得的数据
# data-shopid 商家编号
# shopName 商家名称
# 推荐菜
# <div class="recommend">
# <span>推荐菜：</span>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish190867664" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">红糖冰粉</a>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish349582468" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">粉蒸肉</a>
# <a class="recommend-click" href="https://www.dianping.com/shop/G9B5lBAWimhGRPnh/dish397219048" data-click-name="shop_tag_dish_click" data-shopid="G9B5lBAWimhGRPnh" target="_blank">宜宾燃抄手</a>
# </div>
# * 分析商品详情页
# data-shopid 商家编号
# shopName 商家名称
# star-score 商家评分
# scoreText 各项评分
# price 人均消费
# region 区域
# category 分类
# desc-addr-txt 地址
# reviews 总评论个数

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StringType, StructType
import csv

# 筛选口碑最好的十户商家--按口碑排序
def select_the_ten_merchants_with_the_best_reputation():
    spark = SparkSession.builder.getOrCreate()
    file = "hdfs://localhost:9000/input/shops.txt"
    rdd = spark.sparkContext.textFile(file)
    header = rdd.first()  # 获取第一行
    rdd = rdd.filter(lambda line: line != header)  # 过滤掉表头

    def convert_data(line):
        lines = line.split(",")
        # 返回的三个数据分别是：商户名称，评分
        return lines[1], lines[4]


    # 对数据去重然后排序
    data = rdd.map(lambda line: convert_data(line)).distinct(). \
        sortBy(lambda x: x[1], ascending=False).collect()

    schemaString = "shop_name star_score"
    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)
    df = spark.createDataFrame(data, schema).limit(10)
    df.show()

# 筛选人均消费最高的十户商家
def filter_the_ten_merchants_with_the_highest_average_spending_per_customer():
    spark = SparkSession.builder.getOrCreate()
    file = "hdfs://localhost:9000/input/shops.txt"
    rdd = spark.sparkContext.textFile(file)
    header = rdd.first()  # 获取第一行
    rdd = rdd.filter(lambda line: line != header)  # 过滤掉表头

    def convert_data(line):
        lines = line.split(",")
        # 转成纯数字
        price = parse_price(lines[6])
        # 返回的三个数据分别是：商户名称，评分, 人均消费
        return lines[1], lines[4], price


    # 对数据去重然后排序
    data = rdd.map(lambda line: convert_data(line)).distinct(). \
        sortBy(lambda x: x[2], ascending=False).collect()

    schemaString = "shop_name star_score price"
    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)
    df = spark.createDataFrame(data, schema).limit(10)
    df.show()
# 筛选评价最多的十户商家
def filter_the_ten_merchants_with_the_most_reviews():
    spark = SparkSession.builder.getOrCreate()
    file = "hdfs://localhost:9000/input/shops.txt"
    rdd = spark.sparkContext.textFile(file)
    header = rdd.first()  # 获取第一行
    rdd = rdd.filter(lambda line: line != header)  # 过滤掉表头

    def convert_data(line):
        # 用 csv 解析，自动处理引号、顿号、逗号、嵌套符号，不会错位
        fields = next(csv.reader([line]))

        shop_name = fields[1]
        star_score = fields[4]
        reviews = int(fields[10])

        return shop_name, star_score, reviews


    # 对数据去重然后排序
    data = rdd.map(lambda line: convert_data(line)).distinct(). \
        sortBy(lambda x: x[2], ascending=False).collect()

    schemaString = "shop_name star_score reviews"
    fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
    schema = StructType(fields)
    df = spark.createDataFrame(data, schema).limit(10)
    df.show()
    
def parse_price(price_str):
    if price_str is None:
        return 0
    price_str = price_str.strip()
    # 如果为空或破损数据
    if price_str == "" or price_str == "-":
        return 0
    # 去掉"¥"、"/人"等
    price_str = price_str.replace("¥", "").replace("/人", "").strip()
    # 转成整数
    try:
        return int(price_str)
    except:
        return 0

import re
from pyspark.sql.functions import (
    col, count, avg, sum, desc, udf
)
from pyspark.sql.types import (
    StructField, StringType, StructType,
    IntegerType, DoubleType
)
# 综合分析
def comprehensive_analysis():
    

    spark = SparkSession.builder.getOrCreate()
    file = "hdfs://localhost:9000/input/shops.txt"
    rdd = spark.sparkContext.textFile(file)

    # ---------------------------------------
    # 1. 读取 CSV（自动处理引号、顿号、逗号，不会错位）
    # ---------------------------------------
    df = spark.read.csv(
        file,
        header=True,
        encoding="utf-8",
        multiLine=True,
        quote='"',
        escape='"',
    )

    df.cache()

    print("原始字段：")
    print(df.columns)

    # ---------------------------------------
    # 2. 解析字段函数
    # ---------------------------------------

    # 价格：¥108/人 → 108
    def parse_price(price_str):
        if price_str is None:
            return None
        m = re.search(r"¥(\d+)", price_str)
        return int(m.group(1)) if m else None

    # 解析三分项：口味 环境 服务
    def parse_scores(text):
        if text is None:
            return (None, None, None)
        taste = env = service = None
        m1 = re.search(r"口味[:：](\d+\.\d+)", text)
        m2 = re.search(r"环境[:：](\d+\.\d+)", text)
        m3 = re.search(r"服务[:：](\d+\.\d+)", text)
        return (
            float(m1.group(1)) if m1 else None,
            float(m2.group(1)) if m2 else None,
            float(m3.group(1)) if m3 else None,
        )

    # 地铁距离：例如
    # "距地铁2号线和平门站A1西北口步行450m"
    def parse_metro(text):
        if text is None:
            return (None, None, None)
        line = station = None
        dist = None

        m1 = re.search(r"距地铁(.+?)线", text)
        if m1:
            line = m1.group(1) + "号线"

        m2 = re.search(r"线(.+?站)", text)
        if m2:
            station = m2.group(1)

        m3 = re.search(r"步行(\d+)m", text)
        if m3:
            dist = int(m3.group(1))

        return (line, station, dist)

    # 注册 UDF
    parse_price_udf = udf(parse_price, IntegerType())
    parse_scores_udf = udf(parse_scores, StructType([
        StructField("taste", DoubleType()),
        StructField("environment", DoubleType()),
        StructField("service", DoubleType())
    ]))
    parse_metro_udf = udf(parse_metro, StructType([
        StructField("metro_line", StringType()),
        StructField("metro_station", StringType()),
        StructField("walk_dist", IntegerType())
    ]))

    # ---------------------------------------
    # 3. 构建强结构化数据
    # ---------------------------------------
    df2 = df \
        .withColumn("price_value", parse_price_udf(col("price"))) \
        .withColumn("scores", parse_scores_udf(col("score_text"))) \
        .withColumn("taste", col("scores.taste")) \
        .withColumn("environment", col("scores.environment")) \
        .withColumn("service", col("scores.service")) \
        .withColumn("metro", parse_metro_udf(col("desc_addr_txt"))) \
        .withColumn("metro_line", col("metro.metro_line")) \
        .withColumn("metro_station", col("metro.metro_station")) \
        .withColumn("walk_dist", col("metro.walk_dist")) \
        .drop("scores", "metro")

    df2.cache()

    print("解析后的字段：")
    print(df2.columns)


    # ======================================================
    # ===============  四大核心分析  ========================
    # ======================================================

    # ------------------------------------------------------
    # A. 区域维度分析（区域消费、热度、评分）
    # ------------------------------------------------------
    print("\n【区域消费与热度 Top 10】")
    df2.groupBy("region") \
        .agg(
            count("*").alias("shop_count"),
            avg("price_value").alias("avg_price"),
            avg("star_score").alias("avg_score"),
            sum("reviews").alias("total_reviews"),
        ) \
        .orderBy(desc("total_reviews")) \
        .show(10, False)


    # ------------------------------------------------------
    # B. 分类（菜系）维度分析
    # ------------------------------------------------------
    print("\n【菜系热度排名】")
    df2.groupBy("category") \
        .agg(
            count("*").alias("shop_count"),
            avg("star_score").alias("avg_score"),
            avg("price_value").alias("avg_price"),
            sum("reviews").alias("total_reviews")
        ) \
        .orderBy(desc("total_reviews")) \
        .show(20, False)


    # ------------------------------------------------------
    # C. 性价比指数（评论数 ÷ 价格）
    # ------------------------------------------------------
    print("\n【性价比最高的 20 家店】")
    df2.withColumn(
        "value_index", col("reviews") / col("price_value")
    ).orderBy(desc("value_index")).show(20, False)


    # ------------------------------------------------------
    # D. 推荐菜词频统计（RDD 版）
    # ------------------------------------------------------
    print("\n【全平台最热的推荐菜 Top 50】")

    rdd = df2.select("recommend_dishes").rdd.flatMap(
        lambda row: re.split(r"[、, ]+", row[0]) if row[0] else []
    )

    dish_counts = rdd.map(lambda x: (x, 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda x: x[1], ascending=False) \
        .take(50)

    for dish, cnt in dish_counts:
        print(f"{dish}: {cnt}")


    # ------------------------------------------------------
    # E. 地铁距离与热度关系
    # ------------------------------------------------------
    print("\n【离地铁越近是否越热门？】")
    df2.filter(col("walk_dist").isNotNull()) \
        .groupBy("metro_line") \
        .agg(
            avg("walk_dist").alias("avg_dist"),
            avg("reviews").alias("avg_reviews"),
        ) \
        .orderBy("avg_dist") \
        .show(20, False)

    # ------------------------------------------------------
    # F. 综合评分最高的店
    # ------------------------------------------------------
    print("\n【评分 Top 20】")
    df2.orderBy(desc("star_score"), desc("reviews")) \
        .select("shop_name", "star_score", "price_value", "reviews", "region") \
        .show(20, False)


    print("\n-------------------- Finished --------------------")
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        comprehensive_analysis()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
