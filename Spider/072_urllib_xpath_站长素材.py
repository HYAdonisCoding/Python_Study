# -*- coding: utf-8 -*-

import json
import os
import random
import ssl
from lxml import etree
import certifi
import urllib.request
import requests

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'



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
    
        
# 下载图片
def downloaded_file(filename, url):
    
    image_file = current_directory + 'sc/' + filename + '.jpg'
    url =  'https:' + url
    # print('Downloading file...', filename, url)
    # # 使用urllib.request.urlretrieve方法下载文件  
    # try:  
    #     urllib.request.urlretrieve(url, image_file)  
    #     print(f'图片已成功下载到 {image_file}')  
    # except urllib.error.HTTPError as e:  
    #     print(f'HTTP Error: {e.code} {e.reason}')  
    # except urllib.error.URLError as e:  
    #     print(f'URL Error: {e.reason}')  
    # except Exception as e:  
    #     print(f'An error occurred: {e}')
    try:  
        response = requests.get(url, stream=True)  
        response.raise_for_status()  # 如果请求失败，这将引发HTTPError异常  
        with open(image_file, 'wb') as file:  
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)  
        print(f'图片已成功下载到 {image_file}')  
    except requests.exceptions.HTTPError as e:  
        print(f'HTTP Error: {e}')  
    except requests.exceptions.RequestException as e:  
        print(f'An error occurred: {e}')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def test():
    downloaded_file('纹身美女练瑜伽图片','//scpic1.chinaz.net\\Files\\pic\\pic9\\202008/apic27320_s_w285.jpg')
if __name__ == '__main__':
    # parse_local_file()
    # https://sc.chinaz.com/tu/meinv.html
    # https://sc.chinaz.com/tu/meinv-2-0-0.html
    # https://sc.chinaz.com/tu/meinv-3-0-0.html
    # //div/a/img/@alt
    # //div/a/img/@data-src
    start = int(input('请输入起始页码：'))
    end = int(input('请输入结束页码：'))
    for item in range(start, end+1):
        url = 'https://sc.chinaz.com/tu/meinv.html'
        if item > 1 :
            url = f'https://sc.chinaz.com/tu/meinv-{item}-0-0.html'
            
        print(url)
        
        result = send_get_request(url, headers)
        
        tree = etree.HTML(result)
        name_list = tree.xpath('//div[@class="new_block"]//a/img/@alt')
        src_list = tree.xpath('//div[@class="new_block"]//a/img/@data-src')
        print(name_list, len(name_list))
        print(src_list, len(src_list))
        for idx, item in enumerate(src_list):
            
            downloaded_file(name_list[idx], item)
    