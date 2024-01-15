# -*- coding: utf-8 -*-

import json
import os
import ssl

import certifi
import urllib.request

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/data/'

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
        
def send_get_request_hander(url, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    try:
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        # 2.获取hander
        hander = urllib.request.HTTPSHandler(context=ssl_context)
        # 3.build_opner
        opener = urllib.request.build_opener(hander)
        # 4.open
        response = opener.open(request)
        
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        # fp = open(current_directory+'douban1.json', 'w', encoding='utf-8')
        # fp.write(content)
        # print(content)
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)
def send_get_request(url, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    try:
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        # 2.获取想要的数据
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        fp = open(current_directory+'douban1.json', 'w', encoding='utf-8')
        fp.write(content)
        print(content)
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)

def send_post_request(url, data, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)
    
    
    # post请求的参数必须编码
    data = urllib.parse.urlencode(data).encode('utf-8')
    
    print(data)
    request = urllib.request.Request(url, data, headers)
    
    response = urllib.request.urlopen(request)
    
    content = response.read().decode('utf-8')
    
    obj = json.loads(content)
    print(obj)
    
if __name__ == '__main__':
    url = 'http://www.baidu.com/s?wd=ip'
    url = 'https://en.ipshu.com/'
    headers = {
        'Cookie': '__gads=ID=ec54ccad7b00d309:T=1705311424:RT=1705311424:S=ALNI_MY408XW44pMg2sMxTYDEXSuGtuQTg; __gpi=UID=00000cdd15ed35fc:T=1705311424:RT=1705311424:S=ALNI_MYZrN-r2idhR49aYtMbU8uFvZlMJQ',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    # send_get_request(url, headers)
    
    send_get_request_delegate(url, headers)
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
    