# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'


        
class ScrapySpiderPracticePipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory +'city_list.json', 'a+', encoding='utf-8')
        # self.fp.write('[\n')  # 开始写入 JSON 数组
    def process_item(self, item, spider):
        try:
            # 将 item 转换为字典
            # item_dict = dict(item)
            
            
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()
            
            # 打印 item 和 item_dict 进行调试
            # print(f"Item as dict: {item_dict}")

            json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
            # print(json_string)
            self.fp.write(json_string + ',\n')
            return item
        except TypeError as e:
            raise DropItem(f"Error serializing item: {e}")



    def close_spider(self, spider):
        # self.fp.seek(self.fp.tell() - 2, os.SEEK_SET)  # 移动到最后一个逗号前
        # self.fp.truncate()  # 删除最后一个逗号
        # self.fp.write('\n]\n')  # 结束 JSON 数组
        self.fp.close()
class ScrapySpiderDoubanPipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory +'Douban.json', 'a+', encoding='utf-8')
        # self.fp.write('[\n')  # 开始写入 JSON 数组
    def process_item(self, item, spider):
        try:
            # 将 item 转换为字典
            # item_dict = dict(item)
            
            
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()
            
            # 打印 item 和 item_dict 进行调试
            # print(f"Item as dict: {item_dict}")

            json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
            # print(json_string)
            self.fp.write(json_string + ',\n')
            return item
        except TypeError as e:
            raise DropItem(f"Error serializing item: {e}")



    def close_spider(self, spider):
        # self.fp.seek(self.fp.tell() - 2, os.SEEK_SET)  # 移动到最后一个逗号前
        # self.fp.truncate()  # 删除最后一个逗号
        # self.fp.write('\n]\n')  # 结束 JSON 数组
        self.fp.close()

class ScrapySpiderAutosPipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory +'autos.json', 'a+', encoding='utf-8')
        # self.fp.write('[\n')  # 开始写入 JSON 数组
    def process_item(self, item, spider):
        try:
            # 将 item 转换为字典
            
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()
            
            json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
            # print(json_string)
            self.fp.write(json_string + ',\n')
            return item
        except TypeError as e:
            raise DropItem(f"Error serializing item: {e}")



    def close_spider(self, spider):
        # self.fp.seek(self.fp.tell() - 2, os.SEEK_SET)  # 移动到最后一个逗号前
        # self.fp.truncate()  # 删除最后一个逗号
        # self.fp.write('\n]\n')  # 结束 JSON 数组
        self.fp.close()
SQLITE_DB_PATH = 'spider_database.db'

