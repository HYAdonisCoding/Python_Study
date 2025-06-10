import os
import re
import time
import json
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === 配置区 ===
BASE_DIR = "data"
PROGRESS_FILE = os.path.join(BASE_DIR, "progress.txt")
ERROR_LOG = os.path.join(BASE_DIR, "error.log")
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.icama.cn",
    "Referer": "https://www.icama.cn/BasicdataSystem/pesticideRegistration/queryselect.do",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36"
}

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
        return int(f.read().strip() or 0) + 1  # 从下一页开始

def build_detail_url(pd_id):
    r = round(random.random(), 16)
    return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r}&id={pd_id}"

def extract_detail(url):
    options = Options()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(2)  # 等待页面加载

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 初始化结果字典
        result = {
            "登记证信息": {},
            "有效成分信息": [],
            "制剂用药量信息": []
        }

        # 获取登记证信息表格（假设为第一个表格）
        reg_table = soup.find_all('table', {'id': 'reg'})[0]
        reg_rows = reg_table.find_all('tr')[1:]  # 排除表头

        for row in reg_rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            # print('*' * 20)
            # print(cols)
            if len(cols) >= 2:
                # result["登记证信息"][cols[0]] = cols[1]
                # 如果该行的字段是成对出现的（例如"登记证号："、"PD20151999"）
                for i in range(0, len(cols), 2):  # 每两个字段一对
                    key = cols[i].replace("：", "").strip()  # 处理去掉"："的字段名
                    value = cols[i+1] if i + 1 < len(cols) else ""
                    if key in result["登记证信息"]:
                        # 如果该字段已经存在，存成列表，避免覆盖
                        if isinstance(result["登记证信息"][key], list):
                            result["登记证信息"][key].append(value)
                        else:
                            result["登记证信息"][key] = [result["登记证信息"][key], value]
                    else:
                        result["登记证信息"][key] = value  # 如果该字段没有值，就直接保存

        
        # 获取有效成分信息表格（假设为第三个表格）
        effective_table = soup.find_all('table', {'id': 'reg'})[2]
        rows = effective_table.find_all('tr')[2:]  # 跳过前两行表头

        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) == 3:
                result["有效成分信息"].append({
                    "有效成分": cols[0],
                    "有效成分英文名": cols[1],
                    "有效成分含量": cols[2]
                })

        # 获取制剂用药量信息表格（假设为第四个表格）
        dosage_table = soup.find_all('table', {'id': 'reg'})[3]
        # print(dosage_table)
        # print('*'*30)
        dosage_rows = dosage_table.find_all('tr')[2:]  # 从第二行开始，跳过表头
        # print(dosage_rows)
        # 跳过表头行，从第二行开始提取
        # rows = dosage_table[2].find_all('tr')[1:]  # 跳过表头
        for row in dosage_rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) >= 4:
                result["制剂用药量信息"].append({
                    "作物/场所": cols[0],
                    "防治对象": cols[1],
                    "用药量": cols[2],
                    "施用方法": cols[3]
                })
        # print(result)
        return result

    finally:
        driver.quit()

def fetch_with_retry(url, method='GET', data=None, headers=HEADERS, retries=3, timeout=10):
    for attempt in range(retries):
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            else:
                response = requests.post(url, headers=headers, data=data, timeout=timeout)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            log_error(f"Retry {attempt + 1} failed: {e}")
        time.sleep(random.uniform(1.5, 3.0))
    return None

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

# === 主逻辑 ===
def scrape():
    os.makedirs(BASE_DIR, exist_ok=True)
    start_page = load_progress()
    total_pages = 2488

    for page in range(start_page, total_pages + 1):
        print(f"\n--- 正在抓取第 {page} 页 ---")
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
            log_error(f"第 {page} 页抓取失败")
            continue

        page_data = parse_table(html)

        for item in page_data:
            pd_id = item.get("pd_id")
            if pd_id:
                info = extract_detail(build_detail_url(pd_id))
                if info:
                    item.update(info)
                    # print(f"已获取 {item['登记证号']} 的信息，共 {len(info)} 项。")

        with open(os.path.join(BASE_DIR, f"page_{page:04d}.json"), 'w', encoding='utf-8') as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 第{page}页数据 抓取完成")
        save_progress(page)
        time.sleep(random.uniform(1.5, 3.0))

    print("✅ 所有页面抓取完成")


if __name__ == '__main__':
    scrape()