# -*- coding: utf-8 -*-
import ssl
import urllib.request
import urllib.parse
import certifi
import json

def main(url, data):
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
    
    # post请求的参数必须编码
    data = urllib.parse.urlencode(data).encode('utf-8')
    
    print(data)
    request = urllib.request.Request(url, data, headers)
    
    response = urllib.request.urlopen(request)
    
    content = response.read().decode('utf-8')
    
    obj = json.loads(content)
    print(obj)

if __name__ == '__main__':
    url = 'https://fanyi.baidu.com/sug'
    data = {'kw': 'spider'}
    main(url, data)