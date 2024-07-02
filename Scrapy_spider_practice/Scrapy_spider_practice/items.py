# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySpiderPracticeItem(scrapy.Item):
    # define the fields for your item here like:
    # 通俗的说就是你要下载的数据都有什么
    # 'cName': '台湾省', 'code': '710000', 'py': 'Taiwan Sheng', 'jp': 'tws', 'qp': 'TaiwanSheng
    py = scrapy.Field()
    jp = scrapy.Field()
    qp = scrapy.Field()
    # 地名：+北京市 
    name = scrapy.Field()
    # 驻地：
    resident = scrapy.Field()
    # 人口（万人）：
    population = scrapy.Field()
    # 面积（平方千米）：
    area = scrapy.Field()
    # 行政区划代码：
    code = scrapy.Field()
    # 区号：
    areaCode = scrapy.Field()
    # 邮编：
    postalCode = scrapy.Field()
    # 简称
    shorter = scrapy.Field()
    # 下属辖区
    subList = scrapy.Field()
    
    
    # def __init__(self, name, code, jp='', py='', qp='', subList=[], resident='', postalCode='', areaCode='', population='', area=''):
    #     self.code = code
    #     self.jp = jp
    #     self.name = name
    #     self.py = py
    #     self.qp = qp
    #     self.subList = subList
    #     self.resident = resident
    #     self.postalCode = postalCode
    #     self.population = population
    #     self.area = area
    #     self.areaCode = areaCode

    def to_dict(self):
        return {
            "code": self.code,
            "jp": self.jp,
            "name": self.name,
            "py": self.py,
            "qp": self.qp,
            "areaCode": self.areaCode,
            "area": self.area,
            "postcode": self.postcode,
            "population": self.population,
            "resident": self.resident,
            "subList": [sub_item.to_dict() if hasattr(sub_item, 'to_dict') else sub_item for sub_item in self.subList]
        }

class ScrapySpiderDoubanItem(scrapy.Item):
    name = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    actors = scrapy.Field()
    genre = scrapy.Field()
    official_site = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    release_dates = scrapy.Field()
    duration = scrapy.Field()
    aliases = scrapy.Field()
    imdb = scrapy.Field()
    rating_num = scrapy.Field()
    url = scrapy.Field()
    comment_num = scrapy.Field()

if __name__ == '__main__':
    import json
    # 初始化 item 对象并设置字段值
    item = ScrapySpiderPracticeItem()
    item['code'] = "130000"
    item['jp'] = "hbs"
    item['name'] = "河北省"
    item['py'] = "Hebei Sheng"
    item['qp'] = "HebeiSheng"
    item['subList'] = []

    # 如果需要将 item 转换为字典进行 JSON 序列化
    item_dict = dict(item)
    item_json = json.dumps(item_dict)
    print(item_json)