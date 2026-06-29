# 选择指定的数据库
USE train;

# 查询二手房所有字段的信息
SELECT * 
FROM sec_buildings;

# 查询二手房的小区名称、户型、面积、单价和总价
SELECT name,type,size,price_unit,tot_amt 
FROM sec_buildings;

# 查询所有阳台朝西的二手房信息
SELECT * 
FROM sec_buildings
WHERE direction = '朝西';

# 查询2014年新建的浦东、徐汇、静安、黄浦和长宁二手房信息
SELECT *
FROM sec_buildings
WHERE built_date = '2014年建\r' 
	AND region IN('浦东','徐汇','静安','黄浦','长宁');

# 查询黄浦区房价在7500万以上的二手房名称、户型、面积、朝向和楼层
SELECT name,type,size,direction,floow
FROM sec_buildings
WHERE region = '黄浦' AND tot_amt > 7500;

# 查询浦东新区面积在60~70平之间的二手房名称、类型、面积和总价
SELECT name,type,size,tot_amt 
FROM sec_buildings
WHERE region = '浦东' AND size BETWEEN 60 AND 70;

# 查询小区名称中包含"新天地"字样的二手房信息
SELECT * 
FROM sec_buildings
WHERE name LIKE '%新天地%';

# 查询各行政区域下二手房的数量、总的可居住面积、平均总价格、最大总价格和最小单价
SELECT region,COUNT(*) AS counts,SUM(size) AS tot_size,
	   AVG(tot_amt) AS avg_amt,MAX(tot_amt) AS max_amt,MIN(price_unit) AS min_price
FROM sec_buildings
GROUP BY region;

# 计算客户在1~6月份之间的R、M、F指标值
SELECT Uid,Datediff('2018-06-30',MAX(Order_Date)) AS R,
	   COUNT(DISTINCT Order_Id) AS F,SUM(Order_Amt) AS M
FROM orders
WHERE Order_Date BETWEEN '2018-01-01 00:00:00' AND '2018-06-30 23:59:59'
GROUP BY Uid;

# 按照地区、户型、楼层和朝向分组统计黄浦区与浦东新区二手房的平均单价和总数量,并筛选出平均单价超过100000元的记录
SELECT region,type,floow,direction,
	   AVG(price_unit) AS avg_price, COUNT(*) AS counts
FROM sec_buildings
WHERE region IN ('浦东','黄浦')
GROUP BY region,type,floow,direction
HAVING AVG(price_unit) > 100000;

# 按面积降序、总价升序的方式查询出所有2室2厅的二手房信息（返回小区名称、面积、总价、单价、区域和朝向）
SELECT name,size,tot_amt,price_unit,region,direction
FROM sec_buildings
WHERE type = '2室2厅'
ORDER BY size DESC, tot_amt;

# 按照地区、户型、楼层和朝向分组统计黄浦区与浦东新区二手房的平均单价和平均面积，并按平均单价升序，平均面积降序排序alter
SELECT region,type,floow,direction,
	   AVG(size) AS avg_size,AVG(price_unit) AS avg_price
FROM sec_buildings
WHERE region IN ('浦东','黄浦')
GROUP BY region,type,floow,direction
ORDER BY AVG(size), AVG(price_unit) DESC;

# 查询出建筑时间最悠久的5套二手房
SELECT * 
FROM sec_buildings
WHERE built_date != '\r'
ORDER BY built_date
LIMIT 5;

# 查询出浦东新区2010年建的二手房，并且总价排名在6~10
SELECT * 
FROM sec_buildings
WHERE region = '浦东' 
	AND built_date = '2013年建\r'
ORDER BY tot_amt DESC
LIMIT 5,5;


# 新建数据表
CREATE TABLE Orders(
Uid CHAR(7),
Birthday DATE,
Order_Date DATETIME,
Order_Id VARCHAR(15),
Pay_Type TINYINT,
Pay_Amt DECIMAL(10,2),
Is_Discount TINYINT
);

