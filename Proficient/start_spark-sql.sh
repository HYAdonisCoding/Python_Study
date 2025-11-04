#!/bin/bash

# ---------------------------------------
# Spark SQL 启动脚本（本地 Metastore，Hive MySQL 驱动支持）
# ---------------------------------------

# 日志文件
LOG_DIR=~/Documents/Developer/spark_logs
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/start_$(date +%Y%m%d_%H%M%S).log"

# Hive JDBC 驱动
HIVE_DRIVER_JAR="file:///opt/homebrew/Cellar/apache-hive/4.1.0/lib/mysql-connector-java-8.1.0.jar"

# Spark Warehouse 目录
WAREHOUSE_DIR="file:///Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/spark-warehouse"

# 启动 spark-sql
$SPARK_HOME/bin/spark-sql \
  --master local[*] \
  --driver-class-path "$HIVE_DRIVER_JAR" \
  --jars "$HIVE_DRIVER_JAR" \
  --conf spark.driver.bindAddress=127.0.0.1 \
  --conf spark.driver.host=127.0.0.1 \
  --conf spark.blockManager.port=6066 \
  --conf spark.sql.warehouse.dir="$WAREHOUSE_DIR" \
  2>&1 | tee "$LOG_FILE"

echo "Spark SQL 启动完成，日志文件: $LOG_FILE"