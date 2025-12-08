USE train;
# 没有创建索引之前的条件查询
SELECT *
FROM stu_card
WHERE custom_date BETWEEN '2013-09-01 00:00:00'
	AND '2013-09-01 23:59:59';


# 创建索引
CREATE INDEX date_index ON stu_card(custom_date);
# 执行查询
SELECT *
FROM stu_card
WHERE custom_date BETWEEN '2013-09-01 00:00:00'
	AND '2013-09-01 23:59:59';


# 新建数据表tourism_orders
CREATE TABLE tourism_orders(
userid VARCHAR(20),
orderid VARCHAR(12),
orderTime VARCHAR(15),
orderType VARCHAR(2),
city VARCHAR(20),
country VARCHAR(20),
continent VARCHAR(10));

# 往表中插数据
LOAD DATA INFILE 'E:/tourism_orders.csv' 
INTO TABLE tourism_orders 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# 查询数据前几行
SELECT * FROM tourism_orders LIMIT 10;

# 无索引下的条件查询
SELECT *
FROM tourism_orders
WHERE userid = '100000001445';

# 创建两个组合变量的唯一索引
CREATE UNIQUE INDEX id_idx ON tourism_orders (userid, orderid);
# 再次执行查询语句
SELECT *
FROM tourism_orders
WHERE userid = '100000001445';


# 创建用户注册表和RFM表
CREATE TABLE regit_info(
uid VARCHAR(10),
gender TINYINT,
age TINYINT,
regit_date DATE);

CREATE TABLE RFM(
uid VARCHAR(10),
R INT,
F TINYINT,
M DECIMAL(10,2));

# 批量导入数据
LOAD DATA INFILE 'E:/user_regit_RFM/regit_info.csv' 
INTO TABLE regit_info 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'E:/user_regit_RFM/RFM.csv' 
INTO TABLE RFM 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# 内连接完成两表字段的合并
SELECT t1.*,t2.R,t2.F,t2.M
FROM regit_info AS t1
INNER JOIN RFM AS t2 ON t1.uid=t2.uid;

# 添加主键索引
ALTER TABLE regit_info ADD PRIMARY key (uid);
ALTER TABLE RFM ADD PRIMARY key (uid);

# 再次执行查询
SELECT t1.*,t2.R,t2.F,t2.M
FROM regit_info AS t1
INNER JOIN RFM AS t2 ON t1.uid=t2.uid
LIMIT 1000;

# 查询表tourism_orders中的索引信息
SHOW INDEX FROM regit_info;
SHOW INDEX FROM tourism_orders;

# 删除索引
ALTER TABLE regit_info DROP PRIMARY KEY;
DROP INDEX id_idx ON tourism_orders;