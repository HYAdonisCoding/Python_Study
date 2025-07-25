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
from tqdm import tqdm
from comment_db import CommentDB, Platform

limitation = 100


# 模拟自动评论的主类
class JuejinBot:
    def __init__(self):
        bot_id = self.__class__.__name__
        # 在本文件夹下的json文件
        base_dir = os.path.dirname(os.path.abspath(__file__))
        comment_path = os.path.join(base_dir, "comments.json")
        with open(comment_path, "r", encoding="utf-8") as f:
            self.comments = json.load(f)

        log_dir = os.path.join(base_dir, "log")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "rainbot.log")
        count_log_path = os.path.join(log_dir, "comment_count.log")
        self._setup_loggers(log_path, count_log_path)

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
        self.comment_db = CommentDB()
        self.cookie_path = os.path.join(base_dir, f"{bot_id}_cookies.json")
        # 缓存路径
        self.cache_path = os.path.join(base_dir, f"{bot_id}_cached_hrefs.json")

    def _setup_loggers(self, log_path, count_log_path):
        # 设置主日志 logger
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,
        )
        self.logger = logging.getLogger("JuejinBotLogger")

        # 设置每日计数 logger
        self.count_logger = logging.getLogger("CommentCounter")
        count_handler = logging.FileHandler(count_log_path)
        count_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        self.count_logger.handlers.clear()
        self.count_logger.addHandler(count_handler)
        self.count_logger.setLevel(logging.INFO)
        self.count_logger.propagate = False

    def remove_non_bmp(self, text):
        # return "".join(c for c in text if ord(c) <= 0xFFFF)
        return text

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login_juejin(self):
        self.logger.info("[JuejinBot] 尝试使用 Cookie 登录掘金...")
        self.driver.get("https://juejin.cn/")
        if self.load_and_inject_cookies():
            self.logger.info("[JuejinBot] 成功复用 Cookie 登录")
            return

        self.logger.info("[JuejinBot] Cookie 无效，请手动登录...")
        self.driver.get("https://juejin.cn/login")
        input("[JuejinBot] 请手动登录掘金并完成验证后按回车...")

        cookies = self.driver.get_cookies()
        self.save_cookies(cookies)
        self.logger.info("[JuejinBot] Cookie 已保存，登录流程完成")

        # 登录完成后关闭当前窗口，重新初始化浏览器为“伪无头”模式
        self.driver.quit()

        headless_options = Options()
        headless_options.add_argument("--disable-gpu")
        headless_options.add_argument("--no-sandbox")
        headless_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=headless_options)
        self.driver.get("https://juejin.cn/")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.minimize_window()
        self.logger.info("[JuejinBot] 已切换为伪无头模式浏览器")

    def load_and_inject_cookies(self):
        if not os.path.exists(self.cookie_path):
            return False
        with open(self.cookie_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        self.driver.get("https://juejin.cn/")
        for cookie in cookies:
            cookie.pop("sameSite", None)
            try:
                self.driver.add_cookie(cookie)
            except Exception:
                pass
        self.driver.refresh()
        time.sleep(2)
        # 检查是否跳转到登录页或显示二维码等登录提示
        current_url = self.driver.current_url
        if "juejin.cn/login" in current_url:
            self.logger.warning("[JuejinBot] 当前页面为登录页，Cookie 失效")
            return False
        return True

    def save_cookies(self, cookies):
        with open(self.cookie_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

    def get_random_comment(self):
        return random.choice(self.comments)

    def run(self, interval=30):
        self.setup_browser()
        self.login_juejin()
        # 检查是否已有缓存链接文件
        while True:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    try:
                        hrefs = json.load(f)
                    except json.JSONDecodeError:
                        hrefs = {}
            else:
                hrefs = {}

            if not hrefs:
                self.logger.warning("[JuejinBot] 缓存为空或无效，重新获取链接中...")
                hrefs = self.get_recommended_note_links()
                if hrefs:
                    with open(self.cache_path, "w", encoding="utf-8") as f:
                        json.dump(hrefs, f, ensure_ascii=False, indent=2)
                else:
                    self.logger.error("[JuejinBot] 未获取到笔记链接，等待重试...")
                    time.sleep(10)
                    continue
            self.logger.info("[JuejinBot] 开始评价...")
            self.comment_on_note_links(hrefs)

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            time.sleep(sleep_time)

    def comment_on_note_links(self, note_links):
        """
        Visit each note URL, open the comment box, type a random comment, and send.
        Includes robust waits + fallbacks to reduce ChromeDriver crashes caused by stale/absent elements.
        """
        base = "https://www.zhihu.com"

        # --- 读取缓存文件到 current_cache ---
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    current_cache = json.load(f)
            except Exception:
                current_cache = {}
        else:
            current_cache = {}

        for idx, (url, title) in enumerate(
            tqdm(note_links.items(), desc="评论进度"), 1
        ):
            # 跳过已评论过的链接
            if self.comment_db.has_commented(url, Platform.JUEJIN):
                self.logger.info(f"[JuejinBot] 已跳过已评论过的链接：{url}")
                # --- 移除已评论链接 ---
                if url in current_cache:
                    del current_cache[url]
                continue
            self.logger.info(
                f"[JuejinBot] 正在评论第 {idx}/{len(note_links)} 条（标题：{title}）..."
            )
            # Normalize URL (some feeds return relative URLs)
            if url and url.startswith("/"):
                url = urllib.parse.urljoin(base, url)

            try:
                self.logger.info(f"[JuejinBot] 打开笔记：{url}")
                self.driver.get(url)

                # 等待文档 ready (body 存在 & readyState == complete)
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                WebDriverWait(self.driver, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
                # 改为等待输入框出现（提前预热页面，等待评论输入框可用）
                try:
                    WebDriverWait(self.driver, 5).until(
                        lambda d: d.execute_script(
                            "return !!document.querySelector('div.rich-input')"
                        )
                    )
                except Exception:
                    pass

                # 检测是否被踢回登录页（关键词 login 或 qrcode）
                cur = self.driver.current_url
                if "login" in cur or "account" in cur:
                    self.logger.error(f"[JuejinBot] 页面跳到登录，跳过：{url}")
                    self.exit(1)

                # 用更短的等待 scroll 完成
                time.sleep(random.uniform(0.5, 1.0))

                # 定位掘金“评论”触发元素
                trigger_locators = [
                    (
                        By.CSS_SELECTOR,
                        "div.panel-btn > svg.icon-comment",
                    ),
                    (
                        By.CSS_SELECTOR,
                        "div.panel-btn[badge] svg",
                    ),
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
                    self.logger.info(f"[JuejinBot] 未找到评论入口，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            "[JuejinBot] 连续未找到评论入口 3 次，程序退出"
                        )
                        self.exit(1)
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

                # 等评论输入框（新版掘金 rich-input 编辑器定位）
                input_locators = [
                    (
                        By.CSS_SELECTOR,
                        "div.rich-input[contenteditable='true']",
                    )
                ]

                input_box = None
                for how, what in input_locators:
                    try:
                        input_box = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((how, what))
                        )
                        # 确保输入框在视口中
                        try:
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({block:'center'});",
                                input_box,
                            )
                        except Exception:
                            pass
                        time.sleep(0.3)
                        break
                    except Exception:
                        continue

                if input_box is None:
                    self.logger.info(f"[JuejinBot] 未找到评论输入框，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            "[JuejinBot] 连续未找到评论输入框 3 次，程序退出"
                        )
                        self.exit(1)
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
                    self.logger.info(f"[JuejinBot] 无法输入评论，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[JuejinBot] 连续无法输入评论 3 次，程序退出")
                        self.exit(1)
                    continue

                # 发送评论按钮（新版样式）
                send_locators = [(By.CSS_SELECTOR, "button.submit-btn.active")]

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
                    self.logger.info(f"[JuejinBot] 找不到发送按钮，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            "[JuejinBot] 连续找不到发送按钮 3 次，程序退出"
                        )
                        self.exit(1)
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
                    self.logger.info(f"[JuejinBot] 评论失败（toast）：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[JuejinBot] 连续失败 3 次，程序退出")
                        self.exit(1)
                    continue  # 下一条

                # 成功
                self.logger.info(f"[JuejinBot] 已评论 {comment}   链接：{url}")
                self.comment_count += 1
                self.failed_comment_count = 0
                self.comment_count_data[self.today] = self.comment_count
                with open(self.comment_count_path, "w", encoding="utf-8") as f:
                    json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)
                self.count_logger.info(f"{self.today} 累计评论：{self.comment_count}")

                # 记录已评论
                self.comment_db.record_comment(
                    platform=Platform.JUEJIN,
                    url=url,
                    title=title,
                    comment=comment,
                    status="success",
                )
                if self.comment_count >= limitation:
                    self.logger.info(
                        f"[JuejinBot] 今日评论已达 {limitation} 条，程序退出"
                    )
                    self.exit(0)

                # 改为更短的延迟
                time.sleep(random.uniform(1.0, 2.0))

                # --- 移除已评论链接 ---
                if url in current_cache:
                    del current_cache[url]

            except Exception as e:
                self.logger.info(f"[JuejinBot] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info("[JuejinBot] 连续失败 3 次，程序退出")
                    self.exit(1)

        # --- 循环结束后统一写回缓存 ---
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(current_cache, f, ensure_ascii=False, indent=2)

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        exit(num)

    def get_recommended_note_links(self, scroll_times: int = 5):
        """
        Collect note links from the recommend feed.
        Scroll multiple times to load more.
        Returns a dict: {url: title}
        """
        self.logger.info("[JuejinBot] get_recommended_note_links...")

        self.driver.get("https://juejin.cn/?sort=three_days_hottest")

        # 等初次加载
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        hrefs = dict()
        last_height = 0
        for i in range(scroll_times):
            lis = self.driver.find_elements(By.CSS_SELECTOR, "div.entry-list li.item")
            for li in lis:
                try:
                    a_tag = li.find_element(By.CSS_SELECTOR, "a.title")
                    href = a_tag.get_attribute("href") or ""
                    title = a_tag.get_attribute("title") or ""
                    if href and title:
                        # 拼接完整 URL，确保 href 是绝对路径
                        if href.startswith("/"):
                            href = urllib.parse.urljoin("https://juejin.cn", href)
                        # 跳过已评论过的链接
                        if self.comment_db.has_commented(href, Platform.JUEJIN):
                            continue
                        hrefs[href] = title
                        self.logger.info(f"[JuejinBot] 抓取链接: {href} 标题: {title}")
                except Exception:
                    continue
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

        self.logger.info(f"[JuejinBot] 共获取到 {len(hrefs)} 条链接，其中包含标题信息")
        return hrefs


if __name__ == "__main__":
    print("[JuejinBot] started...")
    bot = JuejinBot()
    bot.run()
    print("[JuejinBot] ended...")
