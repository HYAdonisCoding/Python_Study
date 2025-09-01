from datetime import datetime
import os
import re
import time
import json
import sqlite3
import logging
import random
import requests, certifi
from bs4 import BeautifulSoup
from tqdm import tqdm

# === 配置区 ===
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "pesticide_data.db")
PROGRESS_FILE = os.path.join(DATA_DIR, "sync_progress.txt")
LOG_FILE = os.path.join(DATA_DIR, "sync_log.txt")

os.makedirs(DATA_DIR, exist_ok=True)

# === 日志配置 ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "DNT": "1",
    "Referer": "http://www.icama.org.cn/",
    "Sec-Fetch-Dest": "iframe",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Storage-Access": "none",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}


# === 工具函数 ===
def save_progress(page):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(page))


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return int(f.read().strip() or 1)
    return 1


def fetch_list_page(page):
    url = "https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do"
    data = {
        "pageNo": page,
        "pageSize": 20,
        "djzh": "",
        "nymc": "",
        "cjmc": "",
        "sf": "",
        "nylb": "",
        "zhl": "",
        "jx": "",
        "zwmc": "",
        "fzdx": "",
        "syff": "",
        "dx": "",
        "yxcf": "",
        "yxcf_en": "",
        "yxcfhl": "",
        "yxcf2": "",
        "yxcf2_en": "",
        "yxcf2hl": "",
        "yxcf3": "",
        "yxcf3_en": "",
        "yxcf3hl": "",
        "yxqs_start": "",
        "yxqs_end": "",
        "yxjz_start": "",
        "yxjz_end": "",
        "accOrfuzzy": "2",
    }
    try:
        response = requests.post(url, headers=HEADERS, verify=False, data=data, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e_post:
        logging.warning(f"⚠️ POST 请求失败，第 {page} 页: {e_post}")

        # 尝试 GET 备选方案
        try:
            response = requests.get(url, headers=HEADERS, verify=False, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e_get:
            logging.error(f"❌ GET 备选方案失败，第 {page} 页: {e_get}")
            return None


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    viewpd_pattern = re.compile(r"_viewpd\('([^']+)'\)")
    table = soup.find_all("table")[1]
    rows = table.find_all("tr")
    headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
    records = []
    for row in rows[1:]:
        cols = row.find_all("td")
        values = [td.get_text(strip=True) for td in cols]
        pd_id = None
        for td in cols:
            a_tag = td.find("a", onclick=viewpd_pattern)
            if a_tag:
                match = viewpd_pattern.search(a_tag["onclick"])
                if match:
                    pd_id = match.group(1)
        record = dict(zip(headers, values))
        if pd_id:
            record["pd_id"] = pd_id
        records.append(record)
    return records


def extract_total_pages_and_records(html):
    soup = BeautifulSoup(html, "html.parser")
    controls_li = soup.select_one(".pagination li.disabled.controls")
    logging.debug(f"controls_li = {controls_li}")

    if controls_li:
        inputs = controls_li.find_all("input")
        if len(inputs) >= 2:
            current_page = int(inputs[0]["value"])
            total_pages = int(inputs[1]["value"])
            # 然后再找“共 NNN 条”中的 NNN：
            text = controls_li.get_text()
            match = re.search(r"共\s*(\d+)\s*条", text)
            if match:
                total_records = int(match.group(1))
                return total_pages, total_records
    return None, None


def upsert_to_db(record, cursor):
    djzh = record.get("登记证号")
    cursor.execute("SELECT 1 FROM pesticide_data WHERE 登记证号 = ?", (djzh,))
    exists = cursor.fetchone() is not None

    try:
        cursor.execute(
            """
            INSERT INTO pesticide_data (
                登记证号, 农药名称, 农药类别, 剂型, 总含量, 有效期至, 登记证持有人, pd_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(登记证号) DO UPDATE SET
                农药名称=excluded.农药名称,
                农药类别=excluded.农药类别,
                剂型=excluded.剂型,
                总含量=excluded.总含量,
                有效期至=excluded.有效期至,
                登记证持有人=excluded.登记证持有人,
                pd_id=excluded.pd_id
        """,
            (
                djzh,
                record.get("农药名称"),
                record.get("农药类别"),
                record.get("剂型"),
                record.get("总有效成分含量") or record.get("总含量"),
                record.get("有效期至"),
                record.get("登记证持有人"),
                record.get("pd_id"),
            ),
        )

        if exists:
            # logging.info(f"更新登记证号：{djzh}")
            pass
        else:
            logging.info(f"新增登记证号：{djzh}")

    except Exception as e:
        logging.error(f"❌ DB insert/update error for {djzh}: {e}")


def update_total_expected_from_page(html, total_expected):
    pages, total = extract_total_pages_and_records(html)
    logging.info(f"📊 总页数：{pages}, 总记录数：{total}")
    if total and total > total_expected:
        total_expected = total
    return pages, total_expected


def should_stop_by_db_count(cursor, total_expected):
    """
    判断数据库中记录是否已达到目标数量，适用于提前终止逻辑。
    """
    cursor.execute("SELECT COUNT(*) FROM pesticide_data")
    current_total = cursor.fetchone()[0]
    logging.info(f"📊 当前已同步数据总数: {current_total}")
    return current_total >= total_expected


# === 主逻辑 ===
def main(total_expected=50716, end_page=2536):
    start_page = load_progress()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    logging.info(
        f"-------------{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始抓取，预计总页数 {end_page}，预计总条数约 {total_expected}，从第 {start_page} 页开始-------------"
    )
    pbar = tqdm(total=end_page - start_page + 1, desc="获取列表数据中", ncols=100)
    page = start_page

    try:
        while page <= end_page:
            html = fetch_list_page(page)
            if not html:
                logging.error(f"❌ 第 {page} 页抓取失败")
                page += 1
                pbar.update(1)
                continue

            # 动态更新页数和总条数（防止遗漏）
            pages, new_total = update_total_expected_from_page(html, total_expected)
            if new_total and new_total > total_expected:
                total_expected = new_total
                logging.info(f"📈 动态更新 total_expected = {total_expected}")

            if pages and 1 < pages < end_page:
                delta = end_page - pages
                end_page = pages
                pbar.total -= delta
                pbar.refresh()
                logging.info(f"📉 动态调整总页数为 {end_page}")

            try:
                records = parse_list(html)
                for record in records:
                    if "登记证号" in record and record["登记证号"]:
                        upsert_to_db(record, cursor)
            except Exception as e:
                logging.error(f"❌ 第 {page} 页解析/入库失败: {e}")

            # 每页提交
            conn.commit()
            save_progress(page)
            page += 1
            pbar.update(1)

            # 每 5 页检查一次是否达到目标数据量
            if page % 5 == 0:
                cursor.execute("SELECT COUNT(*) FROM pesticide_data")
                current_total = cursor.fetchone()[0]
                logging.info(f"📊 当前已同步数据总数: {current_total}")
                if current_total >= total_expected:
                    logging.info(f"✅ 数据已达 {total_expected}，提前结束爬虫任务")
                    break

            # 保活（防止数据库连接超时）
            if page % 20 == 0:
                conn.commit()
                conn.close()
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()

            time.sleep(random.uniform(0.5, 1.2))

    except KeyboardInterrupt:
        logging.warning("🛑 收到中断信号，手动终止任务。保存进度后退出...")
        save_progress(page)

    finally:
        pbar.close()
        conn.close()
        logging.info(
            f"✅ 同步任务结束，最终抓取至第 {page - 1} 页，期望条数 {total_expected}"
        )


def test1():

    url = "https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do"
    response = requests.get(url, headers=HEADERS)

    pages, records = extract_total_pages_and_records(response.text)
    print("-" * 10)
    # 保存 HTML 到本地文件
    with open(
        os.path.join(os.path.dirname(__file__), "data/page_sample.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(response.text)
    print(f"📊 总页数 {pages} 页, 总条数: {records}")
    print("-" * 10)


def test():
    with open(
        os.path.join(os.path.dirname(__file__), "data/page_sample.html"),
        encoding="utf-8",
    ) as f:
        html = f.read()
    pages, records = extract_total_pages_and_records(html)
    print("-" * 10)
    print(f"📊 总页数 {pages} 页, 总条数: {records}")
    print("-" * 10)


if __name__ == "__main__":
    main()
