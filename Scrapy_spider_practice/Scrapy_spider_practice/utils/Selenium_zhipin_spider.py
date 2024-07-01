#  1. 导入
import time
from selenium import webdriver
from . import AboutDB


TYPE = '数据分析'
# 创建浏览器操作对象
try:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)# 保持打开
    browser = webdriver.Chrome(options=options)

    #  3. 访问网站
    url = f'https://www.zhipin.com/web/geek/job?query={TYPE}&city=101010100'
    browser.get(url)

    # 4.元素定位
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    max_pages = 10
    for page in range(1, max_pages + 1):
        # 等待页面加载完全
        time.sleep(2)  # 可根据实际情况调整等待时间
        # 根据名字获取对象的
        card = WebDriverWait(browser, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-title clearfix"]/span[@class="job-name"]'))
            )
        print(card)
        # 定义你要抓取的数据的 XPath 路径
        paths = [
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-title clearfix"]/span[@class="job-name"]', 'text'),  # 职位名称
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-title clearfix"]//span[@class="job-area"]', 'text'),  # 地址
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-info clearfix"]/span[@class="salary"]', 'text'),  # 薪资
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-info clearfix"]/ul[@class="tag-list"]', 'li_text'),  # 5-10年本科
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-footer clearfix"]/ul[@class="tag-list"]', 'li_text'),  # Java,SpringCloud,MySQL
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-footer clearfix"]/div[@class="info-desc"]', 'text'),  # 定期体检，节日福利，带薪年假，员工旅游，五险一金，加班补助，年终奖
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-logo"]/a/img', 'src'),  # 公司logo
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/h3/a', 'href'),  # 公司网站链接
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/h3/a', 'text'),  # 公司名称
            ('//div[@class="search-job-result"]//li[@class="job-card-wrapper"]//div[@class="job-card-right"]/div[@class="company-info"]/ul[@class="company-tag-list"]', 'li_text'),  # 互联网未融资100-499人
        ]
        results = []
        for path, attribute in paths:
            try:
                s = []
                elements = WebDriverWait(browser, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, path))
                )

                # 判断返回的是单个元素还是多个元素
                if len(elements) == 0:
                    print(f"No elements found for path: {path}")
                elif len(elements) == 1:
                    element = elements[0]
                    if attribute == 'text':
                        s.append(element.text)
                    else:
                        s.append(element.get_attribute(attribute))
                else:
                    for element in elements:
                        if attribute == 'text':
                            s.append(element.text)
                        elif attribute == 'src' or attribute == 'href':
                            s.append(element.get_attribute(attribute))
                        elif attribute == 'li_text':
                            # 提取所有 li 元素并用 | 分隔内容
                            li_elements = element.find_elements(By.TAG_NAME, 'li')
                            li_texts = [li.text.strip() for li in li_elements if li.text.strip()]  # 使用 strip() 去掉空白字符，并过滤空文本项
                            s.append('|'.join(li_texts))
                results.append(s)
            except Exception as e:
                print(f"Error processing path {path}: {e}")
        
        # 定义一个空列表，用于存放最终的对象
        datas = []

        # 遍历每个元素的索引位置
        for i in range(len(results[0])):
            # 创建一个新的对象字典
            obj = {
                'title': results[0][i],  # 使用第一个子数组的元素作为'title'
                'locations': results[1][i],  # 使用第二个子数组的元素作为'locations'
                'salaries': results[2][i], # 使用第二个子数组的元素作为'salaries'
                'experience_education': results[3][i], # 使用第二个子数组的元素作为'locations'
                'skills': results[4][i], # 使用第二个子数组的元素作为'locations'
                'benefits': results[5][i], # 使用第二个子数组的元素作为'locations'
                'company_logos': results[6][i], # 使用第二个子数组的元素作为'locations'
                'company_href': results[7][i], # 使用第二个子数组的元素作为'locations'
                'company_name': results[8][i], # 使用第二个子数组的元素作为'locations'
                'company_info': results[9][i], # 使用第二个子数组的元素作为'locations'
            }
            # 将创建的对象添加到结果列表中
            datas.append(obj)
        data_tuples = [(TYPE, obj['title'], obj['locations'], obj['salaries'], obj['experience_education'], obj['skills'], obj['benefits'], obj['company_logos'], obj['company_href'], obj['company_name'], obj['company_info']) for obj in datas]
        AboutDB.insert_datas(data_tuples)
        print(f'{TYPE}的第{page}页存储完成，存储了{len(data_tuples)}条数据')
        # 点击下一页按钮（示例，具体操作取决于网页的实现方式） 
        next_page_button = WebDriverWait(browser, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//a/i[@class="ui-icon-arrow-right"]'))
                )
        next_page_button[0].click()
    time.sleep(5)
except Exception as e:
    print('Error processing', e)
finally:
    
    browser.quit()