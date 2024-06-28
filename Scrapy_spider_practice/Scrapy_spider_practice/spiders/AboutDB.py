import sqlite3

def insert_datas(datas):
    # 连接到SQLite数据库文件（如果文件不存在，则会自动创建）
    conn = sqlite3.connect('spider_database.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 创建一个名为jobs的表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            locations TEXT,
            salaries TEXT,
            experience_education TEXT,
            skills TEXT,
            benefits TEXT,
            company_logos TEXT,
            company_href TEXT,
            company_name TEXT,
            company_info TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 示例插入数据
    cursor.executemany('''
        INSERT INTO jobs (type, title, locations, salaries, experience_education, skills, benefits, company_logos, company_href, company_name, company_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', datas)

    # 提交更改（数据的插入）
    conn.commit()

    # 关闭游标对象和连接
    cursor.close()
    conn.close()
