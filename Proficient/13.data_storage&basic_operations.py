#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# 大数据存储与快速分析 Big data storage and rapid analysis
# 13 Hadoop数据存储与基本操作  Hadoop data storage and basic operations

# HDFS 文件的读写流程（Hadoop Distributed File System）。

# 🌳 一、先认识一下HDFS的结构

# HDFS 有三个“角色”：
# 	1.	NameNode（名字节点）：
# → 管家，负责记账。
# 它不存数据，只存“谁住在哪儿”这类信息（即文件到块、块到DataNode的映射表）。
# 	2.	DataNode（数据节点）：
# → 仓库工人。
# 真正存文件数据的机器。
# 	3.	Client（客户端）：
# → 用户。
# 就是我们写程序、上传或下载文件时用的接口。

# ⸻

# ✏️ 二、写文件流程（Client → HDFS）

# 场景：你往HDFS里写入一个大文件，比如 1GB。

# 1️⃣ 客户端请求 NameNode：

# 客户端说：“我要上传 /user/eason/data.txt，行不行？”
# → NameNode 检查权限、空间等，然后说：“可以，我给你分配几个数据块。”

# 2️⃣ NameNode 分块规划：

# HDFS 默认块大小是 128MB，所以 1GB 文件会被切成 8 个块（Block）。
# NameNode 给每个块分配要存放的 DataNode，比如：

# Block1 → DataNode1, DataNode2, DataNode3
# Block2 → DataNode2, DataNode4, DataNode5
# ...

# （因为 HDFS 默认有 3 副本。）

# 3️⃣ 客户端开始写第一个块：

# 客户端先把数据流发给第一个 DataNode（例如 DN1），
# DN1 一边写一边转发给 DN2，DN2 再转发给 DN3。
# 这叫做 数据管道（Pipeline）写入。

# 👉 就像客户 → 仓库工人A → 工人B → 工人C，
# 每个工人都同时接力写入自己那一份副本。

# 4️⃣ 块写完后汇报：

# 当 DN3 写完后，从后往前回报“我写完了”：
# DN3 ✅ → DN2 ✅ → DN1 ✅ → 客户端 ✅
# 客户端再通知 NameNode：“第一个块搞定了。”

# 然后继续写下一个块，直到全部写完。

# 5️⃣ NameNode 更新元数据：

# 写完后，NameNode 把这份文件的块位置信息记账保存。

# 📘 小结：

# NameNode 负责“记账”，DataNode 负责“干活”，
# 客户端像是发指令、搬数据的“协调者”。

# ⸻

# 📖 三、读文件流程（HDFS → Client）

# 场景：你要读取 /user/eason/data.txt。

# 1️⃣ 客户端问 NameNode：

# “我想读 /user/eason/data.txt，在哪？”
# → NameNode 返回：

# Block1 → DN2, DN3, DN5
# Block2 → DN1, DN4, DN6
# ...

# 2️⃣ 客户端选最近的副本：

# 客户端根据网络距离（通常选同机架的）挑一个最近的 DataNode 读取。
# 比如在上海机房的客户端，会优先选上海机房的副本。

# 3️⃣ 顺序读取：

# 客户端按顺序请求每个数据块（Block1 → Block2 → …），
# 从不同的 DataNode 读取流式数据，然后拼接还原成完整文件。

# 4️⃣ NameNode 不参与传输：

# NameNode 只负责告诉你“数据在哪”，
# 数据的实际传输完全是客户端和 DataNode 直接通信完成的。

# ⸻

# ⚙️ 四、关键机制（简短总结）

# 环节	说明
# 块存储	大文件被切成多个 128MB 块
# 副本机制	每块默认存 3 份，提高容错性
# 管道写入	写入时多节点并行接力写
# 本地性优化	读文件时优先从最近节点读
# 心跳机制	DataNode 定期向 NameNode 报平安
# 自动恢复	节点挂了，NameNode 自动复制丢失的块


# ⸻

# 🎯 五、一句话总结

# 写文件时： 你告诉 NameNode → 它分配仓库 → 你按块送去 DataNode。
# 读文件时： 你问 NameNode → 它告诉你在哪 → 你直接去最近的仓库取。

# NameNode 像“导航系统”，
# DataNode 是“仓库工人”，
# 客户端是“调度员 + 搬运工”。


# 🧩 一、YARN 是啥？

# YARN，全称 Yet Another Resource Negotiator，是 Hadoop 的 资源调度系统。
# 一句话概括：

# HDFS 管数据，YARN 管算力。

# 也就是说：
# 	•	HDFS 负责“存文件”；
# 	•	YARN 负责“谁来算、在哪儿算、算多少”。

# ⸻

# 🧱 二、YARN 的结构（像一个公司）

# YARN 就像一家公司，有三个重要角色：

# 角色	职责	类比
# ResourceManager（RM）	全局调度，管理整个集群的资源	总经理
# NodeManager（NM）	管理每台机器上的资源（CPU、内存）	车间主管
# ApplicationMaster（AM）	管理单个任务的执行	项目经理

# 此外还有：

# 组件	说明
# Container	任务运行的“盒子”（分配的资源单位）


