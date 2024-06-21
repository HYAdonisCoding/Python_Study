# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
class ScrapyReadbook101Pipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory+'books.json', 'w', encoding='utf-8')
        
    def process_item(self, item, spider):
        self.fp.write(str(item),)
        return item
    def close_spider(self, spider):
        self.fp.close()

import pymysql
from scrapy.utils.project import get_project_settings
        
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