import os
import random
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# 模拟自动评论的主类
class RainBot:
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
        return "".join(c for c in text if ord(c) <= 0xFFFF)

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

    def login_weibo(self):
        self.driver.get("https://weibo.com/login.php")
        input("[RainBot] 请手动登录微博并完成验证后按回车...")

    def get_random_comment(self):
        return random.choice(self.comments)

    def post_comment(self, comment):
        print(comment)
        # 示例帖子链接，请替换为目标帖子的 URL
        target_post_url = "https://weibo.com/hot/weibo/1028032088"
        self.driver.get(target_post_url)
        time.sleep(5)

        try:
            comment_buttons = self.driver.find_elements(
                By.XPATH,
                '//div[contains(@class, "toolbar_wrap_np6Ug") and .//i[@title="评论"]]',
            )

            random.shuffle(comment_buttons)
            for comment_button in comment_buttons[: random.randint(1, 2)]:
                try:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                        comment_button,
                    )
                    time.sleep(0.5)
                    try:
                        comment_button.click()
                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].click();", comment_button
                        )
                    time.sleep(1)

                    # 1. 等待弹出层中的评论输入框出现
                    comment_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "comment-textarea"))
                    )

                    comment_input.clear()

                    ActionChains(self.driver).move_to_element(
                        comment_input
                    ).click().perform()
                    comment = self.remove_non_bmp(comment)
                    for c in comment:
                        comment_input.send_keys(c)
                        time.sleep(
                            random.uniform(0.05, 0.15)
                        )  # simulate human typing speed

                    # 3. 等按钮变为可用状态
                    submit_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//button[not(@disabled)]//span[contains(text(),'评论')]/..",
                            )
                        )
                    )

                    try:
                        submit_button.click()

                        # 尝试等待浮层提示框的出现，最多等5秒
                        try:
                            toast_element = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((
                                    By.XPATH,
                                    "//div[contains(@class, 'toast') or contains(@class, 'woo-toast') or contains(@class, 'layer')]"
                                ))
                            )
                            toast_text = toast_element.text.strip()
                            if any(keyword in toast_text for keyword in ["操作频繁", "请稍后再试", "发送失败"]):
                                self.logger.info(f"[RainBot] 检测到浮层提示：{toast_text}，评论未成功")
                                self.failed_comment_count += 1
                                if self.failed_comment_count >= 3:
                                    self.logger.info("[RainBot] 当前评论已连续失败 3 次，程序即将退出。")
                                    if self.driver:
                                        self.driver.quit()
                                    exit(1)
                        except Exception:
                            # 没有检测到提示，可能成功
                            pass

                        time.sleep(2)  # 等待可能的提示弹窗出现

                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].click();", submit_button
                        )
                    self.logger.info(f"[RainBot] 已发送评论：{comment}")
                    self.comment_count += 1
                    self.failed_comment_count = 0
                    self.comment_count_data[self.today] = self.comment_count
                    with open(self.comment_count_path, "w", encoding="utf-8") as f:
                        json.dump(
                            self.comment_count_data, f, ensure_ascii=False, indent=2
                        )
                    self.count_logger.info(
                        f"{self.today} 累计评论：{self.comment_count}"
                    )
                    time.sleep(random.uniform(3, 6))

                    # 尝试再次点击 comment_button 收起评论框
                    try:
                        if comment_button.is_displayed():
                            self.driver.execute_script(
                                "arguments[0].scrollIntoView(true);", comment_button
                            )
                            time.sleep(0.5)
                            comment_button.click()
                    except Exception as close_err:
                        self.logger.info("[RainBot] 收起评论框失败，忽略继续")
                    # 向下滚动页面，继续查找更多评论按钮
                    scroll_offset = random.randint(300, 800)
                    self.driver.execute_script(f"window.scrollBy(0, {scroll_offset});")
                    time.sleep(random.uniform(1, 2.5))
                except Exception as e_inner:
                    self.logger.info(f"[RainBot] 当前评论失败: {e_inner}")
                    self.failed_comment_count += 1
                    if self.failed_comment_count >= 3:
                        self.logger.info(
                            "[RainBot] 当前评论已连续失败 3 次，程序即将退出。"
                        )
                        if self.driver:
                            self.driver.quit()
                        exit(1)
        except Exception as e:
            self.logger.info(f"[RainBot] 发送评论失败: {e}")

    def run(self, interval=30):
        self.setup_browser()
        self.login_weibo()
        while True:
            comment = self.get_random_comment()
            self.post_comment(comment)
            self.logger.info("[RainBot] 等待下一次发送...")
            self.driver.refresh()
            sleep_time = interval + random.uniform(-10, 15)
            self.logger.info(f"下轮将在 {int(sleep_time)} 秒后继续...")
            time.sleep(sleep_time)


if __name__ == "__main__":
    print("[RainBot] started...")
    bot = RainBot()
    bot.run()
    print("[RainBot] ended...")
