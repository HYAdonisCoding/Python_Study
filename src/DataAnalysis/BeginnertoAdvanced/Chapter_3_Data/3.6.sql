USE train;
# 新建orders_sub表，并且表结构与orders表一致
CREATE TABLE orders_sub LIKE orders;
# 将查询结果插入到数据表orders_sub中
INSERT INTO orders_sub 
SELECT * FROM orders
WHERE Pay_Type IN (1,2,3);

# 预览数据表orders_sub
SELECT * FROM orders_sub LIMIT 10;


# 往stu_info表中新增字段MySQL
ALTER TABLE stu_info ADD COLUMN MySQL INT DEFAULT 0;
# 预览数据表stu_info
SELECT * FROM stu_info;


# 新建数据表
CREATE TABLE user_info(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(10),
gender TINYINT,
age TINYINT
);

# 手工插入记录
INSERT INTO user_info(name,gender,age) VALUES
('张三',1,22),
('李四',1,27),
('王二',0,25),
('丁一',0,32),
('赵五',0,28);

# 设置删除记录权限
SET SQL_SAFE_UPDATES = 0;

# 删除年龄超过30的用户
DELETE FROM user_info
WHERE age>30;

# 查看数据表
SELECT * FROM user_info;


# 使用DELETE关键词清空数据表
DELETE FROM user_info;
# 插入记录
INSERT INTO user_info(name,gender,age) VALUES
('张三',1,22),
('李四',1,27),
('王二',0,25);
# 查看数据表
SELECT * FROM user_info;


# 使用TRUNCATE关键词清空数据表
TRUNCATE TABLE user_info;
# 插入一条记录
INSERT INTO user_info(name,gender,age) VALUES
('张三',1,22),
('李四',1,27),
('王二',0,25);
# 查看数据表
SELECT * FROM user_info;


# 删除订单表orders中的Is_Discount字段
ALTER TABLE orders DROP Is_Discount;
# 查看数据
SELECT * FROM orders LIMIT 10;


# 手工修改表记录
UPDATE stu_info SET email='liuwei2204@163.com'
WHERE id=3;

# 基于一张表更新另一张表
UPDATE stu_info LEFT JOIN stu_score 
ON stu_info.id=stu_score.id
SET stu_info.MySQL=stu_score.MySQL;

# 查看数据
SELECT * FROM stu_info;


# 修改字段类型
ALTER TABLE titanic MODIFY COLUMN PassengerId VARCHAR(10);
# 或者使用CHANGE关键词
# ALTER TABLE titanic CHANGE PassengerId PassengerId VARCHAR(10);

# 修改字段名称
ALTER TABLE titanic CHANGE Sex Gender VARCHAR(10);


# 修改表名称
ALTER TABLE custom RENAME TO stu_custom;