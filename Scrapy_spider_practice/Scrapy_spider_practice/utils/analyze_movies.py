import sqlite3
import os

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 连接到 SQLite 数据库
db_path = os.path.abspath(os.path.join(current_directory, '../spiders', 'spider_database.db'))
print(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询电影数据
cursor.execute('SELECT name, country FROM movies')
movies = cursor.fetchall()

# 定义一个函数检查电影是否属于中国
def is_chinese_movie(country):
    if any(keyword in country for keyword in ['中国', '香港', '大陆', '台湾']):
        return True
    return False

# 统计中国电影数量
chinese_movies = [movie for movie in movies if is_chinese_movie(movie[1])]
num_chinese_movies = len(chinese_movies)

# 输出结果
print(f"Total number of movies: {len(movies)}")
print(f"Number of Chinese movies: {num_chinese_movies}")

# 如果需要详细列表
for movie in chinese_movies:
    print(f"Movie: {movie[0]}, Country: {movie[1]}")

# 关闭数据库连接
conn.close()
