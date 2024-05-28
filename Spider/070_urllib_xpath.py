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
def send_get_request_delegate(url, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    try:
        # 代理配置
        proxies = {
            'https': '72.10.160.170:24847',
            'http': '72.10.160.170:24847',
        }
        proxy_support = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(proxy_support)

        # 设置证书
        context = ssl.create_default_context()
        context.load_verify_locations(certifi.where())

        # 安装代理和证书配置
        urllib.request.install_opener(opener)
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        
        response = urllib.request.urlopen(request, context=context)
        
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        fp = open(current_directory+'代理1.html', 'w', encoding='utf-8')
        fp.write(content)
        # print(content)
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)
        

    proxies_pool = [
            {'https': '72.10.160.170:24847111'},
            {'https': '72.10.160.170:248472222'},
        ]
    proxy = random.choice(proxies_pool)
    print(proxy)
if __name__ == '__main__':
    parse_local_file()
    
    url = 'http://www.baidu.com/s?wd=ip'
    url = 'https://en.ipshu.com/'
    headers = {
        'Cookie': '__gads=ID=ec54ccad7b00d309:T=1705311424:RT=1705311424:S=ALNI_MY408XW44pMg2sMxTYDEXSuGtuQTg; __gpi=UID=00000cdd15ed35fc:T=1705311424:RT=1705311424:S=ALNI_MYZrN-r2idhR49aYtMbU8uFvZlMJQ',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    # send_get_request(url, headers)
    
    # send_get_request_delegate(url, headers)
    data = {
        'from': 'en',
        'to': 'zh',
        'query': 'spider',
        'transtype': 'enter',
        'simple_means_flag': '3',
        'sign': '63766.268839',
        'token': '1aa74f88c034c0914382c8e42e3f69f3',
        'domain': 'common',
        'ts': '1704960917667',
    }
    # send_post_request(url, data, headers)
    