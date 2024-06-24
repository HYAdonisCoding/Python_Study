import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_readbook_101.items import ScrapyReadbook101Item

class ReadSpider(CrawlSpider):
    name = "read"
    allowed_domains = ["www.dushu.com"]
    start_urls = ["https://www.dushu.com/book/1175.html"]
    # https://www.dushu.com/book/1175_2.html
    rules = (
        Rule(LinkExtractor(allow=r"/book/1175_\d+\.html"), 
             callback="parse_item", 
             follow=True),
        )

    def parse_item(self, response):
        print(response.url, 'start', '-' * 30)
        img_list = response.xpath('//div[@class="bookslist"]//div//img')
        for img in img_list:
            name = img.xpath('./@alt').extract_first()
            src = img.xpath('./@data-original').extract_first()
            # print( name, src)
            book = ScrapyReadbook101Item(name=name, src=src)
            yield book
        print(response.url, 'end', '-' * 30)