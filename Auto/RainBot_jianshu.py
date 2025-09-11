import os
import random
import json
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
from comment_db import CommentDB, Platform
from BaseBot import BaseBot

limitation = 100


# 模拟自动评论的主类
class JianshuBot(BaseBot):
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "log")
        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)  # 确保data目录存在
        comment_path = os.path.join(data_dir, "comments.json")
        home_url = "https://www.jianshu.com"
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
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        def check_login(driver):
            # 检查页面上是否存在登录按钮 <a id="sign_in">
            try:
                sign_in_btn = driver.find_elements(By.CSS_SELECTOR, "a#sign_in")
                return not bool(sign_in_btn)
            except Exception:
                return True  # 如果异常，假定已登录

        self.logger.info(f"[{self.class_name}] 检查登录状态...")
        self.ensure_login(self.driver, self.cookie_path, check_login)


    

    def run(self, interval=30):
        self.setup_browser()
        self.login()
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
            self.comment_on_note_links(hrefs)

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            self.sleep_random(base=1.0, jitter=sleep_time)

    def comment_on_note_links(self, note_links):
        """
        Visit each note URL, open the comment box, type a random comment, and send.
        Includes robust waits + fallbacks to reduce ChromeDriver crashes caused by stale/absent elements.
        """
        base = "https://www.jianshu.com"

        # --- 读取缓存文件到 current_cache ---
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    current_cache = json.load(f)
            except Exception:
                current_cache = {}
        else:
            current_cache = {}

        def wait_until_enabled(driver, element, timeout=10, poll_frequency=0.5):
            start_time = time.time()
            while time.time() - start_time < timeout:
                if element.is_enabled():
                    return True
                time.sleep(poll_frequency)
            return False

        for idx, (url, title) in enumerate(
            tqdm(note_links.items(), desc="评论进度"), 1
        ):
            # 跳过已评论过的链接
            if self.comment_db.has_commented(url, Platform.JIANSHU):
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
                    self.logger.error(f"[{self.class_name}] 页面跳到登录「{cur}」，跳过：{url}")
                    # 移除cookie
                    self.driver.delete_all_cookies()
                    self.save_cookies([])
                    # 清除浏览器缓存
                    self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
                    self.logger.info(f"[{self.class_name}] 清除浏览器缓存")
                    # 重新初始化浏览器
                    self.driver.quit()
                    self.setup_browser()
                    # 尝试重新登录
                    self.login()

                # 用更短的等待 scroll 完成
                self.sleep_random(base=1.0, jitter=1.0)

                # 简书默认加载评论框，无需触发评论按钮

                # 等评论输入框（适配简书评论框 CSS 选择器）
                input_locators = [
                    (
                        By.CSS_SELECTOR,
                        "div.TDvCqd textarea.W2TSX_",
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
                    self.logger.info(f"[{self.class_name}] 未找到评论输入框，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            f"[{self.class_name}] 连续未找到评论输入框 3 次，程序退出"
                        )
                        self.exit(1)
                    continue

                # 激活输入框
                try:
                    ActionChains(self.driver).move_to_element(input_box).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", input_box)
                self.sleep_random(base=1.0, jitter=1.0)

                comment = self.remove_non_bmp(self.get_random_comment())

                # 尝试清空输入框
                try:
                    input_box.send_keys(Keys.COMMAND + "a")
                    input_box.send_keys(Keys.BACKSPACE)
                except Exception:
                    pass

                # 使用 ActionChains 模拟键盘输入
                typed_ok = True
                try:
                    ActionChains(self.driver).send_keys(comment).perform()
                except Exception:
                    typed_ok = False

                if not typed_ok:
                    self.logger.info(f"[{self.class_name}] 无法输入评论，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(f"[{self.class_name}] 连续无法输入评论 3 次，程序退出")
                        self.exit(1)
                    continue

                # 触发 JS 事件，确保输入框内容同步
                self.driver.execute_script("""
                    const el = arguments[0];
                    el.focus();
                    el.dispatchEvent(new KeyboardEvent('keydown', { bubbles: true }));
                    el.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                    el.dispatchEvent(new InputEvent('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                """, input_box)

                # 发送评论按钮（新版样式，适配简书发布按钮新 CSS 选择器）
                send_locators = [(By.CSS_SELECTOR, "button._1OyPqC._3Mi9q9._1YbC5u")]

                submit_button = None
                for how, what in send_locators:
                    try:
                        submit_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((how, what))
                        )
                        if not wait_until_enabled(self.driver, submit_button):
                            self.logger.info(f"[{self.class_name}] 发布按钮长时间未激活，跳过：{url}")
                            submit_button = None
                        break
                    except Exception:
                        continue

                if submit_button:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button)
                    try:
                        submit_button.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", submit_button)
                else:
                    self.logger.info(f"[{self.class_name}] 找不到发送按钮，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(f"[{self.class_name}] 连续找不到发送按钮 3 次，程序退出")
                        self.exit(1)
                    continue

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
                    continue  # 下一条

                # 成功
                self.logger.info(f"[{self.class_name}] 已评论 {comment}   链接：{url}")
                self.comment_count += 1
                self.failed_comment_count = 0
                self.comment_count_data.setdefault(self.class_name, {})[self.today] = self.comment_count
                with open(self.comment_count_path, "w", encoding="utf-8") as f:
                    json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)
                self.logger.info(f"[{self.class_name}] {self.today} 累计评论：{self.comment_count}")

                # 记录已评论
                self.comment_db.record_comment(
                    platform=Platform.JIANSHU,
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

        # --- 循环结束后统一写回缓存（仅保留未被移除的链接） ---
        remaining_cache = {
            url: title for url, title in current_cache.items()
            if not self.comment_db.has_commented(url, Platform.JIANSHU)
        }
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(remaining_cache, f, ensure_ascii=False, indent=2)

    def remove_cache(self, url):
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if url in cached:
                    del cached[url]
                    with open(self.cache_path, "w", encoding="utf-8") as f:
                        json.dump(cached, f, ensure_ascii=False, indent=2)
                    self.logger.info(f"[{self.class_name}] 已从缓存中移除已评论链接：{url}")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 移除链接缓存失败: {e}")

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        exit(num)

    def get_recommended_note_links(self, scroll_times: int = 5):
        """
        Collect note links from the recommend feed.
        Scroll multiple times to load more, until enough un-commented links are found or max scrolls reached.
        Returns a dict: {url: title}
        """
        self.logger.info(f"[{self.class_name}] get_recommended_note_links...")

        self.driver.get("https://www.jianshu.com/techareas/backend")

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div.itemlist-box")
                )
            )
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 页面初始内容加载失败: {e}")
            return {}

        self.sleep_random(base=1.0, jitter=1.0)

        hrefs = dict()
        last_height = 0

        max_scroll = scroll_times
        collected = 0
        max_needed = 100  # 至少获取100条未评论链接再退出

        for i in range(max_scroll):
            self.logger.info(f"[{self.class_name}] 第 {i+1} 次滚动加载")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.sleep_random(base=1.0, jitter=2.0)

            a_tags = self.driver.find_elements(By.CSS_SELECTOR, "div.itemlist-box div.content > a.title")
            self.logger.info(f"[{self.class_name}] 当前抓取 div.itemlist-box div.content > a.title 数量: {len(a_tags)}")
            if not a_tags:
                continue

            # 导出 HTML 逻辑
            # if a_tags:
            #     try:
            #         with open("debug_link_element.html", "w", encoding="utf-8") as f:
            #             f.write(self.driver.execute_script("return arguments[0].outerHTML;", a_tags[0]))
            #     except Exception:
            #         pass

            for a_tag in a_tags:
                try:
                    href = a_tag.get_attribute("href") or ""
                    title = a_tag.get_attribute("title") or a_tag.text.strip() or ""

                    if not href or not title:
                        self.logger.debug(f"[{self.class_name}] href 或 title 为空，跳过元素: {a_tag.get_attribute('outerHTML')}")
                        continue

                    if href.startswith("/"):
                        href = urllib.parse.urljoin("https://www.jianshu.com", href)

                    if not href.startswith("http"):
                        self.logger.warning(f"[{self.class_name}] 非标准链接跳过: {href}")
                        continue

                    if self.comment_db.has_commented(href, Platform.JIANSHU):
                        self.logger.warning(f"[{self.class_name}] 已评论过，跳过链接: {href}")
                        continue

                    if href not in hrefs:
                        hrefs[href] = title
                        collected += 1
                        self.logger.info(f"[{self.class_name}] 抓取链接: {href} 标题: {title}")
                except Exception as e:
                    self.logger.warning(f"[{self.class_name}] 解析 a_tag 元素失败: {e}")

            if collected >= max_needed:
                self.logger.info(f"[{self.class_name}] 已获取到 {collected} 条未评论链接，提前结束滚动")
                break

            try:
                new_height = self.driver.execute_script("return document.body.scrollHeight;")
                if new_height == last_height:
                    break
                last_height = new_height
            except Exception:
                break

        self.logger.info(f"[{self.class_name}] 共获取到 {len(hrefs)} 条链接，其中包含标题信息")
        return hrefs


if __name__ == "__main__":
    print("[JianshuBot] started...")
    for _ in range(3):
        bot = JianshuBot()
        bot.run()
    print("[JianshuBot] ended...")
