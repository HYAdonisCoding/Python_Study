from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

path = '/Users/adam/Documents/Developer/environment/chromedriver-mac-arm64/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get("https://we.51job.com/pc/search?jobArea=010000&keyword=iOS&searchType=2&sortType=0&metro=&pageNum=1")
time.sleep(20)

job_list = driver.find_elements("xpath", '//*[@id="app"]/div//div[@class="joblist-item-job-wrapper"]')
print('职位数：', len(job_list))

driver.quit()