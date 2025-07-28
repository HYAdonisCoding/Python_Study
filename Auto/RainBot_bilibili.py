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
class BilibiliBot:

    def __init__(self):
        # 初始化 CommentDB
        self.comment_db = CommentDB()
        bot_id = self.__class__.__name__
        self.class_name = bot_id
        # 在本文件夹下的json文件
        base_dir = os.path.dirname(os.path.abspath(__file__))
        comment_path = os.path.join(base_dir, "comments.json")
        with open(comment_path, "r", encoding="utf-8") as f:
            self.comments = json.load(f)

        self.cookie_path = os.path.join(base_dir, f"{bot_id}_cookies.json")

        log_dir = os.path.join(base_dir, "log")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "rainbot.log")

        # 缓存路径
        self.cache_path = os.path.join(base_dir, f"{bot_id}_cached_hrefs.json")

        # 设置全局 root logger，并绑定到文件
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            force=True,  # 强制覆盖其他 logging 设置
        )
        self.logger = logging.getLogger()

        # 持久化每日评论计数
        self.comment_count_path = os.path.join(log_dir, f"comment_count_daily.json")
        self.today = time.strftime("%Y-%m-%d")
        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = {}

        self.comment_count = all_data.get(self.class_name, {}).get(self.today, 0)
        self.comment_count_data = all_data

        self.driver = None
        self.failed_comment_count = 0

    def remove_non_bmp(self, text):
        # return "".join(c for c in text if ord(c) <= 0xFFFF)
        return text

    def setup_browser(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        # 反检测设置
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=chrome_options)
        # 隐藏 webdriver 标识
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "*.jpg",
                    "*.jpeg",
                    "*.png",
                    "*.webp",
                    "*.gif",
                    "*.mp4",
                    "*.m4s",
                    "*.flv",
                    "*.woff",
                    "*.ttf",
                ]
            },
        )

    def login_bilibili(self):
        self.logger.info("[BilibiliBot] 打开B站登录页...")
        self.driver.get("https://www.bilibili.com/")
        # 如已有cookie文件，尝试加载并登录
        if os.path.exists(self.cookie_path):
            with open(self.cookie_path, "r", encoding="utf-8") as f:
                try:
                    cookies = json.load(f)
                    for cookie in cookies:
                        if "sameSite" in cookie and cookie["sameSite"] == "None":
                            cookie["sameSite"] = "Strict"
                        self.driver.add_cookie(cookie)
                    self.driver.refresh()
                    time.sleep(2)
                    self.logger.info("[BilibiliBot] 已加载本地cookie，尝试免登录")
                    return
                except Exception as e:
                    self.logger.warning(
                        f"[BilibiliBot] 加载cookie失败，转为手动登录：{e}"
                    )
        input("[BilibiliBot] 请手动登录B站并完成验证后按回车...")
        self.logger.info("[BilibiliBot] 登录成功，继续执行")

        # 登录完成后关闭当前窗口，重新初始化浏览器为“伪无头”模式
        cookies = self.driver.get_cookies()
        # 保存cookie到文件
        with open(self.cookie_path, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        self.driver.quit()

        headless_options = Options()
        headless_options.add_argument("--disable-gpu")
        headless_options.add_argument("--no-sandbox")
        headless_options.add_argument("--window-size=1920,1080")
        # 反检测设置
        headless_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        headless_options.add_experimental_option("useAutomationExtension", False)
        # headless_options.add_argument("--headless=new")  # 注释掉无头参数

        self.driver = webdriver.Chrome(options=headless_options)
        # 隐藏 webdriver 标识
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )
        self.driver.get("https://www.bilibili.com/")
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.minimize_window()  # 添加此行
        self.logger.info("[BilibiliBot] 已切换为伪无头模式浏览器")
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "*.jpg",
                    "*.jpeg",
                    "*.png",
                    "*.webp",
                    "*.gif",
                    "*.mp4",
                    "*.m4s",
                    "*.flv",
                    "*.woff",
                    "*.ttf",
                ]
            },
        )

    def try_with_retry(self, func, retries=3, delay=1):
        for _ in range(retries):
            try:
                return func()
            except Exception:
                time.sleep(delay)
        return None

    def wait_for_shadow_element(self, outer_selector, inner_selector, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script(
                f"""
                const el = document.querySelector('{outer_selector}');
                return el && el.shadowRoot && el.shadowRoot.querySelector('{inner_selector}');
            """
            )
        )
        return self.driver.execute_script(
            f"""
            return document.querySelector('{outer_selector}').shadowRoot.querySelector('{inner_selector}');
        """
        )

    def get_random_comment(self):
        return random.choice(self.comments)

    def run(self, interval=30):
        self.setup_browser()
        self.login_bilibili()

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
                self.logger.warning("[BilibiliBot] 缓存为空或无效，重新获取链接中...")
                hrefs = self.get_recommended_video_links()
                if hrefs:
                    with open(self.cache_path, "w", encoding="utf-8") as f:
                        json.dump(hrefs, f, ensure_ascii=False, indent=2)
                else:
                    self.logger.error("[BilibiliBot] 未获取到视频链接，等待重试...")
                    time.sleep(10)
                    continue
            self.logger.info("[BilibiliBot] 开始评价...")
            self.comment_on_note_links(hrefs)

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            time.sleep(sleep_time)

    def get_shadow_element(self, host_selector, shadow_selector, timeout=10):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        host = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, host_selector))
        )
        shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", host)
        el = WebDriverWait(self.driver, timeout).until(
            lambda d: self.driver.execute_script(
                "return arguments[0].querySelector(arguments[1])",
                shadow_root,
                shadow_selector,
            )
        )
        return el

    def comment_on_note_links(self, note_links):
        """
        Visit each note URL, open the comment box, type a random comment, and send.
        Uses unified comment_on_note function for commenting.
        """
        base = "https://www.zhihu.com"
        for idx, (orig_url, title) in enumerate(
            tqdm(note_links.items(), desc="评论进度"), 1
        ):
            self.logger.info(
                f"[BilibiliBot] 正在评论第 {idx}/{len(note_links)} 条（标题：{title}）..."
            )
            # Normalize URL (some feeds return relative URLs)
            url = orig_url
            if url and url.startswith("/"):
                url = urllib.parse.urljoin(base, url)
            try:
                self.logger.info(f"[BilibiliBot] 打开笔记：{url}")
                self.driver.get(url)
                url = self.driver.current_url
                # 等待页面加载
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                WebDriverWait(self.driver, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
                # 检测是否被踢回登录页
                cur = self.driver.current_url
                if "login" in cur or "account" in cur:
                    self.logger.error(
                        f"[BilibiliBot] 页面跳到登录「{cur}」，跳过：{url}"
                    )
                    # 移除cookie
                    self.driver.delete_all_cookies()
                    self.save_cookies([])
                    # 清除浏览器缓存
                    self.driver.execute_cdp_cmd("Network.clearBrowserCache", {})
                    self.logger.info("[BilibiliBot] 清除浏览器缓存")

                    # 尝试重新登录
                    self.login_bilibili()
                time.sleep(random.uniform(0.5, 1.0))
                # 滚动页面确保评论区加载
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(random.uniform(0.5, 1.5))
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(random.uniform(0.5, 1.5))

                comment = self.remove_non_bmp(self.get_random_comment())
                success = comment_on_note(self.driver, comment, logger=self.logger)
                if not success:
                    self.logger.info(f"[BilibiliBot] 评论失败，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[BilibiliBot] 连续失败 3 次，程序退出")
                        self.exit(1)
                    continue
                self.logger.info(f"[BilibiliBot] 已评论 {comment}   链接：{url}")
                self.comment_db.record_comment(
                    platform=Platform.BILIBILI,
                    url=orig_url,
                    title=title,
                    comment=comment,
                    status="success",
                )
                self.comment_count += 1
                self.failed_comment_count = 0
                self.comment_count_data.setdefault(self.class_name, {})[
                    self.today
                ] = self.comment_count
                with open(self.comment_count_path, "w", encoding="utf-8") as f:
                    json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)
                self.logger.info(
                    f"[JuejinBot] {self.today} 累计评论：{self.comment_count}"
                )
                if self.comment_count >= limitation:
                    self.logger.info(
                        f"[BilibiliBot] 今日评论已达 {limitation} 条，程序退出"
                    )
                    self.exit(0)
                time.sleep(random.uniform(1.0, 2.0))
                # 移除已评论链接并写回缓存
                if os.path.exists(self.cache_path):
                    try:
                        with open(self.cache_path, "r", encoding="utf-8") as f:
                            current_cache = json.load(f)
                        if url in current_cache:
                            del current_cache[url]
                        if orig_url in current_cache:
                            del current_cache[orig_url]
                        with open(self.cache_path, "w", encoding="utf-8") as f:
                            json.dump(current_cache, f, ensure_ascii=False, indent=2)
                    except Exception as e:
                        self.logger.warning(f"[BilibiliBot] 更新缓存文件失败：{e}")
            except Exception as e:
                self.logger.info(f"[BilibiliBot] 评论链接失败: {url}，错误：{e}")
                self.failed_comment_count += 1
                if self.failed_comment_count >= 3:
                    self.logger.info("[BilibiliBot] 连续失败 3 次，程序退出")
                    self.exit(1)

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
        if hasattr(self, "db"):
            self.comment_db.close()
        exit(num)

    def get_recommended_video_links(self, scroll_times: int = 5):
        """
        Collect video links from the B站推荐页.
        Scroll multiple times to load more.
        Returns a dict: {url: title}
        """
        self.logger.info("[BilibiliBot] get_recommended_video_links...")

        self.driver.get("https://www.bilibili.com/c/tech/?spm_id_from=333.1007.0.0")

        # 等初次加载
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(3)

        hrefs = dict()
        last_height = 0
        for i in range(scroll_times):
            # 新的推荐视频卡片选择器逻辑
            all_cards = self.driver.find_elements(
                By.CSS_SELECTOR, "div.head-cards > div.feed-card"
            )
            items = all_cards[1:] if len(all_cards) > 1 else []
            for card in items:
                try:
                    a_tag = card.find_element(By.CSS_SELECTOR, "a.bili-cover-card")
                    title_tag = card.find_element(
                        By.CSS_SELECTOR, "div.bili-video-card__title a"
                    )
                    href = a_tag.get_attribute("href") or ""
                    title = title_tag.get_attribute("title") or title_tag.text or ""
                    if href and title:
                        hrefs[href] = title
                        self.logger.info(
                            f"[BilibiliBot] 抓取链接: {href} 标题: {title}"
                        )
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

        self.logger.info(
            f"[BilibiliBot] 共获取到 {len(hrefs)} 条链接，其中包含标题信息"
        )
        # 过滤已评论链接
        commented = self.comment_db.get_commented_urls(Platform.BILIBILI)
        hrefs = {url: title for url, title in hrefs.items() if url not in commented}
        return hrefs

    def get_nested_shadow_element(self, selectors: list, timeout=15):
        """
        获取嵌套 shadow dom 元素
        """
        import time

        js = """
        const findInShadow = (selectors) => {
            let el = document.querySelector(selectors[0]);
            for (let i = 1; i < selectors.length; i++) {
                if (!el) return null;
                if (el.shadowRoot) {
                    el = el.shadowRoot.querySelector(selectors[i]);
                } else {
                    return null;
                }
            }
            return el;
        };
        return findInShadow(arguments[0]);
        """
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                el = self.driver.execute_script(js, selectors)
                if el:
                    self.logger.debug(f"[ShadowDom] 成功获取 shadow 元素：{selectors}")
                    return el
            except Exception as e:
                self.logger.debug(f"[ShadowDom] 获取失败：{e}")
            time.sleep(0.5)
        self.logger.warning(
            f"[ShadowDom] Timeout locating nested shadow element: {selectors}"
        )
        return None


