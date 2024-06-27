# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
class ScrapySpiderPracticePipeline:
    def open_spider(self, spider):
        self.fp = open(current_directory +'city_list.json', 'a+', encoding='utf-8')
        # self.fp.write('[\n')  # 开始写入 JSON 数组
    def process_item(self, item, spider):
        try:
            # 将 item 转换为字典
            # item_dict = dict(item)
            
            
            adapter = ItemAdapter(item)
            item_dict = adapter.asdict()
            
            # 打印 item 和 item_dict 进行调试
            # print(f"Item as dict: {item_dict}")

            json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
            # print(json_string)
            self.fp.write(json_string + ',\n')
            return item
        except TypeError as e:
            raise DropItem(f"Error serializing item: {e}")



    def close_spider(self, spider):
        # self.fp.seek(self.fp.tell() - 2, os.SEEK_SET)  # 移动到最后一个逗号前
        # self.fp.truncate()  # 删除最后一个逗号
        # self.fp.write('\n]\n')  # 结束 JSON 数组
        self.fp.close()