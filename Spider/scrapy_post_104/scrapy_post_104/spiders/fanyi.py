from scrapy.signalmanager import dispatcher
from typing import Iterable
from scrapy import signals
import scrapy
import json
import logging

class FanyiSpider(scrapy.Spider):
    name = "fanyi"
    allowed_domains = ["fanyi.baidu.com"]
    start_urls = ["https://fanyi.baidu.com/sug"]

    def __init__(self, *args, **kwargs):
        super(FanyiSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.close_log_file_handler, signals.spider_closed)
    def close_log_file_handler(self, spider):
        self.log('Closing log file handler', level=logging.INFO)
        # 遍历所有 Scrapy 日志记录器的处理程序，并关闭任何 logging.FileHandler 实例
        for handler in logging.getLogger('scrapy').handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
    # def parse(self, response):
    #     print('*' * 30, response.url, ' start','*' * 30)
    #     content = response.text
    #     objects = json.loads(content)
    #     print(objects)
    #     print('*' * 30, response.url, ' end','*' * 30)

    def start_requests(self):
        url = "https://fanyi.baidu.com/sug"
        
        data = {
            'kw': 'correctly',
        }
        
        yield scrapy.FormRequest(url=url,formdata=data, callback=self.parse_second)
        
    def parse_second(self, response):
        print('*' * 30, response.url, ' start','*' * 30)
        content = response.text
        objects = json.loads(content)
        print(objects)
        print('*' * 30, response.url, ' end','*' * 30)