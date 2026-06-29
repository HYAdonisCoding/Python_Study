# 往数据库MySQL中新建三张表
CREATE TABLE TransA1710(
shop_id INT,
uid VARCHAR(10),
order_id VARCHAR(20),
date DATETIME,
amt1 DECIMAL(10,2),
amt2 DECIMAL(10,2),
amt3 DECIMAL(10,2),
pay_type TINYINT
);

# 将数据读入到数据框中
CREATE TABLE TransA1801 LIKE TransA1710;
CREATE TABLE TransB1805 LIKE TransA1710;

# 将三张表中支付方式为现金（pay_type=1）的交易合并起来，并且保留门店id、用户id、交易订单号、交易时间和实际交易额信息
LOAD DATA INFILE 'E:/TransA1710.txt' 
INTO TABLE TransA1710 
FIELDS TERMINATED BY '\t' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'E:/TransA1801.txt' 
INTO TABLE TransA1801 
FIELDS TERMINATED BY '\t' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'E:/TransB1805.txt' 
INTO TABLE TransB1805 
FIELDS TERMINATED BY '\t' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT shop_id,uid,order_id,date,amt3
FROM TransA1710
WHERE pay_type = 1
UNION ALL
SELECT shop_id,uid,order_id,date,amt3
FROM TransA1801
WHERE pay_type = 1
UNION ALL
SELECT shop_id,uid,order_id,date,amt3
FROM TransB1805
WHERE pay_type = 1;

USE train;
# ON关键词后面跟不等式
SELECT t1.*,t2.Python,t2.Visualization
FROM stu_info AS t1
LEFT JOIN stu_score AS t2
ON t1.id = t2.id AND MySQL > 90;

# 将不等式条件放在WHERE关键词后面
SELECT t1.*,t2.Python,t2.Visualization
FROM stu_info AS t1
LEFT JOIN stu_score AS t2
ON t1.id = t2.id
WHERE MySQL > 90;


# 创建学生的借书记录表
drop table stu_borrow;
CREATE TABLE stu_borrow(
stu_id VARCHAR(10),
borrow_date DATE,
book_title VARCHAR(500),
book_number VARCHAR(50)
);

# 借书记录的导入
LOAD DATA INFILE 'E:/borrow.csv' 
INTO TABLE stu_borrow 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

# 查询某位学生的借书记录
SELECT * 
FROM stu_borrow 
WHERE stu_id = '9708' 
ORDER BY borrow_date;

# 创建学生的一卡通消费表
CREATE TABLE stu_card(
stu_id VARCHAR(10),
custom_class VARCHAR(10),
custom_add VARCHAR(20),
custom_type VARCHAR(20),
custom_date DATETIME,
amt FLOAT,
balance FLOAT
);

# 一卡通消费表记录的导入
LOAD DATA INFILE 'E:/card.txt' 
INTO TABLE stu_card 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
DROP TABLE stu_dorm;

# 查询某位学生的消费记录
SELECT * 
FROM stu_card 
WHERE stu_id = '1040' 
ORDER BY custom_date;

# 统计2014-9~2015-9学年度每个学生的借书次数以及借阅数量，并将统计结果构成新表
CREATE TABLE borrow_times AS
SELECT stu_id
	,COUNT(DISTINCT borrow_date) AS borrow_times
    ,COUNT(DISTINCT book_title) AS books
FROM stu_borrow
WHERE borrow_date BETWEEN '2014-09-01' AND '2015-08-31'
GROUP BY stu_id;

# 查询统计结果的5行信息
SELECT *
FROM borrow_times
LIMIT 5;

# 删除stu_card表中重复记录以及消费金额为负的记录，并将清洗结果直接存储到stu_card_distinct表中
CREATE TABLE stu_card_distinct AS 
SELECT DISTINCT * 
FROM stu_card
WHERE amt>0;

# 统计2014-9~2015-9学年度每个学生的消费总额，最小金额、最大金额和客单价，并将统计结果直接存储到custom表中
CREATE TABLE custom AS
SELECT stu_id
	,COUNT(*) AS custom_times
	,SUM(amt) AS custom_amt
    ,MIN(amt) AS min_amt
    ,MAX(amt) AS max_amt
    ,SUM(amt)/COUNT(*) pct
FROM stu_card_distinct
WHERE custom_date BETWEEN '2014-09-01' AND '2015-08-31'
GROUP BY stu_id;

# 查询统计结果的5行信息
SELECT * 
FROM custom
LIMIT 5;

# 统计结果的整合
SELECT t1.*, t2.borrow_times,t2.books 
FROM custom AS t1 
LEFT JOIN borrow_times AS t2 
ON t1.stu_id = t2.stu_id;










