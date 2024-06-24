# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyDangdang095Pipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory +'books.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        self.fp.write(str(item)+', ')
        return item
    
    # 在爬虫执行完成后，执行的方法
    def close_spider(self, spider):
        self.fp.close()

import urllib.request
import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
# 多管道开启
# 1. 定义管道类
# 2. 在settings中开启管道
# "scrapy_dangdang_095.pipelines.DangDangDowwnloadPipeline": 301,
class DangDangDowwnloadPipeline:
    def process_item(self, item, spider):
        url = item.get('src')
        filename = current_directory +'books/'+ item.get('name')+'.jpg'
        urllib.request.urlretrieve(url=url, filename=filename)
        return item