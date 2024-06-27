import scrapy

from Scrapy_spider_practice.items import ScrapySpiderPracticeItem


class XzqhSpider(scrapy.Spider):
    name = "xzqh"
    allowed_domains = ["xzqh.mca.gov.cn"]
    start_urls = [
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%A3%A8%BE%A9%A3%A9&diji=-1&xianji=-1', # 北京市（京）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%EC%BD%F2%CA%D0%A3%A8%BD%F2%A3%A9&diji=-1&xianji=-1', # 天津市（津）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1', # 河北省（冀）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%BD%CE%F7%CA%A1%A3%A8%BD%FA%A3%A9&diji=-1&xianji=-1', # 山西省（晋）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C4%DA%C3%C9%B9%C5%D7%D4%D6%CE%C7%F8%A3%A8%C4%DA%C3%C9%B9%C5%A3%A9&diji=-1&xianji=-1', # 内蒙古自治区（内蒙古）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C1%C9%C4%FE%CA%A1%A3%A8%C1%C9%A3%A9&diji=-1&xianji=-1', # 辽宁省（辽）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BC%AA%C1%D6%CA%A1%A3%A8%BC%AA%A3%A9&diji=-1&xianji=-1', # 吉林省（吉）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%DA%C1%FA%BD%AD%CA%A1%A3%A8%BA%DA%A3%A9&diji=-1&xianji=-1', # 黑龙江省（黑）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%CF%BA%A3%CA%D0%A3%A8%BB%A6%A3%A9&diji=-1&xianji=-1', # 上海市（沪）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BD%AD%CB%D5%CA%A1%A3%A8%CB%D5%A3%A9&diji=-1&xianji=-1', # 江苏省（苏）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%D5%E3%BD%AD%CA%A1%A3%A8%D5%E3%A3%A9&diji=-1&xianji=-1', # 浙江省（浙）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B0%B2%BB%D5%CA%A1%A3%A8%CD%EE%A3%A9&diji=-1&xianji=-1', # 安徽省（皖）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B8%A3%BD%A8%CA%A1%A3%A8%C3%F6%A3%A9&diji=-1&xianji=-1', # 福建省（闽）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BD%AD%CE%F7%CA%A1%A3%A8%B8%D3%A3%A9&diji=-1&xianji=-1', # 江西省（赣）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%BD%B6%AB%CA%A1%A3%A8%C2%B3%A3%A9&diji=-1&xianji=-1', # 山东省（鲁）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%C4%CF%CA%A1%A3%A8%D4%A5%A3%A9&diji=-1&xianji=-1', # 河南省（豫）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%FE%B1%B1%CA%A1%A3%A8%B6%F5%A3%A9&diji=-1&xianji=-1', # 湖北省（鄂）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%FE%C4%CF%CA%A1%A3%A8%CF%E6%A3%A9&diji=-1&xianji=-1', # 湖南省（湘）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%E3%B6%AB%CA%A1%A3%A8%D4%C1%A3%A9&diji=-1&xianji=-1', # 广东省（粤）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%E3%CE%F7%D7%B3%D7%E5%D7%D4%D6%CE%C7%F8%A3%A8%B9%F0%A3%A9&diji=-1&xianji=-1', # 广西壮族自治区（桂）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%A3%C4%CF%CA%A1%A3%A8%C7%ED%A3%A9&diji=-1&xianji=-1', # 海南省（琼）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%D6%D8%C7%EC%CA%D0%A3%A8%D3%E5%A3%A9&diji=-1&xianji=-1', # 重庆市（渝）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CB%C4%B4%A8%CA%A1%A3%A8%B4%A8%A1%A2%CA%F1%A3%A9&diji=-1&xianji=-1', # 四川省（川、蜀）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%F3%D6%DD%CA%A1%A3%A8%C7%AD%A1%A2%B9%F3%A3%A9&diji=-1&xianji=-1', # 贵州省（黔、贵）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%D4%C6%C4%CF%CA%A1%A3%A8%B5%E1%A1%A2%D4%C6%A3%A9&diji=-1&xianji=-1', # 云南省（滇、云）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CE%F7%B2%D8%D7%D4%D6%CE%C7%F8%A3%A8%B2%D8%A3%A9&diji=-1&xianji=-1', # 西藏自治区（藏）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%C2%CE%F7%CA%A1%A3%A8%C9%C2%A1%A2%C7%D8%A3%A9&diji=-1&xianji=-1', # 陕西省（陕、秦）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B8%CA%CB%E0%CA%A1%A3%A8%B8%CA%A1%A2%C2%A4%A3%A9&diji=-1&xianji=-1', # 甘肃省（甘、陇）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C7%E0%BA%A3%CA%A1%A3%A8%C7%E0%A3%A9&diji=-1&xianji=-1', # 青海省（青）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%C4%FE%CF%C4%BB%D8%D7%E5%D7%D4%D6%CE%C7%F8%A3%A8%C4%FE%A3%A9&diji=-1&xianji=-1', # 宁夏回族自治区（宁）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%D0%C2%BD%AE%CE%AC%CE%E1%B6%FB%D7%D4%D6%CE%C7%F8%A3%A8%D0%C2%A3%A9&diji=-1&xianji=-1', # 新疆维吾尔自治区（新）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CF%E3%B8%DB%CC%D8%B1%F0%D0%D0%D5%FE%C7%F8%A3%A8%B8%DB%A3%A9&diji=-1&xianji=-1', # 香港特别行政区（港）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B0%C4%C3%C5%CC%D8%B1%F0%D0%D0%D5%FE%C7%F8%A3%A8%B0%C4%A3%A9&diji=-1&xianji=-1', # 澳门特别行政区（澳）
        'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%A8%CD%E5%CA%A1%A3%A8%CC%A8%A3%A9&diji=-1&xianji=-1', # 台湾省（台）
        ]

    def parse(self, response):
        if response.status != 200:
            s = f"Page not found: {response.url}"
            self.logger.error(s)
            print('*'*20,s)
            # 可以根据具体情况判断是否需要重试
            yield scrapy.Request(response.url, callback=self.parse)
            return
        print('-' * 10, response.url, 'start', '-' * 10)
        # directlyCitys = [
        #     # '%B1%B1%BE%A9%CA%D0%A3%A8%BE%A9%A3%A9', # 北京市（京）
        #     '%CC%EC%BD%F2%CA%D0%A3%A8%BD%F2%A3%A9', # 天津市（津）
        #     '%C9%CF%BA%A3%CA%D0%A3%A8%BB%A6%A3%A9', # 上海市（沪）
        #     '%D6%D8%C7%EC%CA%D0%A3%A8%D3%E5%A3%A9', # 重庆市（渝）
        #     ]
        # found = any(city_code in response.url for city_code in directlyCitys)
        # print(found)
        
       
        print("Start parsing province...")
        # //tr[@class="shi_nub"]/td 北京市
        # 地名：+北京市 
        # 驻地：
        # 人口（万人）：
        # 面积（平方千米）：
        # 行政区划代码：
        # 区号：
        # 邮编：
        
        # 省
        obj = dispose_of_url(response.url)
        print('Spider 省级', obj['cName'])
        a = response.xpath('//tr[@class="shi_nub"]')  
        # 市
        citys = []
        # 获取第一个tr元素  
        for municipality in a:
            # 获取第一个td下面的input的value（如果存在）  
            # 省名：
            name = municipality.xpath('./td[1]/input/@value').get()   
            # print(name)
            # 获取该tr元素中后面所有td的内容（去除首尾空格和\r\n）  
            other_td_texts = [td_text.strip().replace('\r\n', '') for td_text in municipality.xpath('./td[position()>1]/text()').getall()]  
            # 驻地：
            resident = other_td_texts[0]
            # 人口（万人）：
            if len(other_td_texts) > 1:
                population = other_td_texts[1]
            # 面积（平方千米）：
            if len(other_td_texts) > 2:
                area = other_td_texts[2]
            # 行政区划代码：
            if len(other_td_texts) > 3:
                code = other_td_texts[3]
                
            # 下属辖区
            subList = []
            # 区县
            path = f'//tr[@type="2" and @parent="{name}"]'
            qu = response.xpath(path)
            for tr in qu:
                # 区的名字
                sub_name = tr.xpath('./td[1]/input/@alt').get()
                # print(sub_name)
                td_texts = [td_text.strip().replace('\r\n', '') for td_text in tr.xpath('./td[position()>1]/text()').getall()]  
                # 驻地：
                sub_resident = td_texts[0]
                # 人口（万人）：
                if len(td_texts) > 1:
                    sub_population = td_texts[1]
                else:
                    sub_population = None  # 或者其他处理方式，例如跳过这个条目
                # 面积（平方千米）：
                if len(td_texts) > 2:
                    sub_area = td_texts[2]
                # 行政区划代码：
                if len(td_texts) > 3:
                    sub_code = td_texts[3]
                # 区号：
                if len(td_texts) > 4:
                    sub_areaCode = td_texts[4]
                # 邮编：
                if len(td_texts) > 5:
                    sub_postalCode = td_texts[5]
                district = ScrapySpiderPracticeItem(name=sub_name, 
                                                    resident=sub_resident, 
                                                    population=sub_population, 
                                                    area=sub_area, 
                                                    code=sub_code, 
                                                    areaCode=sub_areaCode,
                                                    postalCode=sub_postalCode,
                                                    )
                subList.append(district)
            
            city = ScrapySpiderPracticeItem(name=name, 
                                            resident=resident, 
                                            population=population, 
                                            area=area, 
                                            code=code,
                                            subList=subList)
            citys.append(city)
        # py = scrapy.Field()
        # jp = scrapy.Field()
        # qp = scrapy.Field()
        province = ScrapySpiderPracticeItem(name=obj['cName'], 
                                            py=obj['py'],
                                            jp=obj['jp'],
                                            qp=obj['qp'],
                                            code=obj['code'],
                                            shorter=obj['shorter'],
                                            subList=citys)
        yield province
        print("end parsing province...")
      
        print('-' * 10, response.url, 'end', '-' * 10)

    
