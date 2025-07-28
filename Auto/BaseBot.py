


import os
import json
import random
import time
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BaseBot:
    def __init__(self, log_dir, comment_path, home_url):
        self.home_url = home_url
        self.class_name = self.__class__.__name__
        self.today = time.strftime("%Y-%m-%d")

        # 日志设置
        log_path = os.path.join(log_dir, "rainbot.log")
        self._setup_logger(log_path)

        # 评论计数文件
        self.comment_count_path = os.path.join(log_dir, "comment_count_daily.json")
        if os.path.exists(self.comment_count_path):
            with open(self.comment_count_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = {}
        self.comment_count = all_data.get(self.class_name, {}).get(self.today, 0)
        self.comment_count_data = all_data

        # 加载评论语料
        try:
            with open(comment_path, "r", encoding="utf-8") as f:
                self.comments = json.load(f)
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 加载评论语料失败：{e}")
            self.comments = ["有趣", "赞", "支持一下", "感谢分享"]

    def get_random_comment(self):
        return random.choice(self.comments)

    def update_comment_count(self):
        if self.class_name not in self.comment_count_data:
            self.comment_count_data[self.class_name] = {}
        self.comment_count_data[self.class_name][self.today] = self.comment_count
        with open(self.comment_count_path, "w", encoding="utf-8") as f:
            json.dump(self.comment_count_data, f, ensure_ascii=False, indent=2)

    def load_cookies(self, driver, cookie_path):
        if os.path.exists(cookie_path):
            try:
                with open(cookie_path, "r", encoding="utf-8") as f:
                    cookies = json.load(f)
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                self.logger.info(f"[{self.class_name}] 成功加载 cookies")
            except Exception as e:
                self.logger.warning(f"[{self.class_name}] 加载 cookies 失败：{e}")
        else:
            self.logger.info(f"[{self.class_name}] 未找到 cookie 文件，跳过加载")

    def save_cookies(self, driver, cookie_path):
        try:
            cookies = driver.get_cookies()
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            self.logger.info(f"[{self.class_name}] 成功保存 cookies")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 保存 cookies 失败：{e}")

    def load_cache(self, cache_path):
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"[{self.class_name}] 加载缓存失败：{e}")
        return {}

    def save_cache(self, cache_path, cache_data):
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"[{self.class_name}] 已保存缓存，共 {len(cache_data)} 条链接")
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 保存缓存失败：{e}")


    def try_with_retry(self, func, retries=3, delay=1.5):
        for i in range(retries):
            try:
                return func()
            except Exception as e:
                self.logger.warning(f"[{self.class_name}] 第 {i+1} 次尝试失败：{e}")
                time.sleep(delay)
        self.logger.error(f"[{self.class_name}] 所有重试失败")
        return None

    def wait_for_element(self, driver, by, value, timeout=15):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            self.logger.warning(f"[{self.class_name}] 等待元素超时：{value}")
            return None

    def sleep_random(self, base=1.0, jitter=0.8):
        t = base + random.uniform(0, jitter)
        self.logger.debug(f"[{self.class_name}] 随机休眠 {t:.2f} 秒")
        time.sleep(t)


    def is_logged_in(self, driver, check_func):
        try:
            return check_func(driver)
        except Exception as e:
            self.logger.warning(f"[{self.class_name}] 登录状态检查出错：{e}")
            return False

    def ensure_login(self, driver, cookie_path, check_func):
        driver.get(self.home_url)  # 加载平台首页，确保 driver 初始化
        self.load_cookies(driver, cookie_path)
        driver.refresh()
        self.sleep_random()
        if self.is_logged_in(driver, check_func):
            self.logger.info(f"[{self.class_name}] 已登录")
        else:
            self.logger.info(f"[{self.class_name}] 未登录，请手动操作登录")
            input(f"完成登录后按回车继续：")
            self.save_cookies(driver, cookie_path)
    def _setup_logger(self, log_path):
        logger = logging.getLogger(self.class_name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        if not logger.handlers:
            # File handler: INFO 及以上写入文件
            fh = logging.FileHandler(log_path, encoding="utf-8")
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            # Stream handler: ERROR 及以上输出到终端
            sh = logging.StreamHandler()
            sh.setLevel(logging.ERROR)
            sh.setFormatter(formatter)
            logger.addHandler(sh)

        self.logger = logger
    # BaseBot 中添加
    def login(self):
        raise NotImplementedError("请在子类中实现 login() 方法")