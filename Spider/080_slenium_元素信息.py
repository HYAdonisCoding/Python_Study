#  1. 导入
import time
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

# 4.元素定位
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 根据id来找到对象
button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'su'))
    )
print(button.get_attribute('class'))
print(button.tag_name)
print(button.id)
# 根据名字获取对象的
a = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, '贴吧'))
    )
print(a.text)

time.sleep(3)
browser.quit()