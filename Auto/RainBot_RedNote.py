import time
from BaseBot import BaseBot
import os
import random
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from comment_db import CommentDB, Platform
from tqdm import tqdm

limitation = 100


# 模拟自动评论的主类
class XHSBot(BaseBot):
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "log")
        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)  # 确保data目录存在
        comment_path = os.path.join(data_dir, "comments.json")
        home_url = "https://www.xiaohongshu.com"
        super().__init__(log_dir, comment_path, home_url)
        self.driver = None
        self.failed_comment_count = 0
        self.comment_db = CommentDB()

        self.cookie_path = os.path.join(data_dir, f"{self.class_name}_cookies.json")
        self.cache_path = os.path.join(data_dir, f"{self.class_name}_cached_hrefs.json")
        self.comment_count_path = os.path.join(log_dir, "comment_count_daily.json")
        self.today = time.strftime("%Y-%m-%d")

        # 延迟配置参数，可切换 fast/safe 模式
        self.delay_profile = {"base": 0.1, "jitter": 0.3}  # 可调整为 {"base": 0.2, "jitter": 0.6} 用于慢模式

        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                self.comment_count_data = json.load(f)
        else:
            self.comment_count_data = {}

        if self.class_name not in self.comment_count_data:
            self.comment_count_data[self.class_name] = {}

    def setup_browser(self):
        chrome_options = Options()
        # 如需无头运行，可启用下行
        # chrome_options.add_argument('--headless')
        chrome_options.page_load_strategy = "eager"  # 只等 DOMContentLoaded，不等所有资源
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")

        # 下载与当前 Chrome 版本对应的 ChromeDriver
        chrome_version = self.get_chrome_version()
        print(f"Detected Chrome version: {chrome_version}")
        service = Service(ChromeDriverManager(driver_version=chrome_version).install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "*.mp4",
                ]
            },
        )

    def enable_resource_blocking(self):
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {
                    "urls": [
                        "*.png",
                        "*.jpg",
                        "*.jpeg",
                        "*.gif",
                        "*.webp",
                        "*.mp4",
                        "*.webm",
                        "*.svg",
                        "*.woff",
                        "*.ttf",
                    ]
                },
            )
            self.logger.info(f"[{self.class_name}] ✅ 成功启用资源拦截")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] ❌ 启用资源拦截失败: {e}")

    # 登录方法已假设在 BaseBot 中实现为 self.login()

    def get_random_comment(self):
        return random.choice(self.comments)

    def run(self, interval=30):
        self.setup_browser()
        self.login()
        self.enable_resource_blocking()
        while True:
            hrefs = self.get_recommended_note_links()
            if not hrefs:
                self.logger.info(f"[{self.class_name}] 未获取到笔记链接，等待重试...")
                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])
                continue

            should_continue = self.comment_on_note_links(hrefs)
            if should_continue is False:
                break
            if self.failed_comment_count >= 3:
                self.logger.info(f"[{self.class_name}] 已累计失败超过 3 次，主循环退出")
                print(f"[{self.class_name}] 已累计失败超过 3 次，主循环退出")
                break

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            self.sleep_random(base=self.delay_profile["base"], jitter=sleep_time)

    def comment_on_note_links(self, note_links):
        """
        Visit each note URL, open the comment box, type a random comment, and send.
        Includes robust waits + fallbacks to reduce ChromeDriver crashes caused by stale/absent elements.
        """
        base = "https://www.xiaohongshu.com"
        for idx, (url, title) in enumerate(
            tqdm(note_links.items(), desc=f"[{self.class_name}]评论进度", unit="条"), 1
        ):
            # 每次处理前看看数据库中是否评论过
            if self.comment_db.has_commented(url, Platform.XHS):
                self.logger.info(
                    f"[{self.class_name}] 已在数据库中记录为已评论，跳过：{url}"
                )
                try:
                    if os.path.exists(self.cache_path):
                        with open(self.cache_path, "r", encoding="utf-8") as f:
                            cached = json.load(f)
                        if url in cached:
                            del cached[url]
                            with open(self.cache_path, "w", encoding="utf-8") as f:
                                json.dump(cached, f, ensure_ascii=False, indent=2)
                            self.logger.info(
                                f"[{self.class_name}] 已从缓存中移除已评论链接：{url}"
                            )
                except Exception as e:
                    self.logger.warning(f"[{self.class_name}] 移除链接缓存失败: {e}")
                continue

            # 日志记录
            self.logger.info(
                f"[{self.class_name}] 正在评论第 {idx}/{len(note_links)} 条（标题：{title}）..."
            )
            # Normalize URL (some feeds return relative URLs)
            if url and url.startswith("/"):
                url = urllib.parse.urljoin(base, url)

            try:
                self.logger.info(
                    f"[{self.class_name}] 打开笔记：{url}（标题：{title}）"
                )
                self.driver.get(url)

                # 精简页面加载等待，只等 readyState 为 interactive 或 complete
                WebDriverWait(self.driver, 5).until(
                    lambda d: d.execute_script("return document.readyState") in ["interactive", "complete"]
                )
                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])  # 给前端框架一点渲染缓冲

                # 检测是否被踢回登录页（关键词 login 或 qrcode）
                cur = self.driver.current_url
                if "login" in cur or "account" in cur:
                    self.logger.error(f"[{self.class_name}] 页面跳到登录「{cur}」，跳过：{url}")

                    # 清除登录信息（防止下一次仍失败）
                    self.driver.delete_all_cookies()
                    self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
                    self.logger.info(f"[{self.class_name}] 清除浏览器缓存")

                    # 强制跳转到首页 + 等待用户手动登录
                    self.driver.get("https://www.xiaohongshu.com/")
                    self.logger.info(f"[{self.class_name}] 请在当前页面完成登录，然后回到终端按回车继续...")
                    input(f"[{self.class_name}] >>> 手动登录完成后请按下回车")

                    # 保存新的 Cookie
                    self.save_cookies(self.driver, self.cookie_path)

                # 滚动一点确保评论入口渲染
                self.driver.execute_script("window.scrollBy(0, 400);")
                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

                # 定位“说点什么...”触发元素（多种 fallback）
                trigger_locators = [
                    (By.XPATH, "//span[normalize-space()='说点什么...']"),
                    (By.XPATH, "//div[contains(@class,'not-active')]//span[contains(text(),'说点什么')]"),
                    (By.CSS_SELECTOR, "div.not-active.inner-when-not-active span"),
                ]

                comment_trigger = None
                for how, what in trigger_locators:
                    try:
                        comment_trigger = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((how, what))
                        )
                        WebDriverWait(self.driver, 2.5).until(
                            EC.element_to_be_clickable((how, what))
                        )
                        break
                    except Exception:
                        continue

                if comment_trigger is None:
                    self.logger.info(f"[{self.class_name}] 未找到评论入口，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续未找到评论入口 3 次，程序退出"
                        )
                        return False
                    continue

                # 确保在视口中
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        comment_trigger,
                    )
                except Exception:
                    pass
                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

                try:
                    comment_trigger.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", comment_trigger)

                # 等评论输入框（contenteditable）
                input_locators = [
                    (By.CSS_SELECTOR, "p#content-textarea[contenteditable='true']"),
                    (By.CSS_SELECTOR, "div.comment-editor [contenteditable='true']"),
                ]

                input_box = None
                for how, what in input_locators:
                    try:
                        input_box = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((how, what))
                        )
                        break
                    except Exception:
                        continue

                if input_box is None:
                    self.logger.info(
                        f"[{self.class_name}] 未找到评论输入框，跳过：{url}"
                    )
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续未找到评论输入框 3 次，程序退出"
                        )
                        return False
                    continue

                # 激活输入框（有些前端需要点击 innerEditable 子节点）
                try:
                    ActionChains(self.driver).move_to_element(
                        input_box
                    ).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", input_box)
                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

                comment = self.get_random_comment()

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
                    self.logger.info(f"[{self.class_name}] 无法输入评论，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续无法输入评论 3 次，程序退出"
                        )
                        return False
                    continue

                # 发送评论按钮（多个 fallback）
                send_locators = [
                    (By.CSS_SELECTOR, "button.btn.submit"),
                    (By.XPATH, "//button[contains(@class,'submit') and contains(.,'发送')]"),
                ]

                submit_button = None
                for how, what in send_locators:
                    try:
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((how, what))
                        )
                        break
                    except Exception:
                        continue

                if submit_button is None:
                    self.logger.info(f"[{self.class_name}] 找不到发送按钮，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续找不到发送按钮 3 次，程序退出"
                        )
                        return False
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
                    self.logger.info(f"[{self.class_name}] 评论失败（toast）：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(f"[{self.class_name}] 连续失败 3 次，程序退出")
                        return False
                    continue  # 下一条

                # 成功
                self.logger.info(f"[{self.class_name}] 已评论 {comment} 链接：{url}")
                self.comment_db.record_comment(
                    platform=Platform.XHS,
                    url=url,
                    title=title,
                    comment=comment,
                    status="success",
                )
                self.comment_count += 1
                self.failed_comment_count = 0
                self.save_comment_count()

                self.logger.info(
                    f"[{self.class_name}] 今日评论数：{self.comment_count}"
                )
                # 已评论笔记由 CommentDB 管理，无需本地记录
                # 实时更新 note_cache，移除已成功评论的链接
                try:
                    if os.path.exists(self.cache_path):
                        with open(self.cache_path, "r", encoding="utf-8") as f:
                            cached = json.load(f)
                        if url in cached:
                            del cached[url]
                            with open(self.cache_path, "w", encoding="utf-8") as f:
                                json.dump(cached, f, ensure_ascii=False, indent=2)
                            self.logger.info(
                                f"[{self.class_name}] 已从缓存中移除已评论链接：{url}"
                            )
                except Exception as e:
                    self.logger.warning(f"[{self.class_name}] 移除链接缓存失败: {e}")

                if self.comment_count >= limitation:
                    self.logger.info(
                        f"[{self.class_name}] 今日评论已达 {limitation} 条，程序退出"
                    )
                    return False

                self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

            except Exception as e:
                self.logger.info(f"[{self.class_name}] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info(f"[{self.class_name}] 连续失败 3 次，程序退出")
                    return False
        return True

    def login(self):
        self.logger.info(f"[{self.class_name}] 打开小红书首页以加载 Cookie...")
        self.driver.get("https://www.xiaohongshu.com/")

        if self.load_and_inject_cookies():
            self.logger.info(f"[{self.class_name}] 成功复用 Cookie 登录")
            return

        self.logger.info(f"[{self.class_name}] Cookie 无效，请手动登录...")
        input(f"[{self.class_name}] 请在当前页面完成登录后按回车继续...")

        self.save_cookies(self.driver, self.cookie_path)

    def load_and_inject_cookies(self):
        if not os.path.exists(self.cookie_path):
            self.logger.info(f"[{self.class_name}] Cookie 文件不存在")
            return False

        with open(self.cookie_path, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        if not cookies:
            self.logger.warning(f"[{self.class_name}] Cookie 文件内容为空")
            return False

        self.driver.get("https://www.xiaohongshu.com/")
        self.driver.delete_all_cookies()
        valid_cookie_count = 0
        for cookie in cookies:
            cookie.pop("sameSite", None)
            cookie["domain"] = ".xiaohongshu.com"  # 保证 domain 一致
            try:
                self.driver.add_cookie(cookie)
                valid_cookie_count += 1
            except Exception as e:
                self.logger.warning(f"注入 Cookie 失败: {cookie} -> {e}")

        if valid_cookie_count == 0:
            self.logger.warning(f"[{self.class_name}] 无有效 Cookie 被注入")
            return False

        self.driver.refresh()
        self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

        # 重新加载首页或 explore 页面
        self.logger.info(f"[{self.class_name}] 已注入 {valid_cookie_count} 条 Cookie，准备访问 explore 页面")
        self.driver.get("https://www.xiaohongshu.com/explore")
        self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

        # 检查是否仍显示“登录”按钮，或登录弹窗存在
         # 检查是否仍显示登录元素
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button#login-btn.login-btn"))
            )
            self.logger(f"[{self.class_name}] 页面仍包含登录按钮，说明未登录")
            return False
        except:
            pass

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.login-container"))
            )
            self.logger(f"[{self.class_name}] 页面仍包含登录弹窗，说明未登录")
            return False
        except:
            pass

        

        self.logger.info(f"[{self.class_name}] 成功复用 Cookie 登录")
        return True

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        exit(num)

    def get_recommended_note_links(self, scroll_times: int = 15, use_cache: bool = True):
        """
        Collect note links from the recommend feed. Returns a dict: {url: title}
        """
        self.logger.info(f"[{self.class_name}] get_recommended_note_links...")

        # ✅ 优先尝试读取缓存
        if use_cache and os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if cached:
                    self.logger.info(
                        f"[{self.class_name}] 已从缓存加载 {len(cached)} 条链接"
                    )
                    return cached
                else:
                    self.logger.warning(f"[{self.class_name}] 缓存为空，将重新抓取链接")
            except Exception as e:
                self.logger.warning(f"[{self.class_name}] 读取缓存失败: {e}")

        # ✅ 正常爬取流程（原逻辑）
        base_url = "https://www.xiaohongshu.com"
        self.driver.get(
            "https://www.xiaohongshu.com/search_result?keyword=%25E7%25A7%2591%25E6%258A%2580%25E6%2595%25B0%25E7%25A0%2581&source=web_explore_feed"
        )

        WebDriverWait(self.driver, 5).until(
            lambda d: d.execute_script("return document.readyState") in ["interactive", "complete"]
        )
        self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

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
                self.logger.info(f"[{self.class_name}] 抓取链接: {href} 标题: {title}")

            self.driver.execute_script(
                "window.scrollBy(0, document.body.scrollHeight);"
            )
            self.sleep_random(base=self.delay_profile["base"], jitter=self.delay_profile["jitter"])

            try:
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight;"
                )
                if new_height == last_height:
                    break
                last_height = new_height
            except Exception:
                pass
        # 过滤已评论链接（高效批量版）
        commented = set(
            self.comment_db.get_commented_urls_batch(list(hrefs.keys()), Platform.XHS)
        )
        hrefs = {url: title for url, title in hrefs.items() if url not in commented}
        self.logger.info(f"[{self.class_name}] 共获取到 {len(hrefs)} 条链接")

        # ✅ 写入缓存文件
        try:
            if hrefs:  # 只有有数据才写缓存
                with open(self.cache_path, "w", encoding="utf-8") as f:
                    json.dump(hrefs, f, ensure_ascii=False, indent=2)
                self.logger.info(f"[{self.class_name}] 链接已写入缓存")
            else:
                self.logger.warning(f"[{self.class_name}] 抓取结果为空，未写入缓存")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 写入缓存失败: {e}")

        return hrefs


if __name__ == "__main__":
    print("[XHSBot] started...")
    bot = None
    try:
        bot = XHSBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n[XHSBot] 收到中断信号，正在退出...")
    finally:
        if bot:
            try:
                if bot.driver:
                    bot.driver.quit()
                    print("[XHSBot] 浏览器已关闭")
            except Exception as e:
                print(f"[XHSBot] 浏览器关闭失败: {e}")

            try:
                if bot.comment_db:
                    bot.comment_db.close()
                    print("[XHSBot] comment_db 连接已关闭")
            except Exception as e:
                print(f"[XHSBot] 关闭 comment_db 失败: {e}")
            # os.system("sudo shutdown -h now")  # 立即关机

        print("[XHSBot] ended...")
