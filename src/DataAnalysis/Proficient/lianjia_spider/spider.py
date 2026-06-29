#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
import json
import os
from src.DataAnalysis.Proficient.lianjia_spider.storage import SpiderDB
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random, time
import src.DataAnalysis.Proficient.lianjia_spider.parser as parser
from tqdm import tqdm
from selenium.common.exceptions import WebDriverException
import logging

# 在文件顶部设置日志等级
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class HouseSpider:
    def __init__(self, headless=False):
        self.db = SpiderDB()
        self.setup_browser(False)
        if not self.load_cookies():
            self.login()

        print("登录流程处理完成。")

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

        # 禁用图片加载
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)

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
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": """
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'platform', { get: () => 'MacIntel' });
                Object.defineProperty(navigator, 'userAgentData', { get: () => undefined });
            """},
        )
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        chrome_options.add_experimental_option("useAutomationExtension", False)
        user_agent = (
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36"
        )
        chrome_options.add_argument(f"user-agent={user_agent}")

    def login(self):
        print("Opening Lianjia login page...")
        login_url = "https://bj.lianjia.com/"

        self.driver.get(login_url)

        print("\n请使用「链家 App / 贝壳找房 App」扫描二维码登录…")
        print("登录成功后按 Enter 继续执行爬虫。")

        input()  # 用户确认已登录

        # 记录 Cookie，便于下次免登录
        cookies = self.driver.get_cookies()

        with open(
            os.path.join(BASE_DIR, "lianjia_cookies.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(cookies, f)

        print("登录成功，Cookies 已保存。")

    def load_cookies(self):
        path = os.path.join(BASE_DIR, "lianjia_cookies.json")
        if not os.path.exists(path):
            print("No cookies found, need manual login.")
            return False

        self.driver.get("https://bj.lianjia.com/")  # 必须先访问域名
        with open(path, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        for ck in cookies:
            ck.pop("expiry", None)  # 防止 Selenium 报错
            try:
                self.driver.add_cookie(ck)
            except Exception:
                continue

        print("Cookies loaded.")
        return True

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
        self,
        min_step=30,
        max_step=80,
        base_delay=0.015,
        random_extra_delay=0.03,
        max_scroll_height=200,
    ):
        """
        丝滑连续的人类滚动方式（更接近真实用户鼠标滚轮）

        :param max_scroll_height: 最大滚动高度限制，滚动到此高度时停止
        """
        try:
            current_y = 0
            total_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )

            # 如果没有设置最大滚动高度，默认滚动到底部
            if max_scroll_height is None:
                max_scroll_height = total_height

            while current_y < max_scroll_height:
                # 每次滚动的像素（模拟鼠标滚轮：30~80 px）
                step = random.randint(min_step, max_step)
                current_y += step

                # 确保当前滚动位置不超过最大滚动限制
                if current_y > max_scroll_height:
                    current_y = max_scroll_height

                self.driver.execute_script(f"window.scrollTo(0, {current_y});")

                # 模拟微小的人类延迟：基础 + 随机
                time.sleep(base_delay + random.random() * random_extra_delay)

                # 动态更新页面高度（页面懒加载时，页面可能会增加高度）
                total_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

                # 如果总高度超过最大滚动高度，停止滚动
                if total_height > max_scroll_height:
                    break

            # 校准滚动位置，避免出现卡顿
            self.driver.execute_script(f"window.scrollTo(0, {current_y});")

        except Exception as e:
            print(f"Error during human scroll: {e}")

    def fetch_html(self, url, retries=2, wait_selector=None, wait_timeout=30):
        self.driver.execute_cdp_cmd(
            "Network.setExtraHTTPHeaders",
            {
                "headers": {
                    "Referer": "https://bj.lianjia.com/",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
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
        return parser.parse_list(html)

    def crawl_list_page(self, page=1, type=1):
        url = f"https://bj.lianjia.com/ershoufang/pg{page}/"
        html = self.fetch_html(url, wait_selector=".sellListContent")
        if html:
            data_list = self.parse_page(html)
            self.db.save_house_list(data_list)
            self.db.set_progress(page, type)
            return data_list
        else:
            print(f"Failed to crawl list page {page}")
            return None

    def crawl_detail_page(self, shop_url):
        html = self.fetch_html(shop_url, wait_selector=".baseinform")
        if html:
            # Assuming parser has a method to parse detail page
            detail_info = parser.parse_travel(html)
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


def get_list_data(type=1):
    dp_s = HouseSpider(headless=True)
    # 获取上次进度，支持断点续抓
    p = dp_s.db.get_progress(key="last_page")
    start_page = int(p or 1)
    print(p, start_page)
    if start_page < 1:
        start_page = 1

    end_page = 33
    for page in range(start_page, end_page + 1):
        print(f"Crawling page {page}...")
        try:
            data_list = dp_s.crawl_list_page(page, type)
            if not data_list:
                print(f"Page {page} failed, will retry later.")
                time.sleep(random.uniform(5, 10))  # 给自己喘口气
                continue
        except Exception as e:
            print(f"Unexpected error on page {page}: {e}, retrying...")
            time.sleep(random.uniform(5, 10))
            continue

        # 随机停顿 3-8 秒，降低被封风险
        time.sleep(random.uniform(3, 8))

    print("Crawling finished.")
    dp_s.close()


def fetch_missing_details():
    spider = HouseSpider(headless=False)  # 可视化登录更稳
    print("Checking missing house details...")

    BATCH_SIZE = 50

    while True:
        # 使用 LEFT JOIN 寻找还没入表的 house_id，避开 NOT IN 与 NULL 的坑
        rows = spider.db.conn.execute(f"""
            SELECT h.house_id
            FROM houses h
            LEFT JOIN house_details d ON h.house_id = d.house_id
            WHERE d.house_id IS NULL
            OR d.listing_date IS NULL  -- 关键字段
            ORDER BY h.house_id
            LIMIT {BATCH_SIZE};
        """).fetchall()

        if not rows:
            print("🎉 所有房源详情已抓取完毕")
            break

        print(f"本轮需要处理 {len(rows)} 条房源详情")

        for idx, row in enumerate(rows, start=1):
            # row 是单元素 tuple，取第 0 项
            house_id = row[0]
            print(f"[{idx}/{len(rows)}] Processing house_id = {house_id}")

            # 构建 detail url（注意不要传入 tuple）
            detail_url = f"https://bj.lianjia.com/ershoufang/{house_id}.html"

            # 重试机制
            html = None
            for attempt in range(3):
                try:
                    html = spider.fetch_html(
                        detail_url, wait_selector=".introContent", retries=2
                    )
                    # 若 fetch_html 返回页面但被重定向到登录/错误页，进行短延时再试
                    if not html or "指定的服务未被授权" in html:
                        print(
                            f"Attempt {attempt+1}: invalid page or login redirect for {house_id}"
                        )
                        time.sleep(random.uniform(2, 5))
                        continue
                    break
                except WebDriverException as we:
                    print(f"WebDriver error on {house_id}: {we}, retrying...")
                    time.sleep(random.uniform(2, 5))
                except Exception as e:
                    print(f"Unexpected error fetching {house_id}: {e}, retrying...")
                    time.sleep(random.uniform(1, 3))

            if not html:
                print(f"HTML 为空或抓取失败，跳过 {house_id}")
                continue

            # 解析详情页：请确保 parser.parse_detail 存在并返回 dict（包含 house_code 或 house_id）
            try:
                detail_info = parser.parse_detail(html)
                # 兼容：如果解析器返回没有 house_id，用当前 house_id 填充
                if not detail_info.get("house_id") and not detail_info.get(
                    "house_code"
                ):
                    detail_info["house_code"] = house_id
            except Exception as e:
                print(f"解析失败 house_id={house_id}: {e}")
                # 保存 HTML 以便手工分析
                err_path = os.path.join(BASE_DIR, f"err_detail_{house_id}.html")
                with open(err_path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"已保存错误页面: {err_path}")
                continue

            # 入库
            try:
                spider.db.save_house_detail(detail_info)
                print(f"✓ Saved detail for {house_id}")
            except Exception as e:
                print(f"入库失败 {house_id}: {e}")
                # 如果因为主键冲突等问题，可以选择更新或记录错误
                continue

            # 每条之间随机停顿降低被封风险
            time.sleep(random.uniform(1.2, 3.5))

        # 批次间等待
        time.sleep(random.uniform(3, 6))

    spider.close()
    print("Details fetching completed.")


if __name__ == "__main__":
    print("Start testing DB schema and save logic")
    # 6 7 8 10 34 ->
    # get_list_data(type=-1)÷
    fetch_missing_details()
    print("Crawling finished.")
