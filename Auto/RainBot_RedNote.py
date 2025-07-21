import os
import random
import time
import json
import logging
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# 模拟自动评论的主类
class XHSBot:
    def __init__(self):
        # 在本文件夹下的json文件
        base_dir = os.path.dirname(os.path.abspath(__file__))
        comment_path = os.path.join(base_dir, "comments.json")
        with open(comment_path, "r", encoding="utf-8") as f:
            self.comments = json.load(f)

        log_dir = os.path.join(base_dir, "log")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "rainbot.log")

        # 设置全局 root logger，并绑定到文件
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,  # 强制覆盖其他 logging 设置
        )
        self.logger = logging.getLogger()

        # 记录每日评论次数的独立日志
        count_log_path = os.path.join(log_dir, "comment_count.log")
        self.count_logger = logging.getLogger("CommentCounter")
        count_handler = logging.FileHandler(count_log_path)
        count_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.count_logger.addHandler(count_handler)
        self.count_logger.setLevel(logging.INFO)
        self.count_logger.propagate = False

        # 持久化每日评论计数
        self.comment_count_path = os.path.join(log_dir, "comment_count_daily.json")
        self.today = time.strftime("%Y-%m-%d")
        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                all_counts = json.load(f)
        else:
            all_counts = {}
        self.comment_count = all_counts.get(self.today, 0)
        self.comment_count_data = all_counts

        self.driver = None
        self.failed_comment_count = 0

    def remove_non_bmp(self, text):
        # return "".join(c for c in text if ord(c) <= 0xFFFF)
        return text

    def setup_browser(self):
        # options = Options()
        # options.add_argument("--start-maximized")
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver = webdriver.Chrome(options=options)

    def login_xhs(self):
        self.driver.get("https://www.xiaohongshu.com/")
        input("[XHSBot] 请手动登录小红书并完成验证后按回车...")

    def get_random_comment(self):
        return random.choice(self.comments)

    def run(self, interval=30):
        self.setup_browser()
        self.login_xhs()
        while True:
            hrefs = self.get_recommended_note_links()
            if not hrefs:
                self.logger.info("[XHSBot] 未获取到笔记链接，等待重试...")
                time.sleep(10)
                continue

            self.comment_on_note_links(hrefs)

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            time.sleep(sleep_time)

    def comment_on_note_links(self, note_links):
        """
        Visit each note URL, open the comment box, type a random comment, and send.
        Includes robust waits + fallbacks to reduce ChromeDriver crashes caused by stale/absent elements.
        """
        base = "https://www.xiaohongshu.com"
        for raw_url in note_links:
            # Normalize URL (some feeds return relative URLs)
            url = raw_url
            if raw_url and raw_url.startswith("/"):
                url = urllib.parse.urljoin(base, raw_url)

            try:
                self.logger.info(f"[XHSBot] 打开笔记：{url}")
                self.driver.get(url)

                # 等待文档 ready (body 存在 & readyState == complete)
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                WebDriverWait(self.driver, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
                time.sleep(random.uniform(0.5, 1.5))  # 给前端框架一点渲染缓冲

                # 检测是否被踢回登录页（关键词 login 或 qrcode）
                cur = self.driver.current_url
                if "login" in cur or "account" in cur:
                    self.logger.info(f"[XHSBot] 页面跳到登录，跳过：{url}")
                    continue

                # 滚动一点确保评论入口渲染
                self.driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(random.uniform(0.5, 1.0))

                # 定位“说点什么...”触发元素（多种 fallback）
                trigger_locators = [
                    (By.XPATH, "//span[normalize-space()='说点什么...']"),
                    (
                        By.XPATH,
                        "//div[contains(@class,'not-active')]//span[contains(text(),'说点什么')]",
                    ),
                    (By.CSS_SELECTOR, "div.not-active.inner-when-not-active span"),
                ]

                comment_trigger = None
                for how, what in trigger_locators:
                    try:
                        comment_trigger = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((how, what))
                        )
                        WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((how, what))
                        )
                        break
                    except Exception:
                        continue

                if comment_trigger is None:
                    self.logger.info(f"[XHSBot] 未找到评论入口，跳过：{url}")
                    continue

                # 确保在视口中
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        comment_trigger,
                    )
                except Exception:
                    pass
                time.sleep(0.3)

                try:
                    comment_trigger.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", comment_trigger)

                # 等评论输入框（contenteditable）
                input_locators = [
                    (By.CSS_SELECTOR, "p#content-textarea[contenteditable='true']"),
                    (By.XPATH, "//p[@id='content-textarea']"),
                    (By.CSS_SELECTOR, "[contenteditable='true'].content-input"),
                    (By.CSS_SELECTOR, "div.comment-editor [contenteditable='true']"),
                ]

                input_box = None
                for how, what in input_locators:
                    try:
                        input_box = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((how, what))
                        )
                        break
                    except Exception:
                        continue

                if input_box is None:
                    self.logger.info(f"[XHSBot] 未找到评论输入框，跳过：{url}")
                    continue

                # 激活输入框（有些前端需要点击 innerEditable 子节点）
                try:
                    ActionChains(self.driver).move_to_element(
                        input_box
                    ).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", input_box)
                time.sleep(0.2)

                comment = self.remove_non_bmp(self.get_random_comment())

                # 有些 contenteditable 节点不吃 send_keys；先试 send_keys，失败则 JS 赋值
                typed_ok = True
                try:
                    input_box.clear()  # 若支持
                except Exception:
                    pass
                try:
                    input_box.send_keys(comment)
                except Exception:
                    typed_ok = False

                if not typed_ok:
                    try:
                        self.driver.execute_script(
                            "arguments[0].innerText = arguments[1]; arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
                            input_box,
                            comment,
                        )
                        typed_ok = True
                    except Exception:
                        typed_ok = False

                if not typed_ok:
                    self.logger.info(f"[XHSBot] 无法输入评论，跳过：{url}")
                    continue

                # 发送评论按钮（多个 fallback）
                send_locators = [
                    (
                        By.XPATH,
                        "//button[contains(@class,'submit') and contains(.,'发送')]",
                    ),
                    (By.CSS_SELECTOR, "button.btn.submit"),
                    (By.XPATH, "//button[.//text()[contains(.,'发送')]]"),
                ]

                submit_button = None
                for how, what in send_locators:
                    try:
                        submit_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((how, what))
                        )
                        break
                    except Exception:
                        continue

                if submit_button is None:
                    self.logger.info(f"[XHSBot] 找不到发送按钮，跳过：{url}")
                    continue

                try:
                    submit_button.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", submit_button)

                # 检测 toast：失败 OR 成功
                toast_failed = False
                try:
                    # 等待任一 toast 出现
                    toast = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(@class,'toast') or contains(@class,'Toast')]",
                            )
                        )
                    )
                    toast_text = toast.text.strip()
                    if any(k in toast_text for k in ["操作频繁", "失败", "请稍后"]):
                        toast_failed = True
                except Exception:
                    # 无 toast，假设成功
                    pass

                if toast_failed:
                    self.logger.info(f"[XHSBot] 评论失败（toast）：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续失败 3 次，程序退出")
                        if self.driver:
                            self.driver.quit()
                        exit(1)
                    continue  # 下一条

                # 成功
                self.logger.info(f"[XHSBot] 已评论链接：{url}")
                self.comment_count += 1
                self.failed_comment_count = 0
                self.comment_count_data[self.today] = self.comment_count
                with open(self.comment_count_path, "w", encoding="utf-8") as f:
                    json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)
                self.count_logger.info(f"{self.today} 累计评论：{self.comment_count}")

                time.sleep(random.uniform(2.5, 5.5))

            except Exception as e:
                self.logger.info(f"[XHSBot] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info("[XHSBot] 连续失败 3 次，程序退出")
                    if self.driver:
                        self.driver.quit()
                    exit(1)

    def get_recommended_note_links(self, scroll_times: int = 5):
        """
        Collect note links from the recommend feed.
        Scroll multiple times to load more.
        Returns a list of *absolute* URLs.
        """
        self.logger.info("[XHSBot] get_recommended_note_links...")
        base_url = "https://www.xiaohongshu.com"
        self.driver.get(
            "https://www.xiaohongshu.com/explore?channel_id=homefeed_recommend"
        )

        # 等初次加载
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        hrefs = set()
        last_height = 0
        for i in range(scroll_times):
            # 抓当前批
            cards = self.driver.find_elements(
                By.CSS_SELECTOR, "a.cover[href*='/explore/']"
            )
            for a in cards:
                href = a.get_attribute("href") or ""
                if href.startswith("/"):
                    href = urllib.parse.urljoin(base_url, href)
                if href.startswith(base_url + "/explore/"):
                    hrefs.add(href)
            # 滚动到底部加载更多
            self.driver.execute_script(
                "window.scrollBy(0, document.body.scrollHeight);"
            )
            time.sleep(random.uniform(1.5, 3.0))

            # 可选：检测页面高度变化（粗略）
            try:
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
                if new_height == last_height:
                    # 没有新内容，提前退出
                    break
                last_height = new_height
            except Exception:
                pass

        self.logger.info("[XHSBot] len(hrefs): %d", len(hrefs))
        return list(hrefs)


if __name__ == "__main__":
    print("[XHSBot] started...")
    bot = XHSBot()
    bot.run()
    print("[XHSBot] ended...")