# ⸻

# ⚙️ 三、资源调度流程（像项目分配流程）

# 📍1️⃣ 客户端提交任务

# 用户通过客户端提交任务（比如一个 MapReduce 作业）给 YARN。
# 👉 就像提交一个“计算项目申请表”。

# ⸻

# 📍2️⃣ ResourceManager 接收任务

# RM 收到任务后，不直接干活，而是：
# 	•	给这个任务启动一个专属的 ApplicationMaster (AM)。
# 	•	AM 会被放到某个 NodeManager 管辖的节点上运行。

# 📘 RM 负责“指派项目经理（AM）”。

# ⸻

# 📍3️⃣ ApplicationMaster 启动

# AM 启动后：
# 	•	向 ResourceManager 报到；
# 	•	然后申请计算资源（比如“我要 10 台机器，每台 2 核 4G 内存”）。

# ⸻

# 📍4️⃣ RM 分配资源（Container）

# RM 根据集群空闲情况，给它分配若干 Container，并告诉 AM：

# “这几台机器空着，可以用。”

# ⸻

# 📍5️⃣ AM 在 NodeManager 上启动任务

# AM 再去通知这些 NodeManager：

# “你们启动这些任务吧。”
# 每个 NodeManager 启动对应的 Container 并运行计算进程（比如 Map 或 Reduce）。

# ⸻

# 📍6️⃣ 任务执行与监控

# NodeManager 定期向 RM 汇报心跳（资源使用、任务状态）。
# AM 也会实时监控任务完成情况，失败则可重启。

# ⸻

# 📍7️⃣ 任务完成与释放资源

# 所有 Container 执行完毕，AM 向 RM 汇报任务完成，RM 回收资源。

# 📘 整个过程就像：

# RM 统一调度资源 → AM 负责项目协调 → NMs 具体执行。

# ⸻

# 📊 四、调度策略（谁先用资源？）

# YARN 的 RM 有多种调度算法（可配置）：

# 调度器类型	特点
# FIFO	先提交先执行
# Capacity Scheduler	给各部门划定“容量配额”，确保公平
# Fair Scheduler	动态分配资源，让各应用“公平分享”集群资源


# ⸻

# 🎯 五、一句话总结

# YARN = “集群算力中台”。
# ResourceManager 掌舵全局，
# ApplicationMaster 管理每个任务，
# NodeManager 负责实际执行，
# Container 是计算的“盒子”。

# 流程图可简化为👇：

# Client → ResourceManager → ApplicationMaster → NodeManager → Container(任务执行)


# 🌳 一、MapReduce 是啥

# MapReduce 是 Hadoop 的计算模型：

# Map 阶段做数据拆分 + 预处理，Reduce 阶段做汇总 + 聚合

# 一句话：Map 把数据切块并加工，Reduce 把结果合并成最终答案。

# ⸻

# 🏗 二、执行流程（分步解读）

# 假设你要统计一个大文件中每个单词出现次数。

# ⸻

# 1️⃣ 客户端提交任务

# 你写好 MapReduce 程序，然后提交给 YARN 或 Hadoop。
# 	•	Hadoop 接收任务，启动 JobTracker（或 ApplicationMaster）。

# ⸻

# 2️⃣ 输入数据切分（InputSplit）

# Hadoop 会把大文件分成若干个 InputSplit（比如 128MB 一块），
# 每块数据会交给一个 Map Task。

# 就像把大面团分成小块，每个面点师负责揉一块。

# ⸻

# 3️⃣ Map 阶段
# 	•	每个 Map Task 读取自己那块数据。
# 	•	执行 map(key, value) 函数，把原始数据转换成 <key, value> 对。

# 示例：

# hello world hello
# map -> [("hello",1),("world",1),("hello",1)]

# 	•	Map Task 会先做 本地合并（combiner，可选），减少数据量。

# ⸻

# 4️⃣ Shuffle 阶段（关键！）
# 	•	Map 输出的 <key, value> 对需要发送给对应的 Reduce。
# 	•	Hadoop 会按 key 分区（partition）、排序（sort）、合并（merge）后发送。

# 可以理解为：各个面点师做完自己的面团后，把相同类型的面团汇总到同一个盆里。

# ⸻

# 5️⃣ Reduce 阶段
# 	•	每个 Reduce Task 接收对应 key 的所有 value 列表。
# 	•	执行 reduce(key, list<value>)，合并成最终结果。

# 示例：

# reduce("hello",[1,1]) -> ("hello",2)
# reduce("world",[1]) -> ("world",1)


# ⸻

# 6️⃣ 输出结果
# 	•	Reduce 任务把结果写入 HDFS，成为最终输出文件。
# 	•	客户端可以直接读取或继续作为下一个 MapReduce 的输入。

# ⸻

# ⚡ 三、执行过程总结（简化流程图）

# Client 提交任务
#         │
#    Hadoop JobTracker / AM
#         │
#    切分 InputSplit
#         │
#      Map Tasks
#    (处理每块数据)
#         │
#    Shuffle & Sort
#    (按 key 分发)
#         │
#      Reduce Tasks
#    (聚合每个 key)
#         │
#    HDFS 输出


