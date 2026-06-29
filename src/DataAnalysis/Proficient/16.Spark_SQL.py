#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 16 Spark SQL 编程 Spark SQL Programming
from pyspark import since
from pyspark.sql import SparkSession

import warnings

warnings.filterwarnings("ignore")
# spark = SparkSession.builder.getOrCreate()

# 设置 Spark 日志级别
# spark.sparkContext.setLogLevel("ERROR")  # 可选 "WARN"、"INFO"、"DEBUG"

# 初始化元数据库 schematool -dbType mysql -initSchema


# 读取本地文件
def read_local_file():
    spark = SparkSession.builder.getOrCreate()

    df = spark.read.load("/bigdata/testdata/users.parquet")
    print("df的类型:", type(df))
    df.show()


# 读取json文件
def read_json_file():
    # spark = SparkSession.builder.getOrCreate()
    df = spark.read.format("json").load("/bigdata/testdata/people.json", format="json")
    print("读取json格式，df的类型:", type(df))
    df.show()


# insert into people(name, age) values('John', 20);
# insert into people(name, age) values('Jane', 21);
# insert into people(name, age) values('Jim', 22);
# insert into people(name, age) values('Eason', 22);
# insert into people(name, age) values('Tom', 28);
# 读取MySQL数据库
options = {
    "url": "jdbc:mysql://127.0.0.1:3306/sparktest?useSSL=false",
    "driver": "com.mysql.cj.jdbc.Driver",
    "dbtable": "people",
    "user": "eason",
    "password": "chy123",
}


def read_mysql_database():
    # spark = SparkSession.builder.getOrCreate()
    spark = (
        SparkSession.builder.appName("Spark MySQL Test")
        .config(
            "spark.jars",
            "/opt/homebrew/Cellar/apache-hive/4.1.0/lib/mysql-connector-java-8.1.0.jar",
        )
        .getOrCreate()
    )

    df = spark.read.format("jdbc").options(**options).load()
    df.show()
    print("读取MySQL数据库，df的类型:", type(df))


# 读取Hive数据库 ？？？？ /Users/adam/envs/py_arm64/bin/python /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/16.Spark_SQL.py > ~/Documents/Developer/spark_logs/read_$(date +%Y%m%d_%H%M%S).txt 2>&1
def read_hive_database():
    # spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    spark = (
        SparkSession.builder.appName("Spark Hive Test")
        .config(
            "spark.jars",
            "/opt/homebrew/Cellar/apache-hive/4.1.0/lib/mysql-connector-java-8.1.0.jar",
        )
        .enableHiveSupport()
        .getOrCreate()
    )
    spark.sql("use sparktest")
    df = spark.sql("select *from people")
    print("读取hive数据，df的类型:", type(df))
    df.show()


# 读取HBase数据库
def read_hbase_database():
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.format("hbase").load()
    df.show()
    print("读取HBase数据库，df的类型:", type(df))


from pyspark.sql.types import Row


# 利用反射机制推断RDD模式
def infer_rdd_mode():
    spark = SparkSession.builder.getOrCreate()

    def f(item):
        people = {"name": item[0], "age": item[1]}
        return people

    df = (
        spark.sparkContext.textFile("/bigdata/testdata/people.txt")
        .map(lambda line: line.split(","))
        .map(lambda x: Row(**f(x)))
        .toDF()
    )
    print("将RDD转换为DataFrame，转换后df的类型:", type(df))
    df.show()


from pyspark.sql.types import Row, StructType, StructField, StringType, IntegerType


# 构造schema应用到现有的RDD上
def construct_schema_to_rdd():
    spark = SparkSession.builder.getOrCreate()
    schema = StructType(
        [
            StructField("name", StringType(), True),
            StructField("age", IntegerType(), True),
        ]
    )

    rdd = (
        spark.sparkContext.textFile("/bigdata/testdata/people.txt")
        .map(lambda line: line.split(","))
        .map(lambda item: Row(item[0], int(item[1])))
    )
    df = spark.createDataFrame(rdd, schema)
    print("将RDD转换为DataFrame，转换后df的类型:", type(df))
    df.show()


#  DataFrame 常用 API
# 显示数据
# 输出schema信息
def show_schema():
    spark = SparkSession.builder.getOrCreate()
    data = [{"name": "Alice", "age": 1}]
    df = spark.createDataFrame(data)
    print(df.printSchema)


