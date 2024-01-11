# -*- coding: utf-8 -*-
import os
import ssl
import urllib.request
import urllib.parse
import certifi
import json

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/data/'

def getPageData(url):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    # 1.请求对象的定制
    request = urllib.request.Request(url=url, headers=headers)
    # 2.获取想要的数据
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    # 3.数据下载到本地
    # open默认gbk编码
    # fp = open(current_directory+'douban1.json', 'w', encoding='utf-8')
    # fp.write(content)
    
    with open(current_directory+'douban1_1.json', 'w', encoding='utf-8') as fp:
        fp.write(content)
    

def postMethod(url, data):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)

    
    headers = {
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Acs-Token': '1704885023483_1704957569096_vuQqbL2TTjRc+s0ucPGz2+nNwoY+kbSCNNxaKgDXThfvmWS/ntwgN1j1qiMNcsS+juIx3nd36Kiyn71InrDZUCeao7vOtB7a2+zyGcCdMtFq8UfvncoOudNeYOLiOGwEAkUH5oD6VKkItIURBaqkj74poGTug7HgJYHMStHpyVsTrrK/bZHte61eJzaPc9XZEtid7uNc1TbY6caCcxgKJx25t+hKXapbnWTEAz3y08T2Ng1Kh5ytiTODnDpE1v3jA4hz2Rrxo/LPu9fNSOrH8EfNSMoArSCeihx7BnsQuQGxTA+Iz+Z8wOA7uzXhPdyG+AKT3J+I2pQpa0sR4jVTr+UEESN7QDaZ5y+kRbQymg6qNFzlBlg356F03GWPO01/n6p/xnakScL9wlUIAmibNv48u8YIF/3ssYPgRhtniCOMORWAYU1hEu1N4JfUWc+YY33f8tu7HzP0tCjZdB3F0zzszzbT78WoIhkv1d+NFSA=',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '154',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'BIDUPSID=6243585BCB9EDE811A9A0DD5F8580571; PSTM=1704957519; BAIDUID=6243585BCB9EDE81BEA4AE0501218D45:FG=1; H_PS_PSSID=39997_40079_39938; BAIDUID_BFESS=6243585BCB9EDE81BEA4AE0501218D45:FG=1; BA_HECTOR=2ga00180a0210g810l2481253gqk901ipv5ig1t; ZFY=bSskR0Z6zBKGLo:APHEMDoAXwAW:AshaMuWnFsmCVfSuw:C; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; PSINO=1; delPer=0; RT="z=1&dm=baidu.com&si=nmfh0z58i9h&ss=lr8vp2m3&sl=0&tt=0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=l6&hd=n1"; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1704957556; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1704957556; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_M2RhZjdmMGZiYjZkMjY0MzU3MTRkZTJkZjdlMGQxN2M2MWU5NGZmMmUzZDdlNjk1ODBjZjYyNzFhY2EzMDkwMjU2YTYxOTVlYWIyMDk0Zjk2NzFmMWRiZGJiMjk1NTcxZjI4OTkxOTM5NjM0YzE1MTFjZTFlOTFmYjFhNjUwMDJjYzU3ODdmMzg5ZTY5YWIwOWE4ZDY4NDg2MWQyNjI5YQ==',
        # 'DNT': '1',
        # 'Host': 'fanyi.baidu.com',
        # 'Origin': 'https://fanyi.baidu.com',
        # 'Referer': 'https://fanyi.baidu.com/',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"macOS"',
        'Cookie': 'BIDUPSID=6243585BCB9EDE811A9A0DD5F8580571; PSTM=1704957519; BAIDUID=6243585BCB9EDE81BEA4AE0501218D45:FG=1; H_PS_PSSID=39997_40079_39938; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1704957556; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1704957556; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; ab_sr=1.0.1_M2RhZjdmMGZiYjZkMjY0MzU3MTRkZTJkZjdlMGQxN2M2MWU5NGZmMmUzZDdlNjk1ODBjZjYyNzFhY2EzMDkwMjU2YTYxOTVlYWIyMDk0Zjk2NzFmMWRiZGJiMjk1NTcxZjI4OTkxOTM5NjM0YzE1MTFjZTFlOTFmYjFhNjUwMDJjYzU3ODdmMzg5ZTY5YWIwOWE4ZDY4NDg2MWQyNjI5YQ==; BA_HECTOR=a1agah000h85ag2g812ka421fdtbrn1ipv7uo1s; BAIDUID_BFESS=6243585BCB9EDE81BEA4AE0501218D45:FG=1; ZFY=bSskR0Z6zBKGLo:APHEMDoAXwAW:AshaMuWnFsmCVfSuw:C; delPer=0; PSINO=1',
    }
    
    
    # post请求的参数必须编码
    data = urllib.parse.urlencode(data).encode('utf-8')
    
    print(data)
    request = urllib.request.Request(url, data, headers)
    
    response = urllib.request.urlopen(request)
    
    content = response.read().decode('utf-8')
    
    obj = json.loads(content)
    print(obj)
def create_request(page):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    # 创建一个包含自定义 SSL 上下文的 opener
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    base_url = 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    data = {
        'cname': '北京',
        'pid': '',
        'pageIndex': page,
        'pageSize': '10',
    }
    data = urllib.parse.urlencode(data).encode('utf-8')
    url = base_url
    # 1.请求对象的定制
    request = urllib.request.Request(url=url, headers=headers, data=data)
    return request

def get_content(request):
    # 2.获取想要的数据
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content

def down_load(content, page):
    # 3.数据下载到本地
    with open(current_directory+'kfc_'+ str(page)+'.json', 'w', encoding='utf-8') as fp:
         fp.write(content)
def start():
    start_page = int(input('请输入起始页码:'))
    end_page = int(input('请输入结束页码:'))
    for page in range(start_page, end_page+1):
        request = create_request(page)
        
        content = get_content(request)
        
        down_load(content, page)

if __name__ == '__main__':
    
    start()
    # 'https://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
