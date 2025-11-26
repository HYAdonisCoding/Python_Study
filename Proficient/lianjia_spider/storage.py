#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8


import sqlite3
import json
import os
from datetime import datetime, timedelta, timezone

from parser import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, "db", "lianjia.db")

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

CREATE_HOUSES_TABLE = """
-- 房源列表表
CREATE TABLE IF NOT EXISTS houses (
    house_id TEXT PRIMARY KEY,            -- 房源ID
    title TEXT,                           -- 房源标题
    community_name TEXT,                  -- 小区名
    community_url TEXT,                    -- 小区链接
    region TEXT,                           -- 区域
    region_url TEXT,                       -- 区域链接
    bedrooms TEXT,                         -- 户型
    area REAL,                             -- 建筑面积（平米）
    orientation TEXT,                      -- 朝向
    renovation TEXT,                       -- 装修情况
    floor TEXT,                            -- 楼层信息
    year_built TEXT,                        -- 建造年份
    building_type TEXT,                     -- 建筑类型
    followers INTEGER,                      -- 关注人数
    publish_time TEXT,                      -- 发布时间（字符串）
    total_price REAL,                       -- 总价（万）
    unit_price REAL,                        -- 单价（元/平米）
    updated_at TEXT DEFAULT (datetime(CURRENT_TIMESTAMP, '+8 hours'))
);
"""

