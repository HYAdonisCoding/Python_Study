import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
import time
from Scrapy_spider_practice.items import ScrapySpiderDoubanItem
class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        # "https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C&type=5&interval_id=100:90&action=",
        "https://movie.douban.com/typerank?type_name=%E5%96%9C%E5%89%A7%E7%89%87&type=24&interval_id=100:90&action=",
        ]
    cookie_str = 'bid=lhjnGfxjns0; ap_v=0,6.0; _pk_id.100001.4cf6=3bc474a87fa4d674.1719888670.; _pk_ses.100001.4cf6=1; __utma=30149280.355711530.1719888671.1719888671.1719888671.1; __utmb=30149280.0.10.1719888671; __utmc=30149280; __utmz=30149280.1719888671.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1183171314.1719888671.1719888671.1719888671.1; __utmb=223695111.0.10.1719888671; __utmc=223695111; __utmz=223695111.1719888671.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    # https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=20&limit=20
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

        self.logger.debug(f'Page source length: {len(page_source)}')
        cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
    #     self.parse(response, cookies)
        
    # def parse(self, response, cookies):

        self.logger.info('-' * 10 + ' start ' + '-' * 10)
        # print(response.text)
        contents = response.xpath('//div[@class="movie-list-panel pictext"]//div[@class="movie-content"]') 
        if not contents:
            self.logger.error('No contents found with the given XPath')
        infos = []
        self.logger.info(f'Parsing {len(contents)} movies')
        for content in contents:
            # 省名：
            name = content.xpath('.//div[@class="movie-name"]/span/a/text()').get() 
            url = content.xpath('.//div[@class="movie-name"]/span/a/@href').get()  
            rating_num = content.xpath('.//div[@class="movie-rating"]/span[@class="rating_num"]/text()').get()  
            comment_num = content.xpath('.//div[@class="movie-rating"]/span[@class="comment-num"]/text()').get()  
            info = {'name': name, 'url': url, 'rating_num': rating_num, 'comment_num': comment_num}
            infos.append(info)
            # self.logger.debug(f'Found movie: {info}')  
            # 对第二页的链接发起访问
            yield scrapy.Request(url=url, cookies=cookies, callback=self.parse_second, meta=info)
        
        self.logger.info(f'Parsed {len(infos)} movies')
        self.logger.info('-' * 10 + ' end ' + '-' * 10)
    def parse_second(self, response):
        self.logger.info('-' * 10 + ' Details ' + '-' * 10)

        # 注意 如果拿不到数据的情况下 一定检查你的xpath语法是否正确
        
        director = response.xpath('//span[contains(text(), "导演")]/following-sibling::span[@class="attrs"]/a/text()').get()
        writer = response.xpath('//span[contains(text(), "编剧")]/following-sibling::span[@class="attrs"]/a/text()').get()
        actors = response.xpath('//span[contains(text(), "主演")]/following-sibling::span[@class="attrs"]//a/text()').getall()
        genre = response.xpath('//span[contains(text(), "类型")]/following-sibling::span/text()').getall()
        official_site = response.xpath('//span[contains(text(), "官方网站")]/following-sibling::a/text()').get()
        country = response.xpath('//span[contains(text(), "制片国家/地区")]/following-sibling::text()').get()
        language = response.xpath('//span[contains(text(), "语言")]/following-sibling::text()').get()
        release_dates = response.xpath('//span[contains(text(), "上映日期")]/following-sibling::span/text()').getall()
        duration = response.xpath('//span[contains(text(), "片长")]/following-sibling::span/text()').getall()
        aliases = response.xpath('//span[contains(text(), "又名")]/following-sibling::text()').get()
        imdb = response.xpath('//span[contains(text(), "IMDb")]/following-sibling::text()').get()

        # 接受到请求的那个meta的参数值
        name = response.meta['name']
        # 接受到请求的那个meta的参数值
        rating_num = response.meta['rating_num']
        # 接受到请求的那个meta的参数值
        url = response.meta['url']
        # 接受到请求的那个meta的参数值
        comment_num = response.meta['comment_num']
        
        movie = ScrapySpiderDoubanItem(
            name = name, 
            director = director,
            writer = writer,
            actors = actors,
            genre = genre,
            official_site = official_site,
            country = country,
            language = language,
            release_dates = release_dates,
            duration = duration,
            aliases = aliases,
            imdb = imdb,
            rating_num = rating_num, 
            url = url, 
            comment_num = comment_num)
        # self.logger.debug(f'Movie details: {movie}')
        yield movie
        
    def closed(self, reason):
        self.logger.debug('closed with reason: %s', reason)

        self.driver.quit()