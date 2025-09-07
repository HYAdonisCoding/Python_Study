import os
import random
import time
import json
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from comment_db import CommentDB, Platform
from BaseBot import BaseBot

limitation = 100


# 模拟自动评论的主类
class BilibiliBot(BaseBot):

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "log")
        data_dir = os.path.join(base_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)  # 确保data目录存在
        comment_path = os.path.join(data_dir, "comments.json")

        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)

        super().__init__(
            log_dir=log_dir,
            comment_path=comment_path,
            home_url="https://www.bilibili.com",
        )

        self.comment_db = CommentDB()
        self.cookie_path = os.path.join(data_dir, f"{self.class_name}_cookies.json")
        self.cache_path = os.path.join(data_dir, f"{self.class_name}_cached_hrefs.json")
        self.comment_count_path = os.path.join(log_dir, "comment_count_daily.json")

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
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        # 反检测设置
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )
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
                    self.sleep_random(base=1.0, jitter=2.0)
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

        headless_options = webdriver.ChromeOptions()
        # headless_options.add_argument("--disable-gpu")
        headless_options.add_argument("--no-sandbox")
        headless_options.add_argument("--window-size=1920,1080")
        # 反检测设置
        headless_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        headless_options.add_experimental_option("useAutomationExtension", False)
        # headless_options.add_argument("--headless=new")  # 注释掉无头参数
        # 下载与当前 Chrome 版本对应的 ChromeDriver
        service = Service(ChromeDriverManager(version=self.chrome_version()).install())

        self.driver = webdriver.Chrome(service=service, options=headless_options)

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
                self.sleep_random(base=1.0, jitter=delay)
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
                    self.sleep_random(base=1.0, jitter=2.0)
                    continue
            self.logger.info("[BilibiliBot] 开始评价...")
            self.comment_on_note_links(hrefs)

            sleep_time = max(1, interval + random.uniform(-1, 3))
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            self.sleep_random(base=1.0, jitter=sleep_time)

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
            tqdm(note_links.items(), desc=f"[{self.class_name}]评论进度", unit="条"), 1
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
                self.sleep_random(base=1.0, jitter=2.0)
                # 滚动页面确保评论区加载
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                self.sleep_random(base=1.0, jitter=2.0)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                self.sleep_random(base=1.0, jitter=2.0)

                comment = self.remove_non_bmp(self.get_random_comment())
                success = self.comment_on_note(self.driver, comment, logger=self.logger)
                if not success:
                    self.logger.info(f"[BilibiliBot] 评论失败，跳过：{url}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info("[BilibiliBot] 连续失败 3 次，程序退出")
                        self.exit(1)
                        return
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
                self.save_comment_count()
                self.logger.info(
                    f"[JuejinBot] {self.today} 累计评论：{self.comment_count}"
                )
                if self.comment_count >= limitation:
                    self.logger.info(
                        f"[BilibiliBot] 今日评论已达 {limitation} 条，程序退出"
                    )
                    self.exit(0)
                    return
                self.sleep_random(base=1.0, jitter=2.0)
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
                    return

    def exit(self, num=0):
        if self.driver:
            self.driver.quit()
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
        self.sleep_random(base=1.0, jitter=2.0)

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
            self.sleep_random(base=1.0, jitter=2.0)

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
            self.sleep_random(base=1.0, jitter=1.0)
        self.logger.warning(
            f"[ShadowDom] Timeout locating nested shadow element: {selectors}"
        )
        return None

    # 新增独立函数
    def comment_on_note(self, driver, comment_text, logger=None):
        """
        在 B 站视频页面评论框写入内容并发布，增强稳定性，确保获取 Shadow DOM 元素。
        """
        def log(msg):
            if logger:
                logger.info(msg)
            else:
                print(msg)

        log("🔍 开始评论流程...")

        # 滚动到底部触发评论区加载
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 使用 JS 获取 Shadow DOM 内部元素
        input_box = None
        for _ in range(15):  # 最大尝试 15 次
            try:
                input_box = driver.execute_script("""
                const rich = document.querySelector('bili-comment-rich-textarea');
                if (!rich || !rich.shadowRoot) return null;
                const editable = rich.shadowRoot.querySelector('[contenteditable="true"]');
                return editable || null;
                """)
                if input_box:
                    break
            except Exception:
                pass
            time.sleep(0.5)

        if not input_box:
            log("❌ 未找到评论输入框")
            return False

        log("✅ 找到评论输入框，写入内容...")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", input_box)
        time.sleep(random.uniform(0.5, 1.0))

        # 写入评论并触发事件
        driver.execute_script("""
        const el = arguments[0];
        const text = arguments[1];
        el.focus();
        el.innerText = text;
        el.dispatchEvent(new InputEvent('input', {bubbles:true, cancelable:true, data:text}));
        el.dispatchEvent(new KeyboardEvent('keydown', {bubbles:true, cancelable:true, key:'a'}));
        el.dispatchEvent(new KeyboardEvent('keyup', {bubbles:true, cancelable:true, key:'a'}));
        el.blur();
        """, input_box, comment_text)

        log("✅ 评论内容已写入，尝试点击发布按钮...")

        # 获取并点击发布按钮
        btn = None
        for _ in range(10):  # 最大重试 10 次
            try:
                btn = driver.execute_script("""
                const box = document.querySelector('bili-comments-bottom-fixed-wrapper')
                            ?.querySelector('bili-comment-box');
                if (!box) return null;
                const b = Array.from(box.querySelectorAll('button.active'))
                            .find(btn => btn.textContent.includes('发布'));
                return b || null;
                """)
                if btn:
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.3)
                    driver.execute_script("arguments[0].click();", btn)
                    log("✅ 评论发布成功")
                    return True
            except Exception:
                pass
            time.sleep(0.5)

        log("❌ 未找到发布按钮或点击失败")
        return False

    def get_bilibili_comment_input(self, driver, timeout=10):
        """
        返回 B 站评论区的 contenteditable 输入框（shadow DOM 内部）。
        会自动：
        1. 滚动评论区，触发懒加载
        2. 等待元素挂载
        3. 处理 Shadow DOM
        """
        # 滚动页面到评论区域
        driver.execute_script("document.querySelector('#body').scrollIntoView(true);")
        time.sleep(0.5)  # 等待渲染

        textarea = None
        end_time = time.time() + timeout
        while time.time() < end_time:
            # 尝试获取外层 <bili-comment-rich-textarea>
            rich = driver.execute_script(
                "return document.querySelector('bili-comment-rich-textarea')"
            )
            if rich:
                # 点击一次，触发内部 shadow DOM 挂载
                driver.execute_script("arguments[0].click();", rich)
                time.sleep(0.5)

                # 尝试获取 shadowRoot 内部 contenteditable
                textarea = driver.execute_script(
                    """
                    let rich = document.querySelector('bili-comment-rich-textarea');
                    if (!rich || !rich.shadowRoot) return null;
                    return rich.shadowRoot.querySelector('[contenteditable="true"]');
                """
                )
                if textarea:
                    break

            time.sleep(0.5)

        return textarea  # 找不到返回 None

    def set_bilibili_comment_text(self, driver, comment_text, logger=None):
        """
        在 B 站评论框写入内容，并触发 input 事件，让发布按钮点亮
        """
        input_box = self.get_bilibili_comment_input(driver)
        if not input_box:
            if logger:
                logger.info("❌ 找不到评论输入框内部的 contenteditable")
            else:
                print("❌ 找不到评论输入框内部的 contenteditable")
            return False

        # 用 JS 写入内容 + 触发 input 事件
        driver.execute_script(
            """
            const el = arguments[0];
            const text = arguments[1];
            el.innerText = text;
            el.dispatchEvent(new InputEvent('input', {
                bubbles: true,
                cancelable: true,
                inputType: 'insertText',
                data: text
            }));
        """,
            input_box,
            comment_text,
        )

        if logger:
            logger.info("✅ 评论内容已写入")
        else:
            print("✅ 评论内容已写入")

        return True

    def get_nested_shadow_element(
        self, driver, selectors, timeout=10, sleep_interval=0.3
    ):
        """
        通用 Shadow DOM 查找函数
        selectors: 列表，例如 ["bili-comments", "bili-comment-box", "bili-comment-rich-textarea", '[contenteditable="true"]']
        """
        import time

        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                el = driver.execute_script(
                    "return document.querySelector(arguments[0])", selectors[0]
                )
                for sel in selectors[1:]:
                    if not el:
                        break
                    el = driver.execute_script(
                        "return arguments[0].shadowRoot?.querySelector(arguments[1])",
                        el,
                        sel,
                    )
                if el:
                    return el
            except Exception:
                pass
            time.sleep(sleep_interval)
        return None

    def click_bilibili_publish_button(self, driver, logger=None):
        """
        尝试在 B 站评论区点击“发布”按钮
        """
        try:
            # 跨越 Shadow DOM 直接查找按钮
            btn = driver.execute_script(
                """
                let comments = document.querySelector("bili-comments");
                if (!comments) return null;
                let box = comments.shadowRoot.querySelector("bili-comment-box");
                if (!box) return null;
                return box.shadowRoot.querySelector("button.active");
            """
            )

            if not btn:
                if logger:
                    logger.debug("❌ 未找到发布按钮 (button.active)")
                else:
                    print("❌ 未找到发布按钮 (button.active)")
                return False

            # 确认按钮文本，避免误点其他按钮
            text = driver.execute_script("return arguments[0].innerText.trim()", btn)
            if text != "发布":
                if logger:
                    logger.debug(f"❌ 找到按钮但文本不是 '发布'，而是: {text}")
                else:
                    print(f"❌ 找到按钮但文本不是 '发布'，而是: {text}")
                return False

            # 使用 JS click，绕过 shadow dom 的点击问题
            driver.execute_script("arguments[0].click();", btn)

            if logger:
                logger.info("✅ 评论发布成功")
            else:
                print("✅ 评论发布成功")
            return True

        except Exception as e:
            if logger:
                logger.error(f"点击发布按钮时异常: {e}")
            else:
                print(f"点击发布按钮时异常: {e}")
            return False


if __name__ == "__main__":
    print("[BilibiliBot] started...")
    bot = None
    try:
        bot = BilibiliBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n[BilibiliBot] 收到中断信号，正在退出...")
    finally:
        if bot and bot.comment_db:
            try:
                bot.comment_db.close()
                print("[BilibiliBot] comment_db 连接已关闭")
            except Exception as e:
                print(f"[BilibiliBot] 关闭 comment_db 失败: {e}")
        print("[BilibiliBot] ended...")