import sqlite3
from scrapy.utils.project import get_project_settings
class SQLiteAutosPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.db_file = settings.get(SQLITE_DB_PATH, 'spider_database.db')

        if not self.db_file:
            raise ValueError("Database file path is not set.")

        spider.logger.info(f"Connecting to SQLite database at: {self.db_file}")

        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        # 创建表格 movies（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS autos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                url TEXT,
                price TEXT,
                score TEXT,
                models TEXT,
                rank_type TEXT,
                rank_number INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

        # 用于批量插入的数据缓存
        self.batch_data = []
        self.batch_size = 50  # 每次提交的记录数

    def process_item(self, item, spider):
        self.batch_data.append((
            item['name'],
            item['url'],
            item['price'],
            item['score'],
            item['models'],
            item['rank_type'],
            item['rank_number']
        ))

        if len(self.batch_data) >= self.batch_size:
            self._commit_batch(spider)

        return item

    def close_spider(self, spider):
        # 插入剩余的数据
        if self.batch_data:
            self._commit_batch(spider, force=True)

        self.conn.close()

    def _commit_batch(self, spider, force=False):
        try:
            self.cursor.executemany('''
                INSERT INTO movies (name, url, price, score, models, rank_type, rank_number)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', self.batch_data)
            self.conn.commit()
            self.batch_data = []
        except sqlite3.IntegrityError as e:
            spider.logger.error(f"Failed to insert batch: {e}")
            if not force:
                self.conn.rollback()  # 回滚未成功的插入
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
            if not force:
                self.conn.rollback()  # 回滚未成功的插入
class SQLiteMoviesPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.db_file = settings.get(SQLITE_DB_PATH, 'spider_database.db')

        if not self.db_file:
            raise ValueError("Database file path is not set.")

        spider.logger.info(f"Connecting to SQLite database at: {self.db_file}")

        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        # 创建表格 movies（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                actors TEXT,
                aliases TEXT,
                comment_num TEXT,
                country TEXT,
                director TEXT,
                duration TEXT,
                genre TEXT,
                imdb TEXT,
                language TEXT,
                official_site TEXT,
                rating_num TEXT,
                release_dates TEXT,
                url TEXT,
                writer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

        # 用于批量插入的数据缓存
        self.batch_data = []
        self.batch_size = 100  # 每次提交的记录数

    def process_item(self, item, spider):
        self.batch_data.append((
            item['name'],
            ','.join(item['actors']),
            item['aliases'],
            item['comment_num'],
            item['country'],
            item['director'],
            ','.join(item['duration']),
            ','.join(item['genre']),
            item['imdb'],
            item['language'],
            item['official_site'],
            item['rating_num'],
            ','.join(item['release_dates']),
            item['url'],
            item['writer']
        ))

        if len(self.batch_data) >= self.batch_size:
            self._commit_batch(spider)

        return item

    def close_spider(self, spider):
        # 插入剩余的数据
        if self.batch_data:
            self._commit_batch(spider, force=True)

        self.conn.close()

    def _commit_batch(self, spider, force=False):
        try:
            self.cursor.executemany('''
                INSERT INTO movies (name, actors, aliases, comment_num, country, director,
                                    duration, genre, imdb, language, official_site,
                                    rating_num, release_dates, url, writer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', self.batch_data)
            self.conn.commit()
            self.batch_data = []
        except sqlite3.IntegrityError as e:
            spider.logger.error(f"Failed to insert batch: {e}")
            if not force:
                self.conn.rollback()  # 回滚未成功的插入
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
            if not force:
                self.conn.rollback()  # 回滚未成功的插入


class MysqlPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.host = settings['DB_HOST']
        self.port = settings['DB_PORT']
        self.user = settings['DB_USER']
        self.password = settings['DB_PASSWORD']
        self.name = settings['DB_NAME']
        self.charset = settings['DB_CHARSET']
        print('*' * 30)
        print(self.host, self.port, self.user, self.password, self.name, self.charset)
        print('*' * 30)
        self.conn = pymysql.connect(host=self.host, 
                                    port=self.port,
                                    user=self.user, 
                                    password=self.password,
                                    db=self.name, 
                                    charset=self.charset)
        self.cursor = self.conn.cursor()
        
    def process_item(self, item, spider):
        sql = '''INSERT INTO movies(name, actors, aliases, comment_num, country, director, duration, genre, imdb, language, official_site, rating_num, release_dates, url, writer)
         VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(
             item['name'], ','.join(item['actors']), item['aliases'], item['comment_num'], item['country'], item['director'],
             item['duration'], item['genre'], item['imdb'], item['language'], item['official_site'], item['rating_num'],
             item['release_dates'], item['url'], item['writer'])


        sql = 'insert into book(name, src) values("{}", "{}")'.format(item['name'], item['src'])
        # print('--------------------------------')
        # print(sql)
        # print('--------------------------------')
        # 执行sql语句
        self.cursor.execute(sql)
        # 提交
        self.conn.commit()
        
        return item
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
        
class CrawlSpider51JobsPipeline:
    def open_spider(self, spider):
        
        self.conn = sqlite3.connect('spider_database.db')
        self.cursor = self.conn.cursor()
        # 创建表（如已存在不会重复创建）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT,
                job_salary TEXT,
                job_tags TEXT,
                company_name TEXT,
                company_url TEXT,
                company_logo TEXT,
                job_dc TEXT,
                job_area TEXT,
                job_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def process_item(self, item, spider):
        self.cursor.execute('''
            INSERT INTO jobs (job_name, job_salary, job_tags, company_name, company_url, company_logo, job_dc, job_area, job_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('job_name'),
            item.get('job_salary'),
            item.get('job_tags'),
            item.get('company_name'),
            item.get('company_url'),
            item.get('company_logo'),
            item.get('job_dc'),
            item.get('job_area'),
            item.get('job_type')
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()