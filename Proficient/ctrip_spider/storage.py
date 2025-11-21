#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8


import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone

from parser import BASE_DIR

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "dianping.db")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

CREATE_SHOP_TABLE = """
CREATE TABLE IF NOT EXISTS travels (
    travel_id TEXT PRIMARY KEY,                   -- 游记ID（唯一）
    tags TEXT,                                    -- 标签列表，JSON 字符串
    cover_image TEXT,                             -- 封面图片 URL
    cover_id TEXT,                                -- 图片 ID
    cover_link TEXT,                              -- 封面跳转链接
    city_name TEXT,                               -- 城市名
    city_link TEXT,                               -- 城市链接
    title TEXT,                                   -- 游记标题
    article_link TEXT,                            -- 游记详情页链接
    views INTEGER,                                -- 浏览量
    likes INTEGER,                                -- 喜欢数
    replies INTEGER,                              -- 回复数

    author_name TEXT,                             -- 作者姓名
    author_link TEXT,                             -- 作者主页链接
    author_avatar TEXT,                           -- 作者头像 URL

    publish_date TEXT,                            -- 发布时间（ISO 字符串）
    
    -- 以下为详情页新增内容
    days INTEGER,                                 -- 旅行天数
    month TEXT,                                   -- 月份（例如“12”）
    person_cost INTEGER,                          -- 人均费用
    companions TEXT,                              -- 和谁同行（如“和朋友”）
    play TEXT,                                    -- 玩法（如“美食,摄影”）
    places TEXT,                                  -- 作者去过的地点 JSON 数组
    content TEXT,                                 -- 正文内容（纯文本）
    type INTEGER,                                  -- 类型 1推荐 2最新 100头条
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

    def save_travel_basic(self, travels, type):
        """
        批量保存 travels 表基础信息（含更新时间），若已存在则更新。
        travels: List[dict]，每个 dict 包含 travels 表的字段。
        字段严格映射如下：
            - travel_id <- travelId
            - tags <- tags (JSON 序列化)
            - cover_image <- coverImage
            - cover_id <- coverId
            - cover_link <- coverLink / articleLink（优先 coverLink）
            - city_name <- cityName
            - city_link <- cityLink
            - title <- title
            - article_link <- articleLink
            - views <- views
            - likes <- likes
            - replies <- replies
            - author_name <- authorName
            - author_link <- authorLink
            - author_avatar <- authorAvatar
            - publish_date <- publishDate
        """
        try:
            cur = self.conn.cursor()
            local_tz = timezone(timedelta(hours=8))
            local_time = datetime.now(local_tz).isoformat(timespec='seconds')

            values = []
            for t in travels:
                # 字段映射
                travel_id = t.get("travelId")
                tags = t.get("tags", [])
                tags_json = json.dumps(tags, ensure_ascii=False) if tags is not None else None
                cover_image = t.get("coverImage")
                cover_id = t.get("coverId")
                # cover_link 优先 coverLink, 否则 articleLink
                cover_link = t.get("coverLink") or t.get("articleLink")
                city_name = t.get("cityName")
                city_link = t.get("cityLink")
                title = t.get("title")
                article_link = t.get("articleLink")
                views = t.get("views")
                likes = t.get("likes")
                replies = t.get("replies")
                author_name = t.get("authorName")
                author_link = t.get("authorLink")
                author_avatar = t.get("authorAvatar")
                publish_date = t.get("publishDate")

                # 打印调试信息
                # print("[save_travel_basic] travel_id:", travel_id)
                # print("  tags:", tags_json)
                # print("  cover_image:", cover_image)
                # print("  cover_id:", cover_id)
                # print("  cover_link:", cover_link)
                # print("  city_name:", city_name)
                # print("  city_link:", city_link)
                # print("  title:", title)
                # print("  article_link:", article_link)
                # print("  views:", views)
                # print("  likes:", likes)
                # print("  replies:", replies)
                # print("  author_name:", author_name)
                # print("  author_link:", author_link)
                # print("  author_avatar:", author_avatar)
                # print("  publish_date:", publish_date)
                # print("  updated_at:", local_time)

                values.append((
                    travel_id,
                    tags_json,
                    cover_image,
                    cover_id,
                    cover_link,
                    city_name,
                    city_link,
                    title,
                    article_link,
                    views,
                    likes,
                    replies,
                    author_name,
                    author_link,
                    author_avatar,
                    publish_date,
                    local_time,
                    type
                ))

            cur.executemany("""
                INSERT INTO travels (
                    travel_id, tags, cover_image, cover_id, cover_link, city_name, city_link, title,
                    article_link, views, likes, replies, author_name, author_link, author_avatar,
                    publish_date, updated_at, type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(travel_id) DO UPDATE SET
                    tags=excluded.tags,
                    cover_image=excluded.cover_image,
                    cover_id=excluded.cover_id,
                    cover_link=excluded.cover_link,
                    city_name=excluded.city_name,
                    city_link=excluded.city_link,
                    title=excluded.title,
                    article_link=excluded.article_link,
                    views=excluded.views,
                    likes=excluded.likes,
                    replies=excluded.replies,
                    author_name=excluded.author_name,
                    author_link=excluded.author_link,
                    author_avatar=excluded.author_avatar,
                    publish_date=excluded.publish_date,
                    updated_at=excluded.updated_at,
                    type=excluded.type
            """, values)
            self.conn.commit()
        except Exception as e:
            print(f"[save_travel_basic] Error: {e}")

    def save_travel_detail(self, detail):
        """
        保存游记详情信息到 travels 表。
        detail: dict，由 parse_travel 返回，必须包含 travel_id。
        """
        travel_id = detail.get("like_id")
        if not travel_id:
            raise ValueError("detail 必须包含 travel_id 字段")

        sql = """
        INSERT INTO travels (
            travel_id, days, month, person_cost, companions, play,
            places, content, publish_date, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime(CURRENT_TIMESTAMP, '+8 hours'))
        ON CONFLICT(travel_id) DO UPDATE SET
            days = excluded.days,
            month = excluded.month,
            person_cost = excluded.person_cost,
            companions = excluded.companions,
            play = excluded.play,
            places = excluded.places,
            content = excluded.content,
            publish_date = excluded.publish_date,
            updated_at = datetime(CURRENT_TIMESTAMP, '+8 hours');
        """

        self.conn.execute(sql, (
            travel_id,
            detail.get("days"),
            detail.get("month"),
            detail.get("person_cost"),
            detail.get("companions"),
            detail.get("play"),
            json.dumps(detail.get("places", []), ensure_ascii=False),
            detail.get("content"),
            detail.get("publish_time"),
        ))
        self.conn.commit()

    def set_progress(self, value, type=-1, key='last_page'):
        """
        Record or update crawl progress state.

        Args:
            key (str): Progress key name.
            value (str): Progress value.
        """
        cur = self.conn.cursor()
        if type==-1:
            cur.execute(
                "INSERT INTO progress(key_name, value) VALUES (?, ?) "
                "ON CONFLICT(key_name) DO UPDATE SET value=excluded.value;",
                (f"{key}", str(value))
            )
        else:
            cur.execute(
                "INSERT INTO progress(key_name, value) VALUES (?, ?) "
                "ON CONFLICT(key_name) DO UPDATE SET value=excluded.value;",
                (f"{key}_{type}", str(value))
            )
        self.conn.commit()

    def get_progress(self, type=-1, key='last_page'):
        """
        Retrieve the stored progress value for a given key.

        Args:
            key (str): Progress key name.

        Returns:
            str or None: Stored progress value or None if not found.
        """
        if type==-1:
            row = self.conn.execute("SELECT value FROM progress WHERE key_name=?", (f"{key}",)).fetchone()
        else:
            row = self.conn.execute("SELECT value FROM progress WHERE key_name=?", (f"{key}_{type}",)).fetchone()
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
        value = self.get_progress(key=key) or 0
        self.set_progress(int(value)+1, type=-1, key=key)



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

    # 把数据导出为txt
    def export_shops_to_txt(self, file_path="shops_export.txt"):
        """
        Export all shop records to a TXT file, comma-separated.

        Args:
            file_path (str): Path to the output TXT file.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM shops")
        rows = cur.fetchall()
        # 获取字段名
        columns = [desc[0] for desc in cur.description]

        with open(file_path, "w", encoding="utf-8") as f:
            # 写表头（可选）
            f.write(",".join(columns) + "\n")
            for row in rows:
                row_str = []
                for col in row:
                    if col is None:
                        row_str.append("")  # 空值处理
                        continue
                    
                    col_str = str(col)
                    # 如果包含逗号或换行符，替换成顿号
                    if ',' in col_str or '\n' in col_str or '\r' in col_str:
                        col_str = col_str.replace(',', '、').replace('\n', ' ').replace('\r', ' ')
                    
                    row_str.append(col_str)
                
                # 用顿号分隔每个字段写入文件
                f.write(", ".join(row_str) + "\n")

        print(f"Exported {len(rows)} shops to {file_path}")

def test_db_operations():
    """Test database insertions and progress tracking."""
    db = SpiderDB()
    sample_travels = [{'travelId': '3990253', 'tags': ['头条', '精华'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0105y120008crbslg56DD_R_228_10000_Q90.jpg', 'coverId': '509095992', 'coverLink': '/travels/sanya61/3990253.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '海岛之冬，和闺蜜的三亚之旅', 'articleLink': '/travels/sanya61/3990253.html', 'views': '16556', 'likes': '96', 'replies': '29', 'authorName': '阿拖拖晓君', 'authorLink': '/members/639FFB8ED39F4BF7874FFA698BC7D725/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z81r120008ehsou035F6_R_180_180.jpg', 'publishDate': '2020-12-30'}, {'travelId': '3990248', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0106y120008cqy78tDC4C_R_228_10000_Q90.jpg', 'coverId': '509064369', 'coverLink': '/travels/nanjing9/3990248.html', 'cityName': '南京', 'cityLink': '/place/nanjing9.html', 'title': '金陵城市度假好去处，入住南京弘阳酒店，畅玩10万㎡室内外主题乐园', 'articleLink': '/travels/nanjing9/3990248.html', 'views': '73090', 'likes': '30', 'replies': '7', 'authorName': '潘昶永', 'authorLink': '/members/12C9A7996B07408294FCA97288298FF0/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/headphoto/921/477/570/fc290a517430444ba2a661ad82fdc158_R_180_180.jpg', 'publishDate': '2020-12-30'}, {'travelId': '3990329', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0106n120008cqzo5c2D31.gif', 'coverId': '509067284', 'coverLink': '/travels/fuzhou164/3990329.html', 'cityName': '福州', 'cityLink': '/place/fuzhou164.html', 'title': '元旦假期福州周边好去处，来这里圆你一个童话梦', 'articleLink': '/travels/fuzhou164/3990329.html', 'views': '22772', 'likes': '63', 'replies': '19', 'authorName': 'Chen浩文', 'authorLink': '/members/7BF857242EAE4B82AFC1ABCEE0F2971F/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/fd/headphoto/g2/M07/44/19/CghzgVSS6BOAUa6HAAEHat8lBLk630_R_180_180.jpg', 'publishDate': '2020-12-30'}, {'travelId': '3990315', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0101f120008cqgyj938D4_R_228_10000_Q90.jpg', 'coverId': '509027610', 'coverLink': '/travels/lijiang32/3990315.html', 'cityName': '丽江', 'cityLink': '/place/lijiang32.html', 'title': '遇见丽江，遇见不一样的美，看尽不一样的风景', 'articleLink': '/travels/lijiang32/3990315.html', 'views': '9698', 'likes': '55', 'replies': '20', 'authorName': '阿鲁我的确', 'authorLink': '/members/43B8568E037B41258B6B99A4F79DD983/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80q14000000w3pk4025B_R_180_180.jpg', 'publishDate': '2020-12-30'}, {'travelId': '3990162', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102o120008cq1b8wA075_R_228_10000_Q90.jpg', 'coverId': '508938107', 'coverLink': '/travels/sanya61/3990162.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '五天四夜，怎么玩转三亚湾、亚龙湾？【三亚深度游】', 'articleLink': '/travels/sanya61/3990162.html', 'views': '147937', 'likes': '30', 'replies': '7', 'authorName': '奔跑的小东东', 'authorLink': '/members/CC04D144329342D0B37A219F4BCC67B7/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z830120008css4h4C747_R_180_180.jpg', 'publishDate': '2020-12-30'}, {'travelId': '3990223', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102a120008cpnoom7FDF_R_228_10000_Q90.jpg', 'coverId': '508881813', 'coverLink': '/travels/foshan207/3990223.html', 'cityName': '佛山', 'cityLink': '/place/foshan207.html', 'title': '佛山亲子游好去处，住海底酒店看野生动物，距离广州1小时车程', 'articleLink': '/travels/foshan207/3990223.html', 'views': '21101', 'likes': '66', 'replies': '17', 'authorName': '我就是大人', 'authorLink': '/members/07D2E99B0A584AEEABA97D19C3750D33/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z85l12000ehfn50tC488_R_180_180.jpg', 'publishDate': '2020-12-29'}, {'travelId': '3990302', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01049120008cpkc3j71D6_R_228_10000_Q90.jpg', 'coverId': '508887310', 'coverLink': '/travels/sanya61/3990302.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '自驾游三亚｜打卡三亚最美沿海公路共享美食盛宴', 'articleLink': '/travels/sanya61/3990302.html', 'views': '9351', 'likes': '55', 'replies': '17', 'authorName': '沐子酱', 'authorLink': '/members/EAB6F7C58A00487C989A86262619C781/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z862120008z419b91E5E_R_180_180.jpg', 'publishDate': '2020-12-29'}, {'travelId': '3990284', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0103c120008cp1nldBBC2_R_228_10000_Q90.png', 'coverId': '508821463', 'coverLink': '/travels/sanya61/3990284.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '美味三亚，请收下这份美食清单', 'articleLink': '/travels/sanya61/3990284.html', 'views': '63448', 'likes': '248', 'replies': '17', 'authorName': '小宇Sylvia', 'authorLink': '/members/4C0A3F654B114886B7266DFBEEF1696C/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/1h660120009g3x65dA57D_R_180_180.jpg', 'publishDate': '2020-12-29'}, {'travelId': '3990214', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0105m120008cp7crj8109_R_228_10000_Q90.jpg', 'coverId': '508835877', 'coverLink': '/travels/suzhou11/3990214.html', 'cityName': '苏州', 'cityLink': '/place/suzhou11.html', 'title': '2500年历史的吴文化碰撞福朋，读懂姑苏，爱上江南，吴中福朋喜来登刷新我对福朋的认知', 'articleLink': '/travels/suzhou11/3990214.html', 'views': '64680', 'likes': '100', 'replies': '25', 'authorName': '背包客紫漫', 'authorLink': '/members/623D0137B70C4E7F94BFBB3DE15C7227/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z83n120008h8ghnoE6E1_R_180_180.jpg', 'publishDate': '2020-12-29'}, {'travelId': '3990111', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01052120008cngi5f8F49_R_228_10000_Q90.jpg', 'coverId': '508725712', 'coverLink': '/travels/sanya61/3990111.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '三亚周游记，7日吃喝玩乐全攻略', 'articleLink': '/travels/sanya61/3990111.html', 'views': '13503', 'likes': '80', 'replies': '17', 'authorName': '樊凯凯凯子', 'authorLink': '/members/5FC4284699F74F8B9183E4461AB56827/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80w0v000000jy60s6951_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3990109', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0104b120008cnd06381DF_R_228_10000_Q90.jpg', 'coverId': '508722606', 'coverLink': '/travels/sanya61/3990109.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '与美食相逢，那些在三亚海边的味蕾故事', 'articleLink': '/travels/sanya61/3990109.html', 'views': '9035', 'likes': '73', 'replies': '17', 'authorName': '麻小薯', 'authorLink': '/members/5DFD38401826401997FE397BB96F3DE8/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z8070a0000004wvdz0956_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3990101', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0106q120008cmv0sx43F6_R_228_10000_Q90.jpg', 'coverId': '508712085', 'coverLink': '/travels/sanya61/3990101.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '带妈妈去三亚，带她看海陪她吃美食，一次旅行两种住宿体验', 'articleLink': '/travels/sanya61/3990101.html', 'views': '12848', 'likes': '69', 'replies': '17', 'authorName': '任紫玉Renziyu', 'authorLink': '/members/7B2022CA7A1B4ED689CE4ACD1D9D8448/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z84f1200091tgqgo601A_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3990089', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01038120008cmvbkh0204_R_228_10000_Q90.jpg', 'coverId': '508712200', 'coverLink': '/travels/sanya61/3990089.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '漫游“东方夏威夷”三亚 吃喝玩乐攻略', 'articleLink': '/travels/sanya61/3990089.html', 'views': '8046', 'likes': '61', 'replies': '25', 'authorName': '请叫我Summer', 'authorLink': '/members/E14226CAD8FD4D62B6D12360BD752199/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z80i12000atsn367E73B_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3989944', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01030120008cm7qij637A_R_228_10000_Q90.jpg', 'coverId': '508698737', 'coverLink': '/travels/haerbin151/3989944.html', 'cityName': '哈尔滨', 'cityLink': '/place/haerbin151.html', 'title': '冬游哈尔滨，感受不一样的冰雪之旅，附美食攻略', 'articleLink': '/travels/haerbin151/3989944.html', 'views': '53732', 'likes': '62', 'replies': '18', 'authorName': '乐玩日志', 'authorLink': '/members/0F5A6740976A4A19867EE7DABED0FD0E/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80g0u000000ix2wlFBF6_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3989943', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0104o120008cm7x5v5253_R_228_10000_Q90.jpg', 'coverId': '508699001', 'coverLink': '/travels/sanya61/3989943.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '生态与轻奢的碰撞，艺术与酒店的跨界，兼具颜值与内涵的秘密花园~', 'articleLink': '/travels/sanya61/3989943.html', 'views': '20167', 'likes': '65', 'replies': '18', 'authorName': '时代树暴走', 'authorLink': '/members/23447BFF117F45C7BC08F2AD69823F2E/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/fd/headphoto/g3/M00/9D/A0/CggYGlZdjoiATgL5AADB2bqtKwI360_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3989940', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01035120008cmmu8v3ABA_R_228_10000_Q90.jpg', 'coverId': '508707653', 'coverLink': '/travels/sanya61/3989940.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '第一次去三亚，你一定要知道的那些事', 'articleLink': '/travels/sanya61/3989940.html', 'views': '7449', 'likes': '77', 'replies': '17', 'authorName': '背包客紫漫', 'authorLink': '/members/623D0137B70C4E7F94BFBB3DE15C7227/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z83n120008h8ghnoE6E1_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3989937', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01034120008cm2cyyB6F5_R_228_10000_Q90.jpg', 'coverId': '508702602', 'coverLink': '/travels/sanya61/3989937.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '「三亚时光纪」南风过境，又是快乐的海岛时光（吃住行超详细）', 'articleLink': '/travels/sanya61/3989937.html', 'views': '3199', 'likes': '26', 'replies': '6', 'authorName': '林琛Live', 'authorLink': '/members/5BDE730976A84BE9A8D1D339273BCC06/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z80r120008apxqht6DDD_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3990007', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0106n120008cl7ziw9A13_R_228_10000_Q90.jpg', 'coverId': '508673261', 'coverLink': '/travels/changbaishan268/3990007.html', 'cityName': '长白山', 'cityLink': '/place/changbaishan268.html', 'title': '冬游长白山，跟冰天雪地来一场约会！（附详细攻略）', 'articleLink': '/travels/changbaishan268/3990007.html', 'views': '114629', 'likes': '105', 'replies': '35', 'authorName': '唐伯虎2012', 'authorLink': '/members/7332DDA6E2334EE29D692336B184E864/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80p0a0000004gcgj00DF_R_180_180.jpg', 'publishDate': '2020-12-28'}, {'travelId': '3989851', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01016120008ckjvohA0FE_R_228_10000_Q90.jpg', 'coverId': '508655809', 'coverLink': '/travels/changbaishan268/3989851.html', 'cityName': '长白山', 'cityLink': '/place/changbaishan268.html', 'title': '冬季滑雪度假首选：长白山天池脚下森林度假酒店，尽享法式浪漫假期', 'articleLink': '/travels/changbaishan268/3989851.html', 'views': '8818', 'likes': '68', 'replies': '17', 'authorName': '潘昶永', 'authorLink': '/members/12C9A7996B07408294FCA97288298FF0/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/headphoto/921/477/570/fc290a517430444ba2a661ad82fdc158_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989845', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0100p120008ckadxiFA73_R_228_10000_Q90.jpg', 'coverId': '508649383', 'coverLink': '/travels/macau39/3989845.html', 'cityName': '澳门', 'cityLink': '/place/macau39.html', 'title': '宝藏级澳门美狮美高梅 打卡范冰冰同款机位', 'articleLink': '/travels/macau39/3989845.html', 'views': '17882', 'likes': '58', 'replies': '20', 'authorName': '元气少女郭小敏', 'authorLink': '/members/41CC4E2C2F124917964E0CEF234C2F0A/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z84c120008fdrvnx217C_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989989', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01029120008ck0p4b6E8A_R_228_10000_Q90.jpg', 'coverId': '508643311', 'coverLink': '/travels/sanya61/3989989.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '新年去三亚赴一场温暖之约', 'articleLink': '/travels/sanya61/3989989.html', 'views': '7535', 'likes': '48', 'replies': '18', 'authorName': '请叫我Summer', 'authorLink': '/members/E14226CAD8FD4D62B6D12360BD752199/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z80i12000atsn367E73B_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989829', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0106e120008cjen383882_R_228_10000_Q90.jpg', 'coverId': '508632170', 'coverLink': '/travels/sanya61/3989829.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '三亚旅行｜周末惬意自驾打卡网红景点附美食攻略', 'articleLink': '/travels/sanya61/3989829.html', 'views': '40032', 'likes': '72', 'replies': '17', 'authorName': '晓Kathy', 'authorLink': '/members/47B3B8285B22412E994DEF4F2349CEBA/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z81w120009ndmhxx2E09_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989780', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102m120008cjedw908F1_R_228_10000_Q90.jpg', 'coverId': '508631510', 'coverLink': '/travels/sanya61/3989780.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '五天四晚人均1000三亚慢旅行，打卡小众网红点，不一样的海岛之旅', 'articleLink': '/travels/sanya61/3989780.html', 'views': '40118', 'likes': '55', 'replies': '17', 'authorName': 'Rikki大叔', 'authorLink': '/members/B583ED5CCD5042B3A4C5DF348E87E267/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/fd/headphoto/g3/M03/4D/6C/CggYGVX4O7CAdBIoAAB0GkhNOAA865_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989894', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0101z120008cjao9bA5F3_R_228_10000_Q90.jpg', 'coverId': '508628619', 'coverLink': '/travels/nanjing9/3989894.html', 'cityName': '南京', 'cityLink': '/place/nanjing9.html', 'title': '全新登场的苏宁钟山国际高尔夫酒店到底为何惊艳？跟着我一探究竟！', 'articleLink': '/travels/nanjing9/3989894.html', 'views': '32589', 'likes': '66', 'replies': '17', 'authorName': '潘昶永', 'authorLink': '/members/12C9A7996B07408294FCA97288298FF0/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/headphoto/921/477/570/fc290a517430444ba2a661ad82fdc158_R_180_180.jpg', 'publishDate': '2020-12-26'}, {'travelId': '3989893', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0105g120008cjuyiw1CA8_R_228_10000_Q90.jpg', 'coverId': '508640381', 'coverLink': '/travels/haikou37/3989893.html', 'cityName': '海口', 'cityLink': '/place/haikou37.html', 'title': '环岛自驾，去海南赴一个碧海蓝天', 'articleLink': '/travels/haikou37/3989893.html', 'views': '39485', 'likes': '104', 'replies': '19', 'authorName': 'Chen浩文', 'authorLink': '/members/7BF857242EAE4B82AFC1ABCEE0F2971F/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/fd/headphoto/g2/M07/44/19/CghzgVSS6BOAUa6HAAEHat8lBLk630_R_180_180.jpg', 'publishDate': '2020-12-27'}, {'travelId': '3989763', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/01066120008cyv13m0B9D_R_228_10000_Q90.jpg', 'coverId': '510025610', 'coverLink': '/travels/china110000/3989763.html', 'cityName': '中国', 'cityLink': '/place/china110000.html', 'title': '在寂静雪原 遇见雪花真实的形状', 'articleLink': '/travels/china110000/3989763.html', 'views': '11673', 'likes': '76', 'replies': '17', 'authorName': '花泽Ocean', 'authorLink': '/members/242330DA39604BCB83050038279C5289/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80613000000uro5jC31D_R_180_180.jpg', 'publishDate': '2021-01-02'}, {'travelId': '3989659', 'tags': ['头条', '精华'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0103f120008ciptti56B9_R_228_10000_Q90.jpg', 'coverId': '508612714', 'coverLink': '/travels/dali31/3989659.html', 'cityName': '大理白族自治州', 'cityLink': '/place/dali31.html', 'title': '走！一路向西，自驾去大理', 'articleLink': '/travels/dali31/3989659.html', 'views': '28000', 'likes': '76', 'replies': '45', 'authorName': '段小湃湃', 'authorLink': '/members/6FA6EC6378A64D3C8D79DFF7148CEAB8/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/Z80j1600000106uqb3ADE_R_180_180.jpg', 'publishDate': '2020-12-26'}, {'travelId': '3989668', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102p120008cilrec7A7A_R_228_10000_Q90.png', 'coverId': '508610110', 'coverLink': '/travels/dali31/3989668.html', 'cityName': '大理白族自治州', 'cityLink': '/place/dali31.html', 'title': '同全新数字高尔夫一起，去大理！', 'articleLink': '/travels/dali31/3989668.html', 'views': '7873', 'likes': '67', 'replies': '18', 'authorName': '小布行路上', 'authorLink': '/members/A7AE629E214D4D44B2984DACE3C8B498/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/fd/headphoto/g1/M0A/EF/FA/CghzfVUBSiGAcS0FAAq74m2_EeY053_R_180_180.jpg', 'publishDate': '2020-12-26'}, {'travelId': '3989660', 'tags': ['实用'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102u120008cidnaa75A8_R_228_10000_Q90.jpg', 'coverId': '508604714', 'coverLink': '/travels/chengdu104/3989660.html', 'cityName': '成都', 'cityLink': '/place/chengdu104.html', 'title': '宽窄巷子|周边拍照打卡秘籍', 'articleLink': '/travels/chengdu104/3989660.html', 'views': '7303', 'likes': '58', 'replies': '21', 'authorName': '在拍照的叁山', 'authorLink': '/members/C7AFCE1918564141A1649AACD65885F8/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z86t12000ap53ft09DAE_R_180_180.jpg', 'publishDate': '2020-12-26'}, {'travelId': '3989743', 'tags': ['美图'], 'coverImage': 'https://dimg04.c-ctrip.com/images/0102n120008ckjsky7991_R_228_10000_Q90.jpg', 'coverId': '508655645', 'coverLink': '/travels/sanya61/3989743.html', 'cityName': '三亚', 'cityLink': '/place/sanya61.html', 'title': '跨年去哪儿？去三亚，体会海子笔下的面朝大海，春暖花开', 'articleLink': '/travels/sanya61/3989743.html', 'views': '8225', 'likes': '57', 'replies': '17', 'authorName': '老虎的妹妹', 'authorLink': '/members/C7F0B88942EC44759AA2EAAE1AA8350F/journals', 'authorAvatar': 'https://dimg04.c-ctrip.com/images/0Z81912000eivdv9y110B_R_180_180.jpg', 'publishDate': '2020-12-27'}]
    db.save_travel_basic(sample_travels, type=1)

    sample_detail = {'like_id': '3990253', 'days': '5', 'month': '12', 'person_cost': '3000', 'companions': '和朋友', 'play': '美食，摄影', 'places': ['三亚', '蜈支洲岛', '西岛', '情人桥', '海棠湾', '亚龙湾', '第一市场', '大小洞天', '三亚河', '牛王岭', '过江龙索桥', '三亚湾', '椰梦长廊', '凤凰岛', '后海', '大东海', '小东海', '小月湾', '夜游三亚湾'], 'publish_time': '2020-12-30 14:43', 'content': '这是一段闺蜜两人的逛吃逛吃之旅，跟李飘相识还是通过凯凯，那会儿我们一起去 成都 ，正好把这个川妹子叫出来一块儿吃饭。聊起天来很舒服，让人觉得很值得交往，正巧她也非常喜欢藏区，也去过许多藏地，我向来对 西藏 比较熟悉的人都会有种莫名的亲切感。 后来几次我去藏地经过 成都 也都会喊她出来跟我一块儿吃饭喝酒，有一回住在太古里附近的民宿里，我们俩甚至看电影聊人生，彻夜长谈。2020年真的是一个特别的年份，一眨眼它竟然就结束了。\n我们原本约好的先去 腾冲 看银杏，临近出发前发现今年 腾冲 银杏黄得比较晚，我们索性更改目的地来到了暖冬 三亚 。 三亚 一直以来都是国内的热门目的地，特别是今年受疫情的影响，大家出不了国，想要看美丽的大海也就只能来 三亚 了。到过 三亚 大大小小的地儿了，蜈支洲岛、西岛也都去过了。正好李飘也是属于那种吃吃喝喝、不用拼了命打卡景点的玩法，所以我们最终的路线如下。\n五天的三亚路线\nDay1 泉州 - 三亚 -情人桥-萌哒哒椰子鸡-渔村四巷 Day2 三亚 湾-特兰蒂斯水族馆-海棠湾免税店-阿浪海鲜-亚龙湾 Day3 大 东海 -小 东海 -第一市场 Day4 大小洞天-夜游 三亚 湾 Day5 三亚 - 哈尔滨\n一、三亚河上的情人桥\n我和李飘约好的早上十点抵达 三亚 凤凰机场，会面以后租了个共享汽车来到了定好的酒店。卸下行李之后，我们直奔 三亚 情人桥。\n话说情人桥， 三亚 有好几座呢，包括我上次去的蜈支洲岛情人桥、西岛的牛王岭栈桥，还有没去过的非诚勿扰2里的亚龙湾森林公园的过江龙索桥……\n市区的这座步行桥，连接着 三亚 河河东和河西的 通道 ，它就像彩虹一样横跨在 三亚 河上，也有人称之为“彩虹桥”。来的时候天气不算好，我们在情人桥边走走逛逛，桥就像波浪一样，连绵起伏的，听说晚上亮灯的时候很美呢。\n逛着逛着，看到了路边有家萌哒哒椰子鸡，这可是早就在我的打卡清单上的一家店呢。第一顿饭，我们的选择就它了，萌哒哒椰子鸡，一家听起来就很萌的椰子鸡店。\n萌哒哒椰子鸡的整个就餐环境很有森林风，就仿佛置身于椰树林下，脚下的 文昌 鸡到处奔跑，仿佛还原了椰子鸡生活的画面。椰子鸡是 海南 十 大名 菜之首，总听说有椰汁的鸡肉吃不腻，我们也来试试？\n不能错过的花胶木瓜椰子鸡： 海南文昌 鸡的口感非常嫩滑，搭配三个椰子的椰汁以及木瓜、花胶、莲子、新鲜椰子肉和红枣枸杞做的汤底，还有海椰皇和五指山毛桃等多味珍贵食材，吃起来是既健康又美味。当鸡肉与椰汁充分融合后，一定要记得舀上一碗鸡汤喝，美味。\n入座以后服务员很热情，我们除了点一锅椰子鸡外，还点了藤桥炸排骨、麻辣土鸡脚以及 海南定安 猪肉粽，虽然是网红店，但幸好都没有踩雷，吃起来很满意。\n海南 香芋，这个香芋和我们在家里看到的不太一样，很绵，煮久一点，入口即化。野生竹荪是所有配菜里面最爱的了，竹荪口感柔柔嫩嫩的，有点小脆，蘸上萌哒哒家的服务员调配好的酱料，好吃极了。\n最后要推荐的它们家的藤桥炸排骨，远远就闻到了香炸的味儿，吃进嘴里不油不腻，酥脆，排骨的肉很香，忍不住多吃了几根。\n二、深夜寻觅渔村四巷的炸鸡块\n来 三亚 的这一天，巧的是和凯凯他们相差一天的时间，就一起约了一顿饭，吃完饭以后我囔囔着想要吃清补凉。恩铭干脆一不做二不休，我们再去找别的吃的。\n渔村四巷有一个陡坡真的是太好玩了，当你走在小巷子里，既要考虑到车够不够大，还得烦恼这坡上不上得去，特别考验技术，就很喜欢这种奇角旮旯的小地方，仿佛在这里更能看到最 三亚 的一面。\n夜已经很深了，可炸鸡店的人依然络绎不绝，老板顶着一个大肚子，腰间别着菜单和记账本，明眼一看就知道是个老板。\n我们是慕名而来，饿是不饿，就是想试试出了名的网红炸鸡，蘸料是酸甜酱，有点像我们闽南的甜辣酱。炸鸡趁热吃还是好吃的，外酥里嫩，哦，绝对是酒的绝配。听说他们家的海鲜粥也很棒，下次有机会再来尝试吧。\n三、漫步三亚湾，阳光沙滩\n我们就住在 三亚 湾上，下楼或者开窗就是海，冬天的海风还是有点儿大。住了几天，终于从阴天来到了晴天，我俩这几天都是睡到自然醒然后再来想一会儿干吗去。\n三亚 湾由于距离市区最近，海边人也是最多的，但值得欣慰的是整个 三亚 的海边都非常干净，几乎见不到一丝垃圾。\n三亚 湾绵延有22公里远，从机场南下不远就是 三亚 湾了，正好朝着西边的方向，是个看日落的好地方。椰梦长廊是 三亚 湾最出名的景点，这次来 三亚 也找到了一个特别的地方， 三亚 湾婚纱摄影基地，公交车站在“ 三亚 湾西段”下车即可。都是拍婚纱的新人，稍微排一下队，也是可以在这一片区域拍到非常美的照片。\n我和李飘常常在吃饱饭就来 三亚 湾的海边走走， 三亚 湾能提供游玩的还是比较少，适合游泳，会有一些人在海边卖游泳圈等一些游泳的必需品。就这样散步在沙滩上，累了在椰树下乘凉，不远处的凤凰岛就矗立在眼前。\n四、亚特兰蒂斯：失落的空间水族馆\n对亚特兰蒂斯水族馆最深的印象当属电视剧里那蓝蓝的背景，总给人浪漫和梦幻的感觉。忍不住想看来一眼，满足一下偶尔的少女心。\n当你进入水族馆，会先看到各式各样七彩的难得一见的鱼儿，还有晶莹剔透的不一样的水母。走过几个展馆，映入眼帘的就是大使环礁湖！长达16.5米高，蓄海水量13500吨的超大奇妙海底世界就在你眼前，让你瞬间进入了蓝色海洋的梦幻世界。\n二楼还有让人走不开脚步的珊瑚之海，活着的珊瑚随着水流摇摆，小丑鱼在期间游来游去，好不自在。\n亚特兰蒂斯是很有神话故事的一个种族，在 三亚 的亚特兰蒂斯就是以此为蓝本进行打造的一个海洋文化主题的目的地。亚特兰蒂斯的大使环礁湖在特定的时间段会有美人鱼表演，像美人鱼一样潜入水下世界，与自由自在的鱼儿融为一体，随着音乐的起伏带给我们不同的惊喜。\n小Tips：如果没有买门票，走进酒店大堂也是可以免费看到海洋世界的一面观赏幕墙，当然买了门票进去就能看到更多不一样的海底生物了。入住亚特兰蒂斯酒店的住客是可以不限次进入水族馆的。\n想要一场露天与音乐相伴，烧烤与啤酒在旁的晚餐吗？经过怀旧海鲜烧烤的露天区时，我已经被这里的环境深深吸引住了。傍晚时分，看着晚霞千变万化，和小姐妹两人喝杯啤酒，享受着耳边海风吹过，太舒服了。\n怀旧海鲜烧烤的环境真的太适合拍拍拍了，晚间的风轻轻地吹过，舞台上的歌手唱着歌，这样的环境底下吃饭简直不要更美好。\n两个人出门其实也挺好，至少吃烧烤的时候几乎很多种品类都能吃到，我们从海上的生蚝扇贝点到牛肉羊肉串，当然还有好吃的秋葵青椒等等蔬菜类的。\n大鱿鱼板：烤鱿鱼一直以来都是非常适合下酒的一道菜，烤的时候不能太焦也不能时间太短，恰到好处的烤鱿鱼板实在太好吃啦。\n珍珠小鱼干：一口啤酒一口小鱼干，太美味了。\n香烤鸡爪：烤得好吃的鸡爪总是叫人念念不忘。\n五、海棠湾免税店与阿浪海鲜\n看完亚特兰蒂斯的水族馆，当然免不了要来海棠湾的海边走走逛逛。海棠湾距离 三亚 市区最远，而且大部分都还是处于要通过酒店才能抵达的海滩，其余很多区域想要找到入 海口 还比较困难。相对而言，在海棠湾的海边，人数还是比较少的。\n海棠湾被开发出来的区域，酒店价格几乎都是五星标准也比较贵，看亚特兰蒂斯的架势就能看得出来，一个七星级的酒店是连直升飞机都有的。贫穷限制了我的想象。\n李飘是正儿八经 四川 人，总是跑 西藏川西 比较多，这还是她第一次来 三亚 呢。看到大海的时候激动得不行，我是从小看着海长大的孩子，索性来海边的沙滩椅上躺着看她欢乐也算足够了。\n这次因为时间不够，不然我每次来海棠湾都会去一个村子叫后海，那是 三亚 冲浪的著名所在地，当然也是很多文艺青年会呆着的地方。在后海渔村，住宿相对便宜些，也都是一线海景房，是个很不错的目的地。\n来 海南 ，自然免不了 三亚 免税店。免税店经营着国际一流品牌的化妆品、首饰、包包等等，特别是今年推出了 海南 贸易自由港，每个人每年的免税额度提升到了十万元，还以为受疫情影响大家口袋里都空空的，你来 三亚 免税店看下，东西仿佛都是不用钱的。\n不过要在 三亚 免税店买东西还是有一定的规矩要守的，一定要是离岛的人才能购买， 比如三亚 凤凰机场就是过完安检以后在机场隔离区指定的柜台进行领取你所购买的货品，这就需要你在购买东西的时候就出示有效身份证和已购买的离岛机票。 现在 三亚 免税店还有网上购买的商城，如果你跟我一样很懒得逛商场，那你也可以在网上一键购买下单，离岛的时候去提取就好了。记得要提前下单哦。\n逛完免税店，我和李飘往凤塘路走走，这是海鲜烧烤一条街，我们准备在这条街上觅食了。可以说阿浪海鲜是我这些天在 三亚 吃的最接地气的海鲜大排档了，虽然海鲜池不算大，但种类很多可以选择，而且他们家厨师做出来的海鲜味道特别赞，有几道菜是川味做法，很不错。这是一家 海南 人开了23年的老字号海鲜店，当然是不错的了。\n阿浪海鲜大部分都是在露天的环境，很喜欢这样的环境，在海边就应该是跟大自然亲近嘛。阿浪海鲜听说是与 三亚 当地的渔民合作的，所有海鲜都是渔民直供的野生海鲜，超赞。\n清蒸石斑鱼是我不得不推的一道菜，只要新鲜的石斑鱼，轻松地用锅炉一蒸，起锅后加上酱油、香葱和姜丝，锅中油烧热，浇上去，最美味也是最原始的口感立马就体现出来了。\n阿浪海鲜家的椰子饭，椰香十足，软糯香甜，忍不住多吃了两口。大龙虾大概是招牌菜，两个人一只蒜蓉开边大龙虾吃得太爽了，粉丝简直就是整道菜的精华。活鲍鱼搭配一丝丝蒜蓉一些些粉丝，蒸的时间正好，不能过老，鲜甜美味。\n饱食了一餐海鲜啊，太幸福了。\n六、亚龙湾\n海边的天气也是分分钟都在变，在海棠湾的时候天空还行。不过是坐了半小时公交车的功夫，来到了要能够弯，整个海滩就是阴沉沉的了。 如果天气好，亚龙湾是几 大湾 最美的，那海水就跟果冻一样一样的。亚龙湾在《 中国 国家地理》评选的 中国 最美八大海岸线，列居首位，可谓不虚此名。\n亚龙湾的海滩平缓开阔，脚下的沙粒洁白细软，海水清澈见底，在此可以放心地游泳。整个亚龙湾是一个月牙湾，也很适合进行水上运动。所以来到亚龙湾，更多的可能不是观光而是游玩。\n海上娱乐项目会有一个专门验票的码头，现在的 三亚 市场其实不算乱了，很多地方无论是吃海鲜还是游玩都是明码标价的，只要多长个心眼，正常也不会被坑了。\n亚龙湾的海边有许多沙滩椅，提供给游人们休息，有一些小商小贩会带着他们切好的新鲜水果、椰子走到人群中来售卖，真是哪里有人哪里就有买卖啊。\n七、大东海与小东海\n特地将大 东海 和小 东海 安排在一天，离得不是很远。小 东海 在鹿回头的山脚下，每次做功课的时候就是摸不清头脑到底在哪里，这次是特地跟着一个导航来的，导航的是小 东海 婚纱摄影基地。\n一直到了一个高尔夫球场的大门，我也还没看到这个摄影基地在哪里，问了保安让我闯过这片草地，沿着海边一直走就能看到了。前往摄影基地的小 东海 是一片黑黑的布满珊瑚礁的滩涂，走起路来可是有些辛苦的呢，穿着薄薄的拖鞋有点儿咯脚。\n比较开心的事，这片海没有什么人，海水在蓝天的照映下蓝蓝的，好美，忍不住坐在椰子树下乘凉多看两眼这片几乎无人的大海。\n功夫不负有心人，再往前走一段路，就看到了悬崖上许多新人在拍婚纱照，这就是传说中的婚纱摄影基地了。巧的是看到一个摄影师带着一对新人从一个半山坡上爬了下来，我也就顺着他们的路往上爬了一番。\n摄影基地其实在许多地方都有的，蜈支洲岛、大小洞天、 三亚 湾、小 东海 ，等等都有许多布置好了的给新人拍摄婚纱用的。我也不过就是凑凑热闹拍两张照片，不喜欢这般喧嚣，还是离得远远地，去海边晒太阳舒服一些。\n大 东海 就比较大众化了，大 东海 在 榆林 港和鹿回头欧中间，距离小 东海 也不算远。大 东海 我被评为4A级景区，并且成为 三亚 首个不收费的景区。大 东海 三面环山，海岸线不长，并且有一段海岸是被隔起来的，曾经为了找大 东海 的“圣托尼里”差点误闯军区。\n我们在大 东海 等了一个没有晚霞的日落，好在海水好美，冬天的 三亚 真的好舒服，穿着短袖下海水也不冷，在大 东海 这个滩平沙白的海滩上，过一个舒服的午后，也没什么好追求的了。\n大 东海 的海岸上有一整排夜宵的好去处，夜幕降临时，人们可以在这儿听着海浪波涛汹涌，感受着海风习习，喝一杯啤酒，撸一串鸡翅，多么美好的夜晚啊。\n路过张猫猫的店我就已经被门口如花园一般给吸引了，特别卡哇伊，颜色、墙画很丰富，让人不由自主想进去打卡。我和小伙伴看中了一个双人餐，买了张团购就进入餐厅了。\n张猫猫的店不仅是屋外像花园一样，屋子里更是如同在森林里，巨大的蘑菇、满墙的彩绘，很有森林里的画面感，越看越让人的少女心要爆发了。\n双人餐一共有5个菜，每个菜都可圈可点，我和小伙伴又一人多点了一些甜点，海南的椰奶清补凉、椰子冻还有芒果卷，味道都很不错。\n五指山小黄牛肉粒：黑胡椒味的牛肉粒，炒得不老不生，味道刚好，配上一口菠萝饭，绝了。\n饱食一餐以后，从大 东海 回来，我们路过第一市场特地下了车来感受一下 三亚 的夜市。第一市场除了游客们吃海鲜的首选之地，也是 三亚 不可多得的夜市，什么现场开珍珠啦，什么 三亚 的海岛风廉价衣服啦，还有每个景区都会有佛珠啦手链啦，也算是体验一下人生百态吧。\n八、大小洞天\n大小洞天是 三亚 最早的一个景区了，它距离 三亚 市区约40公里，有点小远但还好有公交车可以直达。我特地起了个大早就为了来大小洞天好好玩一下。\n大小洞天是 中国 南端的道家文化旅游胜地， 比如 说唐代高僧鉴真弘扬佛法六次东渡 日本 ，第五次就是在南山大小洞天登岸的，当然这都是为了解说为什么这是道家胜地。大小洞天是集山光水色于一体的一个景区，不仅仅可以看到美丽的滨海风光，还有许多区域可以闲逛， 比如 洞天福地、福寿南山还有 南海 龙王和摩崖题咏等等。\n作为一个旅游摄影爱好者，我更多的是看大小洞天有什么好拍的。大小洞天有许多装饰好的婚纱基地，让每个想在朋友圈里美美美的小姐姐们都有一个很好的打卡点，总的来说还是非常不错的。\n进入大小洞天，可以购买观光车，他会带你到终点站小月湾，但其实走起来也不超过1公里，时间充裕的话还是可以选择步行。\n九、夜游三亚湾\n说来也巧，夜游 三亚 湾是临时加进行程里的。原本以为大小洞天会玩到很晚，没想到早早就回到市区，索性去 三亚 游船旅游中心，来个夜游 三亚 湾好了。\n我选择了永乐号仿古船夜游，天渐渐暗了，岸边的城市也开始明亮了起来，我们登船了，这是全 三亚 唯一一艘仿古船，有着主题地“郑和下西洋”来游 三亚 湾。\n108元的船票，可以享受80分钟的海上之旅，并且还赠送茶水、饮料和啤酒，行程开始十分钟后，船上会有以海上 丝绸之路 为主题的现场表演，让你不无聊地度过一段好时光。\n我们的船踏浪而行，鹿回头眨眼间已经到了远方，我们慢慢地靠近了凤凰岛，我端着一杯啤酒靠在船边，感受着海风吹过来，迎面而来是海水特有的味道。 三亚 的城市灯光虽然不是非常繁华，但在海上看着这座旅游城市倒是别有一番滋味。\n永乐号一共有三层，都可以随意乘坐，游船的复古装饰以及工作人员明朝时代的穿着，让人恍惚间仿佛真的回到了郑和下西洋那会儿。\n十、三亚基本攻略\n吃： 三亚 有许多海鲜加工的市场，我比较建议就是我推荐的阿浪海鲜，毕竟已经亲身尝试过了，并不会被宰。和李飘在逛 三亚 湾的时候还吃过一家小海豚海鲜广场，一栋大房子和户外用餐区域很大，吃起来也不错。另外如果一定要试试 海南 菜的话推荐张猫猫的店，就在大 东海 附近，不仅环境不错菜色吃起来也很nice。\n住：建议住在 三亚 市区附近，就是靠近 三亚 湾， 三亚 湾每天都可以看到日落，当然如果是想要花钱度假的话，亚龙湾和海棠湾的海景房是非常nice的。我们这次就是住的海景公寓，人均差不多200块，还算可以。清晨推开门就是海。 行： 三亚 建议至少安排五天吧，我们这样安排的时候算是比较宽松的，如果可以的话可以安排出一整个白天去一趟蜈支洲岛，还是非常推荐去的。 三亚 的公共交通还算方便，不过有时候需要等很久，有条件的话还是建议自驾更方便了。'}
    db.save_travel_detail(sample_detail)
    db.set_progress("last_page", 0)
    print("progress", db.get_progress("last_page"))
    db.close()


if __name__ == '__main__':
    print("Start testing DB schema and save logic")
    test_db_operations()
    # db = SpiderDB()
    # db.export_shops_to_txt(file_path=os.path.join(BASE_DIR, "shops.txt"))
    # db.close()
    print("Finished")
