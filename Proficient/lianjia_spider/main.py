#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 第四篇
# massage......

import time
from spider import DianpingSpider
from storage import SpiderDB

if __name__ == "__main__":
    spider = DianpingSpider()
    db = SpiderDB()

    start_page = db.get_last_page() or 1
    print(f"从第 {start_page} 页开始爬取...")

    try:
        for page in range(start_page, 51):
            print(f"正在爬取第 {page} 页...")
            shops = spider.fetch_page(page)
            db.save_shops(shops)
            db.update_last_page(page)
            time.sleep(5)
    except KeyboardInterrupt:
        print("用户中断，已保存进度。")
    finally:
        spider.close()
        print("爬取结束。")

