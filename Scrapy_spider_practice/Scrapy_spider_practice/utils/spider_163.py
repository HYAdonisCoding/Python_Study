# -*- coding: utf-8 -*-

import json
import os
import random
import re
from fake_useragent import UserAgent
import requests

def getUA():
    uaList = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15',
        'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    ]
    User_Agent = random.choice(uaList)
    return User_Agent
    
def get_headers():
    ua = UserAgent().random
    headers = {
        'User-Agent': ua if ua else getUA()
    }
    return headers
def download_mp3():
    url = 'https://m10.music.126.net/20240703095220/81526e2dbb55fce1c6447c62ee099fcf/yyaac/obj/wonDkMOGw6XDiTHCmMOi/3945547514/6c7d/4fb4/2def/e560cfe0e71e462bec4ef8efcdfadb5c.m4a'
    url = 'https://m704.music.126.net/20240703113450/2934cb24662cf52001f84e93f61cee1a/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/17266711921/1541/393f/f4ff/86d26c68acbc6e8c02892334ce8b2274.m4a?authSecret=000001907691e07002170a3b1db51782'
    res = requests.get(url, headers=get_headers())
    with open('诛仙我回来-任贤齐.mp3', 'wb') as f:
        f.write(res.content)
# 函数：下载文件
import os
import re
import requests
from enum import Enum

# 定义支持的文件扩展名
class FileExtension(Enum):
    MP3 = '.mp3'
    MP4 = '.mp4'

# 定义下载函数
def download_file(url, filename, default_extension=FileExtension.MP3):
    try:
        # 清理文件名：去除非法字符
        sanitized_filename = re.sub(r'[\\/*?:"<>|]', '', filename).replace(' ', '')
        
        # 检查并自动添加扩展名
        ext = os.path.splitext(sanitized_filename)[1].lower()  # 提取扩展名
        if ext not in [e.value for e in FileExtension]:
            # 如果没有有效扩展名，添加默认扩展名
            sanitized_filename += default_extension.value
        
        # 下载文件
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # 如果状态码不是 2xx，抛出异常
        
        # 保存文件
        with open(sanitized_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"{sanitized_filename} downloaded successfully")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename}: {e}")
    except Exception as e:
        print(f"Unknown error occurred for {filename}: {e}")
def download_mp4():
    url = 'https://vodkgeyttp8.vod.126.net/cloudmusic/NTA5MTI0OTQ=/a7a08ad10ff1fb471e1deaf0c39d1c6f/a687d1e8d5b8666442e3a838aae044a8.mp4?wsSecret=07339ea812d0917da488ee99f8c8f854&wsTime=1719971177'
    res = requests.get(url, headers=get_headers())
    with open('诛仙我回来-任贤齐.mp4', 'wb') as f:
        f.write(res.content)
if __name__ == '__main__':
    # download_mp3()
    # headers = get_headers()
    # download_mp4()
    # url = 'https://m804.music.126.net/20240703113706/367059ade90c59363d993c850c07a4db/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/12360274338/3350/04dc/06d2/43db43480ec8778ccf618f492a0cf856.m4a?authSecret=000001907693f45807130a3b192fbfde'
    # filename =  '北京雨燕.mp3'
    
    # QQ音乐
    # 数据数组
    data_array = [
        {
            'url': 'https://ws6.stream.qqmusic.qq.com/C400000X5jt70BZa35.m4a?guid=3908283232&vkey=DCDB970C81899F59E328E4DBE2CA54FA8607C526BCF4E3146FE159A1E356FB4FF93BFA75EF5FD4ECDB91CE21D4ED7172456946413ADC1486__v21ea05c8d&uin=296786475&fromtag=120032',
            'filename': '缘分一道桥 - 王力宏'
        },
        {
            'url': 'https://ws6.stream.qqmusic.qq.com/C400000QIgrt2qysUB.m4a?guid=4927833278&vkey=922841ABDB9929EB74888B2533B58D78C83434540F29370D853439BFF15EB3380507A1066039AB8D00C89B2AEC294486C4C95B8C5818AA37__v215192f04&uin=296786475&fromtag=120032',
            'filename': '我们的歌 - 王力宏'
        },
        {
            'url': 'https://ws6.stream.qqmusic.qq.com/C400003tRG6711PfE6.m4a?guid=461609377&vkey=3FF82E4016B48953CAE6F1E9B9E984E72654679172A6E09E5B58005C99682BA56A3A31F980B3515BFFD71E17F50AC481FCEBEFF533734EDD__v2152579bd&uin=296786475&fromtag=120032',
            'filename': '红颜 - 胡彦斌'
        }
    ]

    # 遍历数组并下载文件
    for item in data_array:
        download_file(item['url'], item['filename'])
    print('All Download successfully')