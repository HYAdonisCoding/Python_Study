from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def share_browser():
    # 创建 ChromeOptions 对象
    chrome_options = Options()

    # 设置 Chrome 以无头模式启动
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')  # 禁用 GPU 加速

    # 创建 Chrome WebDriver 对象，传入 ChromeOptions 对象
    browser = webdriver.Chrome(options=chrome_options)
    return browser

browser = share_browser()

# 访问网页示例（这里访问百度）
browser.get('https://www.baidu.com/')

# 打印页面标题
print(browser.title)
# browser.save_screenshot('baidu.png')
# 关闭浏览器
browser.quit()
