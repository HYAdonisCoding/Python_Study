# import requests
# from bs4 import BeautifulSoup

# # 这里使用你需要请求的URL
# url = 'http://www.baidu.com'

# # 发起请求
# response = requests.get(url)

# # 获取响应内容
# content = response.content

# # 使用 BeautifulSoup 解析内容，指定 lxml 解析器
# soup = BeautifulSoup(content, 'lxml')

# # 打印解析结果
# print(soup.prettify())

#!/usr/bin/env python
# coding:utf-8
import os
import requests
from hashlib import md5
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    with open('chaojiying_mm', 'r', encoding='utf-8') as f:
        chaojiying_mm = f.read()
    chaojiying = Chaojiying_Client('EasonAdam', chaojiying_mm, '961251')	#用户中心>>软件ID 生成一个替换 96001
    im = open(current_directory+'a.jpg', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    print(chaojiying.PostPic(im, 1902))		
    #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    print(chaojiying.PostPic(im, 1902).get('pic_str'))	
    #print chaojiying.PostPic(base64_str, 1902)  #此处为传入 base64代码

