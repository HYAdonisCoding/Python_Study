
from selenium import webdriver

path = '/Users/adam/Documents/Developer/environment/phantomjs-2.1.1-macosx/bin/phantomjs'

# 创建 PhantomJS WebDriver
driver = webdriver.PhantomJS(executable_path=path)

# 设置窗口大小（可选）
driver.set_window_size(1920, 1080)

# 打开网页
driver.get('https://www.example.com')

# 输出网页标题
print(driver.title)
driver.save_screenshot('baidu.png')
# 关闭浏览器
driver.quit()

