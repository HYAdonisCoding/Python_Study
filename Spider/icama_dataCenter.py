import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import re
import requests
import random
import json

url = 'https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r=0.6570751670519425&id=0d76ebd3de4248dd8394486b8001fa25'

def detail():
    # 可选：无头浏览器
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 等待页面加载完成
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有 id="reg" 的表格
    tables = soup.find_all('table', {'id': 'reg'})

    # 第三个表格是“有效成分信息”
    effective_table = tables[2]

    # 提取行数据（排除表头前两行）
    rows = effective_table.find_all('tr')[2:]

    print("有效成分\t有效成分英文名\t有效成分含量")
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        if len(cols) == 3:
            print("\t".join(cols))

    driver.quit()

# 获取列表数据
def center(pageNo, pageSize=2000):
    


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
        "pageNo": pageNo,
        "pageSize": pageSize,
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

    # print(response.text)
    with open('icama_dataCenter1.html', 'w', encoding='utf-8') as f:
        f.write(response.text)


def get_row(fileName):
    
    # 读取 HTML 文件
    with open(fileName, 'r', encoding='utf-8') as f:
        html = f.read()


    soup = BeautifulSoup(html, 'html.parser')

    # 正则提取 _viewpd('id') 的值
    viewpd_pattern = re.compile(r"_viewpd\('([^']+)'\)")

    # 提取第2个表格（索引为1）
    table = soup.find_all('table')[1]

    table_data = []
    rows = table.find_all('tr')
    headers = []

    for i, row in enumerate(rows):
        cols = row.find_all(['td', 'th'])
        cols_text = []
        pd_id = None

        for col in cols:
            text = col.get_text(strip=True)
            cols_text.append(text)

            a_tag = col.find('a', onclick=viewpd_pattern)
            if a_tag:
                match = viewpd_pattern.search(a_tag['onclick'])
                if match:
                    pd_id = match.group(1)

        if i == 0 and len(cols_text) > 1:
            headers = cols_text
        else:
            if headers and len(cols_text) == len(headers):
                row_dict = dict(zip(headers, cols_text))
                if pd_id:
                    row_dict['pd_id'] = pd_id
                table_data.append(row_dict)
            else:
                table_data.append(cols_text)

    # 保存为 JSON
    with open('table_index_1.json', 'w', encoding='utf-8') as f:
        json.dump(table_data, f, ensure_ascii=False, indent=2)

    print("✅ 第2个表格数据（含 pd_id）已保存为 table_index_1.json")


    def extract_pd_table(html):
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue

            headers = [td.get_text(strip=True) for td in rows[0].find_all('td')]
            # 判断是否是“有效成分”表
            if headers == ['有效成分', '有效成分英文名', '有效成分含量']:
                data = []
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.find_all('td')]
                    if len(cols) == 3:
                        data.append({
                            "有效成分": cols[0],
                            "有效成分英文名": cols[1],
                            "有效成分含量": cols[2]
                        })
                return data
        return []

    def build_url(pd_id):
        r_value = round(random.random(), 16)
        return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r_value}&id={pd_id}"

    # 加载之前提取的表格数据
    with open('table_index_1.json', 'r', encoding='utf-8') as f:
        table_data = json.load(f)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, row in enumerate(table_data):
        pd_id = row.get('pd_id')
        if not pd_id:
            continue

        url = build_url(pd_id)
        try:
            print(f"[{i+1}/{len(table_data)}] 请求详情页: {url}")
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = extract_pd_table(resp.text)
                row["有效成分信息"] = data
            else:
                print(f"⚠️ 请求失败 status={resp.status_code}")
        except Exception as e:
            print(f"❌ 请求出错: {e}")
        
        time.sleep(1.5)  # 防止被封IP，建议限速

    # 保存最终结果
    with open('table_index_1_with_成分.json', 'w', encoding='utf-8') as f:
        json.dump(table_data, f, ensure_ascii=False, indent=2)

    print("✅ 已完成所有详情页请求并写入有效成分信息。")


