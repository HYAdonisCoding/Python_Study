import scrapy
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from scrapy import Spider, Request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ZhipinSpider(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ["www.zhipin.com"]
    start_urls = [
        "https://www.zhipin.com/web/geek/job?query=JAVA&city=101010100",
        # 'https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=JAVA&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=2&pageSize=30',
        ]
    def __init__(self, *args, **kwargs):
        super(ZhipinSpider, self).__init__(*args, **kwargs)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # 无头模式
        self.driver = webdriver.Chrome(options=options)
    def start_requests(self):
        for url in self.start_urls:
            # yield SeleniumRequest(url=url, callback=self.parse)
             yield Request(url=url, callback=self.parse, meta={'driver': self.driver})

    def parse(self, response):
        print('-' * 10, 'start', '-' * 10)
        '''
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-title clearfix"]/span[@class="job-name"] 职位名称
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-title clearfix"]//span[@class="job-area"] 地址
        
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-info clearfix"]/span[@class="salary"] 薪资
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-info clearfix"]/ul[@class="tag-list"]  5-10年本科
        
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"] Java,SpringCloud,MySQL
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-footer clearfix"]/div[@class="info-desc"] 定期体检，节日福利，带薪年假，员工旅游，五险一金，加班补助，年终奖
        
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-logo"]/a/img/@src 公司logo
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/h3/a/@href 公司网站（https://www.zhipin.com/)
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/h3/a/text() 公司名称
        //div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/ul[@class="company-tag-list"] 互联网未融资100-499人
        '''
        print(response.text)
        
        # 使用 Selenium 获取页面内容
        driver = response.meta['driver']
        try:
            # 增加等待时间为 20 秒
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="search-job-result"]//li[@class="job-card-wrapper"]'))
            )
            # 执行操作，例如打印元素的文本内容
            print(element.text)
        except Exception as e:
            # 处理超时异常或其他异常
            print(f"Error: {e}")
        
        # Example: Get the page source after any necessary interactions
        html = driver.page_source
        response = scrapy.Selector(text=html)
        
        print(driver.title, driver.current_url)
        # card = response.xpath('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]')
        # job_title = card.xpath('./div[@class="job-title clearfix"]')
        # job_name = job_title.xpath('./span[@class="job-name"]/text()')
        # job_area = job_title.xpath('.//span[@class="job-name"]/area/text()')
        
        # job_info = card.xpath('.//div[@class="job-info clearfix"]')
        # salary = job_info.xpath('./span[@class="salary"]/text()')
        # job_info_tag = job_info.xpath('./ul[@class="tag-list"]')
        
        # footer = card.xpath('.//div[@class="job-card-footer clearfix"]')
        # job_tag = footer.xpath('./ul[@class="tag-list"]')
        # job_info = footer.xpath('.div[@class="info-desc"]/text()')
        
        # right = card.xpath('.//div[@class="job-card-right"]')
        # logo_src = right.xpath('./div[@class="company-logo"]/a/img/@src')
        # company_href = right.xpath('./div[@class="company-info"]/h3/a/@href')
        # company_name = right.xpath('./div[@class="company-info"]/h3/a/text()')
        # company_tag = right.xpath('./div[@class="company-info"]/ul[@class="company-tag-list"]')
        # print(job_name, job_area, salary, job_info_tag,job_tag, job_info, logo_src, company_href, company_name, company_tag)
        # print(response.request.headers)
        
        print('-' * 10, 'end', '-' * 10)
    def closed(self, reason):
        # Spider 关闭时关闭 WebDriver
        self.driver.quit()