import os
import json
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tqdm import tqdm

DATA_DIR = "data"

def build_url(pd_id):
    r_value = round(random.random(), 16)
    return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r_value}&id={pd_id}"

def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)

def parse_detail_page(soup):
    tables = soup.find_all('table', {'id': 'reg'})
    result = {
        "登记证信息": {},
        "有效成分信息": [],
        "制剂用药量信息": []
    }

    if len(tables) >= 1:
        for row in tables[0].find_all('tr')[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            for i in range(0, len(cols), 2):
                key = cols[i].replace("：", "").strip()
                value = cols[i + 1] if i + 1 < len(cols) else ""
                if key:
                    result["登记证信息"][key] = value

    if len(tables) >= 3:
        for row in tables[2].find_all('tr')[2:]:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) == 3:
                result["有效成分信息"].append({
                    "有效成分": cols[0],
                    "有效成分英文名": cols[1],
                    "有效成分含量": cols[2]
                })

    if len(tables) >= 4:
        for row in tables[3].find_all('tr')[2:]:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) >= 4:
                result["制剂用药量信息"].append({
                    "作物/场所": cols[0],
                    "防治对象": cols[1],
                    "用药量": cols[2],
                    "施用方法": cols[3]
                })

    return result

def get_detail_from_file(driver, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in tqdm(enumerate(data), total=len(data), desc=f"📄 处理 {os.path.basename(file_path)}"):
        pd_id = item.get("pd_id")
        if not pd_id:
            continue

        url = build_url(pd_id)
        # print(f"[{i + 1}/{len(data)}] 请求详情页：{url}")
        try:
            driver.get(url)
            time.sleep(random.uniform(1.5, 3.0))  # 可调节
            soup = BeautifulSoup(driver.page_source, "html.parser")
            detail_info = parse_detail_page(soup)
            item.update(detail_info)
        except Exception as e:
            print(f"❌ 抓取失败：{e}")
    return data

def save_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def extract_batch(start=1, end=5):
    driver = create_driver()
    try:
        for page_num in range(start, end + 1):
            file_name = f"page_{page_num:04d}.json"
            file_path = os.path.join(DATA_DIR, file_name)
            if not os.path.exists(file_path):
                print(f"⚠️ 文件不存在: {file_name}")
                continue

            print(f"\n--- 正在处理文件: {file_name} ---")
            updated_data = get_detail_from_file(driver, file_path)
            save_json(updated_data, file_path)
            print(f"✅ 保存完成: {file_name}")
    finally:
        driver.quit()
        print("✅ 所有详情页处理完成")

if __name__ == "__main__":
    print(f"开始处理详情页{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    extract_batch(start=1382, end=1533)