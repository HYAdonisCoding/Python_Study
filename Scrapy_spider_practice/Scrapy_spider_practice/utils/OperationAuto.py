import os
import sqlite3
import json

# 获取 JSON 文件的路径（上一层目录）
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 获取 JSON 文件的绝对路径（上一层目录）
json_file_path = os.path.abspath(os.path.join(current_directory, '..', 'autos.json'))
# print(f"current_directory：{current_directory}，\nJSON file path: {json_file_path}")

# 读取 JSON 文件
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
print(f"data: {len(data)}")
db_file_path = os.path.abspath(os.path.join(current_directory, '../spiders', 'spider_database.db'))
print(db_file_path)
# 连接到 SQLite 数据库（如果数据库不存在，会自动创建）
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# 创建 movies 表（如果表不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS autos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        url TEXT,
        price TEXT,
        score TEXT,
        models TEXT,
        rank_type TEXT,
        rank_number INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# 插入数据
for item in data:
    try:
        cursor.execute('''
            INSERT INTO autos (name, url, price, score, models, rank_type, rank_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            item['name'],
            item['url'],
            item['price'],
            item['score'],
            item['models'],
            item['rank_type'],
            item['rank_number']
        ))
    except sqlite3.IntegrityError:
        print(f"Duplicate entry for {item['name']}")
    except Exception as e:
        print(f"Error inserting {item['name']}: {e}")

# 提交并关闭数据库连接
conn.commit()
conn.close()

print("Data imported successfully.")
