#!/usr/bin/env python3
# coding: utf-8

import json
from operator import add
from pyspark import SparkConf, SparkContext, StorageLevel
import os

os.environ["SPARK_CONF_DIR"] = (
    "/Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient"
)
# 全面静音配置
os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--conf spark.ui.showConsoleProgress=false "
    "--conf spark.driver.extraJavaOptions='-Dorg.apache.commons.logging.Log=org.apache.commons.logging.impl.NoOpLog "
    "--add-opens=java.base/java.nio=ALL-UNNAMED "
    "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED "
    "--add-opens=java.base/java.util=ALL-UNNAMED "
    "--add-opens=java.base/java.lang=ALL-UNNAMED "
    "--add-opens=java.base/java.io=ALL-UNNAMED' "
    "pyspark-shell"
)
os.environ["HADOOP_OPTS"] = "-Djava.library.path="
os.environ["JAVA_TOOL_OPTIONS"] = "--add-opens=java.base/java.lang=ALL-UNNAMED"
speter = "-" * 10

# 第四篇
# 15 Spark RDD 编程 Spark RDD Programming
# # 启动环境
# unset PYSPARK_DRIVER_PYTHON
# unset PYSPARK_DRIVER_PYTHON_OPTS
# unset SPARK_CONNECT_MODE

# export PYSPARK_PYTHON=/Users/adam/envs/py_arm64/bin/python
# export PYSPARK_DRIVER_PYTHON=/Users/adam/envs/py_arm64/bin/python

# $SPARK_HOME/bin/pyspark
# $HADOOP_HOME/sbin/start-dfs.sh


def f1(item):
    return item, 1


def f2(item):
    return item > 1


def f3(item1, item2):
    return item1 + item2


# RDD 依赖关系
def test():
    # 1️⃣ 初始化 SparkContext
    conf = SparkConf().setAppName("SparkRDDTest").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    print("SparkContext Version", sc.version)
    # 2️⃣ 创建 RDD
    data = [1, 2, 3, 4, 5, 6]
    rdd = sc.parallelize(data)

    # 3️⃣ 定义函数
    def f1(x):
        return x * 2

    def f2(x):
        return x > 5

    def f3(a, b):
        return a + b

    # 4️⃣ RDD 操作
    result = rdd.map(f1).filter(f2).reduce(f3)

    print(f"✅ 计算结果：{result}")

    # 5️⃣ 停止 SparkContext
    sc.stop()


# 读取外部数据源创建RDD
def read_outer_data():
    # 1️⃣ 初始化 SparkContext
    conf = SparkConf().setAppName("ReadOuterData").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")

    try:
        # 创建一个测试文件
        test_file_path = "/tmp/spark_test.txt"
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("Hello Spark\n")
            f.write("This is a test file\n")
            f.write("For Spark RDD operations\n")

        # 读取本地文件创建RDD
        rdd = sc.textFile(f"file://{test_file_path}")

        # 显示文件内容
        print("📄 文件内容:")
        lines = rdd.collect()
        for line in lines:
            print(f"  {line}")

        # 统计行数
        line_count = rdd.count()
        print(f"📊 文件总行数: {line_count}")

        # 清理测试文件
        os.remove(test_file_path)

    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        # 停止 SparkContext
        sc.stop()


