# -*- coding: utf-8 -*-

import json
import os
import random
import ssl
from lxml import etree
import certifi
import urllib.request

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'

def parse_local_file():
    file = current_directory + '069_urllib_xpath.html'
    print(file)
    tree = etree.parse(file)
    # 查找ul下面的li
    # li_list = tree.xpath('//body/ul/li')
    
    # 查找所有有id属性的li , text()获取内容
    # li_list = tree.xpath('//li[@id]/text()')
    
    # 查找所有有id属性为l1的li
    # li_list = tree.xpath('//li[@id="l1"]/text()')
    
    # 查找所有有id属性为l1的li标签的class属性值
    # li_list = tree.xpath('//li[@id="l1"]/@class')
    
    # 查找所有有id属性包含l的li
    # li_list = tree.xpath('//li[contains(@id, "l")]/text()')
    
    # 查找所有有id属性以c开头的li
    # li_list = tree.xpath('//li[starts-with(@id, "c")]/text()')
    
    # 查找所有有id为l1和class为cc的li
    # li_list = tree.xpath('//ul/li[@id="l1" and @class="cc"]/text()')
    
    # 查找所有有id为l1和class为cc的li
    li_list = tree.xpath('//ul/li[@id="l1"]/text() | //ul/li[@class="cc"]/text()')
    
    print(li_list)
    print(len(li_list))
    
def parse_html():
    # tree = etree.HTML(current_directory + '069_urllib_xpath.html')
    pass
def send_get_request(url, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    try:
        
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        # context = ssl._create_unverified_context()
        response = urllib.request.urlopen(request)
        
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        # fp = open(current_directory+'代理1.html', 'w', encoding='utf-8')
        # fp.write(content)
        # print(content)
        return content
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
        return None
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)
        return None
    
        


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}
if __name__ == '__main__':
    # parse_local_file()
    
    url = 'https://www.baidu.com'
    result = send_get_request(url, headers)
    # print(result)
    tree = etree.HTML(result)
    p = tree.xpath('//form/span/input[@id="su"]/@value')[0]
    print(p)
    
    