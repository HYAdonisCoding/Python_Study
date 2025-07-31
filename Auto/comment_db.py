from enum import Enum
import os
import sqlite3
import time
from typing import Set


class Platform(str, Enum):
    BILIBILI = "bilibili"
    XHS = "xhs"
    JUEJIN = "juejin"
    ZHIHU = "zhihu"
    JIANSHU = "jianshu"


class CommentDB:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)  # 确保data目录存在
            db_path = os.path.join(data_dir, "comments.db")
        self.conn = sqlite3.connect(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                platform TEXT,
                url TEXT PRIMARY KEY,
                title TEXT,
                comment TEXT,
                commented_at TEXT,
                status TEXT
            )
        """
        )
        self.conn.commit()

    def record_comment(
        self,
        platform: Platform,
        url: str,
        title: str,
        comment: str,
        status: str = "success",
    ):
        commented_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            """
            REPLACE INTO comments (platform, url, title, comment, commented_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (platform.value, url, title, comment, commented_at, status),
        )
        self.conn.commit()

    def get_commented_urls(self, platform: Platform) -> Set[str]:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT url FROM comments WHERE platform=? AND status='success'",
            (platform.value,),
        )
        return set(row[0] for row in cur.fetchall())

    def has_commented(self, url: str, platform: Platform) -> bool:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT 1 FROM comments WHERE url=? AND platform=? AND status='success' LIMIT 1",
            (url, platform.value),
        )
        return cur.fetchone() is not None
    def get_commented_urls_batch(self, hrefs: list[str], platform: str) -> list[str]:
        if not hrefs:
            return []

        placeholder = ",".join(["?"] * len(hrefs))
        query = f"SELECT url FROM comments WHERE url IN ({placeholder}) AND platform = ?"
        rows = self.conn.execute(query, (*hrefs, platform)).fetchall()
        return [row[0] for row in rows]  # ✅ 改这里，访问 tuple 的第一个元素
    def close(self):
        self.conn.close()

    def import_commented_urls_from_json(self, platform: Platform, json_path: str):
        import json
        from datetime import datetime

        path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(path, json_path)
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON 文件不存在：{json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            urls = json.load(f)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for url in urls:
            try:
                self.conn.execute(
                    """
                    INSERT INTO comments (platform, url, title, comment, commented_at, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO UPDATE SET
                        platform=excluded.platform,
                        title=excluded.title,
                        comment=excluded.comment,
                        commented_at=excluded.commented_at,
                        status=excluded.status
                    """,
                    (platform.value, url, "", "", now, "success"),
                )
                print(f"[✓] 插入成功: {url}")
            except Exception as e:
                print(f"[✗] 插入失败: {url}, 错误: {e}")

        self.conn.commit()


if __name__ == "__main__":
    db = CommentDB()
    db.import_commented_urls_from_json(Platform.XHS, "log/commented_notes.json")