@since(1.3)
def show(self, n=20, truncate=True, vertical=False):
    """
    显示 DataFrame 数据，支持纵向和截断显示
    :param n: 显示前 n 行
    :param truncate: 是否截断列
    :param vertical: 是否纵向显示
    """
    if isinstance(truncate, bool) and truncate:
        print(self._jdf.showString(n, 20, vertical))
    else:
        print(self._jdf.showString(n, int(truncate), vertical))


# 调用show显示数据
def show_data():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"name": "AliceAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "age": 1},
        {"name": "Bob", "age": 3},
    ]
    df = spark.createDataFrame(data)
    print(df.show(vertical=True))


# 查询数据
def query_data():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)
    data_list = df.collect()

    [print("当前元素是", item) for item in data_list]


@since(1.3)
def take(self, num):
    """Returns the first ``num`` rows as a :class:`list` of :class:`Row`.

    >>> df.take(2)
    [Row(age=2, name=u'Alice'), Row(age=5, name=u'Bob')]
    """
    return self.limit(num).collect()


# 返回指定行
def return_specified_rows():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)
    data_list = df.limit(2)
    data_list.show()


# 指定过滤条件
def specify_filter_conditions():
    spark = SparkSession.builder.getOrCreate()

    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)
    tmp_list = df.filter("name = 'Alice' and age = 1").collect()
    print("当前过滤后的元素个数:", len(tmp_list))
    [print("当前元素是:", item) for item in tmp_list]


# 指定过滤条件select
def specify_filter_conditions_select():
    spark = SparkSession.builder.getOrCreate()

    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)
    tmp_list = df.select("name").collect()

    [print("当前元素是:", item) for item in tmp_list]


# 指定过滤条件 selectExpr
def specify_filter_conditions_selectExpr():
    spark = SparkSession.builder.getOrCreate()

    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)
    spark.udf.register("show_name", lambda item: "姓名是：" + item)
    tmp_list = df.selectExpr("show_name(name)", "age + 1").collect()

    [print("当前元素是:", item) for item in tmp_list]


# 统计数据
from pyspark.sql.functions import *


# 排序
def sort_data():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"name": "Alice", "age": 1},
        {"name": "Bob", "age": 3},
        {"name": "Li", "age": 10},
    ]
    df = spark.createDataFrame(data)

    tmp_list = df.sort(df.age.desc()).collect()
    tmp_list1 = df.sort(desc("age")).collect()
    [print("当前元素是:", item) for item in tmp_list1]


# 合并数据
def merge_data():
    spark = SparkSession.builder.getOrCreate()
    data1 = [{"name": "Tom", "height": 80}, {"name": "Bob", "height": 85}]
    data2 = [{"name": "Tom", "age": 4}, {"name": "Bob", "age": 5}]

    df1 = spark.createDataFrame(data1)
    df2 = spark.createDataFrame(data2)
    tmp_list = df1.join(df2, "name").collect()

    [print("当前元素是:", item) for item in tmp_list]


# 分区求平均
def partition_average():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"course": "math", "score": 80},
        {"course": "math", "score": 98},
        {"course": "english", "score": 85},
        {"course": "english", "score": 60},
    ]

    tmp_list = spark.createDataFrame(data).groupBy("course").avg().collect()
    [print("当前元素是:", item) for item in tmp_list]


# 执行SQL语句
# 注册临时表
def register_temporary_table():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"course": "math", "score": 80},
        {"course": "math", "score": 98},
        {"course": "english", "score": 85},
        {"course": "english", "score": 60},
    ]

    course_list = spark.createDataFrame(data).registerTempTable("course_list")
    tmp_list = spark.sql(
        "select course,max(score) from course_list group by course"
    ).collect()
    [print("当前元素是:", item) for item in tmp_list]


# 保存DataFrame


# 保存到json文件
def save_to_json_file():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"course": "math", "score": 80},
        {"course": "math", "score": 98},
        {"course": "english", "score": 85},
        {"course": "english", "score": 60},
    ]

    course_list = spark.createDataFrame(data).registerTempTable("course_list")
    df = spark.sql("select course,sum(score) from course_list group by course")
    hdfs_path = "/bigdata/testdata/course_score"
    df.write.json(hdfs_path, mode="overwrite")


