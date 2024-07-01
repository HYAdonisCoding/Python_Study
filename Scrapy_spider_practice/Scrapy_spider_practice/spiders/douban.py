import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action="]
    cookie_str = 'll="108288"; bid=UCa8McoRtNs; _pk_id.100001.4cf6=e31052bf43648565.1719799004.; __utmc=30149280; __utmz=30149280.1719799005.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; __utmz=223695111.1719799005.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=hK75Hpeu6ZqNDmiNuTcnXsPPrg0S7OGS; _vwo_uuid_v2=D5072F2FD9EE9BE6086FE21F762E51A9C|7daef985e3a6d4703afe62545bd2cf1c; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1719815849%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Db39yX_MrdDsA1XSbfKfvAs9pRGe-zgWPMPIAkpLOvgXLlOFVS4kF_SnGPnI_MSEo%26wd%3D%26eqid%3Da71103f9001f34720000000366820cd9%22%5D; __utma=30149280.1439727717.1719799005.1719812752.1719815850.4; __utma=223695111.1285498082.1719799005.1719812752.1719815850.4'
    
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    def __init__(self, *args, **kwargs):
        super(DoubanSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        cookies = {}
        for cookie in self.cookie_str.split(';'):
            key, value = cookie.split('=', 1)
            cookies[key.strip()] = value
        
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=cookies, callback=self.parse_with_selenium)
    def parse_with_selenium(self, response):
        self.driver.get(response.url)

        # 等待页面加载完成
        time.sleep(5)

        # 滚动页面加载更多数据
        for _ in range(20):  # 滚动10次
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)  # 每次滚动后等待2秒

        # 获取页面源码并交给Scrapy解析
        page_source = self.driver.page_source
        response = scrapy.Selector(text=page_source)

        self.parse(response)
        
    def parse(self, response):
        print('-' * 10, 'start', '-' * 10)
        # print(response.text)
        '''
        //div[@class="movie-list-panel pictext"]//div[@class="movie-content"] 
        //div[@class="movie-list-panel pictext"]//div[@class="movie-content"]//div[@class="movie-name"]/span/a/text() # 电影名
        //div[@class="movie-list-panel pictext"]//div[@class="movie-content"]//div[@class="movie-name"]/span/a/@href # 链接
        //div[@class="movie-list-panel pictext"]//div[@class="movie-content"]//div[@class="movie-rating"]/span[@class="rating_num"]/text() #评分
        //div[@class="movie-list-panel pictext"]//div[@class="movie-content"]//div[@class="movie-rating"]/span[@class="comment-num"]/text() # 多少人评价
        '''
        contents = response.xpath('//div[@class="movie-list-panel pictext"]//div[@class="movie-content"]') 
        infos = []
        for content in contents:
            # 省名：
            name = content.xpath('.//div[@class="movie-name"]/span/a/text()').get() 
            url = content.xpath('.//div[@class="movie-name"]/span/a/@href').get()  
            rating_num = content.xpath('.//div[@class="movie-rating"]/span[@class="rating_num"]/text()').get()  
            comment_num = content.xpath('.//div[@class="movie-rating"]/span[@class="comment-num"]/text()').get()  
            infos.append({'name': name, 'url': url, 'rating_num': rating_num, 'comment_num': comment_num})
        print(infos)
        print(len(infos))
        print('-' * 10, 'end', '-' * 10)
    
    def closed(self, reason):
        self.driver.quit()