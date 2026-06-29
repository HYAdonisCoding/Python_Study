#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 17 Spark 流式计算编程 Spark Streaming Programming
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# 流式处理程序
def test_streaming():
    sc = SparkContext(appName="PythonStreamingNetworkWordCount")
    sc.setLogLevel("ERROR")  # ✅ 正确写法
    ssc = StreamingContext(sc, 1)

    # 默认连接 localhost:9999，如果需要参数传入，也可以加 sys.argv
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

    lines = ssc.socketTextStream(host, port)
    counts = lines.flatMap(lambda line: line.split(" ")) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a + b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
# 创建文件流
def create_filestream():
    sc = SparkContext(appName="HDFSFileStream")
    ssc = StreamingContext(sc, 10)

    lines = ssc.textFileStream("/bigdata/streaming")
    counts = lines.flatMap(lambda line: line.split(" ")).\
	map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
# 创建队列流
def create_queue_stream():
    sc = SparkContext(appName="QueueStream")
    ssc = StreamingContext(sc, 10)

    tmp_list = [j for j in range(1, 10)]
    rdd_queue = []
    for i in range(10):
        rdd_queue += [ssc.sparkContext.parallelize(tmp_list)]

    input_stream = ssc.queueStream(rdd_queue)
    data = input_stream.map(lambda x: (x % 2, 1)).reduceByKey(lambda a, b: a + b)
    data.pprint()

    ssc.start()
    ssc.awaitTermination()
# 结构化流统计词频
def structuredStreamStatisticalWordFrequency():
    spark = SparkSession.builder.appName("WordCount").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    lines = spark.readStream.format("socket").\
    option("host", "localhost").option("port", 9999).load()

    words = lines.select(
        explode(
            split(lines.value, " ")
        ).alias("word")
    )

    wordCounts = words.groupBy("word").count()
    query = wordCounts.writeStream.outputMode("complete").format("console").start()
    query.awaitTermination()
# 读取Kafka数据
def read_Kafka_data():
    bootstrapServers = "localhost:9092"
    subscribeType = "subscribe"
    topics = "bigdata"
    spark = SparkSession.builder.appName("FromKafka").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    lines = spark.readStream.format("kafka").\
		option("kafka.bootstrap.servers", bootstrapServers). \
        option(subscribeType, topics).load().selectExpr("CAST(value AS STRING)")
    words = lines.select(explode(split(lines.value, ',')).alias('word'))
    wordCounts = words.groupBy('word').count()
    query = wordCounts.writeStream.outputMode('complete').format('console').start()
    query.awaitTermination()
    
# 时间窗口聚合
def time_window_aggregation():
    bootstrapServers = "localhost:9092"
    subscribeType = "subscribe"
    topics = "bigdata"
    windowSize = 10
    slideSize = 5
    windowDuration = '{} seconds'.format(windowSize)
    slideDuration = '{} seconds'.format(slideSize)

    spark = SparkSession.builder.appName("KafkaWordCount").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    lines = spark.readStream.format("kafka").\
		option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics).option('includeTimestamp', 'true').load()

    words = lines.select(
        explode(split(lines.value, ' ')).alias('word'),
        lines.timestamp
    )
    windowedCounts = words.groupBy(
        window(words.timestamp, windowDuration, slideDuration),
        words.word
    ).count()

    query = windowedCounts.writeStream.outputMode('complete').format('console').start()
    query.awaitTermination()
# 设置水印
def config_watermark():
    bootstrapServers = "localhost:9092"
    subscribeType = "subscribe"
    topics = "bigdata"
    windowSize = 10
    slideSize = 5
    windowDuration = '{} seconds'.format(windowSize)
    slideDuration = '{} seconds'.format(slideSize)

    spark = SparkSession.builder.appName("KafkaWordCount").getOrCreate()
    lines = spark.readStream.format("kafka").\
		option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics).option('includeTimestamp', 'true').load()
    words = lines.select(
        explode(split(lines.value, ' ')).alias('word'),
        lines.timestamp
    )
    windowedCounts = words.withWatermark("timestamp", "10 seconds").groupBy(
        window(words.timestamp, windowDuration, slideDuration),
        words.word
    ).count()
    query = windowedCounts.writeStream.outputMode('update').format('console').start()
    query.awaitTermination()
    
from pyspark.sql.functions import window
# 输出到HDFS
def output_to_HDFS():
    bootstrapServers = "localhost:9092"
    subscribeType = "subscribe"
    topics = "bigdata"
    windowSize = 10
    slideSize = 5
    windowDuration = '{} seconds'.format(windowSize)
    slideDuration = '{} seconds'.format(slideSize)

    spark = SparkSession.builder.appName("KafkaWordCount").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    lines = spark.readStream.format("kafka").option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics).load()

    query = lines.writeStream.format("json").option("checkpointLocation", "/struct_streaming/checkpoint") \
        .option("path", "/struct_streaming/output").start()

    query.awaitTermination()
# 实时计算贷款金额
def realtime_loan_amount_calculation():
    if len(sys.argv) != 4:
        print("""
        Usage: structured_kafka_wordcount.py <bootstrap-servers> <subscribe-type> <topics>
        """, file=sys.stderr)
        exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]
    spark = SparkSession.builder.appName("SumAmount").getOrCreate()
    lines = spark.readStream.format("kafka").\
        option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics).load().selectExpr("CAST(value AS STRING)")

    def split_vla(val):
        tmp = split(val, ":")
        name_col = tmp.getItem(0).alias("name")
        amount_col = tmp.getItem(1).cast("float").alias("amount")
        return name_col, amount_col

    name_col, amount_col = split_vla(lines.value)
    words = lines.select(name_col, amount_col)
    wordCounts = words.groupBy("name").sum("amount")
    query = wordCounts.writeStream.outputMode('complete').format('console').start()
    query.awaitTermination()
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        realtime_loan_amount_calculation()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