# HDFS文件操作示例
def hdfs_operations():
    """
    HDFS文件操作示例
    注意：需要先启动Hadoop和HDFS服务
    """
    print("🚀 开始HDFS操作示例...")

    # 1️⃣ 初始化 SparkContext
    conf = SparkConf().setAppName("HDFSOperations").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")

    try:
        # 创建测试文件
        local_file = "/tmp/hdfs_test.txt"
        hdfs_path = "/user/spark/test_file.txt"

        # 写入测试数据
        with open(local_file, "w", encoding="utf-8") as f:
            f.write("这是HDFS测试文件\n")
            f.write("包含中文内容\n")
            f.write("用于演示Spark读取HDFS文件\n")
            f.write("数据1,数据2,数据3\n")
            f.write("100,200,300\n")

        print(f"✅ 已创建本地测试文件: {local_file}")

        # 方法1: 使用Hadoop命令上传文件到HDFS (需要手动执行)
        print("📝 手动上传文件到HDFS的命令:")
        print(f"   hadoop fs -mkdir -p /user/spark")
        print(f"   hadoop fs -put {local_file} {hdfs_path}")
        print(f"   hadoop fs -ls /user/spark")

        # 方法2: 使用Python的hdfs3库上传文件 (可选)
        try:
            import hdfs3  # type: ignore

            hdfs = hdfs3.HDFileSystem()
            if hdfs.exists("/user/spark"):
                hdfs.rm("/user/spark", recursive=True)
            hdfs.makedirs("/user/spark")
            hdfs.put(local_file, hdfs_path)
            print(f"✅ 已使用hdfs3库上传文件到HDFS: {hdfs_path}")
        except ImportError:
            print("⚠️  hdfs3库未安装，跳过自动上传")
        except Exception as e:
            print(f"⚠️  HDFS上传失败: {e}")

        # 读取HDFS文件
        print("📖 尝试读取HDFS文件...")
        try:
            # 读取HDFS文件
            rdd = sc.textFile(hdfs_path)

            # 显示文件内容
            print("📄 HDFS文件内容:")
            lines = rdd.collect()
            for line in lines:
                print(f"  {line}")

            # 统计行数
            line_count = rdd.count()
            print(f"📊 HDFS文件总行数: {line_count}")

            # 数据处理示例
            print("🔍 数据处理示例:")

            # 过滤包含"数据"的行
            filtered_rdd = rdd.filter(lambda line: "数据" in line)
            filtered_lines = filtered_rdd.collect()
            print(f"  包含'数据'的行: {filtered_lines}")

            # 统计每行的字符数
            char_count_rdd = rdd.map(lambda line: len(line))
            char_counts = char_count_rdd.collect()
            print(f"  每行字符数: {char_counts}")

        except Exception as e:
            print(f"❌ 读取HDFS文件失败: {e}")
            print("💡 请确保:")
            print("   1. Hadoop和HDFS服务已启动")
            print("   2. 文件已上传到HDFS")
            print("   3. HDFS路径正确")

        # 清理本地文件
        os.remove(local_file)

    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        # 停止 SparkContext
        sc.stop()


# 完整的HDFS操作流程示例
def complete_hdfs_workflow():
    """
    完整的HDFS工作流程示例
    """
    print("🔄 完整HDFS工作流程示例...")

    # 1️⃣ 初始化 SparkContext
    conf = SparkConf().setAppName("CompleteHDFSWorkflow").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")

    try:
        # 创建多个测试文件
        files_data = [
            ("file1.txt", ["用户1,购买,100", "用户2,购买,200", "用户3,退款,50"]),
            ("file2.txt", ["用户4,购买,150", "用户5,购买,300", "用户6,退款,75"]),
            ("file3.txt", ["用户7,购买,250", "用户8,购买,400", "用户9,退款,100"]),
        ]

        hdfs_base_path = "/user/spark/sales_data"

        # 创建本地文件
        local_files = []
        for filename, data in files_data:
            local_file = f"/tmp/{filename}"
            with open(local_file, "w", encoding="utf-8") as f:
                for line in data:
                    f.write(line + "\n")
            local_files.append((local_file, f"{hdfs_base_path}/{filename}"))
            print(f"✅ 创建本地文件: {local_file}")

        # 显示上传命令
        print("\n📝 上传文件到HDFS的命令:")
        print(f"hadoop fs -mkdir -p {hdfs_base_path}")
        for local_file, hdfs_file in local_files:
            print(f"hadoop fs -put {local_file} {hdfs_file}")

        # 读取HDFS目录中的所有文件
        print(f"\n📖 读取HDFS目录: {hdfs_base_path}")
        try:
            # 读取整个目录
            rdd = sc.textFile(hdfs_base_path)

            print("📄 所有文件内容:")
            lines = rdd.collect()
            for line in lines:
                print(f"  {line}")

            # 数据分析示例
            print("\n🔍 数据分析:")

            # 解析数据并计算总销售额
            sales_rdd = rdd.filter(lambda line: "购买" in line)
            sales_amounts = sales_rdd.map(lambda line: int(line.split(",")[2]))
            total_sales = sales_amounts.sum()
            print(f"  总销售额: {total_sales}")

            # 统计退款金额
            refund_rdd = rdd.filter(lambda line: "退款" in line)
            refund_amounts = refund_rdd.map(lambda line: int(line.split(",")[2]))
            total_refunds = refund_amounts.sum()
            print(f"  总退款额: {total_refunds}")

            # 计算净销售额
            net_sales = total_sales - total_refunds
            print(f"  净销售额: {net_sales}")

        except Exception as e:
            print(f"❌ 读取HDFS目录失败: {e}")

        # 清理本地文件
        for local_file, _ in local_files:
            os.remove(local_file)

    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        sc.stop()


