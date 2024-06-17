#  1. 导入
from selenium import webdriver

# 创建浏览器操作对象
# path = '/Users/adam/Documents/Developer/environment/chromedriver-mac-x64_123/chromedriver'
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)# 保持打开
browser = webdriver.Chrome(options=options)

#  3. 访问网站
url = 'https://www.baidu.com'

browser.get(url)
import time
time.sleep(2)

# 4.元素定位
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 获取文本框的对象
input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'kw'))
    )
input.send_keys('周杰伦')

time.sleep(2)

# 获取百度一下的按钮
button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'su'))
    )
button.click()

time.sleep(2)

# 滑动到底部
js_bottom = 'document.documentElement.scrollTop=100000'
browser.execute_script(js_bottom)

time.sleep(2)

# 获取下一页的按钮
nextBtn = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@class="n"]'))
    )
nextBtn.click()

time.sleep(2)

# 回到上一页
browser.back()
time.sleep(2)

# 回去
browser.forward()
time.sleep(5)

browser.quit()