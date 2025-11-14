#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
"""
Database schema and storage logic for Dianping spider.

Table:
 - shops: stores combined basic and detailed shop information.

Fields:

shops:
 - data_shopid (TEXT, PRIMARY KEY): Shop identifier.
 - shop_name (TEXT): Shop name.
 - recommend_dishes (TEXT): Recommended dishes, comma-separated.
 - shop_link (TEXT): URL to the shop's page.
 - star_score (REAL): Average star rating.
 - score_text (TEXT): JSON or text of detailed scores.
 - price (TEXT): Average price per person (raw text).
 - region (TEXT): Shop region.
 - category (TEXT): Shop category.
 - desc_addr_txt (TEXT): Address description.
 - reviews (INTEGER): Total number of reviews.
 - address (TEXT): Detailed address.
 - biz_time (TEXT): Business hours.
 - updated_at (TEXT): Last update timestamp, stored as ISO-8601 timestamp in UTC+08:00 when written by the application.

This module includes:
 - SQLite storage with unified shops table supporting both list and detail data saving.
 - Progress tracking for crawl state.
 - Test routine demonstrating database operations.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "dianping.db")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

CREATE_SHOP_TABLE = """
CREATE TABLE IF NOT EXISTS shops (
    data_shopid TEXT PRIMARY KEY,
    shop_name TEXT,
    recommend_dishes TEXT,
    shop_link TEXT,
    star_score REAL,
    score_text TEXT,
    price TEXT,
    region TEXT,
    category TEXT,
    desc_addr_txt TEXT,
    reviews INTEGER,
    address TEXT,
    biz_time TEXT,
    updated_at TEXT DEFAULT (datetime(CURRENT_TIMESTAMP, '+8 hours'))
);
"""



CREATE_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY,
    key_name TEXT UNIQUE,
    value TEXT
);
"""

