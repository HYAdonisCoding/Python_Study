#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8

import os
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pyspark.sql.types import StructField, StringType, IntegerType, StructType, LongType
from pyspark.sql import functions as F

speter = "-" * 10

# 第四篇
# 19 分析旅游网站数据 Analyzing travel website data
# * 分析主页面
#  步骤 01 打开主页  https://you.ctrip.com/
# 推荐：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=14&Idea=0&Type=1&Plate=0
# 最新：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=2&Idea=0&Type=2&Plate=0
# 头条：https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml?p=2&Idea=0&Type=100&Plate=0

# <div class="city" data-travelid="3990253"><div class="yj_type"><span class="pic-tagico-5">头条</span><span class="pic-tagico-1">精华</span></div><a target="_blank" class="city-image" href="/travels/sanya61/3990253.html" rel="nofollow"><img data-travelcoverid="509095992" class="pic" width="228" height="152" src="https://dimg04.c-ctrip.com/images/0105y120008crbslg56DD_R_228_10000_Q90.jpg"></a><div class="city-sub"><a target="_blank" class="city-name" href="/place/sanya61.html">三亚</a>：<a target="_blank" class="cpt" title="海岛之冬，和闺蜜的三亚之旅" href="/travels/sanya61/3990253.html">海岛之冬，和闺蜜的三亚之旅</a><p class="opts"><i class="numview" title="浏览">16556</i> <i class="want" title="喜欢">96</i>&nbsp;&nbsp;<i class="numreply" title="回复">29</i></p></div><div class="authorinfo"><p class="author" data-authorid="14457689"><a class="imgnav" target="_blank" href="/members/639FFB8ED39F4BF7874FFA698BC7D725/journals" rel="nofollow"><img title="阿拖拖晓君" width="28" height="28" class="pic" src="https://dimg04.c-ctrip.com/images/0Z81r120008ehsou035F6_R_180_180.jpg"></a><a target="_blank" href="/members/639FFB8ED39F4BF7874FFA698BC7D725/journals" rel="nofollow" title="阿拖拖晓君">阿拖拖晓君</a>&nbsp;&nbsp;<i class="time">2020-12-30</i></p></div></div>
import matplotlib.pyplot as plt

# ? 数据分析
# 分析“驴友”普遍去了哪些地方
def analysis_of_the_places_that_backpackers_typically_visit():
    # 指定Mysql的配置
    # options = {
    #     "url": "jdbc:mysql://localhost:3306/sparktest?useSSL=true",
    #     "driver": "com.mysql.jdbc.Driver",
    #     "dbtable": "(SELECT * from travels_detail where price!='None') t1",
    #     "user": "root",
    #     "password": "root"
    # }
    # spark = SparkSession.builder.getOrCreate()
    # # 加载Mysql数据
    # data = spark.read.format("jdbc").options(**options).load()
    # /Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar
    
    
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )
    options = {
        "url": "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/ctrip_spider/db/dianping.db",
        "driver": "org.sqlite.JDBC",
        "dbtable": "travels"
    }

    data = spark.read.format("jdbc").options(**options).load()
    # 对目的地列进行分组，调用聚合函数count获取每个组的个数
    df = data.groupby("city_name").count().orderBy("count", ascending=False)
    # 筛选游记中提到的前10个目的地，并将Spark数据帧转为Pandas数据帧
    result_pdf = df.select("*").limit(10).toPandas()
    # 设置matplotlib支持中文（macOS 使用系统自带的苹方）
    # 字体文件路径（macOS 用户字体安装在 ~/Library/Fonts/ 下）
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.bar(result_pdf["city_name"], result_pdf["count"], width=0.8)

    plt.legend()
    plt.show()
    
