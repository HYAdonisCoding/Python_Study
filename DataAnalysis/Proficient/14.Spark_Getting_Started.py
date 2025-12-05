#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 大数据存储与快速分析 Big data storage and rapid analysis
# 14 Spark 入门 Spark Getting Started
# Apache Spark 是一个通用的分布式数据处理框架，用于对海量数据进行快速、可扩展的计算与分析。它最初由加州大学伯克利分校 AMPLab 开发，后成为 Apache 基金会的开源顶级项目。

# 以下是对 Spark 的核心特征和概念的简要说明：
# 	1.	核心定位
# Spark 是一种基于内存计算的大数据处理引擎，相较于早期的 Hadoop MapReduce，Spark 能显著减少磁盘 I/O，提高计算速度，适用于批处理、流处理、机器学习和图计算等多种场景。
# 	2.	核心组件
# 	•	Spark Core：提供分布式任务调度、内存管理、容错和数据并行计算的基础功能。
# 	•	Spark SQL：用于结构化数据处理，支持 SQL 查询、DataFrame 与 Dataset 操作。
# 	•	Spark Streaming：支持实时数据流处理。
# 	•	MLlib：内置机器学习算法库。
# 	•	GraphX：用于图计算和图分析。
# 	3.	编程接口
# Spark 提供多语言 API，包括 Scala、Python、Java、R 等，用户可灵活编写分布式计算任务。
# 	4.	运行环境
# Spark 可运行在多种集群环境中（如 YARN、Kubernetes、Standalone 模式），并能直接读取多种数据源（如 HDFS、Hive、Kafka、Cassandra、S3 等）。
# 	5.	核心优势
# 	•	内存计算性能高，速度可比 Hadoop MapReduce 快数十倍；
# 	•	支持多种计算类型（批处理、流处理、交互查询、机器学习）；
# 	•	易于扩展，可处理从 GB 到 PB 级的数据集。

# 简言之：

# Spark 是一个高性能的分布式数据处理框架，通过内存计算实现对大规模数据的快速分析与处理，是现代大数据生态中最核心的计算引擎之一。


# Apache Spark 相较于 Hadoop（尤其是 Hadoop MapReduce）具有以下主要优势：

# ⸻

# 一、计算性能显著提升
# 	•	内存计算（In-Memory Computing）
# Spark 在计算过程中将中间结果保存在内存中，而 Hadoop MapReduce 每一步都需将结果写入磁盘再读取下一步输入，I/O 开销极大。
# → 在迭代计算、机器学习、图计算等场景中，Spark 的速度可比 MapReduce 快 10～100 倍。

# ⸻

# 二、通用性更强
# 	•	Spark 不仅支持 批处理（Batch Processing），还支持：
# 	•	实时流处理（Spark Streaming）
# 	•	交互式查询（Spark SQL）
# 	•	机器学习（MLlib）
# 	•	图计算（GraphX）
# Hadoop MapReduce 只能处理离线批任务，而 Spark 能在一个统一框架中支持多种计算类型，实现真正的一体化分析平台。

# ⸻

# 三、编程模型更简洁
# 	•	Spark 提供了高层抽象，如 RDD（弹性分布式数据集）、DataFrame 和 Dataset，可通过函数式编程接口实现复杂逻辑。
# 	•	用户可用 Scala、Python、Java、R 编写任务，开发效率高、代码量少。
# 	•	相比之下，MapReduce 代码冗长、逻辑复杂、调试困难。

# ⸻

# 四、资源利用率更高
# 	•	Spark 的DAG 调度器可智能优化任务执行顺序，减少无效数据传输和磁盘操作。
# 	•	能充分利用集群内存、CPU 等资源，实现更高吞吐量。

# ⸻

# 五、生态集成度更强
# 	•	Spark 能无缝对接 Hadoop 生态中的 HDFS、YARN、Hive，也支持 Kafka、Cassandra、HBase、S3 等外部系统。
# 	•	这使其可在原 Hadoop 集群上平滑部署，兼容性与扩展性更好。

# ⸻