# 获取详情，英文名啥的
def get_detail():
    import requests
    import random
    import time
    import json
    from bs4 import BeautifulSoup

    def extract_pd_table(html):
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue

            headers = [td.get_text(strip=True) for td in rows[0].find_all('td')]
            # 判断是否是“有效成分”表
            if headers == ['有效成分', '有效成分英文名', '有效成分含量']:
                data = []
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.find_all('td')]
                    if len(cols) == 3:
                        data.append({
                            "有效成分": cols[0],
                            "有效成分英文名": cols[1],
                            "有效成分含量": cols[2]
                        })
                return data
        return []

    def build_url(pd_id):
        r_value = round(random.random(), 16)
        return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r_value}&id={pd_id}"

    # 加载之前提取的表格数据
    with open('table_index_1.json', 'r', encoding='utf-8') as f:
        table_data = json.load(f)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, row in enumerate(table_data):
        pd_id = row.get('pd_id')
        if not pd_id:
            continue

        url = build_url(pd_id)
        try:
            print(f"[{i+1}/{len(table_data)}] 请求详情页: {url}")
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = extract_pd_table(resp.text)
                row["有效成分信息"] = data
            else:
                print(f"⚠️ 请求失败 status={resp.status_code}")
        except Exception as e:
            print(f"❌ 请求出错: {e}")
        
        time.sleep(1.5)  # 防止被封IP，建议限速

    # 保存最终结果
    with open('table_index_1_with_成分.json', 'w', encoding='utf-8') as f:
        json.dump(table_data, f, ensure_ascii=False, indent=2)

    print("✅ 已完成所有详情页请求并写入有效成分信息。")

def extract_pd_table_with_selenium(url):
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

        # 找到所有 id="reg" 的表格
        tables = soup.find_all('table', {'id': 'reg'})
        if len(tables) < 3:
            print(f"⚠️ 页面中未找到有效成分表格: {url}")
            return []

        effective_table = tables[2]
        rows = effective_table.find_all('tr')[2:]  # 跳过前两行表头

        result = []
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            if len(cols) == 3:
                result.append({
                    "有效成分": cols[0],
                    "有效成分英文名": cols[1],
                    "有效成分含量": cols[2]
                })
        return result
    finally:
        driver.quit()
def get_detail1():

    def extract_pd_table(html):
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            if not rows:
                continue
            headers = [td.get_text(strip=True) for td in rows[0].find_all("td")]
            if headers == ['有效成分', '有效成分英文名', '有效成分含量']:
                result = []
                for row in rows[1:]:
                    cols = [td.get_text(strip=True) for td in row.find_all("td")]
                    if len(cols) == 3:
                        result.append({
                            "有效成分": cols[0],
                            "有效成分英文名": cols[1],
                            "有效成分含量": cols[2]
                        })
                print(result)
                print('-' * 10)
                return result
        return []

    def build_url(pd_id):
        r_value = round(random.random(), 16)
        return f"https://www.icama.cn/BasicdataSystem/pesticideRegistration/viewpd.do?r={r_value}&id={pd_id}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    # 加载你的 page_0001.json 数据
    with open(os.path.join("data", "page_0001.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        pd_id = item.get("pd_id")
        if not pd_id:
            continue

        url = build_url(pd_id)
        print(f"[{i+1}/{len(data)}] 请求详情页：{url}")

        try:
            成分信息 = extract_pd_table_with_selenium(url)
            
            
            if len(成分信息) > 0:
                item["有效成分信息"] = 成分信息
                print(f"已获取 {item['登记证号']} 的成分信息，共 {len(成分信息)} 项。")
            else:
                item["有效成分信息"] = []
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            item["有效成分信息"] = []

        time.sleep(random.uniform(1.5, 3.0))  # 防止 IP 被封

    # 保存结果
    with open("page_0001_with_components.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ 成功提取所有有效成分信息，已保存至 page_0001_with_components.json")


if __name__ == '__main__':
    # center()   
    fileName = 'icama_dataCenter.html'
    # get_row(fileName) 
    get_detail1()