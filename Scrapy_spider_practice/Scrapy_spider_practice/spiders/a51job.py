import scrapy
from scrapy_selenium import SeleniumRequest

class A51jobSpider(scrapy.Spider):
    name = "51job"
    allowed_domains = ["we.51job.com"]
    start_urls = ["https://we.51job.com/pc/search?jobArea=010000&keyword=iOS&searchType=2&sortType=0&metro=&pageNum=1"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800
        },
        'SELENIUM_DRIVER_NAME': 'chrome',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': '/Users/adam/Documents/Developer/environment/chromedriver-mac-x64/chromedriver',
        'SELENIUM_DRIVER_ARGUMENTS': [],  # 可以加 '--headless' 试试
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=10,
                wait_until=lambda driver: driver.find_elements_by_xpath('//*[@id="app"]/div//div[@class="joblist-item-job-wrapper"]')
            )

    def parse(self, response):
        print("抓到页面：", response.url)
        job_list = response.xpath('//*[@id="app"]/div//div[@class="joblist-item-job-wrapper"]')
        print('职位数：', len(job_list))
        for div in job_list:
            # ...你的解析逻辑...
            pass

from scrapy.cmdline import execute

if __name__ == '__main__':
    
    execute(['scrapy', 'runspider', __file__])