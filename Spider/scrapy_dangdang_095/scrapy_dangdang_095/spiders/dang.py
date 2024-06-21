import scrapy

from scrapy_dangdang_095.items import ScrapyDangdang095Item
class DangSpider(scrapy.Spider):
    name = "dang"
    allowed_domains = ["bang.dangdang.com"]
    start_urls = ["http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-1"]

    # http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-2
    base_url = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-'
    page = 1
    
    def parse(self, response):
        print("bang.dangdang.com Spider =================")
        # pipelines 下载数据
        # items 定义数据结构的
        #   src = //ul[@class="bang_list clearfix bang_list_mode"]/li/div[@class="pic"]//img/@src
        #   alt = //ul[@class="bang_list clearfix bang_list_mode"]/li/div[@class="pic"]//img/@alt
        #   pricr = //ul[@class="bang_list clearfix bang_list_mode"]/li/div[@class="price"]//span[@class="price_n"]
        # 所有的selector的对象都可以再次调用xpath、css方法
        li_list = response.xpath('//ul[@class="bang_list clearfix bang_list_mode"]/li')
        print("================================", len(li_list), "================================")
        for li in li_list:
            src = li.xpath('.//div[@class="pic"]//img/@src').extract_first()
            if not src:
                # src = li.xpath('.//div[@class="pic"]//img/@src')
                print('Not exist image!!!')
            name = li.xpath('.//div[@class="pic"]//img/@alt').extract_first()
            price = li.xpath('.//div[@class="price"]//span[@class="price_n"]/text()').get()
            
            # print(src, name, price)
            book = ScrapyDangdang095Item(src=src, name=name, price=price)
            # 获取一个book就将book交给pipelines
            yield book
            
        if self.page < 100:
            self.page += 1
            url = self.base_url + str(self.page)
            # 怎么去调用parse方法scrapy.Request就是scrpay的get请求
            # url就是请求地址
            # callback是要执行的那个函数，注意不而要加()
            yield scrapy.Request(url=url, callback=self.parse)
        print("bang.dangdang.com Spider =================")
