
# __VIEWSTATE: BgmygB8+0cJmfxfrot9k/J2A7igdBbOYw3KJxB1VcZoRMmwbl33D1PZ/UoQWm1bSO+Qrip4TkF1hR1OQ0B3NRFWVdEK1iJWxJRx/vPnu0e3nLdMMBDuKnS+NMA9KCUVRaaf11kM4avJrcdZWXQGp2v4AMds=
# __VIEWSTATEGENERATOR: C93BE1AE
# from: https://www.gushiwen.cn/
# email: 296786475@qq.com
# pwd: 2967864751
# code: Gqya
# denglu: 登录
import requests

url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn%2fuse'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}
response = requests.get(url=url, headers=headers)

content = response.text

# print(content)

from bs4 import BeautifulSoup

soup = BeautifulSoup(content, 'lxml')
# 获取 __VIEWSTATE
viewstate = soup.select('#__VIEWSTATE')[0].attrs.get('value')
# 获取 __VIEWSTATEGENERATOR: 
viewstategenerator = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')
# 获取验证码图片
code = soup.select('#imgCode')[0].attrs.get('src')
code_url = 'https://so.gushiwen.cn' + code
print(viewstate)
print(viewstategenerator)
print(code_url)
# 有坑
# import urllib.request
# urllib.request.urlretrieve(url = code_url, filename='code.png')
# requests里有一个方法session() 通过session的返回值 就能使用请求变成一个对象
session = requests.session()
# 验证码的url内容
response_code = session.get(code_url)
# 注意此时要使用二进制数据 因为我们要下载图片
content_code = response_code.content
# wb的模式就是将二进制数据写入到文件
with open('code.png', 'wb') as fp:
    fp.write(content_code)
# 获取了验证码图片后 下载到本地 然后观察验证码输入

code_name = input('请输入您的验证码：')
# 点击登录
url_post = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
data_post = {
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'from': 'https://www.gushiwen.cn/',
    'email': '296786475@qq.com',
    'pwd': '296786475',
    'code': code_name,
    'denglu': '登录'
}

response_post = session.post(url_post, headers=headers, data=data_post)

content_post = response_post.text

with open('gushiwen.html', 'w', encoding='utf-8') as f:
    f.write(content_post)