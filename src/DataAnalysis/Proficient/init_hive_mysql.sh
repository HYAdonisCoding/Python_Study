# ----------------------------
# Hive 4.1.0 MySQL 元数据库初始化
# ----------------------------
MYSQL_JAR="$HIVE_HOME/lib/mysql-connector-j-8.1.0.jar"
if ! jar tf "$MYSQL_JAR" >/dev/null 2>&1; then
  echo "❌ MySQL JDBC jar 文件损坏或不存在: $MYSQL_JAR"
  echo "请重新下载: https://dev.mysql.com/downloads/connector/j/"
  exit 1
fi

# 1. 设置环境变量
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH=$JAVA_HOME/bin:$PATH
export HIVE_HOME=~/opt/apache-hive-4.1.0-bin
export PATH=$HIVE_HOME/bin:$PATH
export HIVE_AUX_JARS_PATH=$HIVE_HOME/lib/mysql-connector-java-8.1.0.jar
# 关键：强制将 JDBC jar 加入 Hive 的 classpath
export HIVE_CLASSPATH=$HIVE_HOME/lib/mysql-connector-java-8.1.0.jar

# 2. 检查 MySQL JDBC jar 是否存在
if [ ! -f "$HIVE_AUX_JARS_PATH" ]; then
    echo "Error: MySQL JDBC jar not found at $HIVE_AUX_JARS_PATH"
    exit 1
fi

# 3. 初始化 MySQL 元数据库
# java -cp "$HIVE_HOME/conf:$HIVE_HOME/lib/*:$HIVE_AUX_JARS_PATH" \
#   org.apache.hadoop.hive.metastore.tools.SchemaTool \
#   -dbType mysql -initSchema


# java -cp "$HIVE_HOME/conf:\
# $HIVE_HOME/lib/hive-metastore-4.1.0.jar:\
# $HIVE_HOME/lib/hive-common-4.1.0.jar:\
# $HIVE_HOME/lib/hive-exec-4.1.0.jar:\
# $HIVE_HOME/lib/mysql-connector-java-8.1.0.jar" \
# org.apache.hadoop.hive.metastore.tools.SchemaTool \
# -dbType mysql -initSchema


# $HIVE_HOME/bin/schematool -dbType mysql -initSchema
# ~/opt/apache-hive-4.1.0-bin/bin/schematool -dbType mysql -initSchema

# java -cp "$HIVE_HOME/conf:\
# $HIVE_HOME/lib/hive-metastore-4.1.0.jar:\
# $HIVE_HOME/lib/hive-common-4.1.0.jar:\
# $HIVE_HOME/lib/hive-exec-4.1.0.jar:\
# $HIVE_HOME/lib/mysql-connector-java-8.1.0.jar:\
# $HIVE_HOME/lib/*" \
# org.apache.hadoop.hive.metastore.tools.SchemaTool \
# -dbType mysql \
# -initSchema \
# --verbose

# $HIVE_HOME/bin/schematool \
#   -dbType mysql \
#   -driver com.mysql.cj.jdbc.Driver \
#   -url "jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true&useSSL=false" \
#   -userName eason \
#   -passWord chy123 \
#   -initSchema \
#   --verbose

$HIVE_HOME/bin/schematool \
  -dbType mysql \
  -driver com.mysql.cj.jdbc.Driver \
  -url "jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true" \
  -userName eason \
  -passWord chy123 \
  -initSchema \
  --verbose