# 六、适合迭代与交互式计算
# 	•	机器学习和图计算常需多轮迭代，MapReduce 每轮均需磁盘读写，而 Spark 内存缓存可直接复用数据。
# 	•	同时支持 交互式查询（Spark Shell, Spark SQL），更适合数据探索与分析。

# ⸻

# ✅ 总结一句话：

# Spark 在性能、通用性、易用性和实时处理能力上全面超越 Hadoop MapReduce，是新一代高性能分布式数据计算引擎。

from pyspark.sql import SparkSession
import sys
import subprocess
import pyspark

def test():
    spark = SparkSession.builder.appName("TestSpark").getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()

def check_environment():
    # 检查 Spark 版本
    spark_version = None
    try:
        
        spark_version = pyspark.__version__
        print(f"✅ Spark version: {spark_version}")
    except ImportError:
        print("⚠️  Spark (pyspark) is not installed.")
    except Exception as e:
        print(f"⚠️  Failed to detect Spark version: {e}")

    # 检查 Java 版本
    java_version = None
    try:
        result = subprocess.run(
            ["java", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stderr if result.stderr else result.stdout
        # Java version info is usually in the first line
        first_line = output.splitlines()[0] if output else ""
        # Try to extract version number
        import re
        m = re.search(r'version "([^"]+)"', first_line)
        if m:
            java_version = m.group(1)
            print(f"✅ Java version: {java_version}")
        else:
            print("⚠️  Failed to parse Java version output.")
    except FileNotFoundError:
        print("⚠️  Java is not installed or not in PATH.")
    except Exception as e:
        print(f"⚠️  Failed to detect Java version: {e}")

    # 检查 Python 版本
    try:
        python_version = sys.version.split()[0]
        print(f"✅ Python version: {python_version}")
    except Exception as e:
        print(f"⚠️  Failed to detect Python version: {e}")

    # 检查整体环境
    if spark_version and java_version:
        print("✅ Environment ready!")
    else:
        print("⚠️  Some required components are missing or not detected correctly.")

# Local（本地模式）
def local():

    spark = SparkSession.builder.appName("LocalTest").master("local[*]").getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()
# Standalone（独立集群模式）
# SPARK_HOME="$(brew --prefix apache-spark)/libexec"
# "$SPARK_HOME/sbin/start-master.sh"
# "$SPARK_HOME/sbin/start-worker.sh" "spark://127.0.0.1:7077"
# start-master.sh
# start-worker.sh spark://127.0.0.1:7077
# # 或一键
# start-all.sh

# 一键启动/停止 Master+Worker：
# $SPARK_HOME/sbin/start-all.sh
# $SPARK_HOME/sbin/stop-all.sh
# 在终端设置环境变量，让 Standalone Master/Worker 都使用你虚拟环境的 Python 3.13：
# export PYSPARK_PYTHON=/Users/adam/envs/py_arm64/bin/python
# export PYSPARK_DRIVER_PYTHON=/Users/adam/envs/py_arm64/bin/python

# # 然后重启 Spark Standalone
# $SPARK_HOME/sbin/stop-all.sh
# $SPARK_HOME/sbin/start-all.sh
def standalone():
    spark = SparkSession.builder \
    .appName("StandaloneTest") \
    .master("spark://127.0.0.1:7077") \
    .getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()
# YARN（Hadoop 集群模式）
# export HADOOP_CONF_DIR=/opt/homebrew/opt/hadoop/libexec/etc/hadoop
# export YARN_CONF_DIR=/opt/homebrew/opt/hadoop/libexec/etc/hadoop
def YARN():
    spark = SparkSession.builder \
    .appName("YARNTest") \
    .master("yarn") \
    .getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()
# Mesos（Apache Mesos 集群模式）
def mesos():
    spark = SparkSession.builder \
    .appName("MesosTest") \
    .master("mesos://mesos-master:5050") \
    .getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()
    
# Kubernetes（容器集群模式）
def kubernetes():
    spark = SparkSession.builder \
    .appName("K8sTest") \
    .master("k8s://https://<k8s-apiserver>") \
    .config("spark.kubernetes.container.image", "<spark-image>") \
    .getOrCreate()
    df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
    df.show()
    spark.stop()
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    # check_environment()
    try:
        standalone()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:
        print(f"{speter*2}Finished{speter*2}")


