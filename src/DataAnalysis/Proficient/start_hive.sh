#!/bin/bash
# File: start_hive.sh
# Description: Start HDFS, Hive Metastore, HiveServer2 and connect Beeline
# Usage: ./start_hive.sh start|stop|restart|beeline

set -uo pipefail
IFS=$'\n\t'

HADOOP_HOME=/opt/homebrew/opt/hadoop/libexec
HIVE_HOME=/opt/homebrew/Cellar/apache-hive/4.1.0
BEELINE="$HIVE_HOME/bin/beeline"
METASTORE_LOG="$HIVE_HOME/logs/metastore.log"
HIVESERVER2_LOG="$HIVE_HOME/logs/hiveserver2.log"

HIVE_USER=${USER:-eason}

mkdir -p "$HIVE_HOME/logs"

# Ensure env consistency
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-$HADOOP_HOME/etc/hadoop}
if [ "${HIVE_CONF_DIR:-}" != "$HIVE_HOME/conf" ]; then
  echo "⚠️  Detected non-default HIVE_CONF_DIR: ${HIVE_CONF_DIR:-<unset>}"
  echo "   Switching HIVE_CONF_DIR -> $HIVE_HOME/conf"
  export HIVE_CONF_DIR=$HIVE_HOME/conf
fi
export HIVE_CONF_DIR

# Helper: wait for TCP port
wait_for_port() {
  local host=${1:-localhost}
  local port=${2:?}
  local timeout=${3:-60}
  local i=0
  while ! nc -z $host $port 2>/dev/null; do
    ((i++))
    if [ $i -ge $timeout ]; then
      return 1
    fi
    sleep 1
  done
  return 0
}

# Helper: check for obvious bad file://file entries in conf
check_bad_fs() {
  local bad=0
  for f in "$HIVE_CONF_DIR"/core-site.xml "$HIVE_CONF_DIR"/hive-site.xml; do
    [ -f "$f" ] || continue
    if grep -q "file://file" "$f"; then
      echo "ERROR: Found 'file://file' in $f -- this will break Hadoop/Hive FS parsing."
      bad=1
    fi
  done
  return $bad
}

cleanup_cache() {
  echo "Cleaning Hive/DataNucleus cache..."
  rm -rf /tmp/hive-* /tmp/datanucleus-* ~/.hive
}

start_hive() {
  cleanup_cache

  echo "Starting HDFS..."
  "$HADOOP_HOME/sbin/start-dfs.sh"

  # Quick HDFS sanity check
  if ! hdfs dfs -ls / >/dev/null 2>&1; then
    echo "WARNING: hdfs dfs -ls / failed. Ensure NameNode is running and fs.defaultFS is correct."
  fi

  # pre-check configs
#   if check_bad_fs; then
#     echo "Please fix the bad URI(s) above (replace file://file -> file:/// or use hdfs://). Aborting start."
#     return 1
#   fi

  # MySQL driver and Tez jars for auxpath
  MYSQL_JAR="/opt/homebrew/Cellar/apache-hive/4.1.0/lib/mysql-connector-java-8.1.0.jar"
  TEZ_JARS="/Users/adam/opt/tez/apache-tez-0.10.5-bin/tez-api-0.10.5.jar:/Users/adam/opt/tez/apache-tez-0.10.5-bin/tez-common-0.10.5.jar"
  AUXPATH="$MYSQL_JAR:$TEZ_JARS"

  echo "正在启动 Hive Metastore... 日志 -> $METASTORE_LOG"
  nohup "$HIVE_HOME/bin/hive" \
    --auxpath "$AUXPATH" \
    --service metastore >"$METASTORE_LOG" 2>&1 &
  METASTORE_PID=$!
  echo "Metastore PID: $METASTORE_PID"

  echo "等待 Hive Metastore (端口 9083) 启动完成..."
  if wait_for_port localhost 9083 60; then
    echo "Hive Metastore 已启动，端口 9083 可用。"
  else
    echo "Metastore did not become ready within timeout. See last 200 lines of log:" 
    tail -n 200 "$METASTORE_LOG" | sed -n '1,200p'
    return 1
  fi

  echo "正在启动 HiveServer2... 日志 -> $HIVESERVER2_LOG"
  nohup "$HIVE_HOME/bin/hive" \
    --auxpath "$AUXPATH" \
    --hiveconf fs.file.impl=org.apache.hadoop.fs.LocalFileSystem \
    --hiveconf fs.file.impl.disable.cache=true \
    --service hiveserver2 >"$HIVESERVER2_LOG" 2>&1 &
  HIVESERVER2_PID=$!
  echo "HiveServer2 PID: $HIVESERVER2_PID"

  echo "等待 HiveServer2 (端口 10000) 启动完成..."
  if wait_for_port localhost 10000 160; then
    echo "HiveServer2 已启动，端口 10000 可用，启动完成。"
  else
    echo "HiveServer2 did not start within timeout. Tail hive server log:" 
    tail -n 200 "$HIVESERVER2_LOG" | sed -n '1,200p'
    return 1
  fi

  echo "Hive started. Use './start_hive.sh beeline' to connect Beeline."
}

stop_hive() {
  echo "Stopping HiveServer2..."
  pkill -f 'hive --service hiveserver2' || true
  echo "Stopping Hive Metastore..."
  pkill -f 'hive --service metastore' || true
  echo "Stopping HDFS..."
  "$HADOOP_HOME/sbin/stop-dfs.sh"
}

restart_hive() {
  stop_hive
  sleep 2
  start_hive
}

start_beeline() {
  echo "Checking HiveServer2 port 10000..."
  if ! wait_for_port localhost 10000 10; then
    echo "HiveServer2 is not listening on 10000. Start hive first: ./start_hive.sh start"
    return 1
  fi
  echo "Connecting Beeline..."
  "$BEELINE" -u jdbc:hive2://localhost:10000 -n "$HIVE_USER"
}

case "${1:-}" in
  start)
    start_hive
    ;;
  stop)
    stop_hive
    ;;
  restart)
    restart_hive
    ;;
  beeline)
    start_beeline
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|beeline}"
    exit 1
    ;;
esac