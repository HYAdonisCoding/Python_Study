# 利用Python进行数据分析

Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

Wes McKinney 著
徐敬一 译
机械工业出版社

## 第1章 准备工作

1.1 本书内容  
1.1.1 什么类型的数据  
1.2 何利用 Python 行数据分析  
1.2.1 Python 作为胶水  
1.2.2 解决“双语言”难题  
1.2.3 为何不使用 Python  
1.3 重要的 Python 库  
1.3.1 NumPy.  
1.3.2 pandas  
1.3.3 matplotlib  
1.3.4 Python 5 Jupyter  
1,3.5 SciPy  
1.3.6 scikit-learn  
1.3.7 statsmodels  
1.4 安装与设置  
1.4.1 Windows  
1.4.2 Apple (OS X #l macOS)  
1.4.3 GNU/Linux  
1.4.4 安装及更新 Python 包  
1.4.5 Python 2 70 Python 3  
1.4.6集成开发环境和文本编辑器  
1.5 社区和会议  
1.6快速浏览本书  
1.6.1 代码示例  
1.6.3导入约定  
1.6.4术语  

## 第2章 Python 语言基础

2.1 Python 解释器  
2.2 IPython 基础  
2.2.1 运行IPython 命令行  
2.2.2 运行 Jupyter notebook  
2.2.3 Tab 补全  
2.2.4 内省  
2.2.5 %run 命令  
2.2.6 执行剪贴板中的程序  
2.2.7 终端快捷键.  
2.2.8 关于魔术命令  
2.2.9 matplotlib 集成  
2.3 Python 语言基础  
2.3.1 语言语义  
2.3.2 标量类型  
2.3.3 控制流  

## 第3章 内建数据结构、函数及文件

3.1 数据结构和序列  
3.1.1 元组  
3.1.2 列表  
3.1.3 内建序列函数  
3.1.4 字典  
3.1.5 集合  
3.1.6 列表、集合和字典的推导式.  
3.2 函数  
3.2.1 命名空间、作用域和本地函数  
3.2.2 返回多个值  
3.2.3 函数是对象  
3.2.4 匿名（Lambda）函数  
3.2.5 柯里化：部分参数应用  
3.2.6 生成器  
3.2.7 错误和异常处理  
3.3 文件与操作系统  
3.3.1 字节与 Unicode 文件  
3.4 本章小结  

## 第4章 NumPy基础：数组与向量化计算

4.1 NumPy ndarray：多维数组对象  
4.1.1 生成 ndarray  
4.1.2 ndarray 的数据类型  
4.1.3 NumPy 数组算术  
4.1.4 基础索引与切片  
4.1.5 布尔索引  
4.1.6 神奇索引  
4.1.7 数组转置和换轴  
4.2 通用函数：快速的逐元素数组函数  
4.3 使用数组进行面向数组编程  
4.3.1 将条件逻辑作为数组操作  
4.3.2 数学和统计方法  
4.3.3 布尔值数组的方法  
4.3.4 排序  
4.3.5 唯一值与其他集合逻辑  
4.4 使用数组进行文件输入和输出  
4.5 线性代数  
4.6 伪随机数生成  
4.7 示例：随机漫步  
4.7.1 一次性模拟多次随机漫步  
4.8 本章小结  

## 第5章 pandas入门

5.1 pandas 数据结构介绍  
5.1.1 Series  
5.1.2 DataFrame  
5.1.3 索引对象  
5.2 基本功能  
5.2.1 重建索引  
5.2.2 轴向上删除条目  
5.2.3 索引、选择与过滤  
5.2.4 整数索引  
5.2.5 算术和数据对齐  
5.2.6 函数应用和映射  
5.2.7 排序和排名  
5.2.8 含有重复标签的轴索引  
5.3 描述性统计的概述与计算  
5.3.1 相关性和协方差  
5.3.2 唯一值、计数和成员属性  
5.4 本章小结  

## 第6章 数据载入、存储及文件格式

6.1 文本格式数据的读写  
6.1.1 分块读入文本文件  
6.1.2 将数据写入文本格式  
6.1.3 使用分隔格式  
6.1.4 JSON数据  
6.1.5 XML 和 HTML：网络抓取  
6.2 二进制格式  
6.2.1 使用 HDF5格式  
6.2.2 读取 Microsoft Excel 文件  
6.3 与Web API 交互  
6.4 与数据库交互  
6.5 本章小结  

## 第7章 数据清洗与准备

7.1 处理缺失值  
7.1.1 过滤缺失值  
7.1.2 补全缺失值  
7.2 数据转换  
7.2.1 删除重复值  
7.2.2 使用函数或映射进行数据转换  
7.2.3 替代值  
7.2.4 重命名轴索引  
7.2.5 离散化和分箱  
7.2.6 检测和过滤异常值  
7.2.7 置換和随机抽样  
7.2.8 计算指标/虚拟变量  
7.3 字符串操作  
7.3.1 字符串对象方法  
7.3.2 正则表达式  
7.3.3 pandas 中的向量化字符串函数  
7.4 本章小结  

## 第8章 数据规整：连接、联合与重塑

8.1分层索引  
8.1.1 重排序和层级排序  
8.1.2 按层级进行汇总统计  
8.1.3 使用 DataFrame 的列进行索引  
8.2 联合与合并数据集  
8.2.1 数据库风格的 DataFrame 连接  
8.2.2 根据索引合并  
8.2.3 沿轴向连接  
8.2.4 联合重叠数据  
8.3 重塑和透视  
8.3.1 使用多层索引进行重塑  
8.3.2 将“长”透视为“宽”  
8.3.3 将“宽”透视为“木”  
8.4 本章小结  

## 第9章 绘图与可视化

9.1 简明 matplotlib API 入门  
9.1.1 图片与子图  
9.1.2 颜色、标记和线类型  
9.1.3 刻度、标签和图例  
9.1.4 注释与子图加工  
9.1.5 将图片保存到文件  
9.1.6 matplotlib 设置  
9.2 使用 pandas 和 seaborn 绘图  
9.2.1 折线图  
9.2.2 柱状图  
9.2.3 直方图和密度图  
9.2.4 散点图或点图  
9.2.5 分面网格和分类数据  
9.3 其他 Python 可视化工具  
9.4 本章小结  

## 第10章 数据聚合与分组操作

10.1 GroupBy 机制  
10.1.1 遍历各分组  
10.1.2 选择一列或所有列的子集  
10.1.3 使用字典和 Series 分组  
10.1.4 使用函数分组  
10.1.5 根据索引层级分组  
10.2 数据聚合.  
10.2.1 逐列及多函数应用  
10.2.2 返回不含行索引的聚合数据  
10.3 应用：通用拆分-应用-联合  
10.3.1 压缩分组键  
10.3.2 分位数与桶分析  
10.3.3 示例：使用指定分组值填充缺失值  
10.3.4 示例：随机采样与排列  
10.3.5 示例：分组加权平均和相关性  
10.3.6 示例：逐组线性回归  
10.4 数据透视表与交叉表  
10.4.1 交叉表：crosstab  
第10章 数据聚合与分组操作（小结）

一、本章核心思想（★★★★★）

一句话：

Split → Apply → Combine（拆分 → 应用 → 合并）

即：

DataFrame
    │
groupby()
    │
每个组分别统计
    │
得到新的 Series/DataFrame

几乎所有数据分析都遵循这个流程。

⸻

二、必须掌握的 API（★★★★★）

API	作用
groupby()	分组
agg()	聚合统计
apply()	自定义分组处理
transform()	分组后返回与原数据等长（后续章节重点）
pivot_table()	数据透视表
crosstab()	交叉统计

⸻

三、常用统计函数

count()
size()
sum()
mean()
median()
std()
min()
max()
describe()
quantile()

重点掌握：

* mean()：平均值
* sum()：求和
* count()：非空数量
* size()：总数量
* describe()：快速统计

⸻

四、数据分析的一般流程

读取数据
    ↓
查看数据（head/info/describe）
    ↓
数据清洗
    ↓
groupby 分组
    ↓
agg/apply 聚合统计
    ↓
pivot_table 汇总
    ↓
可视化
    ↓
得出结论

⸻

五、本章重点掌握程度

⭐⭐⭐⭐⭐ 必会

* groupby
* agg
* apply
* pivot_table

⭐⭐⭐⭐ 熟悉

* crosstab
* cut
* qcut

⭐⭐⭐ 了解

* 分组回归
* 加权平均
* 多级索引分组

⸻

一句话总结

第10章就是学习如何把数据按某种规则分组，并对每组进行统计分析，是 Pandas 数据分析中最核心、最常用的内容。

⸻

建议记忆口诀：

分组（GroupBy）→ 聚合（Agg）→ 透视（Pivot）→ 分析（EDA）


## 第11章时间序列

11.1 日期和时间数据的类型及工具  
11.1.1 字符串与 datetime 互相转换  
11.2 时间序列基础  
11.2.1 索引、选择、子集  
11.2.2 含有重复索引的时间序列  
11.3 日期范围、频率和移位  
11.3.1 生成日期范围  
11.3.2 频率和日期偏置  
11.3.3 移位（前向和后向）日期  
11.4 时区处理  
11.4.1 时区的本地化和转换  
11.4.2 时区感知时间戳对象的操作  
11.4.3 不同时区间的操作  
11.5 时间区间和区间算术  
11.5.1 区间频率转换  
11.5.2 季度区间频率  
11.5.3 将时间戳转换区间（以及逆转换）  
11.5.4 从数组生成 PeriodIndex  
11.6 重新采样与频率转换  
11.6.1 向下采样  
11.6.2 向上采样与插值  
11.6.3 使用区间进行重新采样  
11.7 移动窗口函数  
11.7.1 指数加权函数  
11.7.2 二元移动窗口函数  
11.7.3 用户自定义的移动窗口函数  
11.8 本章小结  

第11章 时间序列 —— 学习总结

1. Python 日期时间基础

掌握：

* datetime
* timedelta
* 字符串与时间互转

核心：

datetime.strptime()
datetime.strftime()
pd.to_datetime()

理解：

datetime 是单个时间点，timedelta 是时间差。

⸻

2. Pandas 时间序列基础

核心对象：

Series + DatetimeIndex

例如：

ts = pd.Series(
    values,
    index=pd.date_range(...)
)

掌握：

* 时间索引访问
* 日期切片
* 按年/月筛选

例如：

ts["2011"]
ts["2011-05"]

⸻

3. 日期范围和频率

掌握：

pd.date_range()

常用频率：

频率	含义
D	天
B	工作日
h	小时
min	分钟
ME	月末
Y-DEC	年末
Q-DEC	季度

理解：

Pandas 时间序列的核心是 Index + Frequency。

⸻

4. 日期偏移 Offset

掌握：

Hour()
Minute()
Day()
MonthEnd()

例如：

date + MonthEnd()

可以实现：

* 月末调整
* 日期滚动

⸻

5. 时区处理（重点）

三个核心操作：

本地化

tz_localize()

给无时区时间增加时区。

转换

tz_convert()

不同地区时间转换。

注意夏令时

例如：

2012-03-11
美国夏令时开始
01:30 + 1小时
变成
03:30

原因：

本地时间跳过不存在的小时。

⸻

6. Period 时间区间（本章重点）

区别：

Timestamp

表示：

一个时间点

例如：

2026-07-09 10:30

Period

表示：

一个时间范围

例如：

2026年
2026Q1
2026-07

创建：

pd.Period()
pd.period_range()

⸻

7. Period 频率转换

核心：

asfreq()

例如：

年度：

2011

转换：

.asfreq("M")

得到：

2011-01
...
2011-12

理解：

* start
* end

决定落在哪个时间点。

⸻

8. PeriodIndex

用途：

把业务时间转换成时间索引。

例如：

原始：

year quarter
2000   1
2000   2

转换：

2000Q1
2000Q2

新版 pandas：

pd.PeriodIndex(
    year.astype(str)+"Q"+quarter.astype(str),
    freq="Q-DEC"
)

⸻

9. Resample 重采样（重点）

两个方向：

⸻

降采样 Downsampling

高频 → 低频

例如：

分钟
 ↓
小时
 ↓
天

常用：

.resample("5min").sum()
.resample("ME").mean()

⸻

升采样 Upsampling

低频 → 高频

例如：

周
 ↓
日

需要填充：

ffill()
bfill()
interpolate()

⸻

10. 向前填充

核心：

ffill()

含义：

使用最近一次已知值填充未来缺失值。

金融数据：

周三价格
 ↓
周四继续使用

非常常见。

⸻

11. 移动窗口函数（金融分析重点）

核心：

rolling()

例如：

price.rolling(30).mean()

计算：

30日移动平均。

其他：

rolling().std()
rolling().corr()
rolling().apply()

应用：

* 均线
* 波动率
* 相关性
* 技术指标

⸻

本章核心一句话

Pandas 时间序列的核心能力，就是围绕 时间索引（DatetimeIndex / PeriodIndex）进行定位、转换、重采样、窗口计算和时区处理。





## 第12章 高阶 pandas

12.1 分类数据  
12.1.1 背景和目标  
12.1.2 pandas 中的 Categorical类型  
12.1.3 使用Categorical 对象进行计算  
12.1.4 分类方法  
12.2 高阶 GroupBy 应用  
12.2.1 分组转换和 “展开”GroupBy  
12.2.2 分组的时间重新采样  
12.3 方法链技术  
12.3.1 pipe 方法  
12.4 本章小结  



本章主要学习 Pandas 在真实数据分析场景中的高级应用，包括分类数据处理、高级 GroupBy 操作、时间序列聚合以及 DataFrame 方法链编程。  

通过本章学习，可以使用 Pandas 更高效地处理复杂业务数据，提高数据清洗、转换、统计分析的能力。

---

## 12.1 Categorical 分类数据

### 1. 为什么需要 Category 类型？

在实际数据分析中，大量字段属于**低基数分类数据（Low Cardinality Data）**：
例如：

- 用户等级：普通会员、VIP、SVIP
- 商品类别：手机、电脑、家电
- 地区：北京、上海、深圳
- 性别：男、女
这些字段虽然字符串重复很多，但 Pandas 默认使用 object 存储，会占用较多内存。
Categorical 类型通过：

categories（类别字典）
+
codes（整数编码）

方式存储，提高内存利用率和计算效率。

---

### 2. 创建 Category 数据

常用方式：
```python
# Series 转换
s = pd.Series(["apple", "orange", "apple"])
s = s.astype("category")
# 创建 Categorical 对象
cat = pd.Categorical(
    ["foo", "bar", "foo"]
)
# 根据编码创建分类
pd.Categorical.from_codes(
    codes=[0,1,0],
    categories=["apple","orange"]
)

⸻

3. Category 常用操作

查看编码：

s.cat.codes

获取分类：

s.cat.categories

修改分类名称：

s.cat.rename_categories()

增加或设置分类：

s.cat.set_categories()

删除无效分类：

s.cat.remove_unused_categories()

⸻

4. Ordered Category 有序分类

适用于具有业务等级关系的数据。

例如：

普通 < VIP < SVIP

创建：

pd.Categorical(
    data,
    categories=[
        "普通",
        "VIP",
        "SVIP"
    ],
    ordered=True
)

应用场景：

* 用户等级排序
* 商品评级
* 客户价值分层
* 问卷满意度分析

⸻

实际应用

Categorical 常用于：

* 大规模数据内存优化
* 特征工程
* 报表分类排序
* 数据清洗统一字段

例如百万级用户数据：

df["city"] = df["city"].astype("category")

可以明显降低内存占用。

⸻

12.2 高阶 GroupBy 应用

GroupBy 是 Pandas 数据分析中的核心能力。

典型流程：

Split
  ↓
Apply
  ↓
Combine

即：

分组 → 计算 → 合并结果。

⸻

1. 基础聚合

常用：

df.groupby("key").sum()
df.groupby("key").mean()
df.groupby("key").count()

⸻

2. 多指标聚合 agg()

实际分析中经常需要同时计算多个指标：

df.groupby("category").agg(
    {
        "sales":"sum",
        "price":"mean",
        "id":"count"
    }
)

例如：

电商分析：

指标	含义
sales sum	销售总额
price mean	平均价格
id count	订单数量

⸻

12.2.1 transform 与 apply

transform()

特点：

* 返回结果长度和原数据一致
* 可以直接回填 DataFrame

例如：

计算用户消费金额相对于用户平均消费的偏差：

df["avg"] = (
    df.groupby("user")
    ["amount"]
    .transform("mean")
)

常见用途：

* 标准化
* 缺失值填充
* 组内排名
* 计算相对指标

⸻

apply()

特点：

* 灵活
* 可以返回任意结构

适用于复杂业务逻辑：

df.groupby("group").apply(func)

常见用途：

* 自定义统计规则
* 复杂数据转换
* 分组后生成新结构

⸻

transform 和 apply 区别

方法	返回	适用场景
transform	与原数据同长度	生成新字段
apply	任意结构	复杂业务逻辑

⸻

12.2.2 分组时间重新采样

实际业务经常需要：

* 每小时交易量
* 每日访问量
* 每月销售额

使用：

pd.Grouper()

例如：

df.groupby(
    [
        "category",
        pd.Grouper(
            key="time",
            freq="M"
        )
    ]
).sum()

应用：

* 用户行为分析
* 股票行情分析
* 日志分析
* 订单趋势分析

⸻

12.3 方法链 Method Chaining

方法链是一种更加工程化的数据处理方式。

传统写法：

df1 = df[df.price>100]
df2 = df1.groupby("type").sum()

方法链：

(
    df
    [lambda x:x.price>100]
    .groupby("type")
    .sum()
)

优点：

* 减少中间变量
* 提高代码可读性
* 方便构建 ETL 流程

⸻

12.3.1 assign()

用于创建新字段。

例如：

计算利润：

df.assign(
    profit=df.sales-df.cost
)

常用于：

* 指标计算
* 特征生成
* 数据转换

⸻

12.3.2 lambda

匿名函数。

常配合：

* apply
* assign
* filter

使用。

例如：

df[
    lambda x:x.score>80
]

⸻

12.3.3 pipe()

用于构建复杂数据处理流程。

例如：

(
    df
    .pipe(clean_data)
    .pipe(feature_engineering)
    .pipe(model_prepare)
)

适合：

* 数据清洗 Pipeline
* 机器学习特征处理
* 企业级数据分析流程

⸻

本章总结

通过本章学习，掌握 Pandas 高级数据处理能力：

分类数据

掌握：

* Category
* Codes
* Categories
* Ordered Category

解决：

* 分类字段管理
* 内存优化
* 数据排序问题

高级 GroupBy

掌握：

* groupby
* agg
* transform
* apply
* Grouper

解决：

* 分组统计
* 用户分析
* 时间趋势分析

方法链

掌握：

* assign
* lambda
* pipe

提升：

* 数据处理代码可读性
* ETL 流程设计能力
* 生产级数据分析能力

本章内容是 Pandas 从基础操作进入实际数据分析工程的重要阶段，为后续数据建模、机器学习特征工程和商业数据分析提供基础能力。



## 第13章 Python 建模库介绍

13.1 pandas 与建模代码的结合  
13.2 使用 Patsy 创建模型描述  
13.2.1 Patsy 公式中的数据转换  
13.2.2 分类数据与 Patsy  
13.3 statsmodels 介绍  
13.3.1 评估线性模型  
13.3.2 评估时间序列处理  
13.4 scikit-learn 介绍  
13.5 继续你的教育  


### 本章重点

1. pandas 与建模流程结合
   - DataFrame 是数据分析和机器学习之间的桥梁
   - 从 DataFrame 中选择特征列，并转换为 NumPy 数组供模型使用
   - 分类变量需要进行编码处理（如 One-Hot Encoding）

2. Patsy 模型公式
   - 使用公式语法描述统计模型：
     - `y ~ x0 + x1`
     - 分类变量自动转换为哑变量
     - 支持数据转换、标准化、中心化等操作
   - 通过 design matrix 将数据转换为模型可使用的矩阵

3. statsmodels 统计建模
   - 使用 OLS 进行线性回归分析
   - 查看模型参数、统计显著性、预测结果
   - 支持时间序列模型（如 AutoReg）

4. scikit-learn 机器学习流程
   - 数据预处理：
     - 缺失值填充
     - 特征工程
     - 分类变量编码
   - 模型训练：
     - Logistic Regression
     - LogisticRegressionCV
   - 模型评估：
     - Cross Validation（交叉验证）

---

### 数据分析建模通用流程

原始数据
|
↓
pandas 数据清洗
|
↓
特征选择 / 特征工程
|
↓
NumPy 数组转换
|
↓
统计模型 / 机器学习模型
|
↓
模型评估与预测

---

### 核心掌握

- 熟练使用 pandas 构造模型输入数据
- 理解 DataFrame、NumPy Array、模型之间的数据转换
- 掌握分类变量编码方法
- 理解训练集、测试集、交叉验证流程
- 能使用 statsmodels / sklearn 完成基础建模任务

## 第14章数据分析示例

14.1 从 Bitly 获取 1.USA.gov 数据  
14.1.1 纯 Python 时区计数  
14.1.2 使用pandas 进行时区计数  
14.2 MovieLens 1M 数据集  
14.2.1 测量评价分歧  
14.3 美国 1880～2010年的婴儿名字  
14.3.1 分析名字趋势  
14.4 美国农业部食品数据库  
14.5 2012年联邦选举委员会数据库  
14.5.1 按职业和雇主的捐献统计  
14.5.2 捐赠金额分桶  
14.5.3 按州进行捐赠统计  
14.6 本章小结  

本章通过多个真实数据集案例，学习了使用 Python 进行数据分析的完整流程：

* 数据读取
* 数据清洗
* 数据转换
* 分组统计
* 聚合分析
* 数据可视化
* 从数据中发现规律

核心思想：

数据分析不是直接画图，而是先理解数据结构，再提出问题，通过转换和统计得到结论。

⸻

一、数据分析通用流程

以后面对任何新的数据分析任务，可以按照以下流程：

1. 明确分析目标
        ↓
2. 读取数据
        ↓
3. 查看数据结构
        ↓
4. 数据清洗
        ↓
5. 数据转换
        ↓
6. 分组聚合分析
        ↓
7. 可视化展示
        ↓
8. 得出业务结论

⸻

1. 明确分析目标

开始分析前，需要先回答：

* 我要解决什么问题？
* 哪些字段与问题相关？
* 最终希望得到什么结论？

例如：

Bitly访问数据

目标：

分析用户来自哪些地区，以及不同系统用户比例。

关注字段：

tz      时区
a       User-Agent
os      操作系统

⸻

MovieLens电影评分

目标：

分析不同用户群体对电影评分的偏好。

关注字段：

user_id
gender
movie
rating

⸻

美国婴儿名字趋势

目标：

分析名字流行趋势变化。

关注字段：

year
name
sex
births

⸻

2. 数据读取与结构探索

拿到数据后，不要急着分析。

第一步：

df.head()

查看前几行。

第二步：

df.info()

确认：

* 字段名称
* 数据类型
* 缺失情况

第三步：

df.describe()

查看：

* 数值范围
* 平均值
* 异常值

重点关注：

shape
columns
dtype
missing values

⸻

3. 数据清洗

真实数据通常存在：

* 缺失值
* 重复数据
* 类型错误
* 字段格式不统一

常用方法：

缺失值处理

df.isna()
df.fillna()
df.dropna()

例如：

clean_tz = frame["tz"].fillna("Missing")

⸻

去重

df.drop_duplicates()

⸻

类型转换

例如：

pd.to_datetime()
astype()

⸻

4. 数据转换

数据分析的核心：

将原始数据转换成适合统计的数据结构。

常用操作：

新增字段

df["new_column"] = value

例如：

根据 User-Agent 判断系统：

df["os"] = np.where(
    df["a"].str.contains("Windows"),
    "Windows",
    "Other"
)

⸻

数据透视表

pd.pivot_table()

适合：

* 多维统计
* 对比分析

例如：

不同性别电影评分：

          Male Female
Movie A    4.2  4.5
Movie B    3.8  4.0

⸻

5. 分组统计（最重要）

pandas 数据分析核心：

groupby()

基本形式：

df.groupby("字段")["指标"].统计函数()

例如：

统计不同类别数量：

df.groupby("category").size()

统计平均值：

df.groupby("category")["price"].mean()

多维分析：

df.groupby(
    ["year","sex"]
)["births"].sum()

⸻

6. 排序与排名

常用：

sort_values()
nlargest()
argsort()

例如：

找到访问量最高的10个地区：

tz_counts.nlargest(10)

⸻

7. 可视化分析

数据分析最终需要图形表达。

常用：

柱状图

比较类别：

df.plot(kind="bar")

折线图

观察趋势：

df.plot()

横向柱状图

排名：

df.plot(kind="barh")

原则：

* 趋势 → 折线图
* 分类比较 → 柱状图
* 分布 → 直方图
* 占比 → 饼图

⸻

8. 本章核心工具总结

pandas

数据处理核心：

DataFrame
Series
groupby
pivot_table
merge
concat
apply
transform

⸻

NumPy

数值计算：

array
where
argsort
linspace

⸻

matplotlib / seaborn

数据展示：

plot
bar
barh
scatter

⸻

以后拿到一个新数据集如何分析？

建议按照以下模板：

Step 1：认识数据

df.head()
df.info()
df.describe()

回答：

* 有多少数据？
* 有哪些字段？
* 数据类型是什么？

⸻

Step 2：提出问题

例如：

用户数据：

哪个地区用户最多？
用户有什么特点？
趋势如何变化？

商品数据：

哪个品牌销量最高？
价格和评价是否相关？
差评主要原因是什么？

⸻

Step 3：设计指标

不要直接统计。

先定义指标：

例如电商分析：

销售量
销售额
好评率
差评率
价格区间
品牌占比

⸻

Step 4：数据转换

根据问题设计：

过滤
分组
聚合
排序
关联
透视

⸻

Step 5：可视化验证

通过图表寻找：

* 趋势
* 异常
* 规律
* 关系

⸻

本章最终能力提升

完成本章后，可以独立完成：

✅ CSV / JSON 数据读取

✅ DataFrame 数据探索

✅ 缺失数据处理

✅ 数据清洗

✅ 分组统计分析

✅ 多表关联分析

✅ 时间趋势分析

✅ 分类数据分析

✅ 基础商业数据分析

⸻

数据分析核心思想

好的数据分析 = 正确的问题 + 合适的数据处理方法 + 清晰的数据表达。

不要从代码开始，而应该从问题开始。


附录A高阶 NumPy  
附录 B 更多 IPython 系统相关内容  

整理成一张统一思维框架（核心版），你以后看到任何 reshape 操作都能直接定位。

⸻

🧠 Pandas 数据结构变换总地图（核心版）

🟦 一、三种基础形态

① 宽表 Wide
   一行 = 一个对象
   多列 = 多个变量
② 长表 Long（tidy）
   一行 = 一个观测值
   三列：key + variable + value
③ MultiIndex 表
   用 index 表达层级结构

⸻

🔷 二、核心变换关系图（重点）

                 melt
        ┌────────────────────┐
        │                    ↓
    宽表 Wide  ─────────→  长表 Long
        ↑                    │
        │                    │ pivot
        │                    ↓
        └───────────────  宽表 Wide
        stack / unstack（另一条路线）
    宽表 + MultiIndex
        │
        │ stack
        ↓
    长形式 Series
        │
        │ unstack
        ↓
    宽表 DataFrame

⸻

🔷 三、四个核心操作（你必须彻底吃透）

1️⃣ melt（宽 → 长）

记忆：

把“列名”变成“值”

A  B  C
↓  ↓  ↓
variable + value

结构变化：

(宽)
key  A  B  C
(长)
key variable value

⸻

2️⃣ pivot（长 → 宽）

记忆：

把 variable 再变回列

variable → columns
value    → cell

必备三参数：

pivot(index=行, columns=列, values=值)

⸻

3️⃣ stack（列 → 行）

记忆：

把“列压进 index”

columns → index

⸻

4️⃣ unstack（行 → 列）

记忆：

把“index展开成列”

index → columns

⸻

5️⃣ reset_index（救命操作）

记忆：

把 index 变回普通列

index → column

⸻

🔷 四、用你的例子串一遍（最重要）

原始宽表

key   A  B  C
foo   1  4  7
bar   2  5  8
baz   3  6  9

⸻

👉 melt（宽 → 长）

key variable value
foo   A       1
foo   B       4
foo   C       7
...

⸻

👉 pivot（长 → 宽）

        A  B  C
foo     1  4  7
bar     2  5  8
baz     3  6  9

⸻

👉 reset_index（还原结构）

key   A  B  C
foo   1  4  7
bar   2  5  8
baz   3  6  9

⸻

🔷 五、最关键的“本质理解”

这一章所有操作，本质不是数据变化，而是：

🔥 同一份数据，不同“结构视角”的重排

⸻

🔷 六、考试/面试级总结（非常重要）

你只要记住这 3 句话：

1️⃣ melt

列变“变量标签”

⸻

2️⃣ pivot

变量标签变列

⸻

3️⃣ stack/unstack

index 和 columns 的对调

⸻

🔷 七、终极心智模型（建议背这个）

           ┌──────────────┐
           │   Wide表     │
           └──────┬───────┘
                  │ melt
                  ↓
           ┌──────────────┐
           │   Long表     │
           └──────┬───────┘
                  │ pivot
                  ↓
           ┌──────────────┐
           │   Wide表     │
           └──────────────┘
stack/unstack = Wide内部结构翻转
reset_index = 把索引“拉平”

⸻
