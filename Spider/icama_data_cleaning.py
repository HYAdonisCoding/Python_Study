import sqlite3
import json
import os
import time
import random
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "pesticide_data.db")
MAX_RETRIES = 2
MAX_WORKERS = 1
LOG_FILE = os.path.join(DATA_DIR, "fix_empty_ingredients.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def build_url(pd_id):
    r_value = round(random.random(), 16)
    return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r_value}&id={pd_id}"


def parse_detail_page(soup):
    tables = soup.find_all("table", {"id": "reg"})
    result = {"登记证信息": {}, "有效成分信息": [], "制剂用药量信息": []}

    for table in tables:
        title_cell = table.find("td")
        if not title_cell:
            continue
        title = title_cell.get_text(strip=True)
        # print(f"⚙️ 表格标题识别：{title}")
        # print(json.dumps(result, ensure_ascii=False, indent=2))

        if "农药登记证信息" in title:
            for row in table.find_all("tr")[1:]:
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                for i in range(0, len(cols), 2):
                    key = cols[i].replace("：", "").strip()
                    value = cols[i + 1] if i + 1 < len(cols) else ""
                    if key:
                        result["登记证信息"][key] = value

        elif "有效成分信息" in title:
            for row in table.find_all("tr")[2:]:
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(cols) == 3:
                    result["有效成分信息"].append(
                        {
                            "有效成分": cols[0],
                            "有效成分英文名": cols[1],
                            "有效成分含量": cols[2],
                        }
                    )

        elif "制剂用药量信息" in title:
            for row in table.find_all("tr")[2:]:
                cols = [td.get_text(strip=True) for td in row.find_all("td")]
                if len(cols) >= 4:
                    result["制剂用药量信息"].append(
                        {
                            "作物/场所": cols[0],
                            "防治对象": cols[1],
                            "用药量": cols[2],
                            "施用方法": cols[3],
                        }
                    )

    return result


def extract_all_info_with_selenium(url, retries=MAX_RETRIES):
    for attempt in range(1, retries + 1):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
            options.add_argument("--allow-insecure-localhost")  # 允许不安全的 https
            options.add_argument("--disable-web-security")  # 关闭部分安全检查（可选）
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )

            driver.get(url)

            # 等待表格加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "reg"))
            )

            time.sleep(1.5)  # 页面渲染时间

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            return parse_detail_page(soup)

        except Exception as e:
            logging.warning(f"⚠️ 第 {attempt} 次请求失败: {url} - {e}")
            time.sleep(random.uniform(2, 4))
        finally:
            try:
                driver.quit()
            except:
                pass

    logging.error(f"❌ 最终失败，放弃抓取: {url}")
    return None


def process_record(record):
    djzh, pd_id = record
    url = build_url(pd_id)
    detail_info = extract_all_info_with_selenium(url)

    if detail_info and detail_info["有效成分信息"]:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE pesticide_data
                SET 登记证信息 = ?, 有效成分信息 = ?, 制剂用药量信息 = ?
                WHERE 登记证号 = ?
            """,
                (
                    json.dumps(detail_info.get("登记证信息", {}), ensure_ascii=False),
                    json.dumps(detail_info.get("有效成分信息", []), ensure_ascii=False),
                    json.dumps(
                        detail_info.get("制剂用药量信息", []), ensure_ascii=False
                    ),
                    djzh,
                ),
            )
            conn.commit()
            conn.close()
            logging.info(f"✅ Updated {djzh}")
        except Exception as e:
            logging.error(f"❌ DB update failed for {djzh}: {e}")
    else:
        logging.warning(f"⚠️ No valid info found for {djzh} (URL: {url})")


def main():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 登记证号, pd_id FROM pesticide_data WHERE 有效成分信息 IS NULL OR 有效成分信息 = '[]'"
    )
    records = cursor.fetchall()
    conn.close()

    logging.info(f"Total records to update: {len(records)}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_record, rec) for rec in records]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="补全中"):
            pass

    logging.info("✅ 所有补全任务完成。")


if __name__ == "__main__":
    main()
    # url = build_url("5602b94c384e4795b226cee1fb723a23")
    # data = extract_all_info_with_selenium(url)
    # print(json.dumps(data, ensure_ascii=False, indent=2))
