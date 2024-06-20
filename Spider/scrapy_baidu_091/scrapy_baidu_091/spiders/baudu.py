import scrapy


class BauduSpider(scrapy.Spider):
    # 爬虫的名字 用于运行爬虫的时候 使用的值
    name = "baudu"
    # 允许访问的域名
    allowed_domains = ["www.baidu.com"]
    # 超始的ur1地址 指的是第一次要访问的域名
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        print("BauduSpider ========'" + response.text[1:1000])
