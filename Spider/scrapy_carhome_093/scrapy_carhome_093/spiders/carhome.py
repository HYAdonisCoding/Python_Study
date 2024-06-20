import scrapy


class CarhomeSpider(scrapy.Spider):
    name = "carhome"
    allowed_domains = ["www.autohome.com.cn"]
    # https://www.autohome.com.cn/price/fueltypedetail_3-levelid_9
    # start_urls = ["https://www.autohome.com.cn/price/brandid_75"]
    start_urls = ["https://www.autohome.com.cn/price/fueltypedetail_3-levelid_9"]

    def parse(self, response):
        print("www.autohome.com.cn Spider =================")
        # content = response.text
        # print(content)
        name_list = response.xpath('//li/div[@class="tw-mt-1 tw-px-4"]/a')
        
        price_list = response.xpath('//li/div[@class="tw-mt-1 tw-px-4"]/p[@class="tw-pb-[10px] tw-font-avenir tw-text-base tw-font-medium tw-leading-[1] tw-text-[#FF6600]"]')
        for i in range(len(price_list)):
            print(name_list[i].xpath('text()').get(), price_list[i].xpath('text()').get())
        
        print("www.autohome.com.cn Spider =================")
        
        
'''
https://www.autohome.com.cn/price/brandid_75
www.autohome.com.cn Spider =================
秦PLUS 7.98-17.98万
海鸥 6.98-8.58万
宋PLUS新能源 12.98-20.98万
驱逐舰05 7.98-12.88万
元PLUS 11.98-16.38万
宋Pro新能源 10.98-15.98万
汉 16.98-29.98万
唐新能源 17.98-26.98万
海豚 9.98-13.98万
元UP 9.68-11.98万
海豹 14.98-24.98万
宋L 18.98-24.98万
比亚迪e2 8.98-14.78万
护卫舰07 17.98-31.98万
秦新能源 15.58-16.98万
海狮07 EV 18.98-23.98万
秦L 9.98-13.98万
元Pro 9.58-11.38万
比亚迪e3 15.48-15.58万
比亚迪D1 16.08-16.98万
海豹06 DM-i 9.98-13.98万
宋MAX新能源 14.78-17.48万
比亚迪e9 24.18万
海豹X 暂无报价
www.autohome.com.cn Spider =================
'''

'''
https://www.autohome.com.cn/price/fueltypedetail_3-levelid_9
www.autohome.com.cn Spider =================
锋兰达 12.58-18.48万
RAV4荣放 17.68-26.38万
威兰达 17.38-26.48万
卡罗拉锐放 12.98-18.48万
本田CR-V 18.59-26.39万
皓影 18.59-26.39万
汉兰达 24.98-34.88万
博越L 11.57-17.07万
皇冠陆放 27.78-35.28万
皓瀚 8.99-13.69万
途胜 16.18-22.58万
红旗HS3 14.58-19.58万
航海家 32.88-46.88万
本田HR-V 15.99-22.89万
威飒 21.68-30.38万
锐界 22.98-30.98万
冒险家 23.58-34.58万
传祺GS8 15.98-26.98万
五菱星辰 6.88-10.98万
狮铂拓界 17.98-23.78万
凌放HARRIER 21.18-29.88万
马自达CX-50行也 15.98-23.98万
丰田C-HR 15.28-19.28万
领克01 15.58-19.68万
皓极 12.69-14.69万
ZR-V 致在 15.99-22.89万
红旗HS7 25.58-33.58万
影酷 11.98-16.98万
奕泽IZOA 14.98-18.98万
五菱星云 8.98-10.58万
www.autohome.com.cn Spider =================
'''