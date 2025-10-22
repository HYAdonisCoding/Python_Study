# HDFS操作指南

## 1. HDFS环境设置

### 1.1 安装Hadoop
```bash
# 使用Homebrew安装Hadoop (macOS)
brew install hadoop

# 或者下载并手动安装
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.4/hadoop-3.3.4.tar.gz
tar -xzf hadoop-3.3.4.tar.gz
sudo mv hadoop-3.3.4 /opt/hadoop
```

### 1.2 配置环境变量
```bash
# 添加到 ~/.zshrc 或 ~/.bash_profile
export HADOOP_HOME=/opt/hadoop
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

### 1.3 配置Hadoop
编辑 `$HADOOP_HOME/etc/hadoop/core-site.xml`:
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```

编辑 `$HADOOP_HOME/etc/hadoop/hdfs-site.xml`:
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/tmp/hadoop/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/tmp/hadoop/datanode</value>
    </property>
</configuration>
```

## 2. 启动HDFS服务

### 2.1 格式化NameNode (首次启动)
```bash
hdfs namenode -format
```

### 2.2 启动HDFS服务
```bash
# 启动NameNode和DataNode
start-dfs.sh

# 检查服务状态
jps
```

### 2.3 验证HDFS服务
```bash
# 检查HDFS状态
hdfs dfsadmin -report

# 列出根目录
hdfs dfs -ls /
```

## 3. 文件上传到HDFS

### 3.1 使用Hadoop命令
```bash
# 创建目录
hdfs dfs -mkdir -p /user/spark

# 上传单个文件
hdfs dfs -put /local/path/file.txt /user/spark/

# 上传整个目录
hdfs dfs -put /local/directory/ /user/spark/

# 查看上传的文件
hdfs dfs -ls /user/spark/
```

### 3.2 使用Python hdfs3库
```bash
# 安装hdfs3库
pip install hdfs3
```

```python
import hdfs3

# 连接HDFS
hdfs = hdfs3.HDFileSystem()

# 创建目录
hdfs.makedirs('/user/spark')

# 上传文件
hdfs.put('/local/file.txt', '/user/spark/file.txt')

# 列出文件
files = hdfs.ls('/user/spark/')
```

## 4. Spark读取HDFS文件

### 4.1 基本读取
```python
from pyspark import SparkContext

sc = SparkContext()

# 读取HDFS文件
rdd = sc.textFile("hdfs://localhost:9000/user/spark/file.txt")

# 或者使用简写形式 (如果core-site.xml已配置)
rdd = sc.textFile("/user/spark/file.txt")
```

### 4.2 读取整个目录
```python
# 读取目录中的所有文件
rdd = sc.textFile("/user/spark/data/")

# 读取特定文件模式
rdd = sc.textFile("/user/spark/data/*.txt")
```

### 4.3 处理大数据文件
```python
# 设置分区数
rdd = sc.textFile("/user/spark/large_file.txt", minPartitions=4)

# 缓存RDD以提高性能
rdd.cache()

# 执行操作
result = rdd.map(lambda line: line.upper()).collect()
```

## 5. 常用HDFS命令

### 5.1 文件操作
```bash
# 列出文件
hdfs dfs -ls /path/to/directory

# 查看文件内容
hdfs dfs -cat /path/to/file.txt

# 复制文件
hdfs dfs -cp /source /destination

# 移动文件
hdfs dfs -mv /source /destination

# 删除文件
hdfs dfs -rm /path/to/file.txt

# 删除目录
hdfs dfs -rm -r /path/to/directory
```

### 5.2 权限管理
```bash
# 设置权限
hdfs dfs -chmod 755 /path/to/file

# 设置所有者
hdfs dfs -chown user:group /path/to/file
```

### 5.3 监控和统计
```bash
# 查看文件大小
hdfs dfs -du /path/to/directory

# 查看HDFS使用情况
hdfs dfsadmin -report

# 查看NameNode状态
hdfs dfsadmin -safemode get
```

## 6. 故障排除

### 6.1 常见问题
1. **NameNode启动失败**: 检查端口是否被占用
2. **DataNode连接失败**: 检查网络连接和防火墙设置
3. **权限问题**: 确保用户有适当的HDFS权限

### 6.2 日志查看
```bash
# 查看NameNode日志
tail -f $HADOOP_HOME/logs/hadoop-*-namenode-*.log

# 查看DataNode日志
tail -f $HADOOP_HOME/logs/hadoop-*-datanode-*.log
```

## 7. 性能优化

### 7.1 配置优化
- 调整HDFS块大小
- 优化副本数量
- 配置适当的缓冲区大小

### 7.2 Spark优化
- 合理设置分区数
- 使用适当的缓存策略
- 优化数据序列化

## 8. 示例代码

参考 `15.Spark_RDD.py` 文件中的完整示例，包括：
- 基础HDFS操作
- 文件上传和读取
- 数据处理和分析
- 错误处理和异常管理
