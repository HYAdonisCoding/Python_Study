from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder.appName("ReadKafkaExample").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# 从 Kafka 读取
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test-topic") \
    .option("startingOffsets", "latest") \
    .load()

# Kafka 的 value 默认是二进制，需要转为字符串
lines = df.selectExpr("CAST(value AS STRING)")

query = lines.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()