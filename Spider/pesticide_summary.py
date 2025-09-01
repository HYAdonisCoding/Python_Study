import os
import sqlite3
from .icama_data_cleaning import DB_FILE,DATA_DIR
import logging
from . import icama_spider_optimized_list, icama_data_cleaning

def summary():
    # 连接数据库
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 查询每种农药名称及对应数量
    cursor.execute("""
        SELECT 农药名称, COUNT(*) AS 数量
        FROM pesticide_data
        GROUP BY 农药名称
        ORDER BY 数量 DESC
    """)
    rows = cursor.fetchall()

    # 导出到 TXT
    with open(os.path.join(DATA_DIR, "pesticide_name_counts.txt"), "w", encoding="utf-8") as f:
        for name, count in rows:
            f.write(f"{name}: {count}\n")

    print("导出完成：pesticide_name_counts.txt")
    conn.close()

def icama_spider():
    """
    调度 icama 爬虫：
    1. 先抓取列表页，存入数据库
    2. 再抓取详情页，存入数据库
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        logging.info("===== 开始抓取列表数据 =====")
        icama_spider_optimized_list.main()
        logging.info("===== 列表数据抓取完成 =====")
    except Exception as e:
        logging.error(f"列表爬虫出错: {e}", exc_info=True)

    try:
        logging.info("===== 开始抓取详情数据 =====")
        icama_data_cleaning.main()
        logging.info("===== 详情数据抓取完成 =====")
    except Exception as e:
        logging.error(f"详情爬虫出错: {e}", exc_info=True)
if __name__ == "__main__":
    # 运行数据统计脚本
    summary()