# 数据读入
LOAD DATA INFILE 'E:/Orders.csv' 
INTO TABLE Orders 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# 数据前10行的预览
SELECT *
FROM Orders
LIMIT 5;

# 离散数值与实际含义的映射
SELECT *,
	CASE WHEN Is_Discount = 1 THEN '享受折扣'
    ELSE '无折扣' END AS Discount_New,
    CASE WHEN Pay_Type IN (1,3,5,7,10) THEN '微信支付'
    WHEN Pay_Type IN (6,9,12) THEN '快捷支付'
    ELSE '支付宝支付' END AS Pay_Type_New
FROM Orders
LIMIT 5;

# 连续数值转离散值
SELECT *,
    CASE WHEN YEAR(Birthday) BETWEEN 1960 AND 1969 THEN '60后'
    WHEN YEAR(Birthday) BETWEEN 1970 AND 1979 THEN '70后'
    WHEN YEAR(Birthday) BETWEEN 1980 AND 1989 THEN '80后'
    ELSE '90后' END AS Age_Group
FROM Orders
LIMIT 5;

# 构建长形统计表
SELECT MONTH(Order_Date) AS Month,
    CASE WHEN Pay_Type IN (1,3,5,7,10) THEN '微信支付'
    WHEN Pay_Type IN (6,9,12) THEN '快捷支付'
    ELSE '支付宝支付' END AS Pay_Type,
    SUM(Pay_Amt) AS Amt
FROM Orders
WHERE YEAR(Order_Date) = 2018
GROUP BY MONTH(Order_Date),
    CASE WHEN Pay_Type IN (1,3,5,7,10) THEN '微信支付'
    WHEN Pay_Type IN (6,9,12) THEN '快捷支付'
    ELSE '支付宝支付' END;
    
 # 构建宽形统计表 
 SELECT MONTH(Order_Date) AS Month,
    SUM(CASE WHEN Pay_Type IN (1,3,5,7,10) THEN Pay_Amt END) AS 'Wechat',
    SUM(CASE WHEN Pay_Type IN (6,9,12) THEN Pay_Amt END) AS 'Bank_Card',
    SUM(CASE WHEN Pay_Type NOT IN (1,3,5,7,10,6,9,12) THEN Pay_Amt END) AS 'Ali_Pay'
FROM Orders
WHERE YEAR(Order_Date) = 2018
GROUP BY MONTH(Order_Date)
ORDER BY MONTH(Order_Date);

# 创建学员信息表
CREATE TABLE stu_info(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(20),
gender CHAR(1),
department VARCHAR(10),
age TINYINT,
province VARCHAR(10),
email VARCHAR(50),
mobilephone CHAR(11)
 );

# 创建学员成绩表
CREATE TABLE stu_score(
id INT ,
MySQL TINYINT,
Python TINYINT,
Visualization TINYINT
 );

# 向学员表中插入数据
 INSERT INTO stu_info(name,gender,department,age,province,email,mobilephone) VALUES
('张勇','男','数学系',23,'河南','sfddf123dd@163.com','13323564321'),
('王兵','男','数学系',25,'江苏','lss1993@163.com','17823774329'),
('刘伟','男','计算机系',21,'江苏','qawsed112@126.com','13834892240'),
('张峰','男','管理系',22,'上海','102945328@qq.com','13923654481'),
('董敏','女','生物系',22,'浙江','82378339@qq.com','13428439022'),
('徐晓红','女','计算机系',24,'浙江','xixiaohong@gmail.com','13720097528'),
('赵伊美','女','数学系',21,'江苏','zhaomeimei@163.com','13417723980'),
('王建国','男','管理系',24,'浙江','9213228402@qq.com','13768329901'),
('刘清','女','统计系',23,'安徽','lq1128@gmail.com','17823651180'),
('赵家和','男','计算机系',28,'山东','dcrzdbjh@163.com','13827811311');