# 新增独立函数
def comment_on_note(driver, comment_text, logger=None):
    from selenium.common.exceptions import WebDriverException
    import time

    def log(msg):
        if logger:
            logger.info(msg)
        else:
            print(msg)

    def get_nested_shadow_element(driver, selectors):
        element = driver.execute_script(
            f"return document.querySelector('{selectors[0]}')"
        )
        for selector in selectors[1:]:
            if element is None:
                return None
            element = driver.execute_script(
                "return arguments[0].shadowRoot?.querySelector(arguments[1])",
                element,
                selector,
            )
        return element

    try:
        log("🔍 正在查找评论输入框...")
        input_box = get_nested_shadow_element(
            driver,
            [
                "bili-comments",
                "bili-comment-box",
                "bili-comment-rich-textarea",
                'div[contenteditable="true"]',
            ],
        )
        if not input_box:
            log("❌ 未找到评论输入框，跳过")
            return False

        log("✅ 找到评论输入框，输入内容中...")
        driver.execute_script("arguments[0].scrollIntoView(true);", input_box)
        time.sleep(0.5)

        try:
            input_box.click()
        except Exception:
            if logger:
                logger.debug("fallback to JS focus")
            else:
                print("fallback to JS focus")
            driver.execute_script("arguments[0].focus();", input_box)

        try:
            input_box.send_keys(comment_text)
        except Exception:
            if logger:
                logger.debug("fallback to JS set innerText")
            else:
                print("fallback to JS set innerText")
            driver.execute_script(
                "arguments[0].innerText = arguments[1];", input_box, comment_text
            )
        time.sleep(1)  # 等待触发 footer 显示

        log("🔍 正在查找发布按钮...")
        time.sleep(1)  # 等待 footer 激活
        footer = get_nested_shadow_element(
            driver, ["bili-comments", "bili-comment-box", "#footer"]
        )
        if not footer:
            log("❌ 未找到 footer")
            return False

        buttons = driver.execute_script(
            "return arguments[0].querySelectorAll('button.active')", footer
        )
        for btn in buttons:
            if (
                driver.execute_script("return arguments[0].textContent", btn).strip()
                == "发布"
            ):
                log("✅ 点击发布按钮")
                btn.click()
                time.sleep(1)
                log("✅ 评论发布成功")
                return True

        log("❌ 未找到发布按钮")
        return False

    except WebDriverException as e:
        log(f"❌ 异常中断: {e}")
        return False


if __name__ == "__main__":
    print("[BilibiliBot] started...")
    bot = BilibiliBot()
    bot.run()
    print("[BilibiliBot] ended...")
