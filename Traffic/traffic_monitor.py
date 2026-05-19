import requests
from bs4 import BeautifulSoup
import sqlite3
import schedule
import time
from datetime import datetime

# ================= 1. 数据库初始化 =================
def init_db():
    """初始化 SQLite 数据库和表结构"""
    conn = sqlite3.connect('beijing_traffic.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS congestion_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fetch_time TEXT,
            region_name TEXT,
            traffic_index REAL,
            congestion_level TEXT,
            avg_speed REAL
        )
    ''')
    conn.commit()
    conn.close()

# ================= 2. 数据抓取与解析 =================
def fetch_and_parse_data():
    """抓取网页并解析表格数据"""
    url = "https://service.jtw.beijing.gov.cn/uservice/app/congestion/serviceCongestion"
    
    # 模拟真实浏览器请求头，防止被基础反爬拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # 检查请求是否成功
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 定位目标表格
        table = soup.find('table', class_='qyzs_table')
        if not table:
            print(f"[{datetime.now()}] 未找到目标表格，网页结构可能已更改。")
            return []

        # 提取数据行 (跳过第一行表头)
        rows = table.find_all('tr')[1:]
        data_list = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                region = cols[0].text.strip()
                t_index = float(cols[1].text.strip())
                level = cols[2].text.strip()
                speed = float(cols[3].text.strip())
                
                data_list.append((current_time, region, t_index, level, speed))
                
        return data_list

    except Exception as e:
        print(f"[{datetime.now()}] 抓取数据时发生错误: {e}")
        return []

# ================= 3. 数据存储 =================
def save_to_db(data_list):
    """将数据批量写入 SQLite 数据库"""
    if not data_list:
        return
        
    conn = sqlite3.connect('beijing_traffic.db')
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO congestion_data (fetch_time, region_name, traffic_index, congestion_level, avg_speed)
        VALUES (?, ?, ?, ?, ?)
    ''', data_list)
    conn.commit()
    conn.close()
    print(f"[{datetime.now()}] 成功抓取并存储 {len(data_list)} 条交通数据。")

# ================= 4. 核心任务调度 =================
def job():
    """定义单次执行的工作流"""
    print(f"[{datetime.now()}] 开始执行定时抓取任务...")
    data = fetch_and_parse_data()
    save_to_db(data)

if __name__ == "__main__":
    # 初始化数据库
    init_db()
    
    # 脚本启动时先执行一次
    job()
    
    # 设置定时任务：每小时执行一次
    schedule.every().hour.at(":00").do(job)  # 可以在每个整点执行
    
    print("服务已启动，正在后台进行每小时的定时抓取... (按 Ctrl+C 终止)")
    
    # 保持主线程运行
    while True:
        schedule.run_pending()
        time.sleep(1)