class SpiderDB:
    """Manages SQLite database connection and operations for spider data."""

    def __init__(self, db_path=DB_PATH):
        """Initialize database connection and prepare tables."""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.create_tables()

    def create_tables(self):
        """Create necessary tables if they do not exist."""
        cur = self.conn.cursor()
        cur.execute(CREATE_SHOP_TABLE)
        cur.execute(CREATE_PROGRESS_TABLE)
        self.conn.commit()

    def save_shop_basic(self, shops):
        """保存列表页基础信息（含更新时间），若已存在则更新"""
        cur = self.conn.cursor()
        local_tz = timezone(timedelta(hours=8))
        local_time = datetime.now(local_tz).isoformat(timespec='seconds')

        for s in shops:
            cur.execute("""
                INSERT INTO shops (data_shopid, shop_name, recommend_dishes, shop_link, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(data_shopid) DO UPDATE SET
                    shop_name = excluded.shop_name,
                    recommend_dishes = excluded.recommend_dishes,
                    shop_link = excluded.shop_link,
                    updated_at = excluded.updated_at
            """, (
                s["data_shopid"],
                s["shop_name"],
                s.get("recommend_dishes"),
                s["shop_link"],
                local_time
            ))
        self.conn.commit()

    def save_shop_detail(self, detail):
        """更新详情页信息"""
        cur = self.conn.cursor()
        local_tz = timezone(timedelta(hours=8))
        local_time = datetime.now(local_tz).isoformat(timespec='seconds')

        cur.execute("""
            UPDATE shops SET
                shop_name = COALESCE(?, shop_name),
                star_score = ?,
                score_text = ?,
                price = ?,
                region = ?,
                category = ?,
                desc_addr_txt = ?,
                reviews = ?,
                address = ?,
                biz_time = ?,
                updated_at = ?
            WHERE data_shopid = ?
        """, (
            detail.get("shop_name"),
            detail.get("star_score"),
            json.dumps(detail.get("score_text"), ensure_ascii=False) if detail.get("score_text") else None,
            detail.get("price"),
            detail.get("region"),
            detail.get("category"),
            detail.get("desc_addr_txt"),
            detail.get("reviews"),
            detail.get("address"),
            detail.get("biz_time"),
            local_time,
            detail["data_shopid"]
        ))
        self.conn.commit()

    def set_progress(self, value, key='last_page'):
        """
        Record or update crawl progress state.

        Args:
            key (str): Progress key name.
            value (str): Progress value.
        """
        cur = self.conn.cursor()
        cur.execute("INSERT INTO progress(key_name, value) VALUES (?, ?) ON CONFLICT(key_name) DO UPDATE SET value=excluded.value;", (key, str(value)))
        self.conn.commit()

    def get_progress(self, key='last_page'):
        """
        Retrieve the stored progress value for a given key.

        Args:
            key (str): Progress key name.

        Returns:
            str or None: Stored progress value or None if not found.
        """
        row = self.conn.execute("SELECT value FROM progress WHERE key_name=?", (key,)).fetchone()
        return row[0] if row else None

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def fix_legacy_timestamps(self):
        """
        (Optional) Shift legacy UTC timestamps stored in `updated_at` to UTC+8.
        Run this manually if you know your existing rows were recorded in UTC and
        you want to convert them to Beijing time.
        """
        cur = self.conn.cursor()
        # This will convert rows where updated_at is a SQLite datetime string (UTC)
        # to UTC+8 by applying +8 hours. Use with caution (don't run twice).
        cur.execute("UPDATE shops SET updated_at = datetime(updated_at, '+8 hours') WHERE updated_at IS NOT NULL;")
        self.conn.commit()
    def increment_progress(self, key):
        value = self.get_progress(key) or 0
        self.set_progress(int(value)+1, key=key)



    def convert_row(self, updated_at):
        # 如果是 None、空、或者已经包含时区(+ 或 Z)，跳过
        if not updated_at:
            return None
        if '+' in updated_at or 'Z' in updated_at:
            return None
        # 兼容 'YYYY-MM-DD HH:MM:SS' 和 'YYYY-MM-DDTHH:MM:SS'
        s = updated_at.replace('T', ' ')
        try:
            # 解析为“UTC 的天真时间”
            dt = datetime.fromisoformat(s)
        except Exception:
            try:
                dt = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return None
        # 视作 UTC，转为 +08:00 并返回 ISO 字符串
        dt_utc = dt.replace(tzinfo=timezone.utc)
        beijing = dt_utc.astimezone(timezone(timedelta(hours=8)))
        return beijing.isoformat(timespec='seconds')



