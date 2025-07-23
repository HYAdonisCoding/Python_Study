from enum import Enum
import os
import sqlite3
import time
from typing import Set

class Platform(str, Enum):
    BILIBILI = "bilibili"
    XHS = "xhs"
    JUEJIN = "juejin"

class CommentDB:
    def __init__(self, db_path=None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "comments.db")
        self.conn = sqlite3.connect(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                platform TEXT,
                url TEXT PRIMARY KEY,
                title TEXT,
                comment TEXT,
                commented_at TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def record_comment(self, platform: Platform, url: str, title: str, comment: str, status: str = "success"):
        commented_at = time.strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute("""
            REPLACE INTO comments (platform, url, title, comment, commented_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (platform.value, url, title, comment, commented_at, status))
        self.conn.commit()

    def get_commented_urls(self, platform: Platform) -> Set[str]:
        cur = self.conn.cursor()
        cur.execute("SELECT url FROM comments WHERE platform=? AND status='success'", (platform.value,))
        return set(row[0] for row in cur.fetchall())

    def close(self):
        self.conn.close()