import requests
from bs4 import BeautifulSoup

# 这里使用你需要请求的URL
url = 'http://www.baidu.com'

# 发起请求
response = requests.get(url)

# 获取响应内容
content = response.content

# 使用 BeautifulSoup 解析内容，指定 lxml 解析器
soup = BeautifulSoup(content, 'lxml')

# 打印解析结果
print(soup.prettify())
