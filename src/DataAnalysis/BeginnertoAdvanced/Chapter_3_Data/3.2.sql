# 新建数据库
CREATE DATABASE train;

# 指定接下来需要操作的数据库
USE train;

# 新建数据表
CREATE TABLE user_info(
memid INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(10),
gender ENUM('男','女'),
tel CHAR(11) NOT NULL UNIQUE,
income DECIMAL(10,2),
birthday DATE DEFAULT '1990-01-01',
interest SET('篮球','唱歌','足球','骑行','乒乓球','象棋'),
regist_date DATETIME,
email VARCHAR(20),
edu VARCHAR(10)
) AUTO_INCREMENT = 100001;


# 指定需要操作的数据库
USE train;

drop table film_top10;
# 构建用于存储Top10电影的空表
CREATE TABLE film_top10(
rank TINYINT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
uptime YEAR,
country VARCHAR(20),
director VARCHAR(30),
type SET('剧情','犯罪','爱情','同性','动作','喜剧','战争','动画','奇幻','灾难','历史','悬疑','冒险','科幻'),
score DECIMAL(2,1),
Num_Commentaries INT,
description VARCHAR(100)
);

# 插入数据
INSERT INTO film_top10(name,uptime,country,director,type,score,Num_Commentaries,description) VALUES
('肖申克的救赎',1994,'美国','弗兰克·德拉邦特','犯罪,剧情',9.6,1034791,'希望让人自由。'),
('霸王别姬',1993,'中国大陆 香港','陈凯歌','剧情,爱情,同性',9.5,753297,'风华绝代。'),
('这个杀手不太冷',1994,'法国','吕克·贝松','剧情,动作,犯罪',9.4,968089,'怪蜀黍和小萝莉不得不说的故事。'),
('阿甘正传',1994,'美国','Robert Zemeckis','剧情,爱情',9.4,824062,'一部美国近现代史。'),
('美丽人生',1997,'意大利','罗伯托·贝尼尼','剧情,喜剧,爱情,战争',9.5,481250,'最美的谎言。'),
('千与千寻',2001,'日本','宫崎骏','剧情,动画,奇幻',9.3,771592,'最好的宫崎骏，最好的久石让。'),
('泰坦尼克号',1997,'美国','詹姆斯·卡梅隆','剧情,爱情,灾难',9.3,763515,'失去的才是永恒的。'),
('辛德勒的名单',1993,'美国','史蒂文·斯皮尔伯格','剧情,历史,战争',9.4,437907,'拯救一个人，就是拯救整个世界。'),
('盗梦空间',2010,'美国 英国','克里斯托弗·诺兰','剧情,科幻,悬疑,冒险',9.3,861722,'诺兰给了我们一场无法盗取的梦。'),
('机器人总动员',2008,'美国','安德鲁·斯坦顿','爱情,科幻,动画,冒险',9.3,565035,'小瓦力，大人生。');

# 查看数据表
SELECT * FROM film_top10;

# 往表中插入字符型的数值
INSERT INTO film_top10(name,uptime,score,Num_Commentaries) VALUES
('三傻大闹宝莱坞','2009','9.2',775279),
('海上钢琴师','1998','9.2',663039);

# 查看数据表
SELECT * FROM film_top10;

# 查看批量导入的数据
SELECT * FROM Titanic;


# 新建存储二手房数据的表格
CREATE TABLE sec_buildings (
    name VARCHAR(20),
    type VARCHAR(10),
    size DECIMAL(10,2),
    region VARCHAR(10),
    floow VARCHAR(20),
    direction VARCHAR(20),
    tot_amt INT,
    price_unit INT,
    built_date VARCHAR(20)
);

# 使用命令行完成数据的批量导入
LOAD DATA INFILE 'E:/sec_buildings.csv' 
INTO TABLE sec_buildings 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

# 查看数据
select * from sec_buildings;