CREATE_HOUSE_DETAILS_TABLE = """
-- 房源详情表
CREATE TABLE IF NOT EXISTS house_details (
    house_id TEXT PRIMARY KEY,             -- 房源ID
    house_type TEXT,                       -- 房型
    floor_info TEXT,                        -- 楼层信息
    build_area REAL,                        -- 建筑面积
    inner_area REAL,                        -- 套内面积
    structure_type TEXT,                     -- 结构类型
    construction TEXT,                       -- 结构方式
    staircase_ratio TEXT,                    -- 梯户比
    heating_type TEXT,                       -- 供暖方式
    has_elevator BOOLEAN,                    -- 是否有电梯
    floor_height REAL,                       -- 层高
    listing_date TEXT,                       -- 挂牌日期
    ownership_type TEXT,                     -- 权属类型
    last_transaction TEXT,                   -- 上次交易
    usage TEXT,                              -- 用途
    property_age TEXT,                       -- 房龄
    property_right TEXT,                     -- 房产性质
    mortgage_info TEXT,                      -- 按揭信息
    documents_uploaded TEXT,                 -- 房产证照片
    tags TEXT,                               -- 标签JSON
    core_selling_points TEXT,                -- 核心卖点
    community_intro TEXT,                    -- 小区介绍
    updated_at TEXT DEFAULT (datetime(CURRENT_TIMESTAMP, '+8 hours')),
    FOREIGN KEY(house_id) REFERENCES houses(house_id)
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
        cur.execute(CREATE_HOUSES_TABLE)
        cur.execute(CREATE_HOUSE_DETAILS_TABLE)
        cur.execute(CREATE_PROGRESS_TABLE)
        self.conn.commit()

    def save_house_list(self, house_list):
        """批量保存列表页信息"""
        cur = self.conn.cursor()
        local_time = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
        values = []
        for h in house_list:
            total_price = float(str(h['total_price']).replace('万',''))
            unit_price = float(str(h['unit_price']).replace('元/平','').replace(',',''))
            area = float(str(h['area']).replace('平米',''))
            values.append((
                h['house_id'], h['title'], h['community_name'], h['community_url'],
                h['region'], h['region_url'], h['bedrooms'], area, h['orientation'], 
                h['renovation'], h['floor'], h['year_built'], h['building_type'], 
                h['followers'], h['publish_time'], total_price, unit_price, local_time
            ))
        cur.executemany("""
            INSERT INTO houses(
                house_id, title, community_name, community_url, region, region_url,
                bedrooms, area, orientation, renovation, floor, year_built, building_type,
                followers, publish_time, total_price, unit_price, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(house_id) DO UPDATE SET
                title=excluded.title,
                community_name=excluded.community_name,
                community_url=excluded.community_url,
                region=excluded.region,
                region_url=excluded.region_url,
                bedrooms=excluded.bedrooms,
                area=excluded.area,
                orientation=excluded.orientation,
                renovation=excluded.renovation,
                floor=excluded.floor,
                year_built=excluded.year_built,
                building_type=excluded.building_type,
                followers=excluded.followers,
                publish_time=excluded.publish_time,
                total_price=excluded.total_price,
                unit_price=excluded.unit_price,
                updated_at=excluded.updated_at
        """, values)
        self.conn.commit()

    def save_house_detail(self, detail):
        """保存详情页信息"""
        cur = self.conn.cursor()
        local_time = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
        tags_json = json.dumps(detail.get('tags', []), ensure_ascii=False)
        build_area = self.parse_area(detail.get('build_area'))
        inner_area = self.parse_area(detail.get('inner_area'))
        unit_price = detail.get('unit_price')  # 保留原字符串或数值可自行处理
        has_elevator = 1 if detail.get('has_elevator') == '有' else 0
        cur.execute("""
            INSERT INTO house_details(
                house_id, house_type, floor_info, build_area, inner_area, structure_type,
                construction, staircase_ratio, heating_type, has_elevator, floor_height,
                listing_date, ownership_type, last_transaction, usage, property_age,
                property_right, mortgage_info, documents_uploaded, tags, core_selling_points,
                community_intro, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(house_id) DO UPDATE SET
                house_type=excluded.house_type,
                floor_info=excluded.floor_info,
                build_area=excluded.build_area,
                inner_area=excluded.inner_area,
                structure_type=excluded.structure_type,
                construction=excluded.construction,
                staircase_ratio=excluded.staircase_ratio,
                heating_type=excluded.heating_type,
                has_elevator=excluded.has_elevator,
                floor_height=excluded.floor_height,
                listing_date=excluded.listing_date,
                ownership_type=excluded.ownership_type,
                last_transaction=excluded.last_transaction,
                usage=excluded.usage,
                property_age=excluded.property_age,
                property_right=excluded.property_right,
                mortgage_info=excluded.mortgage_info,
                documents_uploaded=excluded.documents_uploaded,
                tags=excluded.tags,
                core_selling_points=excluded.core_selling_points,
                community_intro=excluded.community_intro,
                updated_at=excluded.updated_at
        """, (
            detail['house_code'], detail.get('house_type'), detail.get('floor_info'),
            build_area, inner_area, detail.get('structure_type'), detail.get('construction'),
            detail.get('staircase_ratio'), detail.get('heating_type'), has_elevator,
            detail.get('floor_height'), detail.get('listing_date'), detail.get('ownership_type'),
            detail.get('last_transaction'), detail.get('usage'), detail.get('property_age'),
            detail.get('property_right'), detail.get('mortgage_info'),
            detail.get('documents_uploaded'), tags_json, detail.get('core_selling_points'),
            detail.get('community_intro'), local_time
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
    def parse_area(self, value):
        """Convert area string like '54.8㎡' to float, return None for invalid data."""
        if not value:
            return None
        value = value.replace('㎡','').strip()
        try:
            return float(value)
        except ValueError:
            return None
def test_db_operations():
    """Test database insertions and progress tracking."""
    db = SpiderDB()
    sample_travels = [{'house_id': '101133895297', 'detail_url': 'https://bj.lianjia.com/ershoufang/101133895297.html', 'title': '金隅丽港06年小区 人车分流 满五唯一、精致一居室', 'community_name': '金隅丽港城', 'community_url': 'https://bj.lianjia.com/xiaoqu/1111027377528/', 'region': '望京', 'region_url': 'https://bj.lianjia.com/ershoufang/wangjing/', 'bedrooms': '1室1厅', 'area': '54.8平米', 'orientation': '东', 'renovation': '简装', 'floor': '低楼层(共26层)', 'year_built': '2004年', 'building_type': '塔楼', 'followers': 11, 'publish_time': '31天以前发布', 'total_price': '255', 'unit_price': '46,533元/平'}]
    db.save_house_list(sample_travels)

    sample_detail = {'total_price': '255万', 'unit_price': '46533元/平米', 'house_code': '101133895297', 'house_type': '1室1厅1厨1卫', 'floor_info': '低楼层 (共26层)', 'build_area': '54.8㎡', 'structure_type': '平层', 'inner_area': '暂无数据', 'building_type': '塔楼', 'orientation': '东', 'construction': '钢混结构', 'renovation': '简装', 'staircase_ratio': '三梯十二户', 'heating_type': '集中供暖', 'has_elevator': '有', 'floor_height': '暂无数据', 'listing_date': '2025-10-24', 'ownership_type': '商品房', 'last_transaction': '2021-12-04', 'usage': '普通住宅', 'property_age': '满两年', 'property_right': '非共有', 'mortgage_info': '有抵押 110万元 光大银行 客户偿还', 'documents_uploaded': '已上传房本照片', 'tags': ['地铁', 'VR房源', '房本满两年'], 'core_selling_points': '小区总价低大1居，高原值\n税费低，要比满五唯一税费还要低！', 'community_intro': '金隅丽港城2006年小区，人车分流\n小区4栋板楼、3栋塔楼，国企开发，户户带飘窗阳台。\n洋房成本低，物业费1.7、车位350/月地下固定！'}
    db.save_house_detail(sample_detail)
    db.close()


if __name__ == '__main__':
    print("Start testing DB schema and save logic")
    test_db_operations()
    print("Finished")