# 使用数组创建RDD
def array_RDD():
    sc = SparkContext()
    rdd = sc.parallelize([0, 1, 2, 3, 4, 6], 5)
    print(rdd.getNumPartitions())
    print(rdd.count())


# 转换操作
def conversion_Operation():
    print(f"{speter*2}使用map转换数据{speter*2}")
    sc = SparkContext()
    rdd1 = sc.parallelize([0, 1, 2, 3, 4, 6])
    rdd2 = rdd1.map(lambda x: x * 2)
    local_data = rdd2.collect()
    [print("当前元素是：", item) for item in local_data]

    print(f"{speter*2}使用 flatMap 转换数据{speter*2}")
    # sc = SparkContext()
    rdd1 = sc.parallelize(["lesson1 spark", "lesson2 hadoop", "lesson3 hive"])
    rdd2 = rdd1.flatMap(lambda x: x.split(" "))
    local_data = rdd2.collect()
    [print("当前元素是：", item) for item in local_data]

    print(f"{speter*2}使用 filter 转换数据{speter*2}")
    rdd1 = sc.parallelize([0, 1, 2, 3, 4, 6])
    rdd2 = rdd1.filter(lambda x: x > 3)
    local_data = rdd2.collect()
    [print("当前元素是：", item) for item in local_data]

    print(f"{speter*2}使用 groupByKey 将数据分组{speter*2}")
    rdd1 = sc.parallelize([("a", 1), ("a", 1), ("a", 1), ("b", 1), ("b", 1), ("c", 1)])
    list1 = rdd1.groupByKey().mapValues(len).collect()
    [print("按key分组后的数据项： ", item) for item in list1]
    list2 = rdd1.groupByKey().mapValues(list).collect()
    [print("每一个key对应的数据：", item) for item in list2]

    print(f"{speter*2}使用 reduceByKey 将数据分组{speter*2}")
    rdd1 = sc.parallelize(["Spark", "Spark", "hadoop", "hadoop", "hadoop", "hive"])
    rdd2 = rdd1.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).collect()
    [print("当前元素是： ", item) for item in rdd2]

    print(f"{speter*2}使用 union 合并RDD{speter*2}")
    rdd1 = sc.parallelize(["Spark", "hadoop", "hive"])
    rdd2 = sc.parallelize(["Spark", "kafka", "hbase"])
    rdd3 = rdd1.union(rdd2).collect()
    print("合并结果： ", rdd3)

    print(f"{speter*2}使用 distinct 去除重复数据{speter*2}")
    rdd1 = sc.parallelize(["Spark", "hadoop", "hive"])
    rdd2 = sc.parallelize(["Spark", "kafka", "hbase"])
    rdd3 = rdd1.union(rdd2).distinct().collect()
    print("去除重复项结果： ", rdd3)


