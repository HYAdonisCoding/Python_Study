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
from comment_db import CommentDB, Platform

limitation = 100


# 模拟自动评论的主类
class XHSBot:
    def __init__(self):
        bot_id = self.__class__.__name__
        # 初始化 CommentDB
        self.comment_db = CommentDB()
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

        # 读取原始数据
        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = {}

        # 初始化类名下的数据
        self.class_name = bot_id
        class_data = all_data.get(self.class_name, {})
        self.comment_count = class_data.get(self.today, 0)

        # 保存引用用于更新
        self.comment_count_data = all_data
        self.comment_count_data.setdefault(self.class_name, {})[self.today] = self.comment_count

        # 写入文件
        with open(self.comment_count_path, "w", encoding="utf-8") as f:
            json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)

        self.count_logger.info(f"{self.class_name} - {self.today} 累计评论：{self.comment_count}")

        self.cookie_path = os.path.join(base_dir, "xhs_cookies.json")
        self.note_cache_path = os.path.join(base_dir, f"{bot_id}_cached_notes.json")

        self.driver = None
        self.failed_comment_count = 0
        # 缓存路径
        self.cache_path = os.path.join(base_dir, f"{bot_id}_cached_hrefs.json")

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
        # 禁用图片和视频加载以节省流量
        self.driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.mp4", "*.webm"]})
        self.driver.execute_cdp_cmd("Network.enable", {})
        # self.driver = webdriver.Chrome(options=options)

    def login_xhs(self):
        self.logger.info("[XHSBot] 打开小红书首页以加载 Cookie...")
        self.driver.get("https://www.xiaohongshu.com/")

        if self.load_and_inject_cookies():
            self.logger.info("[XHSBot] 成功复用 Cookie 登录")
            return

        self.logger.info("[XHSBot] Cookie 无效，请手动登录...")
        input("[XHSBot] 请在当前页面完成登录后按回车继续...")

        cookies = self.driver.get_cookies()
        self.save_cookies(cookies)
        self.logger.info("[XHSBot] Cookie 已保存，登录流程完成")

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
        for idx, (url, title) in enumerate(note_links.items(), 1):
            # 显示进度条
            percent = int((idx / len(note_links)) * 100)
            bar_length = 30
            filled_length = int(bar_length * percent // 100)
            bar = "█" * filled_length + "-" * (bar_length - filled_length)
            print(
                f"\r[{percent:3}%] |{bar}| 第 {idx}/{len(note_links)} 条 - {title}",
                end="",
                flush=True,
            )
            # 每次处理前看看数据库中是否评论过
            if self.comment_db.has_commented(url, Platform.XHS):
                self.logger.info(f"[XHSBot] 已在数据库中记录为已评论，跳过：{url}")
                try:
                    if os.path.exists(self.note_cache_path):
                        with open(self.note_cache_path, "r", encoding="utf-8") as f:
                            cached = json.load(f)
                        if url in cached:
                            del cached[url]
                            with open(self.note_cache_path, "w", encoding="utf-8") as f:
                                json.dump(cached, f, ensure_ascii=False, indent=2)
                            self.logger.info(f"[XHSBot] 已从缓存中移除已评论链接：{url}")
                except Exception as e:
                    self.logger.warning(f"[XHSBot] 移除链接缓存失败: {e}")
                continue
            
            # 日志记录
            self.logger.info(
                f"[XHSBot] 正在评论第 {idx}/{len(note_links)} 条（标题：{title}）..."
            )
            # Normalize URL (some feeds return relative URLs)
            if url and url.startswith("/"):
                url = urllib.parse.urljoin(base, url)

            try:
                self.logger.info(f"[XHSBot] 打开笔记：{url}（标题：{title}）")
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
                    self.logger.error(f"[XHSBot] 页面跳到登录「{cur}」，跳过：{url}")
                    # 移除cookie
                    self.driver.delete_all_cookies()
                    self.save_cookies([])
                    # 清除浏览器缓存
                    self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
                    self.logger.info("[XHSBot] 清除浏览器缓存")
                    
                    # 尝试重新登录
                    self.login_xhs()

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
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续未找到评论入口 3 次，程序退出")
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
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续未找到评论输入框 3 次，程序退出")
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
                    self.logger.info(f"[XHSBot] 无法输入评论，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续无法输入评论 3 次，程序退出")
                        self.exit(1)
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
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续找不到发送按钮 3 次，程序退出")
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
                    self.logger.info(f"[XHSBot] 评论失败（toast）：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[XHSBot] 连续失败 3 次，程序退出")
                        self.exit(1)
                    continue  # 下一条

                # 成功
                self.logger.info(f"[XHSBot] 已评论 {comment} 链接：{url}")
                self.comment_db.record_comment(
                    platform=Platform.XHS,
                    url=url,
                    title=title,
                    comment=comment,
                    status="success",
                )
                self.comment_count += 1
                self.failed_comment_count = 0
                self.comment_count_data[self.class_name][self.today] = self.comment_count
                with open(self.comment_count_path, "w", encoding="utf-8") as f:
                    json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)

                self.count_logger.info(f"{self.today} 累计评论：{self.comment_count}")
                # 已评论笔记由 CommentDB 管理，无需本地记录
                # 实时更新 note_cache，移除已成功评论的链接
                try:
                    if os.path.exists(self.note_cache_path):
                        with open(self.note_cache_path, "r", encoding="utf-8") as f:
                            cached = json.load(f)
                        if url in cached:
                            del cached[url]
                            with open(self.note_cache_path, "w", encoding="utf-8") as f:
                                json.dump(cached, f, ensure_ascii=False, indent=2)
                            self.logger.info(f"[XHSBot] 已从缓存中移除已评论链接：{url}")
                except Exception as e:
                    self.logger.warning(f"[XHSBot] 移除链接缓存失败: {e}")
                

                if self.comment_count >= limitation:
                    self.logger.info(f"[XHSBot] 今日评论已达 {limitation} 条，程序退出")
                    self.exit(0)

                time.sleep(random.uniform(2.5, 5.5))

            except Exception as e:
                self.logger.info(f"[XHSBot] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info("[XHSBot] 连续失败 3 次，程序退出")
                    self.exit(1)

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        exit(num)

    def get_recommended_note_links(self, scroll_times: int = 5, use_cache: bool = True):
        """
        Collect note links from the recommend feed. Returns a dict: {url: title}
        """
        self.logger.info("[XHSBot] get_recommended_note_links...")

        # ✅ 优先尝试读取缓存
        if use_cache and os.path.exists(self.note_cache_path):
            try:
                with open(self.note_cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if cached:
                    self.logger.info(f"[XHSBot] 已从缓存加载 {len(cached)} 条链接")
                    return cached
                else:
                    self.logger.warning("[XHSBot] 缓存为空，将重新抓取链接")
            except Exception as e:
                self.logger.warning(f"[XHSBot] 读取缓存失败: {e}")

        # ✅ 正常爬取流程（原逻辑）
        base_url = "https://www.xiaohongshu.com"
        self.driver.get(
            "https://www.xiaohongshu.com/search_result?keyword=%25E7%25A7%2591%25E6%258A%2580%25E6%2595%25B0%25E7%25A0%2581&source=web_explore_feed"
        )

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        hrefs = dict()
        last_height = 0
        for i in range(scroll_times):
            cards = self.driver.find_elements(
                By.CSS_SELECTOR, "div.feeds-container section.note-item"
            )
            for a in cards:
                try:
                    cover_a = a.find_element(By.CSS_SELECTOR, "a.cover")
                    href = cover_a.get_attribute("href") or ""
                    if href.startswith("/"):
                        href = urllib.parse.urljoin(base_url, href)
                    if (
                        not href.startswith(base_url + "/explore/")
                        and "/search_result/" not in href
                    ):
                        continue
                except Exception:
                    continue
                try:
                    title_elem = a.find_element(
                        By.CSS_SELECTOR, "div.footer a.title span"
                    )
                    title = title_elem.text.strip()
                except Exception:
                    title = ""
                hrefs[href] = title
                self.logger.info(f"[XHSBot] 抓取链接: {href} 标题: {title}")

            self.driver.execute_script(
                "window.scrollBy(0, document.body.scrollHeight);"
            )
            time.sleep(random.uniform(1.5, 3.0))

            try:
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
                if new_height == last_height:
                    break
                last_height = new_height
            except Exception:
                pass
        # 过滤已评论链接
        commented = self.comment_db.get_commented_urls(Platform.XHS)
        hrefs = {url: title for url, title in hrefs.items() if url not in commented}
        self.logger.info(f"[XHSBot] 共获取到 {len(hrefs)} 条链接")

        # ✅ 写入缓存文件
        try:
            if hrefs:  # 只有有数据才写缓存
                with open(self.note_cache_path, "w", encoding="utf-8") as f:
                    json.dump(hrefs, f, ensure_ascii=False, indent=2)
                self.logger.info("[XHSBot] 链接已写入缓存")
            else:
                self.logger.warning("[XHSBot] 抓取结果为空，未写入缓存")
        except Exception as e:
            self.logger.warning(f"[XHSBot] 写入缓存失败: {e}")

        return hrefs

    def load_and_inject_cookies(self):
        if not os.path.exists(self.cookie_path):
            return False
        with open(self.cookie_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        self.driver.get("https://www.xiaohongshu.com/")
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
        page_source = self.driver.page_source
        if "xiaohongshu.com/login" in current_url:
            self.logger.warning("[XHSBot] 当前页面为登录页，Cookie 失效")
            return False
        return True

    def save_cookies(self, cookies):
        with open(self.cookie_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    print("[XHSBot] started...")
    bot = XHSBot()
    bot.run()
    print("[XHSBot] ended...")
