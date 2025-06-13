import os
import json
import sqlite3
from glob import glob
import csv
from datetime import datetime

# 配置路径
BASE_DIR = "./data"
DB_FILE = os.path.join(BASE_DIR, "pesticide_data.db")
PROGRESS_FILE = os.path.join(BASE_DIR, "import_progress.txt")
LOG_FILE = os.path.join(BASE_DIR, 'db_import_log.txt')

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 1
    with open(PROGRESS_FILE, "r") as f:
        return int(f.read().strip() or 1)

def save_progress(page_no):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(page_no))
        
def log_entry(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")
def data_todb(end_page=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pesticide_data (
        登记证号 TEXT PRIMARY KEY,
        农药名称 TEXT,
        农药类别 TEXT,
        剂型 TEXT,
        总含量 TEXT,
        有效期至 TEXT,
        登记证持有人 TEXT,
        pd_id TEXT,
        登记证信息 TEXT,
        有效成分信息 TEXT,
        制剂用药量信息 TEXT
    )
    """)
    conn.commit()

    start_page = load_progress()
    json_files = sorted(glob(os.path.join(BASE_DIR, "page_*.json")))
    total_inserted = 0
    total_updated = 0

    for file_path in json_files:
        filename = os.path.basename(file_path)
        try:
            page_no = int(filename.split('_')[1].split('.')[0])
        except ValueError:
            continue

        if page_no < start_page:
            continue
        # 页码过滤
        if page_no < start_page:
            continue
        if end_page is not None and page_no > end_page:
            break
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                records = json.load(f)

            insert_count = 0
            update_count = 0

            for entry in records:
                djzh = entry.get("登记证号")
                if not djzh:
                    continue

                cursor.execute("SELECT 1 FROM pesticide_data WHERE 登记证号 = ?", (djzh,))
                exists = cursor.fetchone() is not None

                cursor.execute("""
                    INSERT INTO pesticide_data (
                        登记证号, 农药名称, 农药类别, 剂型, 总含量, 有效期至,
                        登记证持有人, pd_id, 登记证信息, 有效成分信息, 制剂用药量信息
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(登记证号) DO UPDATE SET
                        农药名称=excluded.农药名称,
                        农药类别=excluded.农药类别,
                        剂型=excluded.剂型,
                        总含量=excluded.总含量,
                        有效期至=excluded.有效期至,
                        登记证持有人=excluded.登记证持有人,
                        pd_id=excluded.pd_id,
                        登记证信息=excluded.登记证信息,
                        有效成分信息=excluded.有效成分信息,
                        制剂用药量信息=excluded.制剂用药量信息
                """, (
                    djzh,
                    entry.get("农药名称"),
                    entry.get("农药类别"),
                    entry.get("剂型"),
                    entry.get("总含量"),
                    entry.get("有效期至"),
                    entry.get("登记证持有人"),
                    entry.get("pd_id"),
                    json.dumps(entry.get("登记证信息", ""), ensure_ascii=False),
                    json.dumps(entry.get("有效成分信息", []), ensure_ascii=False),
                    json.dumps(entry.get("制剂用药量信息", []), ensure_ascii=False),
                ))

                if exists:
                    update_count += 1
                else:
                    insert_count += 1

            conn.commit()
            total_inserted += insert_count
            total_updated += update_count
            save_progress(page_no + 1)

            log_entry(f"✅ {filename} 导入完成：新增 {insert_count} 条，更新 {update_count} 条")
            print(f"✅ 已导入 {filename}，新增 {insert_count}，更新 {update_count}")

        except Exception as e:
            log_entry(f"❌ {filename} 导入失败：{e}")
            print(f"❌ 错误：{filename} 导入失败 - {e}")

    conn.close()
    log_entry(f"✅ 所有文件处理完成，共新增 {total_inserted} 条，更新 {total_updated} 条")
    print(f"✅ 所有文件处理完成，共新增 {total_inserted} 条，更新 {total_updated} 条")


CSV_FILE = os.path.join(BASE_DIR, "pesticide_data_export.csv")
# 导出数据到 CSV
def export_db_to_csv(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取所有数据
    cursor.execute("SELECT * FROM pesticide_data")
    rows = cursor.fetchall()

    # 获取列名
    column_names = [description[0] for description in cursor.description]

    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)  # 写入表头
        for row in rows:
            # 把 json 列转为纯文本（如有）
            processed_row = []
            for value in row:
                if isinstance(value, str):
                    try:
                        val = json.loads(value)
                        if isinstance(val, (dict, list)):
                            processed_row.append(json.dumps(val, ensure_ascii=False))
                        else:
                            processed_row.append(val)
                    except:
                        processed_row.append(value)
                else:
                    processed_row.append(value)
            writer.writerow(processed_row)

    conn.close()
    print(f"✅ 数据已成功导出至 {csv_path}")

# 执行导出
if __name__ == '__main__':
    # data_todb()
    export_db_to_csv(DB_FILE, CSV_FILE)
