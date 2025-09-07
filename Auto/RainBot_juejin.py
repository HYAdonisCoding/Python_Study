import os
import random
import json
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
from comment_db import CommentDB, Platform
from BaseBot import BaseBot

limitation = 100


# 模拟自动评论的主类
class JuejinBot(BaseBot):
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "log")
        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)  # 确保data目录存在
        comment_path = os.path.join(data_dir, "comments.json")
        home_url = "https://juejin.cn"
        super().__init__(log_dir, comment_path, home_url)

        self.driver = None
        self.failed_comment_count = 0
        self.comment_db = CommentDB()

        self.cookie_path = os.path.join(data_dir, f"{self.class_name}_cookies.json")
        self.cache_path = os.path.join(data_dir, f"{self.class_name}_cached_hrefs.json")
        self.comment_count_path = os.path.join(log_dir, "comment_count_daily.json")
        self.today = time.strftime("%Y-%m-%d")

        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                self.comment_count_data = json.load(f)
        else:
            self.comment_count_data = {}

        if self.class_name not in self.comment_count_data:
            self.comment_count_data[self.class_name] = {}

    def remove_non_bmp(self, text):
        # return "".join(c for c in text if ord(c) <= 0xFFFF)
        return text

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--window-size=1920,1080")
        # 下载与当前 Chrome 版本对应的 ChromeDriver
        chrome_version = self.get_chrome_version()
        print(f"Detected Chrome version: {chrome_version}")
        service = Service(ChromeDriverManager(driver_version=chrome_version).install())

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # 启用 CDP 进行图片/视频拦截
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
                        "*.svg",
                        "*.mp4",
                        "*.avi",
                    ]
                },
            )
            self.logger.info(f"[{self.class_name}] 已设置阻止图片和视频资源加载")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}]设置资源拦截失败: {e}")

    def login_juejin(self):
        def check_login(driver):
            return (
                "login" not in driver.current_url
                and "account" not in driver.current_url
            )

        self.logger.info(f"[{self.class_name}] 检查登录状态...")
        self.ensure_login(self.driver, self.cookie_path, check_login)

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
                self.logger.warning(f"[{self.class_name}] 缓存为空或无效，重新获取链接中...")
                hrefs = self.get_recommended_note_links()
                if hrefs:
                    with open(self.cache_path, "w", encoding="utf-8") as f:
                        json.dump(hrefs, f, ensure_ascii=False, indent=2)
                else:
                    self.logger.error(f"[{self.class_name}] 未获取到笔记链接，等待重试...")
                    self.sleep_random(base=1.0, jitter=1.0)
                    continue
            self.logger.info(f"[{self.class_name}] 开始评价...")
            should_exit = self.comment_on_note_links(hrefs)
            if should_exit:
                break

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            self.sleep_random(base=1.0, jitter=sleep_time)

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
            tqdm(note_links.items(), desc=f"[{self.class_name}]评论进度", unit="条"), 1
        ):
            # 跳过已评论过的链接
            if self.comment_db.has_commented(url, Platform.JUEJIN):
                self.logger.info(f"[{self.class_name}] 已跳过已评论过的链接：{url}")
                # --- 移除已评论链接 ---
                if url in current_cache:
                    self.remove_cache(url)
                    del current_cache[url]
                continue
            self.logger.info(
                f"[{self.class_name}] 正在评论第 {idx}/{len(note_links)} 条（标题：{title}）..."
            )
            # Normalize URL (some feeds return relative URLs)
            if url and url.startswith("/"):
                url = urllib.parse.urljoin(base, url)

            try:
                self.logger.info(f"[{self.class_name}] 打开笔记：{url}")
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
                    self.logger.error(
                        f"[{self.class_name}] 页面跳到登录「{cur}」，跳过：{url}"
                    )
                    # 移除cookie
                    self.driver.delete_all_cookies()
                    self.save_cookies([])
                    # 清除浏览器缓存
                    self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
                    self.logger.info(f"[{self.class_name}] 清除浏览器缓存")

                    # 尝试重新登录
                    self.login_juejin()

                # 用更短的等待 scroll 完成
                self.sleep_random(base=1.0, jitter=1.0)

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
                    self.logger.info(f"[{self.class_name}] 未找到评论入口，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续未找到评论入口 3 次，程序退出"
                        )
                        self.exit(1)
                        return True
                    continue

                # 确保在视口中
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        comment_trigger,
                    )
                except Exception:
                    pass
                self.sleep_random(base=1.0, jitter=1.0)

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
                        self.sleep_random(base=1.0, jitter=1.0)
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
                        self.exit(1)
                        return True
                    continue

                # 激活输入框（有些前端需要点击 innerEditable 子节点）
                try:
                    ActionChains(self.driver).move_to_element(
                        input_box
                    ).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", input_box)
                self.sleep_random(base=1.0, jitter=1.0)

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
                    self.logger.info(f"[{self.class_name}] 无法输入评论，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(f"[{self.class_name}] 连续无法输入评论 3 次，程序退出")
                        self.exit(1)
                        return True
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
                    self.logger.info(f"[{self.class_name}] 找不到发送按钮，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续找不到发送按钮 3 次，程序退出"
                        )
                        self.exit(1)
                        return True
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
                        self.exit(1)
                        return True
                    continue  # 下一条

                # 成功
                self.logger.info(f"[{self.class_name}] 已评论 {comment}   链接：{url}")
                self.comment_count += 1
                self.failed_comment_count = 0
                self.save_comment_count()
                self.logger.info(
                    f"[{self.class_name}] {self.today} 累计评论：{self.comment_count}"
                )

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
                        f"[{self.class_name}] 今日评论已达 {limitation} 条，程序退出"
                    )
                    self.exit(0)
                    return True

                # 改为更短的延迟
                self.sleep_random(base=1.0, jitter=1.0)

                # --- 移除已评论链接 ---
                if url in current_cache:
                    self.remove_cache(url)
                    del current_cache[url]

            except Exception as e:
                self.logger.info(f"[{self.class_name}] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info(f"[{self.class_name}] 连续失败 3 次，程序退出")
                    self.exit(1)
                    return True

        # --- 循环结束后统一写回缓存（仅保留未被移除的链接） ---
        remaining_cache = {
            url: title
            for url, title in current_cache.items()
            if not self.comment_db.has_commented(url, Platform.JUEJIN)
        }
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(remaining_cache, f, ensure_ascii=False, indent=2)
        return False

    def remove_cache(self, url):
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

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        try:
            if self.comment_db:
                self.comment_db.close()
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 关闭 comment_db 失败: {e}")
        # exit(num)

    def _extract_links_from_page(self) -> dict:
        """
        从当前页面提取文章链接与标题
        返回字典: {url: title}
        """
        link_dict = {}
        try:
            article_elements = self.driver.find_elements(By.CSS_SELECTOR, 'a.jj-link.title[href^="/post/"]')
            for elem in article_elements:
                href = elem.get_attribute("href")
                title = elem.get_attribute("title") or elem.text.strip()
                if href and href.startswith("http") and title:
                    link_dict[href] = title
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 提取链接失败: {e}")
        return link_dict

    def get_recommended_note_links(self, max_count: int = 300, scroll_times: int = 5) -> dict:
        self.logger.info(f"[{self.class_name}] 开始抓取推荐链接")

        sources = [
            ("推荐", "https://juejin.cn/"),
            ("三日热榜", "https://juejin.cn/?sort=three_days_hottest"),
            ("周热榜", "https://juejin.cn/?sort=weekly_hottest"),
            ("月热榜", "https://juejin.cn/?sort=monthly_hottest"),
            ("总热榜", "https://juejin.cn/?sort=hottest"),
        ]

        seen_urls = set()
        result_links = {}
        commented_urls = set(self.comment_db.get_commented_urls(Platform.JUEJIN))

        for name, url in sources:
            self.logger.info(f"[{self.class_name}]抓取来源: {name} - {url}")
            self.driver.get(url)
            self.sleep_random(base=1.0, jitter=3.0)

            if name == "推荐":
                for _ in range(scroll_times):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.sleep_random(base=1.0, jitter=2.0)

            links = self._extract_links_from_page()

            for link, title in links.items():
                if link in seen_urls:
                    continue
                if link in commented_urls:
                    continue
                seen_urls.add(link)
                result_links[link] = title
                if len(result_links) >= max_count:
                    self.logger.info(f"[{self.class_name}]达到抓取上限 {max_count}，提前返回")
                    return result_links

        self.logger.info(f"[{self.class_name}]抓取完成，共获取未评论链接: {len(result_links)} 条")
        return result_links


if __name__ == "__main__":
    print("[JuejinBot] started...")
    bot = None
    try:
        bot = JuejinBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n[JuejinBot] 收到中断信号，正在退出...")
    finally:
        if bot and bot.comment_db:
            try:
                bot.comment_db.close()
                print("[JuejinBot] comment_db 连接已关闭")
            except Exception as e:
                print(f"[JuejinBot] 关闭 comment_db 失败: {e}")
        print("[JuejinBot] ended...")