def test_db_operations():
    """Test database insertions and progress tracking."""
    db = SpiderDB()
    sample_shops = [{'data_shopid': 'G9B5lBAWimhGRPnh', 'shop_name': '北京宜宾招待所(南翠花街店)', 'recommend_dishes': '红糖冰粉, 粉蒸肉, 宜宾燃抄手', 'shop_link': 'https://www.dianping.com/shop/G9B5lBAWimhGRPnh'}, {'data_shopid': 'l5jXXDwnM5PbZB93', 'shop_name': '百花人家(门城水岸店)', 'recommend_dishes': '火盆石磨豆腐, 烤羊肉串, 大厨功夫鱼', 'shop_link': 'https://www.dianping.com/shop/l5jXXDwnM5PbZB93'}, {'data_shopid': 'H3SyNUSShP5BYm87', 'shop_name': '逗思都吃韩国料理(五道口店)', 'recommend_dishes': '自制金枪鱼饭团, 奶酪辣鸡, 部队火锅', 'shop_link': 'https://www.dianping.com/shop/H3SyNUSShP5BYm87'}, {'data_shopid': 'k6ASsfEU2GWeDmTk', 'shop_name': '浩海火烧云傣家菜(京广店)', 'recommend_dishes': '油焖鸡, 黑三剁, 小锅米线', 'shop_link': 'https://www.dianping.com/shop/k6ASsfEU2GWeDmTk'}, {'data_shopid': 'l7TjgjzVZS6j8830', 'shop_name': '南门涮肉(国贸商城店)', 'recommend_dishes': '麻酱小料, 自制烧饼, 鲜羊肉', 'shop_link': 'https://www.dianping.com/shop/l7TjgjzVZS6j8830'}, {'data_shopid': 'l4RMiRJoi6FBJ4v4', 'shop_name': '铃木食堂(杨梅竹店)', 'recommend_dishes': '日式牛肉火锅, 杏仁豆腐, 铃木肉饼', 'shop_link': 'https://www.dianping.com/shop/l4RMiRJoi6FBJ4v4'}, {'data_shopid': 'l3AK2xTtKoddz7SD', 'shop_name': '四季民福烤鸭店(东四十条店)', 'recommend_dishes': '酥香嫩烤鸭, 贝勒烤肉, 巧拌豆苗', 'shop_link': 'https://www.dianping.com/shop/l3AK2xTtKoddz7SD'}, {'data_shopid': 'j6rTOedDbGNsLVFd', 'shop_name': 'Bada kitchen 和风洋食(中关村店)', 'recommend_dishes': '嫩滑蛋包咖喱饭, 猪肉奶酪紫苏卷, 奶酪厚蛋烧', 'shop_link': 'https://www.dianping.com/shop/j6rTOedDbGNsLVFd'}, {'data_shopid': 'kaXGb95W714S3AK8', 'shop_name': '九本居酒屋(亚运村店)', 'recommend_dishes': '厚切三文鱼, 极上炭烤鳗鱼, 海胆酱焗牛油梨', 'shop_link': 'https://www.dianping.com/shop/kaXGb95W714S3AK8'}, {'data_shopid': 'G9VwkrHORDQkQMpr', 'shop_name': '胖妹面庄(香饵胡同店)', 'recommend_dishes': '豌杂面, 狼牙土豆, 经典混合面', 'shop_link': 'https://www.dianping.com/shop/G9VwkrHORDQkQMpr'}, {'data_shopid': 'G3ZxMJTDLITGsxLX', 'shop_name': '南门涮肉(东单店)', 'recommend_dishes': '小料双拼, 自制烧饼, 糖蒜', 'shop_link': 'https://www.dianping.com/shop/G3ZxMJTDLITGsxLX'}, {'data_shopid': 'FUs9OoiuF7Ey68y1', 'shop_name': '福和小馆(顺义店)', 'recommend_dishes': '侉炖千岛湖鱼头泡饼, 薄脆锅贴, 乾隆白菜', 'shop_link': 'https://www.dianping.com/shop/FUs9OoiuF7Ey68y1'}, {'data_shopid': 'FPcwD2D5x1QfVFoQ', 'shop_name': '金悦•梦华录(金融街购物中心店)', 'recommend_dishes': '家嫂姜葱熘牛展, 鲜虾龙皇饺, 铁镬脆皮蚝仔烙煎', 'shop_link': 'https://www.dianping.com/shop/FPcwD2D5x1QfVFoQ'}, {'data_shopid': 'G5leUTaSm4qGOalp', 'shop_name': '淮扬府(安定门店)', 'recommend_dishes': '招牌茨菇红烧肉, 响油鳝糊, 淮扬鸡汤大煮干丝', 'shop_link': 'https://www.dianping.com/shop/G5leUTaSm4qGOalp'}, {'data_shopid': 'G42raZgZrwxB69Oj', 'shop_name': '京兆尹(雍和宫店)', 'recommend_dishes': '糖醋藕排, 金刚沙豆腐, 桃胶珍菌卤味饭', 'shop_link': 'https://www.dianping.com/shop/G42raZgZrwxB69Oj'}]
    # db.save_shop_basic(sample_shops)

    sample_detail = {'data_shopid': 'l5jXXDwnM5PbZB93', 'shop_name': '百花人家(门城水岸店)', 'star_score': '4.7', 'score_text': '口味:4.7 环境:4.7 服务:4.7', 'price': '¥93/人', 'region': '门头沟城区', 'category': '农家菜', 'desc_addr_txt': '', 'address': '西六环与永堤西路交叉口南100米路东', 'reviews': 14901, 'biz_time': '11:00开始营业'}
    db.save_shop_detail(sample_detail)
    db.set_progress("last_page", 1)
    print("progress", db.get_progress("last_page"))
    db.close()


if __name__ == '__main__':
    print("Start testing DB schema and save logic")
    test_db_operations()
    print("Finished")
