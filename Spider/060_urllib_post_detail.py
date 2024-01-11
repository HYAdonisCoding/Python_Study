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

if __name__ == '__main__':
    url = 'https://fanyi.baidu.com/v2transapi?from=srp&to=zh'
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
    main(url, data)