# 保存到MySQL
def save_to_mysql():
    properties = {
        "driver": "com.mysql.cj.jdbc.Driver",  # ✅ 新驱动类名
        "user": "eason",
        "password": "chy123",
    }
    spark = (
        SparkSession.builder.appName("Spark MySQL Write")
        .config(
            "spark.jars",
            "/opt/homebrew/Cellar/apache-hive/4.1.0/lib/mysql-connector-java-8.1.0.jar",  # ✅ 指定 jar 路径
        )
        .getOrCreate()
    )
    data = [
        {"course": "math", "score": 80},
        {"course": "math", "score": 98},
        {"course": "english", "score": 85},
        {"course": "english", "score": 60},
    ]

    course_list = spark.createDataFrame(data).registerTempTable("course_list")
    df = spark.sql("select course,sum(score) from course_list group by course")

    df.write.jdbc(
        "jdbc:mysql://localhost:3306/sparktest",
        table="course_list",
        mode="overwrite",
        properties=properties,
    )


# 保存到Hive
def save_to_hive():
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    data = [{'course': 'math', 'score': 80}, {'course': 'math', 'score': 98},
        {'course': 'english', 'score': 85}, {'course': 'english', 'score': 60}]

    course_list = spark.createDataFrame(data).registerTempTable("course_list")
    df = spark.sql("select course,avg(score) from course_list group by course")
    df.registerTempTable("score_avg")
    spark.sql("use sparktest")

    spark.sql("insert into hive_score_avg select * from score_avg")


# 保存到csv文件
def save_to_csv_file():
    spark = SparkSession.builder.getOrCreate()
    data = [
        {"course": "math", "score": 80},
        {"course": "math", "score": 98},
        {"course": "english", "score": 85},
        {"course": "english", "score": 60},
    ]

    df = spark.createDataFrame(data)
    df.write.format("csv").save("/bigdata/testdata/course_list.csv")
    [print("当前元素是:", item) for item in tmp_list]

# 创建全局临时表
def create_global_temporary_table():
    spark = SparkSession.builder.enableHiveSupport().getOrCreate()
    data = [{'course': 'math', 'score': 80}, {'course': 'math', 'score': 98},
        {'course': 'english', 'score': 85}, {'course': 'english', 'score': 60}]

    course_list = spark.createDataFrame(data).registerTempTable("course_list")
    df = spark.sql("select course,avg(score) from course_list group by course")
    df.createGlobalTempView("score_avg")
    spark.sql("SELECT * FROM global_temp.score_avg").show()
    spark.newSession().sql("SELECT * FROM global_temp.score_avg").show()


# 统计手机销售情况
# 汇总销售数据
def summarize_sales_data():
    spark = SparkSession.builder.getOrCreate()
    options = {"url": "jdbc:mysql://localhost:3306/sparktest?useSSL=false", 
            "driver": "com.mysql.cj.jdbc.Driver",
            "user": "eason", "password": "chy123"}

    options["dbtable"] = "tb_jd"
    jd_df = spark.read.format("jdbc").options(**options).load()

    options["dbtable"] = "tb_taobao"
    taobao_df = spark.read.format("jdbc").options(**options).load()

    all_data_df = jd_df.join(taobao_df, on="brand", how="left")
    all_data_df.show()


# 统计销售排名
def statistics_ranking_of_sales():
    spark = SparkSession.builder.getOrCreate()
    options = {"url": "jdbc:mysql://localhost:3306/sparktest?useSSL=false", 
            "driver": "com.mysql.cj.jdbc.Driver",
            "user": "eason", "password": "chy123"}

    sql = '''
    (SELECT brand, cast(sum(performance) as signed) sumperformance  FROM (
            SELECT brand, (sales * price) performance FROM tb_jd
            UNION
            SELECT brand, (sales * price) performance FROM tb_taobao
        ) alldata
    GROUP BY brand) total_performance
    '''
    options["dbtable"] = sql
    total_performance_df = spark.read.format("jdbc").options(**options).load()
    total_performance_df.orderBy(total_performance_df.sumperformance.desc()).show()



if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        statistics_ranking_of_sales()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
