#!/bin/bash
HADOOP_HOME=/opt/homebrew/Cellar/hadoop/3.4.2/libexec
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# 启动 HDFS（绕过 nice）
$HADOOP_HOME/bin/hdfs --daemon start namenode
$HADOOP_HOME/bin/hdfs --daemon start datanode
$HADOOP_HOME/bin/hdfs --daemon start secondarynamenode

# 启动 YARN
$HADOOP_HOME/bin/yarn --daemon start resourcemanager
$HADOOP_HOME/bin/yarn --daemon start nodemanager