# 分析“驴友”出行特点
def analyzing_the_characteristics_of_backpackers():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )
    options = {
        "url": "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/ctrip_spider/db/dianping.db",
        "driver": "org.sqlite.JDBC",
        "dbtable": "travels"
    }
    # 加载Mysql数据
    data = spark.read.format("jdbc").options(**options).load()


    # 把 play 字段里的 "#" 去掉，再按逗号拆分为数组，展开计数
    df_exploded = (
        data
        .withColumn("play_clean", F.regexp_replace(F.col("play"), "#", ""))    
        # 将中文逗号统一替换为英文逗号
        .withColumn("play_clean", F.regexp_replace(F.col("play_clean"), "，", ","))
        # 去掉空白字符
        .withColumn("play_clean", F.regexp_replace(F.col("play_clean"), "\\s+", ""))
        # 逗号拆分
        .withColumn("play_item", F.explode(F.split(F.col("play_clean"), ",")))
        .filter(F.col("play_item") != "")
        .filter(~F.col("play_item").contains("牛"))
    )

    result_df = (
        df_exploded.groupBy("play_item")
        .count()
        .orderBy(F.desc("count"))
    )


    # 将数据转换为Pandas数据帧
    # result_pdf = schema_data.limit(5).toPandas()
    top5_pdf = result_df.select(F.col("play_item").alias("play"), "count").limit(8).toPandas()

    print("\n===== Top 5 玩法统计 =====")
    print(top5_pdf.to_string(index=False))
    # 设置matplotlib支持中文
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)

    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    # colors=color, explode=explode,
    fig, ax = plt.subplots()

    ax.pie(top5_pdf["count"], labels=top5_pdf["play"], shadow=True, autopct='%1.1f%%')

    # 把图例放在右侧
    ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))

    plt.show()

# 推测“驴友”都喜欢在哪个季节出行
def ppeculating_on_the_preferred_seasons_for_backpackers_to_travel():
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )
    options = {
        "url": "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/ctrip_spider/db/dianping.db",
        "driver": "org.sqlite.JDBC",
        "dbtable": "travels"
    }
    # 加载Mysql数据
    data = spark.read.format("jdbc").options(**options).load()

    def convert_to_quarter(line):
        m = line['month']

        if m is None or m.strip() == "":
            return ("未知", 1)

        try:
            month = int(m)  # 转整数
        except:
            return ("未知", 1)

        if month in [3, 4, 5]:
            return ("春季", 1)
        elif month in [6, 7, 8]:
            return ("夏季", 1)
        elif month in [9, 10, 11]:
            return ("秋季", 1)
        elif month in [12, 1, 2]:
            return ("冬季", 1)
        else:
            return ("未知", 1)
    zeroValue = 0
    rdd = (
        data.rdd
            .map(lambda line: convert_to_quarter(line))
            .filter(lambda x: x[0] != "未知")          # ← 关键过滤
            .foldByKey(zeroValue, lambda v, x: v + x)
    )    
    schema = StructType([
        StructField("quarter", StringType(), True),
        StructField("count", IntegerType(), True)
    ])
    schema_data = spark.createDataFrame(rdd, schema).orderBy("count", ascending=False)

    # 将数据转换为Pandas数据帧
    result_pdf = schema_data.limit(100).toPandas()
    print("\n===== Top 季节统计 =====")
    print(result_pdf.to_string(index=False))
    # 设置matplotlib支持中文
    font_path = os.path.expanduser('~/Library/Fonts/SourceHanSansHWSC-Regular.otf')
    fm.fontManager.addfont(font_path)
    # 打印 month 的分布（前 50 条示例）
    data.select("month").groupBy("month").count().orderBy(F.desc("count")).show(50, truncate=False)
    # 设置 Matplotlib 使用该字体
    plt.rcParams['font.family'] = 'Source Han Sans HW SC'
    plt.rcParams['axes.unicode_minus'] = False
    # colors=color, explode=explode,
    counts = result_pdf["count"]
    quarters = result_pdf["quarter"]

    # 合并标签和百分比
    labels = [f"{q} {c/sum(counts)*100:.1f}%" for q, c in zip(quarters, counts)]

    plt.pie(counts, labels=labels, 
            labeldistance=0.5,  # 标签离圆心的比例
            shadow=True, startangle=90)
    
    plt.title('分析出行季节')
    plt.show()

