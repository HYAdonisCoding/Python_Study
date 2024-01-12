# -*- coding: utf-8 -*-

import json
import os
import ssl

import certifi
import urllib.request

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/data/'

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
        fp = open(current_directory+'weibo.html', 'w', encoding='utf-8')
        fp.write(content)
        # print(content)
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
    url = 'https://weibo.cn/1833633545/info'
    headers = {
        'Cookie': 'SUB=_2A25IpI_DDeRhGedG6FEX8y3JzzmIHXVr240LrDV6PUJbktANLU7nkW1NUVZ59YeLx6jmhT8pxCx87K5fQZGm0rsK; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFF4GdBox5fXBwRZuLnwSHm5JpX5KzhUgL.Fo2Re0ece0efSh-2dJLoIEBLxKML1hML1K-LxKBLB.2L1K2LxK-LBo5L1K2LxK-L1K5L1-zt; SSOLoginState=1705050003; ALF=1707642003; _T_WM=8dcc16642495c37ae39b127f822e1650',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    send_get_request(url, headers)
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
    