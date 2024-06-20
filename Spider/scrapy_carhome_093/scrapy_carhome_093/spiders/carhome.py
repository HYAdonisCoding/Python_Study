import scrapy


class CarhomeSpider(scrapy.Spider):
    name = "carhome"
    allowed_domains = ["www.autohome.com.cn"]
    start_urls = ["https://www.autohome.com.cn/price/brandid_75"]

    def parse(self, response):
        print("www.autohome.com.cn Spider =================")
        # content = response.text
        # print(content)
        name_list = response.xpath('//li/div[@class="tw-mt-1 tw-px-4"]/a')
        
        price_list = response.xpath('//li/div[@class="tw-mt-1 tw-px-4"]/p[@class="tw-pb-[10px] tw-font-avenir tw-text-base tw-font-medium tw-leading-[1] tw-text-[#FF6600]"]')
        for i in range(len(price_list)):
            print(name_list[i].xpath('text()').get(), price_list[i].xpath('text()').get())
        
        print("www.autohome.com.cn Spider =================")