# 行动操作
def action_operation():
    print(f"{speter*2}使用 count 计算数据总数{speter*2}")
    sc = SparkContext()
    rdd = sc.parallelize(["Spark", "hadoop", "hive"])
    result = rdd.count()
    print("rdd元素个数", result)

    print(f"{speter*2}使用 first 获取第一项{speter*2}")
    rdd = sc.parallelize([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)])
    result = rdd.sortBy(lambda x: x[1], False).first()
    print("当前元素是：", result)

    print(f"{speter*2}使用 take 获取前n项{speter*2}")
    rdd = sc.parallelize([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)])
    result = rdd.sortBy(lambda x: x[1], False).take(3)
    print("当前元素是：", result)

    print(f"{speter*2}使用 reduce {speter*2}")
    rdd = sc.parallelize([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)])

    result = rdd.map(lambda x: x[1]).reduce(add)
    print("当前结果：", result)

    print(f"{speter*2}使用 foreach {speter*2}")
    rdd = sc.parallelize([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)], 2)

    def f(x):
        print("当前数据项：", x)

    result = rdd.foreach(f)

    print(f"{speter*2}使用 foreachPartition {speter*2}")
    rdd = sc.parallelize([("a", 1), ("b", 2), ("c", 3), ("d", 4), ("e", 5)], 2)

    def f(iterator):
        print(list(iterator))

    result = rdd.foreachPartition(f)


# 键值对RDD
# # 把文件从 /user/adam/bigdata/chapter 拷贝到 /bigdata/chapter
# hdfs dfs -cp /user/adam/bigdata/chapter/a_seafood.txt /bigdata/chapter/
def key_value_pairs_RDD():
    print(f"{speter*2}读取外部文件创建Pair RDD{speter*2}")
    sc = SparkContext()
    rdd1 = sc.textFile("/bigdata/chapter/a_seafood.txt")
    # rdd1 = sc.textFile("hdfs:///user/adam/bigdata/chapter/a_seafood.txt")

    def func(item):
        data = item.split(":")
        return data[0], data[1]

    rdd2 = rdd1.map(func)
    result = rdd2.collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]

    print(f"{speter*2}使用数组创建Pair RDD{speter*2}")
    # sc = SparkContext()
    rdd1 = sc.parallelize(["黑虎虾,扇贝,黄花鱼,鲈鱼,罗非鱼,鲜贝,阿根廷红虾"])

    rdd2 = rdd1.flatMap(lambda item: item.split(",")).map(lambda item: (item, 1))
    result = rdd2.collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]

    print(f"{speter*2}常见的键值对转换操作{speter*2}")

    rdd1 = sc.parallelize(["黑虎虾,扇贝,黄花鱼,鲈鱼,罗非鱼,鲜贝,阿根廷红虾"])
    rdd2 = rdd1.flatMap(lambda item: item.split(",")).map(lambda item: (item, 1))

    print("当前key是：", rdd2.keys().collect())
    print("当前value是：", rdd2.values().collect())

    print(f"{speter*2}使用 lookup 进行查找{speter*2}")
    rdd1 = sc.textFile("/bigdata/chapter/a_seafood.txt")

    def func(item):
        data = item.split(":")
        return data[0], data[1]

    rdd2 = rdd1.map(func)
    result = rdd2.lookup("罗非鱼")
    print("罗非鱼价格：", result)

    print(f"{speter*2}使用 zip 组合 RDD{speter*2}")
    rdd1 = sc.parallelize([139, 16.9, 49.9, 35.9, 29.9], 3)
    rdd2 = sc.parallelize(["黑虎虾", "扇贝", "黄花鱼", "鲈鱼", "罗非鱼"], 3)

    result = rdd2.zip(rdd1).collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]

    print(f"{speter*2}使用 join 连接两个 RDD{speter*2}")
    rdd1 = sc.parallelize([("黑虎虾", 100), ("扇贝", 10.2), ("鲈鱼", 59.9)])
    rdd2 = sc.parallelize(
        [("黑虎虾", 139), ("扇贝", 16.9), ("鲈鱼", 35.9), ("罗非鱼", 29.9)]
    )

    result = rdd1.join(rdd2).collect()
    print("join结果是：", result)

    print(f"{speter*2}使用 leftOuterJoin 连接两个 RDD{speter*2}")
    rdd1 = sc.parallelize([("黑虎虾", 100), ("扇贝", 10.2), ("海参", 59.9)])
    rdd2 = sc.parallelize(
        [("黑虎虾", 139), ("扇贝", 16.9), ("鲈鱼", 35.9), ("罗非鱼", 29.9)]
    )

    result = rdd1.leftOuterJoin(rdd2).collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]
    print(f"{speter*2}使用 rightOuterJoin 连接两个 RDD{speter*2}")
    result2 = rdd1.rightOuterJoin(rdd2).collect()

    [f(item) for item in result2]

    print(f"{speter*2}使用 fullOuterJoin 连接两个 RDD{speter*2}")
    rdd1 = sc.parallelize([("黑虎虾", 100), ("扇贝", 10.2), ("海参", 59.9)])
    rdd2 = sc.parallelize(
        [("黑虎虾", 139), ("扇贝", 16.9), ("鲈鱼", 35.9), ("罗非鱼", 29.9)]
    )

    result = rdd1.fullOuterJoin(rdd2).collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]

    print(f"{speter*2}使用 combineByKey{speter*2}")
    rdd = sc.parallelize(
        [
            ("黑虎虾", 139),
            ("黑虎虾", 100),
            ("扇贝", 16.9),
            ("扇贝", 10.2),
            ("海参", 59.9),
            ("鲈鱼", 35.9),
            ("罗非鱼", 29.9),
        ]
    )

    def to_list(a):
        return [a]

    def append(a, b):
        a.append(b)
        return a

    def extend(a, b):
        a.extend(b)
        return a

    result = rdd.combineByKey(to_list, append, extend).collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]


