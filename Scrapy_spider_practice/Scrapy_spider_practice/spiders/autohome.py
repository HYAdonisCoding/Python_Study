import scrapy


class AutohomeSpider(scrapy.Spider):
    name = "autohome"
    allowed_domains = ["www.autohome.com.cn"]
    start_urls = [
        "https://www.autohome.com.cn/price/",
        ]

    def parse(self, response):
        print(response.url, " start =================")
        
        with open('autohome.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        print("保存成功：autohome.html")

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
            # 按照'第'和'名'分割字符串
            if ranking:
                parts = ranking.split('第')[1].split('名')

                # 排名类型和具体排名
                rank_type = parts[0]  # 排名类型
                rank_number = int(parts[1])  # 第几名，转换为整数类型

                # 输出结果
                print(f"排名类型: {rank_type}, 第几名: {rank_number}")
            print(f"{name}, {url}, {price}, {score}, {models}, {ranking}")
        print(response.url, " end =================")
