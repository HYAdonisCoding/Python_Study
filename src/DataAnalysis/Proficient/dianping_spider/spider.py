#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
import os
from src.DataAnalysis.Proficient.dianping_spider.storage import SpiderDB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, time
import src.DataAnalysis.Proficient.dianping_spider.parser as parser
from tqdm import tqdm
from selenium.common.exceptions import WebDriverException
import logging

# 在文件顶部设置日志等级
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DianpingSpider:
    def __init__(self, headless=False):
        self.db = SpiderDB()
        self.setup_browser()

    def setup_browser(self, headless=False):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.page_load_strategy = (
            "eager"  # 只等 DOMContentLoaded，不等所有资源
        )
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")

        # 下载与当前 Chrome 版本对应的 ChromeDriver
        chrome_version = self.get_chrome_version()
        print(f"Detected Chrome version: {chrome_version}")
        # service = Service(ChromeDriverManager(driver_version=chrome_version).install())
        # service = Service(ChromeDriverManager().install())
        service = Service(
            ChromeDriverManager(driver_version="142.0.7444.135").install()
        )
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_cdp_cmd("Network.enable", {})

    def get_chrome_version(self):
        # Helper method to get chrome version for driver manager
        import subprocess
        import re

        try:
            output = subprocess.check_output(["google-chrome", "--version"]).decode()
        except Exception:
            try:
                output = subprocess.check_output(
                    ["chromium-browser", "--version"]
                ).decode()
            except Exception:
                output = "Chrome 114.0.0.0"
        match = re.search(r"(\d+)\.", output)
        if match:
            return match.group(1)
        return None

    def human_scroll(
        self, min_step=30, max_step=80, base_delay=0.015, random_extra_delay=0.03
    ):
        """
        丝滑连续的人类滚动方式（更接近真实用户鼠标滚轮）
        """
        try:
            current_y = 0
            total_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            while current_y < total_height:
                # 每次滚动的像素（模拟鼠标滚轮：30~80 px）
                step = random.randint(min_step, max_step)
                current_y += step

                self.driver.execute_script(f"window.scrollTo(0, {current_y});")

                # 模拟微小的人类延迟：基础 + 随机
                time.sleep(base_delay + random.random() * random_extra_delay)

                # 动态更新高度（页面懒加载时高度会增加）
                total_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

            # 最后位置校准到底部
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

        except Exception as e:
            print(f"Smooth scroll error: {e}")

    def fetch_html(self, url, retries=2, wait_selector=None, wait_timeout=10):
        self.driver.execute_cdp_cmd(
            "Network.setExtraHTTPHeaders",
            {
                "headers": {
                    "Referer": "https://www.dianping.com/beijing",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                }
            },
        )
        for attempt in range(retries):
            try:
                self.driver.get(url)
                time.sleep(random.uniform(1, 3))  # 简单等待 DOM 加载
                self.human_scroll()
                if wait_selector:
                    WebDriverWait(self.driver, wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector))
                    )
                else:
                    time.sleep(random.uniform(3, 6))
                return self.driver.page_source
            except Exception as e:
                print(f"Error fetching {url}: {e}, retrying {attempt+1}/{retries}")

                return self.driver.page_source
        return None

    def parse_page(self, html):
        return parser.parse_list_page(html)

    def save_shop_list(self, shop_list, page):
        self.db.save_shop_basic(shop_list)
        self.db.set_progress(page)

    def crawl_list_page(self, page):
        url = f"https://www.dianping.com/beijing/ch10/p{page}"
        html = self.fetch_html(url, wait_selector=".shop-list")
        if html:
            shop_list = self.parse_page(html)
            self.save_shop_list(shop_list, page)
            return shop_list
        else:
            print(f"Failed to crawl list page {page}")
            return None

    def crawl_detail_page(self, shop_url):
        html = self.fetch_html(shop_url, wait_selector=".shop-detail")
        if html:
            # Assuming parser has a method to parse detail page
            detail_info = parser.parse_detail_page(html)
            # Save detail info if needed
            self.db.save_shop_detail(detail_info)
            current_detail_count = self.db.get_progress(key="detail_count")
            current_detail_count = (
                int(current_detail_count) if current_detail_count is not None else 0
            )
            self.db.set_progress(current_detail_count + 1, key="detail_count")
            return detail_info
        else:
            print(f"Failed to crawl detail page {shop_url}")
            return None

    def close(self):
        try:
            # 打印当前模式
            mode = self.db.conn.execute("PRAGMA journal_mode;").fetchone()[0]
            print(f"Current SQLite journal mode: {mode}")

            # 执行 checkpoint
            self.db.conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
            self.db.conn.commit()
            print("✅ WAL checkpoint executed successfully.")

            # 等待系统刷新文件锁
            self.db.conn.close()
            print("✅ Database connection closed.")
            time.sleep(0.5)

            # 二次验证清理（仅在所有连接都断开的情况下）
            if os.path.exists("dianping.db-wal"):
                os.remove("dianping.db-wal")
            if os.path.exists("dianping.db-shm"):
                os.remove("dianping.db-shm")
                print("🧹 Residual SQLite cache files removed.")

        except Exception as e:
            print(f"⚠️ Error during database cleanup: {e}")


