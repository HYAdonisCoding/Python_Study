import requests

url = 'http://www.baidu.com/s'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

data = {
    'wd': 'ip'
}
proxies = {
    # 'http': '58.20.248.139:9002'
    'http': '198.44.255.3:80'
}
response = requests.get(url=url, params=data, headers=headers, proxies=proxies)

content = response.text
print(response.status_code)
with open('daili.html', 'w', encoding='utf-8') as f:
    f.write(content)
