import scrapy


class TcSpider(scrapy.Spider):
    name = "tc"
    allowed_domains = ["bj.58.com"]
    start_urls = ["https://bj.58.com/sou/?key=%E5%89%8D%E7%AB%AF&classpolicy=classify_B%2Cuuid_0bce525860db4bb79cc21c921abd5f43&search_uuid=0bce525860db4bb79cc21c921abd5f43/"]

    def parse(self, response):
        print("bj.58.com Spider =================")
        # content = response.text
        # print(content)
        # content = response.body
        # print(content[:1000])
        # span_list = response.xpath('//div[@id="filter"]/div[@class="tabs"]/a/span')
        # span_list = response.xpath('//div[@id="filter"]/div[@class="tabs"]')
        # print(span_list)
        span = response.xpath('//div[@id="filter"]/div[@class="tabs"]/a/span')[0]
        print(span.extract())
        
        print("bj.58.com Spider =================")