# 文件读写
# hdfs dfs -mkdir -p /spark/files
# hdfs dfs -cp /Users/adam/Documents/Developer/MyGithub/Python_Study/README.md /spark/files/
# hdfs dfs -put /Users/adam/Documents/Developer/MyGithub/Python_Study/README.md /spark/files/
# 验证文件是否上传成功 hdfs dfs -ls /spark/files/
def file_reading_writing():
    print(f"{speter*2}读取 HDFS 并保存到本地{speter*2}")
    sc = SparkContext()
    rdd = sc.textFile("/spark/files/README.md")
    # rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y).saveAsTextFile(
    #     "file:///tmp/filter_rdd_result/result.txt")

    print(f"{speter*2}读取 HDFS 并保存到 HDFS{speter*2}")
    # rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda x, y: x + y).saveAsTextFile(
    # "/spark/files/filter_rdd/result.txt")

    print(f"{speter*2}读取 本地文件 并保存到 HDFS{speter*2}")
    rdd = sc.textFile(
        "file:///Users/adam/Documents/Developer/MyGithub/Python_Study/README.md"
    )
    rdd.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(
        lambda x, y: x + y
    ).saveAsTextFile("/spark/files/filter_rdd/result1.txt")


# 编程进阶
def advanced_Programming():
    print(f"{speter*2}分区 partitionBy{speter*2}")
    sc = SparkContext()

    pairs = sc.parallelize(
        [("黑虎虾", 139), ("扇贝", 16.9), ("鲈鱼", 35.9), ("罗非鱼", 29.9)]
    )
    sets = pairs.partitionBy(2).glom().collect()
    print(sets)

    print(f"{speter*2}自定义分区{speter*2}")
    pairs = sc.parallelize(
        [
            ("高品质", "黑虎虾"),
            ("一般品质", "扇贝"),
            ("高品质", "鲈鱼"),
            ("一般品质", "罗非鱼"),
        ]
    )

    def custom_partition(key):
        if key == "高品质":
            return 0
        else:
            return 1

    sets = pairs.partitionBy(2, partitionFunc=custom_partition).glom().collect()
    print(sets)

    print(f"{speter*2}重分区 coalesce{speter*2}")
    data = [
        ("高品质", "黑虎虾"),
        ("一般品质", "扇贝"),
        ("高品质", "鲈鱼"),
        ("一般品质", "罗非鱼"),
    ]
    sets1 = sc.parallelize(data, 4).glom().collect()
    print(sets1)
    sets2 = sc.parallelize(data, 4).coalesce(1).glom().collect()
    print(sets2)

    print(f"{speter*2}持久化 persist{speter*2}")
    data = [1, 2, 3, 4, 5, 6]

    def show(item):
        print("当前元素", item)
        return item * 2

    rdd = sc.parallelize(data, 4).map(lambda x: show(x))
    rdd.persist(StorageLevel.MEMORY_ONLY)
    print("获取最小值：", rdd.min())
    print("获取最大值：", rdd.max())

    print(f"{speter*2}广播变量{speter*2}")
    list1 = [2]
    broadcast = sc.broadcast(list1)

    list2 = [4, 5, 6]

    def f(item):
        broadcast_value = broadcast.value
        return item, broadcast_value[0]

    data = sc.parallelize(list2, 4).map(lambda x: f(x)).collect()

    [print("当前元素是：", item) for item in data]

    print(f"{speter*2}累加器{speter*2}")
    list1 = [1, 2, 3, 4, 5, 6]

    accumulator = sc.accumulator(0)

    def f(item):
        accumulator.add(1)
        print("当前元素是：", item)

    data = sc.parallelize(list1, 4).foreach(lambda item: f(item))
    print("循环次数：", accumulator.value)

    print(f"{speter*2}json 转换为Pair RDD{speter*2}")
    # package.json
    rdd = sc.textFile(
        "file:///Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/package_test.json"
    )

    def f(line):
        array = line.split(":")
        return array[0], array[1]

    # rdd.map(lambda line:f(line))
    def parse_json(line):
        try:
            data = json.loads(line)
            # 遍历 dependencies 字段
            deps = data.get("dependencies", {})
            # 返回 (name, version) 的列表
            # print(deps)
            return list(deps.items())
        except json.JSONDecodeError as e:
            print("JSONDecodeError", e)
            return []

    # flatMap 展开每个依赖
    pair_rdd = rdd.flatMap(parse_json)
    result = pair_rdd.collect()
    for item in result:
        print(item)

    print(f"{speter*2}checkpoint{speter*2}")

    sc.setCheckpointDir("/spark/checkpoint")
    rdd1 = sc.parallelize([1, 2, 3, 4, 5, 6])
    rdd2 = rdd1.map(lambda x: x * 2)
    rdd2.cache()
    rdd2.checkpoint()
    rdd2.sum()