# ⸻

# 🧠 四、人话记忆版
# 	1.	Map = 切块 + 统计 → 每个人先做自己份
# 	2.	Shuffle = 分发 + 排序 → 按类别搬运到对应的人
# 	3.	Reduce = 汇总 + 输出 → 每个人算好总数写回仓库


# 🌳 一、前提条件
# 	1.	macOS 系统
# 	2.	安装 Java（Hadoop 需要 JDK 1.8+）

# java -version

# 如果没有，安装：

# brew install openjdk@17

# 并配置环境变量：

# echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zshrc
# source ~/.zshrc


# 	3.	安装 Homebrew（如果还没装）：

# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"


# ⸻

# 🌳 二、下载 Hadoop
# 	1.	官网下载稳定版 Hadoop：
# 	•	地址：https://hadoop.apache.org/releases.html
# 	•	建议版本：3.3.x
# 	2.	或使用 Homebrew：

# brew install hadoop


# ⸻

# 🌳 三、解压 & 配置环境变量

# 如果手动下载：

# tar -zxvf hadoop-3.3.6.tar.gz -C /usr/local/
# mv /usr/local/hadoop-3.3.6 /usr/local/hadoop

# 配置环境变量 (~/.zshrc 或 ~/.bash_profile)：

# export HADOOP_HOME=/usr/local/hadoop
# export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
# export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
# export JAVA_HOME=$(/usr/libexec/java_home)

# 然后：

# source ~/.zshrc


# ⸻

# 🌳 四、修改 Hadoop 配置（单机模式）

# 进入 HADOOP_HOME/etc/hadoop，修改以下配置文件：

# 1️⃣ hadoop-env.sh

# 确保 JAVA_HOME 配置正确：

# export JAVA_HOME=/usr/libexec/java_home

# 2️⃣ core-site.xml

# 添加 HDFS 默认文件系统：

# <configuration>
#     <property>
#         <name>fs.defaultFS</name>
#         <value>hdfs://localhost:9000</value>
#     </property>
# </configuration>

# 3️⃣ hdfs-site.xml

# 设置 HDFS 存储目录：

# <configuration>
#     <property>
#         <name>dfs.replication</name>
#         <value>1</value> <!-- 单机模式只用 1 -->
#     </property>
#     <property>
#         <name>dfs.namenode.name.dir</name>
#         <value>file:///usr/local/hadoop/data/namenode</value>
#     </property>
#     <property>
#         <name>dfs.datanode.data.dir</name>
#         <value>file:///usr/local/hadoop/data/datanode</value>
#     </property>
# </configuration>

# 4️⃣ mapred-site.xml

# 如果没有，复制模板：

# cp mapred-site.xml.template mapred-site.xml

# 修改：

# <configuration>
#     <property>
#         <name>mapreduce.framework.name</name>
#         <value>yarn</value>
#     </property>
# </configuration>

# 5️⃣ yarn-site.xml

# 配置 ResourceManager：

# <configuration>
#     <property>
#         <name>yarn.nodemanager.aux-services</name>
#         <value>mapreduce_shuffle</value>
#     </property>
# </configuration>


# ⸻

# 🌳 五、格式化 HDFS

# 第一次启动前，需要格式化 NameNode：

# hdfs namenode -format

# 这会在 dfs.namenode.name.dir 下生成元数据文件。

# ⸻

# 🌳 六、启动 Hadoop 服务（单机模式）
# 	1.	启动 HDFS：

# start-dfs.sh

# 	2.	启动 YARN：

# start-yarn.sh

# 检查进程：

# jps

# 应该看到：

# NameNode
# DataNode
# SecondaryNameNode
# ResourceManager
# NodeManager


# ⸻

# 🌳 七、测试 Hadoop
# 	1.	创建 HDFS 目录：

# hdfs dfs -mkdir /user
# hdfs dfs -mkdir /user/yourname

# 	2.	上传本地文件：

# hdfs dfs -put ~/test.txt /user/yourname/

# 	3.	查看文件：

# hdfs dfs -ls /user/yourname
# hdfs dfs -cat /user/yourname/test.txt


# ⸻

# 🌳 八、停止 Hadoop 服务

# stop-yarn.sh
# stop-dfs.sh


# ⸻

# 🔧 小贴士
# 	•	单机模式 = pseudo-distributed，所有服务在本机跑。
# 	•	数据目录不要放在 /tmp，建议用 /usr/local/hadoop/data/。
# 	•	如果 Homebrew 安装，路径会不同，环境变量要改对应的 HADOOP_HOME。
# 	•	默认端口：
# 	•	NameNode: 9870（web）
# 	•	ResourceManager: 8088（web）


# 启动脚本在：~/.local/bin/start-hadoop-mac.sh
# 启动命令：start-hadoop-mac.sh
# 可以访问：
# 👉 http://localhost:9870 （HDFS Web UI）
# 👉 http://localhost:8088 （YARN Web UI）
# 查看进程：jps
# 验证 : hdfs dfsadmin -report

# 关闭服务
# stop-yarn.sh
# stop-dfs.sh

def test():
    pass


if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        test()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")