import json
import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
# 假设文件路径为 'data.json'
file_path = current_directory+  'allArea.json'
def read_json():
    print(file_path)
    # 打开文件并加载内容
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def read_json():
    # 打开文件并加载内容
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 现在可以操作 data，它包含了 JSON 文件中的内容
    # print(data)  # 打印整个 JSON 内容


    # 如果是列表，可以按索引访问特定元素
    # print(data[0], data[-1])  # 例如，假设 JSON 文件中是一个列表，这里访问第一个元素
    return data

from urllib.parse import urlparse, parse_qs
def dispose_of_url(url):
    # url = 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1'
    # url = 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%A8%CD%E5%CA%A1%A3%A8%CC%A8%A3%A9&diji=-1&xianji=-1'
    parsed_url = urlparse(decode(url))
    query_params = parse_qs(parsed_url.query)
    # print(query_params)
    if 'shengji' in query_params:
        shengji_value = query_params['shengji'][0]
        
        # print(f"shengji value: {shengji_value}")
        # 用括号分割
        arr = shengji_value.split("（")  # 使用括号（作为分隔符
        parts = arr[0]
        shorter = arr[1].split("）")[0] 
        # 输出分割后的结果
        # print(parts)
        list = read_json()
        # 在数据中找到"cName":"河北省"的对象
        desired_obj = next(item for item in list if item["cName"] == parts)
        # 向desired_obj中插入shorter属性
        desired_obj['shorter'] = shorter
        # print(desired_obj)
        return desired_obj
    else:
        print("shengji parameter not found in the URL.")
        return None

import urllib.parse  
def decode(encoded_text):
    # 先进行 URL 解码
    decoded_bytes = urllib.parse.unquote_to_bytes(encoded_text)
    # 再用 GB2312 解码
    decoded_text = decoded_bytes.decode('gb2312')

    # print(decoded_text)
    return decoded_text
if __name__ == '__main__':
    # read_json()
    # city_urls()
    obj = dispose_of_url('http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1')
    print(obj)