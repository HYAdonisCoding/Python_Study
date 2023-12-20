import urllib.request, urllib.parse, urllib.error
import certifi
import ssl

# get
response = urllib.request.urlopen("http://httpbin.org/get")
# print(response.read().decode('utf-8'), timeout= 0.01)

response.status

# post
# url = 'http://httpbin.org/post'
# data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
# response = urllib.request.urlopen(url, data=data)
# print(response.read().decode('utf-8'))

url = "https://movie.douban.com/top250"
headers = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Cookie": "bid=6V3OXSc6jgU; _pk_id.100001.4cf6=95aaa198f3a792d6.1703039542.; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __yadk_uid=JPWzueMBuDoU6mevtZMgd6UxMXfSCzr2; __utma=30149280.1470670587.1703039544.1703039544.1703039544.1; __utmb=30149280.0.10.1703039544; __utmc=30149280; __utmz=30149280.1703039544.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.705131127.1703039544.1703039544.1703039544.1; __utmb=223695111.0.10.1703039544; __utmc=223695111; __utmz=223695111.1703039544.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    # "DNT": "1",
    # "Host": "movie.douban.com",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    # "sec-ch-ua-mobile": "?0",
    # "sec-ch-ua-platform": '"macOS"',
    }

try:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    req = urllib.request.Request(url, headers=headers)
    
    response = urllib.request.urlopen(req, context=ssl_context)
    print(response.read().decode('utf-8', errors='replace'))
    # 处理响应的代码
except Exception as e:
    print(f"Error: {e}")