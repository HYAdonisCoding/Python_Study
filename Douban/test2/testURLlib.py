import urllib.request,urllib.parse

# get
response = urllib.request.urlopen("http://httpbin.org/get")
# print(response.read().decode('utf-8'), timeout= 0.01)

response.status

# post
# url = 'http://httpbin.org/post'
# data = bytes(urllib.parse.urlencode({'hello': 'world'}), encoding='utf-8')
# response = urllib.request.urlopen(url, data=data)
# print(response.read().decode('utf-8'))

url = "http://www.douban.com"
headers = {
    'Accept': 'application/json',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    }
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))