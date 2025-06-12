# icama_spider_optimized.py

import os
import re
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm  # 加在文件顶部

# === 配置区 ===
BASE_DIR = "data"
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.txt")
ERROR_LOG = os.path.join(BASE_DIR, "error.log")
DETAIL_CACHE = os.path.join(BASE_DIR, "detail_cache")

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.icama.cn",
    "Referer": "https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36"
}

os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(DETAIL_CACHE, exist_ok=True)

# === 工具函数 ===
def log_error(msg):
    with open(ERROR_LOG, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')

def save_progress(page_no):
    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(page_no))

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return 1
    with open(PROGRESS_FILE, 'r') as f:
        return int(f.read().strip() or 0) + 1

def build_detail_url(pd_id):
    r = round(random.random(), 16)
    return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r}&id={pd_id}"

def parse_detail_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = {"登记证信息": {}, "有效成分信息": [], "制剂用药量信息": []}

    tables = soup.find_all('table', {'id': 'reg'})
    if not tables or len(tables) < 4:
        return result

    # 登记证信息解析
    for row in tables[0].find_all('tr')[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        for i in range(0, len(cols), 2):
            key = cols[i].replace("：", "").strip()
            value = cols[i+1] if i + 1 < len(cols) else ""
            result["登记证信息"][key] = value

    # 有效成分
    for row in tables[2].find_all('tr')[2:]:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        if len(cols) == 3:
            result["有效成分信息"].append({"有效成分": cols[0], "有效成分英文名": cols[1], "有效成分含量": cols[2]})

    # 用药量
    for row in tables[3].find_all('tr')[2:]:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        if len(cols) >= 4:
            result["制剂用药量信息"].append({"作物/场所": cols[0], "防治对象": cols[1], "用药量": cols[2], "施用方法": cols[3]})

    return result

def extract_detail_with_driver(driver, pd_id):
    cache_file = os.path.join(DETAIL_CACHE, f"{pd_id}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    url = build_detail_url(pd_id)
    try:
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        detail = parse_detail_html(html)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(detail, f, ensure_ascii=False)
        return detail
    except Exception as e:
        log_error(f"extract_detail: {pd_id} - {str(e)}")
        return {}

def parse_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    viewpd_pattern = re.compile(r"_viewpd\('([^']+)'\)")
    table = soup.find_all('table')[1]
    rows = table.find_all('tr')
    headers = [td.get_text(strip=True) for td in rows[0].find_all('td')]
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        values = [td.get_text(strip=True) for td in cols]
        pd_id = None
        for td in cols:
            a_tag = td.find('a', onclick=viewpd_pattern)
            if a_tag:
                match = viewpd_pattern.search(a_tag['onclick'])
                if match:
                    pd_id = match.group(1)
        row_data = dict(zip(headers, values))
        if pd_id:
            row_data['pd_id'] = pd_id
        data.append(row_data)
    return data

def fetch_with_retry(url, method='GET', data=None, headers=HEADERS, retries=3):
    for _ in range(retries):
        try:
            if method == 'POST':
                response = requests.post(url, data=data, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            log_error(f"fetch retry fail: {e}")
        time.sleep(random.uniform(1.5, 3.0))
    return None

# === 主逻辑 ===1241-1533，2025-06-12 page2503-50043条
def scrape():
    start_page = load_progress()
    total_pages = 2488
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver = webdriver.Chrome(options=chrome_options)

    for page in range(start_page, total_pages + 1):
        # print(f"\n--- 正在抓取第 {page} 页 ---")
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Origin": "https://www.icama.cn",
            "Referer": "https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Storage-Access": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }
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
            "accOrfuzzy": "2"
        }
        response = requests.post(url, headers=headers, data=data)
        html = response.text
        

        html = fetch_with_retry(
            url="https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do",
            method='POST',
            data=data,
            headers=headers
        )
        if not html:
            log_error(f"Page {page} fetch failed")
            continue
        page_data = parse_table(html)

        # 用 tqdm 显示进度条
        for item in tqdm(page_data, desc=f"第 {page} 页抓取中", ncols=80):
            pd_id = item.get("pd_id")
            if pd_id:
                detail = extract_detail_with_driver(driver, pd_id)
                item.update(detail)

        with open(os.path.join(BASE_DIR, f"page_{page:04d}.json"), 'w', encoding='utf-8') as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)
        save_progress(page)
        # print(f"✅ 第 {page} 页完成")
        time.sleep(random.uniform(1.5, 3.0))

    driver.quit()
    print("✅ 所有页面抓取完成")

if __name__ == '__main__':
    scrape()
    # 有问题的数据
    # WP20070003