def get_list_data():
    dp_s = DianpingSpider(headless=True)
    dp_s.driver.get("https://www.dianping.com/login")
    input("请在浏览器中完成登录后按回车继续...")
    # 获取上次进度，支持断点续抓
    start_page = int(dp_s.db.get_progress("list_page") or 2)
    if start_page < 2:
        start_page = 2

    end_page = 50
    for page in range(start_page, end_page + 1):
        print(f"Crawling page {page}...")
        try:
            shop_list = dp_s.crawl_list_page(page)
            if not shop_list:
                print(f"Page {page} failed, will retry later.")
                time.sleep(random.uniform(5, 10))  # 给自己喘口气
                continue
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}, retrying...")
            time.sleep(random.uniform(5, 10))
            continue

        # 随机停顿 3-8 秒，降低被封风险
        time.sleep(random.uniform(3, 8))
    dp_s.crawl_list_page(10)

    print("Crawling finished.")
    dp_s.close()


def fetch_missing_details():
    dp_s = DianpingSpider(headless=False)  # headless=False 更稳
    dp_s.driver.get("https://www.dianping.com/login")
    input("请在浏览器中完成登录后按回车继续...")
    dp_s.driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": """
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """},
    )

    try:
        # 查询数据库里未抓取详情页的商户
        # 假设 save_shop_detail 会更新某个关键字段，比如 'star_score' 或 'address'
        while True:
            rows = dp_s.db.conn.execute(
                "SELECT data_shopid, shop_link FROM shops WHERE star_score IS NULL OR star_score = ''"
            ).fetchall()

            print(f"Found {len(rows)} shops without details")

            if len(rows) == 0:
                print("🎉 All details fetched successfully.")
                break

            for idx, (shopid, shop_link) in enumerate(
                tqdm(rows, desc="Fetching details", unit="shop"), start=1
            ):
                tqdm.write(f"[{idx}/{len(rows)}] Processing detail for {shopid}...")

                local_html_path = os.path.join(BASE_DIR, f"page_Error_{shopid}.html")

                try:
                    # 1. 用 Selenium 获取页面 HTML
                    html = dp_s.fetch_html(shop_link, wait_selector=".shop-detail")
                    if not html:
                        tqdm.write(f"[{idx}] Failed to fetch HTML for {shopid}")
                        continue

                    try:
                        # 2. 尝试解析 HTML
                        detail_info = parser.parse_detail_page(html)
                    except Exception as e:
                        tqdm.write(f"[{idx}] Parsing failed for {shopid}: {e}")
                        # 3. 如果解析失败，将 HTML 保存到本地
                        with open(local_html_path, "w", encoding="utf-8") as f:
                            f.write(html)
                        try:
                            # 4. 立即从保存的本地 HTML 再解析一次
                            with open(local_html_path, "r", encoding="utf-8") as f:
                                local_html = f.read()
                            detail_info = parser.parse_detail_page(local_html)
                        except Exception as e2:
                            tqdm.write(
                                f"[{idx}] Re-parsing local HTML failed for {shopid}: {e2}"
                            )
                            continue  # 跳过当前商户，继续下一个

                    # 5. 成功解析后入库，并删除本地文件
                    if detail_info:
                        try:
                            dp_s.db.save_shop_detail(detail_info)
                            dp_s.db.increment_progress("detail_count")
                            tqdm.write(
                                f"[{idx}/{len(rows)}] Parsed and saved detail for {shopid}"
                            )
                            if os.path.exists(local_html_path):
                                os.remove(local_html_path)
                        except Exception as e:
                            tqdm.write(
                                f"[{idx}] Failed to save detail or update progress for {shopid}: {e}"
                            )

                except Exception as e:
                    tqdm.write(f"[{idx}] Unexpected error processing {shopid}: {e}")

                # 随机停顿，降低被封风险
                time.sleep(random.uniform(2, 6))

    except KeyboardInterrupt:
        tqdm.write("\n⚠️ 用户手动终止，正在安全关闭资源...")

    finally:
        dp_s.close()
        tqdm.write("✅ 已安全关闭浏览器和数据库连接。")


if __name__ == "__main__":
    print("Start testing DB schema and save logic")
    fetch_missing_details()
    print("Crawling finished.")
