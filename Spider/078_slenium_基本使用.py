#  1. 导入
from selenium import webdriver

# 创建浏览器操作对象
# path = '/Users/adam/Documents/Developer/environment/chromedriver-mac-x64_123/chromedriver'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)# 保持打开
browser = webdriver.Chrome(options=options)

#  3. 访问网站
url = 'https://www.baidu.com'
# url = 'https://www.jingdong.com'
browser.get(url)
