import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from Scrapy_spider_practice.items import ScrapySpiderAutohomeItem

class AutohomeSpider(scrapy.Spider):
    name = "autohome"
    allowed_domains = ["www.autohome.com.cn"]
    start_urls = [
        "https://www.autohome.com.cn/price/",
        ]
    def __init__(self, *args, **kwargs):
        super(AutohomeSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def start_requests(self):
        # cookies = {}
        # for cookie in self.cookie_str.split(';'):
        #     key, value = cookie.split('=', 1)
        #     cookies[key.strip()] = value
        
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_with_selenium)
    def parse_with_selenium(self, response):
        self.driver.get(response.url)

        # 等待页面加载完成
        time.sleep(5)

        # 滚动页面加载更多数据
        for _ in range(35):  # 滚动10次
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)  # 每次滚动后等待2秒

        # 获取页面源码并交给Scrapy解析
        page_source = self.driver.page_source
        response = scrapy.Selector(text=page_source)

        print(" start =================")
        
        # with open('autohome.html', 'w', encoding='utf-8') as f:
        #     f.write(response.text)

        # print("保存成功：autohome.html")

        lists = response.xpath('//li[@class="tw-group tw-relative tw-cursor-pointer tw-overflow-hidden tw-rounded tw-bg-[#F7FAFE] tw-pb-4 tw-text-center tw-text-[#111E36] hover:tw-shadow-[0_8px_32px_0_rgba(17,30,54,0.1)]"]')
        print(len(lists))
        for content in lists:
            # /a/@href
            ranking = content.xpath('.//p/text()').get()
            name = content.xpath('./div[@class="tw-mt-1 tw-px-4"]/a/text()').get() 
            url = content.xpath('./div[@class="tw-mt-1 tw-px-4"]/a/@href').get()
            price = content.xpath('./div[@class="tw-mt-1 tw-px-4"]/p[@class="tw-pb-[10px] tw-font-avenir tw-text-base tw-font-medium tw-leading-[1] tw-text-[#FF6600]"]/text()').get() 
            score = content.xpath('./div[@class="tw-mt-1 tw-px-4"]/p//span/text()').get()
            models = content.xpath('./div[@class="tw-mt-1 tw-px-4"]/div/em/text()').get()
            rank_type = None
            rank_number = None
            # 按照'第'和'名'分割字符串
            if ranking:
                # print(ranking)
                # 新能源销量第1名
                parts = ranking.split('第')
                if len(parts) > 1:
                    # 排名类型和具体排名
                    rank_type = parts[0]  # 排名类型
                    s = parts[1].split('名')
                    if len(s) > 0:
                        rank_number = int(parts[1].split('名')[0])  # 第几名，转换为整数类型

                # 输出结果
                # print(f"排名类型: {rank_type}, 第几名: {rank_number}")
            # print(f"{name}, {url}, {price}, {score}, {models}, {ranking}, 排名类型: {rank_type}, 第几名: {rank_number}")
            auto = ScrapySpiderAutohomeItem(
                    name = name,
                    url = url,
                    price = price,
                    score = score,
                    models = models,
                    rank_type = rank_type,
                    rank_number = rank_number,
                )
            yield auto
        print(" end =================")
    def closed(self, reason):
        self.driver.quit()
