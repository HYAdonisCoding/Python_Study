# -*- coding: utf-8 -*-
import ssl
import urllib.request
import urllib.parse
import os
import certifi

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'

def name(args=""):
 pass

def main():
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    }
    # x 
    url_page = 'https://www.google.com/search?q='
    name = urllib.parse.quote('周杰伦')
    url_page = url_page + name
    print(url_page)
    # 请求对象的定制
    request = urllib.request.Request(url = url_page, headers=headers)
    # 模拟浏览器向服务器发送请求
    response = urllib.request.urlopen(request)
    
    content = response.read().decode('utf-8')
    
    print(content)
    
    print('Finished!')

if __name__ == '__main__':
    main() 
    # name()