# 统计海鲜销售情况
# hdfs dfs -put /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/a_seal.txt /bigdata/chapter/
# hdfs dfs -put /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/b_seal.txt /bigdata/chapter/
# 验证文件是否上传成功 hdfs dfs -ls /bigdata/chapter/
def statistics_on_seafood_sales():
    print(f"{speter*2}统计海鲜销售情况{speter*2}")
    sc = SparkContext()
    a_rdd = sc.textFile("/bigdata/chapter/a_seal.txt")
    b_rdd = sc.textFile("/bigdata/chapter/b_seal.txt")
    print(f"{speter*2}统计各商品总销量{speter*2}")
    union_rdd = a_rdd.union(b_rdd)

    def f(item):
        tmp = item.split(":")
        return tmp[0], int(tmp[1])

    map_rdd = union_rdd.map(f)
    result = map_rdd.reduceByKey(lambda x, y: x + y).collect()
    [print("当前元素是：", item) for item in result]

    print(f"{speter*2}统计平均销量{speter*2}")

    map_rdd = union_rdd.map(f)
    map_rdd.cache()

    def create_combiner(v):
        return v, 1

    def merge_value(c, v):
        return c[0] + v, c[1] + 1

    def merge_combiners(c1, c2):
        return c1[0] + c2[0], c1[1] + c2[1]

    rdd = map_rdd.combineByKey(create_combiner, merge_value, merge_combiners)
    result = rdd.map(lambda x: (x[0], x[1][0] / x[1][1])).collect()

    def f(item):
        print("当前元素是：", item)

    [f(item) for item in result]

    print(f"{speter*2}统计销量排名{speter*2}")

    def f1(item):
        tmp = item.split(":")
        return tmp[0], int(tmp[1])

    a_map_rdd = a_rdd.map(f1)
    b_map_rdd = b_rdd.map(f1)
    join_rdd = a_map_rdd.join(b_map_rdd)

    def f2(item):
        return item[0], sum(item[1])

    result = join_rdd.map(f2).sortBy(lambda x: x[1], False).collect()
    [print(item) for item in result]


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        statistics_on_seafood_sales()

    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    except Exception as e:
        print(f"❌ 程序执行错误: {e}")
    finally:
        print(f"{speter*2}Finished{speter*2}")
