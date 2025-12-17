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

def export_db_to_csv_pro(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 获取所有数据
    cursor.execute("SELECT * FROM pesticide_data")
    rows = cursor.fetchall()

    # 获取列名
    column_names = [description[0] for description in cursor.description]

    # 先找出最大有效成分数量
    max_components = 0
    comp_lists = []
    for row in rows:
        val = row[column_names.index("有效成分信息")]
        try:
            comps = json.loads(val) if val else []
            if not isinstance(comps, list):
                comps = []
        except:
            comps = []
        comp_lists.append(comps)
        max_components = max(max_components, len(comps))

    # 生成新的列名，追加有效成分列
    expanded_column_names = column_names.copy()
    for i in range(1, max_components + 1):
        expanded_column_names.extend([
            f"有效成分{i}",
            f"有效成分{i}英文",
            f"有效成分{i}含量"
        ])

    # 写入 CSV
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(expanded_column_names)

        for row, comps in zip(rows, comp_lists):
            processed_row = list(row)  # 复制原始数据
            # 追加每个有效成分的值
            for comp in comps:
                processed_row.append(comp.get("有效成分", ""))
                processed_row.append(comp.get("有效成分英文名", ""))
                processed_row.append(comp.get("有效成分含量", ""))
            # 如果这一行有效成分少于 max_components，补空列
            empty_cols = (max_components - len(comps)) * 3
            processed_row.extend([""] * empty_cols)

            writer.writerow(processed_row)

    conn.close()
    print(f"✅ 数据已成功导出至 {csv_path}")
def export_db_to_csv_pro_max(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pesticide_data")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    idx_reg_info = column_names.index("登记证信息")
    idx_comp_info = column_names.index("有效成分信息")
    idx_dosage_info = column_names.index("制剂用药量信息")

    # ===== 解析登记证信息（去重字段）=====
    main_fields = set(column_names)
    reginfo_keys = set()
    reginfo_list = []

    for row in rows:
        try:
            info = json.loads(row[idx_reg_info]) if row[idx_reg_info] else {}
            if not isinstance(info, dict):
                info = {}
        except:
            info = {}
        reginfo_list.append(info)
        for k in info.keys():
            if k not in main_fields:
                reginfo_keys.add(k)

    reginfo_keys = sorted(reginfo_keys)

    # ===== 解析有效成分信息 =====
    comp_lists = []
    max_components = 0
    for row in rows:
        try:
            comps = json.loads(row[idx_comp_info]) if row[idx_comp_info] else []
            if not isinstance(comps, list):
                comps = []
        except:
            comps = []
        comp_lists.append(comps)
        max_components = max(max_components, len(comps))

    # ===== 解析制剂用药量信息 =====
    dosage_lists = []
    max_dosages = 0
    for row in rows:
        try:
            dosages = json.loads(row[idx_dosage_info]) if row[idx_dosage_info] else []
            if not isinstance(dosages, list):
                dosages = []
        except:
            dosages = []
        dosage_lists.append(dosages)
        max_dosages = max(max_dosages, len(dosages))

    # ===== 构造表头 =====
    base_columns = [
        c for c in column_names
        if c not in ("登记证信息", "有效成分信息", "制剂用药量信息")
    ]

    expanded_columns = base_columns + reginfo_keys

    for i in range(1, max_components + 1):
        expanded_columns.extend([
            f"有效成分{i}",
            f"有效成分{i}英文",
            f"有效成分{i}含量"
        ])

    for i in range(1, max_dosages + 1):
        expanded_columns.extend([
            f"用药{i}_作物/场所",
            f"用药{i}_防治对象",
            f"用药{i}_用药量",
            f"用药{i}_施用方法"
        ])

    # ===== 写入 CSV =====
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(expanded_columns)

        for row, reginfo, comps, dosages in zip(rows, reginfo_list, comp_lists, dosage_lists):
            base_row = [
                row[column_names.index(c)] for c in base_columns
            ]

            # 登记证信息补充字段
            for k in reginfo_keys:
                base_row.append(reginfo.get(k, ""))

            # 有效成分展开
            for comp in comps:
                base_row.append(comp.get("有效成分", ""))
                base_row.append(comp.get("有效成分英文名", ""))
                base_row.append(comp.get("有效成分含量", ""))
            base_row.extend([""] * ((max_components - len(comps)) * 3))

            # 制剂用药量展开
            for d in dosages:
                base_row.append(d.get("作物/场所", ""))
                base_row.append(d.get("防治对象", ""))
                base_row.append(d.get("用药量", ""))
                base_row.append(d.get("施用方法", ""))
            base_row.extend([""] * ((max_dosages - len(dosages)) * 4))

            writer.writerow(base_row)

    conn.close()
    print(f"✅ 数据已成功导出至 {csv_path}")
# 统计有效成分信息中 有效成分、有效成分英文名 出现的次数
def statistical_information_effective_components(db_path=DB_FILE, top=10):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT 有效成分信息 FROM pesticide_data")
    rows = cursor.fetchall()

    from collections import Counter
    cn_counter = Counter()
    en_counter = Counter()

    for (val,) in rows:
        try:
            comps = json.loads(val) if val else []
            if not isinstance(comps, list):
                continue
        except:
            continue

        for comp in comps:
            cn = comp.get("有效成分")
            en = comp.get("有效成分英文名")
            if cn:
                cn_counter[cn] += 1
            if en:
                en_counter[en] += 1

    conn.close()

    # ===== 终端输出 =====
    print(f"\n📊 有效成分（中文）出现次数 Top {top}:")
    for name, cnt in cn_counter.most_common(top):
        print(f"{name}：{cnt}")

    print(f"\n📊 有效成分（英文）出现次数 Top {top}:")
    for name, cnt in en_counter.most_common(top):
        print(f"{name}：{cnt}")

    print(f"\n✅ 统计完成：共统计中文 {len(cn_counter)} 种，英文 {len(en_counter)} 种有效成分")

    # ===== 写入 CSV =====
    cn_csv = os.path.join(BASE_DIR, "effective_components_cn_stats.csv")
    en_csv = os.path.join(BASE_DIR, "effective_components_en_stats.csv")

    with open(cn_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["有效成分", "出现次数"])
        for name, cnt in cn_counter.most_common():
            writer.writerow([name, cnt])

    with open(en_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["有效成分英文名", "出现次数"])
        for name, cnt in en_counter.most_common():
            writer.writerow([name, cnt])

    print(f"\n📁 CSV 已生成：")
    print(f" - {cn_csv}")
    print(f" - {en_csv}")
    
    
# 执行导出
if __name__ == '__main__':
    # data_todb()
    statistical_information_effective_components(DB_FILE)
