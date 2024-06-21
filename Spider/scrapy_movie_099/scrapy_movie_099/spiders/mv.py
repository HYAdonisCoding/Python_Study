import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy_movie_099.items import ScrapyMovie099Item
class MvSpider(scrapy.Spider):
    name = "mv"
    allowed_domains = ["www.dytt89.com", "www.dygod.net"]
    # https://www.dygod.net/html/gndy/china/index.html
    start_urls = ["https://www.dygod.net/html/gndy/china/index.html","https://www.dytt89.com/html/tv/hytv/index.html"]
    # def start_requests(self):
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    #         'Accept-Language': 'en-US,en;q=0.5',
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'Connection': 'keep-alive',
    #         'Upgrade-Insecure-Requests': '1',
    #         'Pragma': 'no-cache',
    #         'Cache-Control': 'no-cache',
    #     }
    #     cookies = {
    #         'guardok': 'j/b0z1T3xNLo/co+O5co15IlMbVHAPRFapyc3lkraOp5WPr6GRavaFhzgOsyoWby4v51oFF2JzCTIfVKX3rFlQ==',
    #         # 添加其他必要的 Cookie
    #     }
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, headers=headers, cookies=cookies)
    def start_requests(self):
        
          for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,  # 增加等待时间
                wait_until=EC.presence_of_element_located((By.XPATH, '//div[@class="co_content8"]//td//a[@class="ulink"]'))
            )



    def parse(self, response):
        print(f"{response.url} Spider start =================")
        a_list = response.xpath('//div[@class="co_content8"]//td//a[@class="ulink"]')
        base = 'https://www.dytt89.com'
        print(response.text)
        print(f"================= {len(a_list)} =================")
        for a in a_list:
            name = a.xpath('./text()').extract_first()
            href = a.xpath('./@href').extract_first()
            url = base + href
            print(name, url)
            # 对第二页的链接发起访问
            yield scrapy.Request(url=url, callback=self.parse_second, meta={'name': name})
        print(f"{response.url} Spider end =================")
        
    def parse_second(self, response):
        # 注意 如果拿不到数据的情况下 一定检查你的xpath语法是否正确
        src = response.xpath('//div[@id="Zoom"]/img/@src').extract_first()
        # 接受到请求的那个meta的参数值
        name = response.meta['name']
        
        movie = ScrapyMovie099Item(src = src, name = name)
        yield movie