# 推测未来的热门景点
def predicting_future_popular_tourist_attractions():
    
    spark = (
        SparkSession.builder
        .appName("ReadSQLite")
        .config("spark.jars", "/Users/adam/Documents/Developer/environment/sqlite-jdbc-3.51.0.0.jar")
        .getOrCreate()
    )
    options = {
        "url": "jdbc:sqlite:/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/ctrip_spider/db/dianping.db",
        "driver": "org.sqlite.JDBC",
        "dbtable": "travels"
    }
    
    # 加载Mysql数据
    # options["dbtable"] = "(SELECT travel_id, city_name, person_cost from travels)travels_detail"
    # data1 = spark.read.format("jdbc").options(**options).load()

    # options["dbtable"] = "(SELECT travel_id,views from travels)travels"
    # data2 = spark.read.format("jdbc").options(**options).load()
    # print(data2.columns)
    # # 将viewCount类型（字符串类型）转为长整型（LongType），以方便在sql语句中排序
    # data3 = data2.select("travel_id", data2.views.cast(LongType()).alias("views"))

    # # 进行join操作，将两个数据帧连接为一个数据帧
    # data4 = data1.join(data3, data1.travel_id == data3.travel_id)
    # # 将连接后的数据注册为临时表
    # data4.createOrReplaceTempView("travel")

    # 使用sql查询生成新的数据帧
    # data5 = spark.sql(
    #     "SELECT city_name,views,person_cost FROM travel where city_name!='None' and views>200000  order by views desc")

    # data5.show()
    
    data = spark.read.format("jdbc").options(**options).load()
    df_views = (
        data.withColumn("views_long", F.col("views").cast(LongType()))
        .filter((F.col("city_name").isNotNull()) & F.col("person_cost").isNotNull() & (F.col("views_long") > 200000))
        .select("city_name", "views_long", "person_cost")
        .orderBy(F.desc("views_long"))
    )
    df_views.show()
#     +---------+------+-----------+
# |city_name| views|person_cost|
# +---------+------+-----------+
# |     清远|873312|        500|
# |   巴厘岛|692151|       3000|
# |     肇庆|680691|       3000|
# |     广东|605679|        100|
# |     广东|605651|        100|
# |     广州|604544|         70|
# |     昆明|529118|       1500|
# |     东莞|472065|        500|
# |     上饶|390599|       NULL|
# |   黑龙江|360699|       5000|
# |     浙江|351047|       NULL|
# |     林芝|350869|       NULL|
# |     全南|337158|       NULL|
# |     暹粒|311903|       NULL|
# |     拉萨|303755|       NULL|
# |     西安|303551|       3000|
# |     老挝|289386|       4000|
# |     荣成|278639|       2000|
# |     衡山|270581|          8|
# |     西安|261878|       5000|
# +---------+------+-----------+
# +--------------+----------+-----------+
# |     city_name|views_long|person_cost|
# +--------------+----------+-----------+
# |          清远|    873312|        500|
# |        巴厘岛|    692151|       3000|
# |          肇庆|    680691|       3000|
# |          广东|    605679|        100|
# |          广东|    605651|        100|
# |          广州|    604544|         70|
# |          昆明|    529118|       1500|
# |          东莞|    472065|        500|
# |        黑龙江|    360699|       5000|
# |          西安|    303551|       3000|
# |          老挝|    289386|       4000|
# |          荣成|    278639|       2000|
# |          衡山|    270581|          8|
# |          西安|    261878|       5000|
# |          三亚|    259237|       2000|
# |大理白族自治州|    258804|       5000|
# |          威海|    257128|       4000|
# |          东莞|    250338|         50|
# |          西安|    245523|       2000|
# |          重庆|    243982|         39|
# +--------------+----------+-----------+
def test():
    pass


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        predicting_future_popular_tourist_attractions()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
