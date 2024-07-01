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
def insert_restaurant_datas(datas):
    # 连接到SQLite数据库文件（如果文件不存在，则会自动创建）
    conn = sqlite3.connect('spider_database.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 创建一个名为restaurants的表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            href TEXT,
            comments INTEGER,
            averages TEXT,
            styles TEXT,
            addrs TEXT,
            recommends TEXT,
            group_flag INTEGER,
            discount_flag INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 批量插入数据
    # insert_query = '''
    #     INSERT INTO restaurants (title, href, comments, averages, styles, addrs, recommends, group_flag, discount_flag)
    #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    # '''
    insert_query = '''
        INSERT OR REPLACE INTO restaurants (title, href, comments, averages, styles, addrs, recommends, group_flag, discount_flag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    # 使用 executemany 执行批量插入
    insert_data = [(item['title'], item['href'], item['comments'], item['averages'], item['styles'], item['addrs'], item['recommends'], item['group'], item['discounts']) for item in datas]
    cursor.executemany(insert_query, insert_data)

    # 提交更改（数据的插入）
    conn.commit()

    # 关闭游标对象和连接
    cursor.close()
    conn.close()
    
def alter_table_to_add_unique_constraint():
    conn = sqlite3.connect('spider_database.db')
    cursor = conn.cursor()

    # 为了确保可以成功运行，先删除旧的唯一约束
    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_title ON restaurants (title)
    ''')

    conn.commit()
    cursor.close()
    conn.close()
def get_table_structure(table_name):
    conn = sqlite3.connect('spider_database.db')
    cursor = conn.cursor()

    # 使用 PRAGMA 查询表结构
    cursor.execute(f'PRAGMA table_info({table_name})')
    table_info = cursor.fetchall()

    # 打印表结构信息
    print(f"Table structure for '{table_name}':")
    for column in table_info:
        print(column)

    # 查询表的创建语句
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    create_table_sql = cursor.fetchone()

    print("\nCreate table statement:")
    print(create_table_sql[0])

    cursor.close()
    conn.close()

def test_insert():
    conn = sqlite3.connect('spider_database.db')
    cursor = conn.cursor()
    data = {
    'title': '逗思都吃韩国料理(五道口店)',
    'href': 'https://www.dianping.com/shop/H3SyNUSShP5BYm87',
    'comments': 12562,
    'averages': '￥89',
    'styles': '韩国料理',
    'addrs': '五道口',
    'recommends': '自制金枪鱼饭团|奶酪辣鸡|部队火锅',
    'group_flag': 1,
    'discount_flag': 0
    }

    insert_query = '''
        INSERT OR REPLACE INTO restaurants (title, href, comments, averages, styles, addrs, recommends, group_flag, discount_flag)
        VALUES (:title, :href, :comments, :averages, :styles, :addrs, :recommends, :group_flag, :discount_flag)
    '''

    try:
        cursor.execute(insert_query, data)
        conn.commit()
        print("Data inserted or updated successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting or updating data: {e}")

    # 记得关闭数据库连接
    conn.close()

if __name__ == '__main__':
    # alter_table_to_add_unique_constraint()
    get_table_structure('restaurants')
    # test_insert()