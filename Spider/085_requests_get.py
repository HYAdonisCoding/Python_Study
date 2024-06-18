
# urllib
# 1. 一个类型和六个方法
# 2. get请求
# 3. Post请求 百度翻译
# 4. ajax的get请求
# 5. ajax的post请求
# 6. cookie登录 微博
# 7. 代理

# requests
# 1. 一个类型和六个属性
# 2. get请求
# 3. Post请求 
# 4. 代理
# 5. cookie验证码

import requests

url = 'https://www.baidu.com/s'
headers = {
    'Accept': '*/*',
    # # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Connection': 'keep-alive',
    'Cookie': 'BIDUPSID=F01E32202B282770C372730340F0BE6D; PSTM=1718693729; BAIDUID=F01E32202B282770177C3B572A67C3E1:FG=1; H_PS_PSSID=60327_60334_60345; BD_HOME=1; BD_UPN=123253; BA_HECTOR=80al8h0h0ga48420058kak0g0p3c201j72br41v; BAIDUID_BFESS=F01E32202B282770177C3B572A67C3E1:FG=1; ZFY=mT2uAmbes1o4cd4a4WDLTJVIKKVGXJIFcWscaEL8h2Q:C; BD_CK_SAM=1; PSINO=1; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; ab_sr=1.0.1_ZGVjYmQ3ZGQ1MWYxMzdjOTQ1NTc2MTU5N2I5NGE3ZWQ5MTI1YTRmYjk1YTcwMDFmZmUxZjkwNWNlYmE3MWZiYzA3N2IxODFkODZmNjU1NzJiNGIxYWUzMmE1Y2EyNGQwYTdiMWYyNjZlM2Q3ODQ4NGJiODgwMTg5ODVkYTAyODhlZmU4NmZkZmFkMTIwNGFhODYwYjRiMjUxNDljNDk1OA==; H_PS_645EC=5f5c7xIXDPJ8GcLksbTYSewBYjYTqtaW19r4wAMvhwunymcq7RYEY6mz5lY; BDSVRTM=716; WWW_ST=1718694670359',   'Dnt': '1',
    'Host': 'www.baidu.com',
    # 'Is_pbs': '%E5%8C%97%E4%BA%AC',
    # 'Is_referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%8C%97%E4%BA%AC&fenlei=256&oq=%25E7%2599%25BE%25E5%25BA%25A6%25E7%25BF%25BB%25E8%25AF%2591&rsv_pq=8d8b5d30005f50b8&rsv_t=66d6mLttsXQKOZ2dztCHYuynpmgpmrDbdW4umxwnFMOfHDyzRGUI7YB%2FO5Y&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_btype=t&inputT=5605&rsv_sug3=23&rsv_sug1=27&rsv_sug7=100&rsv_sug2=0&rsv_sug4=5605&bs=%E7%99%BE%E5%BA%A6%E7%BF%BB%E8%AF%91',
    # 'Is_xhr': '1',
    # 'Ps-Dataurlconfigqid': '0xe41e236500027559',
    'Referer': 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E5%8C%97%E4%BA%AC&fenlei=256&oq=%25E5%258C%2597%25E4%25BA%25AC&rsv_pq=a5b95eb2003df8c5&rsv_t=1fd6sf1U4g0Uiw5oVbwdaRFsqF%2FtFIMbkAmwPHQMS0dd2x7NNvEuskna18c&rqlang=cn&rsv_enter=0&rsv_dl=tb&rsv_btype=t',
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
    'wd': '北京'
}
response = requests.get(url=url, params=data, headers=headers)


# 设置响应的编码格式
response.encoding = 'utf-8'


# 以字符串形式来返回网页的源码
print(response.text[:1000])
print(len(response.text))
print(response.status_code)
# 总结：
# 参数使用params传递
# 参数无需urlencode编码
# 不需要请求对象的定制
# 请求资源路径中的？可以加也可以不加