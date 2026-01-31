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

        # 1. 首先去除系统非法字符
        sanitized_filename = re.sub(r'[\\/*?:"<>|]', '', filename)

        # 2. 判断是否包含中文字符
        # 如果包含中文，则执行去除空格的操作
        if re.search(r'[\u4e00-\u9fa5]', sanitized_filename):
            sanitized_filename = sanitized_filename.replace(' ', '')
        
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
            'url': 'https://m804.music.126.net/20260131214520/ba9cf3ea1ca596796bf51a7a88c17eef/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/29344086099/fcf2/19aa/952e/b72653f2be7a36570f3cf424e7b83097.m4a?vuutv=i2n4TpD6maBp4U1dNUYTGvSNGXzag3npqC2ugrEu1Yd1kZhwUJJvqD0i3JP8bZPTotqLjAbKabftl98i/zd/lsqky3V0AhHKa+SDpRAGV/c=&authSecret=0000019c14362d271d9f0a3b18170d64&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': 'Yesterday Once More'
        },
        {
            'url': 'https://m804.music.126.net/20260131214838/127cab2b78bb40913cdf505a05008d98/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/18712801509/518a/4407/9fbc/555f890bacbb9a179dc0d5d785ab6520.m4a?vuutv=GGi2knBFt2/seqggDuo2tZKhznq/D3Hv9wupaR3hzzIxKe9kj2JqWxlIrgyitTT0nYR5NgCdfR5TCX+fnPEE9Dwc9C4glEi8GDaT85m29sU=&authSecret=0000019c14392fbd073f0aaf79b40006&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': 'The Day You Went Away'
        },
        {
            'url': 'https://m804.music.126.net/20260131215114/05865da483c56f341b407c85c5ee7593/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/22259852866/2e6d/a20d/6ad6/cfab44cef6e266202668709544527487.m4a?vuutv=RaQdBY8MzudV72vlYN/n28L9u1fpiuLpJBDdFrSWz4gExSKW+DQvTYygRPjQbdMqN+T1TLRQ8ubijC1Ex+3tXwMg4fucHNjsuwhmNz+08lI=&authSecret=0000019c143b91151b660a3b22fd23b7&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': 'Because of You'
        },
        {
            'url': 'https://m704.music.126.net/20260131215300/7a77eb5b5d70e8f062d15d27fdbb17a5/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/24757137791/e634/235d/587d/7fce3d0a36652bc98d292f5b61ac0a32.m4a?vuutv=wwcmmt6gvIwyKw11sNreEUyaeiaQtVy7g0oOB09MOuaJrRKO+CecDUSOFXI/Fw4rbbAAss79UnWUncvKVU3tkJcywkC9mu/Qz+f58db+Yu0=&authSecret=0000019c143d32591d700a3b21321dab&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': 'My Stupid Heart (Kids Version)'
        },
        {
            'url': 'https://m704.music.126.net/20260131215539/f530caf34ef0bc730457b71b354cf4a2/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/25981403000/ab63/ba51/dc2d/a767429c84d3854f0dc5edf32a20f9ac.m4a?vuutv=7xCJT3UbnAe0vFa/4hVUh6rCdBhANF+lDxw3Zb+QgiZpKmOVGnnHunZgzjKpeBqupa0mmXNC3tuzSZW7siQ98yf2EMKb4YaDwLaIEp2UDiA=&authSecret=0000019c143f9d0c1bfa0a3b1be403c9&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': 'Take Me to Your Heart'
        },
        {
            'url': 'https://m704.music.126.net/20260131215650/1dea6ed6d44a418993d4113c5bb1ac47/jdyyaac/obj/w5rDlsOJwrLDjj7CmsOj/16717793379/2774/0015/bb1a/90f6d0e070661fa4f5f3e3af2be83fae.m4a?vuutv=M/+7+aVxkHjVvGmUPDqyMY+GB8PggzYPcqJ+DYoPpCorNl1DlYA3Gpeu28K0uHVecAkORUudXGEdqYusXlHjNVxSY2SOTzW9I6wY5z6IEOs=&authSecret=0000019c1440b31315d00a3b23f401b5&cdntag=bWFyaz1vc193ZWIscXVhbGl0eV9leGhpZ2g',
            'filename': '我爱祖国的蓝天'
        },
    ]

    # 遍历数组并下载文件
    for item in data_array:
        download_file(item['url'], item['filename'])
    print('All Download successfully')