# 向成绩表中插入数据
 INSERT INTO stu_score VALUES
 (1,87,72,88),
 (3,90,66,72),
 (2,90,70,86),
 (4,88,82,76),
 (8,92,67,80),
 (10,88,82,89),
 (5,79,66,60),
 (7,91,78,90),
 (6,82,79,88),
 (9,85,70,85);
 
# 查询表中数据
SELECT * FROM stu_info;
SELECT * FROM stu_score;

# 查询与张勇、刘伟同一个系的学员信息
SELECT *
FROM stu_info
WHERE department IN (SELECT department FROM stu_info WHERE name IN('张勇','刘伟'));

# 查询MySQL成绩大于90分的学员信息
SELECT * 
FROM stu_info 
WHERE id IN (SELECT id FROM stu_score WHERE MySQL > 90);

SELECT *
FROM stu_info
WHERE EXISTS(SELECT * FROM stu_score WHERE id = stu_info.id AND MySQL > 90);

# 查询年龄超过所属系科平均年龄的学员信息
SELECT * FROM stu_info AS t1
WHERE  age >= (SELECT AVG(age) FROM stu_info AS t2 
				WHERE t1.department = t2.department);


# 查询非管理系中比管理系任意一个学员年龄小的学员信息
SELECT * FROM stu_info
WHERE age <ANY (SELECT DISTINCT age FROM stu_info 
				WHERE department = '管理系')
	AND department != '管理系';

# 查询非管理系中比管理系所有学员年龄大的学员信息
SELECT * FROM stu_info
WHERE age <ALL (SELECT DISTINCT age FROM stu_info 
				WHERE department = '管理系')
	AND department != '管理系';
	
	
# 创建虚拟的业务员销售数据
CREATE TABLE Sales(
date date,
name char(2),
sales int);

# 向表中插入数据
INSERT INTO Sales VALUES
('2018/1/1', '丁一', 200),
('2018/2/1', '丁一', 180),
('2018/2/1', '李四', 100),
('2018/3/1', '李四', 150),
('2018/3/1', '刘猛', 80),
('2018/1/1', '王二', 200),
('2018/2/1', '王二', 270),
('2018/3/1', '王二', 300),
('2018/1/1', '张三', 300),
('2018/2/1', '张三', 280),
('2018/3/1', '张三', 280);

# 数据查询
SELECT * FROM Sales;

# 实现ROW_NUMBER OVER(PARTITION BY ORDER BY)的功能 
SET @num := 0, @temp_date := NULL;
SELECT t1.*,
@num := IF(@temp_date = t1.date, @num + 1, 1) AS row_num,
@temp_date := t1.date AS temp_date
FROM Sales t1
ORDER BY date, sales;


# 基于如上的排序风格，查询各月中销售最差的业务员
SET @num := 0, @temp_date := NULL;
SELECT date,name,sales
FROM (
SELECT t1.*,
@num := IF(@temp_date = t1.date, @num + 1, 1) AS row_num,
@temp_date := t1.date AS temp_date
FROM Sales t1
ORDER BY date, sales) tt
WHERE row_num = 1;

# 实现DENSE_RANK OVER(PARTITION BY ORDER BY)的功能
SET @num := 0, @temp_date := '', @temp_sales := 0;
SELECT t1.*,
@num := IF(@temp_date = t1.date, IF(@temp_sales = sales, @num,@num + 1), 1) AS dense_num,
@temp_date := t1.date AS temp_date,
@temp_sales := t1.sales AS temp_sales
FROM Sales t1
ORDER BY date, sales;

# 实现RANK OVER(PARTITION BY ORDER BY)的功能
SET @num1 := 0, @num2 := 0, @temp_date := '', @temp_sales := 0;
SELECT t1.*,
@num1 := IF(@temp_date = t1.date, @num1 + 1, 1) AS row_num,
@num2 := IF(@temp_date = t1.date, IF(@temp_sales = sales, @num2, @num1), 1) AS rank_num,
@temp_date := t1.date AS temp_date,
@temp_sales := t1.sales AS temp_sales
FROM Sales t1
ORDER BY date, sales;