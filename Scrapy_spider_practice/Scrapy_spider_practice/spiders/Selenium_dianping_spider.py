#  1. 导入
import time
from selenium import webdriver
# 定义你要抓取的数据的 XPath 路径
# paths = [
#             ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li', 'li'), # 内容
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="tit"]/a/@title', 'text'),  # 名称
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="tit"]/a[1]/@href', 'text'),  # 链接
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="comment"]/a[1]/b', 'text'),  # 评价条数
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="comment"]/a[2]/b', 'text'),  # 人均消费￥89
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="tag-addr"]/a[1]/span', 'text'),  # 菜系
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="tag-addr"]/a[2]/span', 'text'),  # 地址
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="recommend"]/a', 'a_text'),  # 推荐菜
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="svr-info"]//a[2]/span', 'text'),  # 团购标签 可能没有
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="svr-info"]//a[2]/span', 'text'),  # 团购标签 可能没有
#             # ('//div[@class="shop-list J_shop-list shop-all-list"]/ul/li//div[@class="svr-info"]', 'text'),  # 团购标签 可能没有
#         ]
# # 尝试获取div[@class="svr-info"]
# try:
#     svr_info_elements = element.find_elements(By.XPATH, './/div[@class="svr-info"]')
#     for info in svr_info_elements:
#         info_string = info.find_element(By.XPATH, './div/a[2]/span/text()')
#         print(info_string)
#         info_string1 = info.find_element(By.XPATH, './a/span/text()')
#         print(info_string, info_string1)
# except Exception:
#     svr_info_text = None
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 保持浏览器打开
    try:
        browser = webdriver.Chrome(options=options)
        return browser
    except Exception as e:
        print(f"Error initializing ChromeDriver: {e}")
        return None

def fetch_page(browser, url):
    try:
        browser.get(url)
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")

def extract_elements(browser, path):
    try:
        elements = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, path))
        )
        return elements
    except Exception as e:
        print(f"Error extracting elements with path {path}: {e}")
        return []

def extract_data_from_elements(elements):
    data_list = []
    for element in elements:
        try:
            # 获取div[@class="tit"]下的第一个a标签的href
            tit_element = element.find_element(By.XPATH, './/div[@class="tit"]/a[1]')
            title = tit_element.get_attribute('title')
            href = tit_element.get_attribute('href')
            comment = element.find_element(By.XPATH, './/div[@class="comment"]/a[1]/b')
            comments = comment.text
            average = element.find_element(By.XPATH, './/div[@class="comment"]/a[2]/b')
            averages = average.text
            # 菜系
            style = element.find_element(By.XPATH, './/div[@class="tag-addr"]/a[1]/span')
            styles = style.text
            # 地址
            addr = element.find_element(By.XPATH, './/div[@class="tag-addr"]/a[2]/span')
            addrs = addr.text
            # 推荐菜
            recommend_elements = element.find_elements(By.XPATH, './/div[@class="recommend"]/a')
            
            # 提取所有 a 标签的非空文本并用 | 分隔
            recommends = '|'.join([recommend.text for recommend in recommend_elements if recommend.text.strip()])
            # print(recommends)
            
            # 尝试获取div[@class="svr-info"] 团购： 优惠：
            group = 0
            discounts = 0
            try:
                # svr_info_elements = element.find_element(By.XPATH, './/div[@class="svr-info"]')
                svr_info_element = WebDriverWait(element, 10).until(
                    EC.presence_of_element_located((By.XPATH, './/div[@class="svr-info"]'))
                )
                # 查找 a[2]/span 子元素并处理
                group_elements = svr_info_element.find_elements(By.XPATH, './/a[2]/span')
                print(group_elements)
                for elem in group_elements:
                    if elem.text == '团购：':
                        group = 1
                        break
                    elif elem.text == '优惠：':
                        discounts = 1
                        break

                # 查找 a/span 子元素并处理
                discount_elements = svr_info_element.find_elements(By.XPATH, './a/span')
                print(discount_elements)
                for elem in discount_elements:
                    if elem.text == '团购：':
                        group = 1
                        break
                    elif elem.text == '优惠：':
                        discounts = 1
                        break
            except Exception as e:
                svr_info_text = None
                print('svr_info_text is none!')

            data_list.append({'title':title,'href': href,'comments':comments,'averages':averages,'styles':styles,'addrs':addrs,'recommends':recommends, 'group': group,'discounts':discounts})

        except Exception as e:
            print(f"Error processing element: {e}")
    return data_list

if __name__ == '__main__':
    # 主程序
    url = 'https://www.dianping.com/beijing/ch10'  # 替换为你的目标网站
    path = '//div[@class="shop-list J_shop-list shop-all-list"]/ul/li'

    browser = initialize_browser()
    if browser:
        fetch_page(browser, url)
        
        elements = extract_elements(browser, path)
        data = extract_data_from_elements(elements)
        #  //a[@class="next"]
        print(data)

        browser.quit()
'''
jsons = [
{'title': '逗思都吃韩国料理(五道口店)', 'href': 'https://www.dianping.com/shop/H3SyNUSShP5BYm87', 'comments': '12562', 'averages': '￥89', 'styles': '韩国料理', 'addrs': '五道口', 'recommends': '自制金枪鱼饭团|奶酪辣鸡|部队火锅', 'group': 1, 'discounts': 0}, 
{'title': '北京宜宾招待所(南翠花街店)', 'href': 'https://www.dianping.com/shop/G9B5lBAWimhGRPnh', 'comments': '26280', 'averages': '￥116', 'styles': '川菜馆', 'addrs': '宣武门', 'recommends': '红糖冰粉|面壁思过桌位|蒜泥白肉', 'group': 0, 'discounts': 0}, 
{'title': '浩海火烧云傣家菜(京广店)', 'href': 'https://www.dianping.com/shop/k6ASsfEU2GWeDmTk', 'comments': '25344', 'averages': '￥103', 'styles': '云南菜|滇菜', 'addrs': '朝阳公园/团结湖', 'recommends': '油焖鸡|黑三剁|虾饼', 'group': 0, 'discounts': 0}, 
{'title': 'The Cheesecake Factory 芝乐坊餐厅(王府中環店)', 'href': 'https://www.dianping.com/shop/l9qGXZvHDjAHzDkB', 'comments': '23325', 'averages': '￥206', 'styles': '西餐', 'addrs': '王府井/东单', 'recommends': '鲜草莓芝士蛋糕|红丝绒芝士蛋糕|虾和鸡肉杂烩浓汤饭', 'group': 0, 'discounts': 0}, 
{'title': '铃木食堂(杨梅竹店)', 'href': 'https://www.dianping.com/shop/l4RMiRJoi6FBJ4v4', 'comments': '13461', 'averages': '￥96', 'styles': '日本料理', 'addrs': '前门/大栅栏', 'recommends': '日式牛肉火锅|杏仁豆腐|铃木肉饼', 'group': 1, 'discounts': 0}, 
{'title': '聚宝源(牛街总店)', 'href': 'https://www.dianping.com/shop/Enk0gTkqu0Cyj7Ch', 'comments': '46105', 'averages': '￥118', 'styles': '老北京火锅', 'addrs': '牛街', 'recommends': '手切鲜羊肉|一品烧饼|涮羊肉', 'group': 1, 'discounts': 0}, 
{'title': 'Q MEX 库迈墨西哥餐吧(三里屯店)', 'href': 'https://www.dianping.com/shop/H5B4OsRxDyVni3Oj', 'comments': '16548', 'averages': '￥145', 'styles': '西餐', 'addrs': '三里屯/工体', 'recommends': '加州风格墨西哥卷|鲜虾脆皮塔可|taco', 'group': 1, 'discounts': 1}, 
{'title': '四季民福烤鸭店(东四十条店)', 'href': 'https://www.dianping.com/shop/l3AK2xTtKoddz7SD', 'comments': '25120', 'averages': '￥176', 'styles': '烤鸭', 'addrs': '东四十条', 'recommends': '酥香嫩烤鸭|贝勒烤肉|巧拌豆苗', 'group': 1, 'discounts': 0}, 
{'title': '南门涮肉(国贸商城店)', 'href': 'https://www.dianping.com/shop/l7TjgjzVZS6j8830', 'comments': '11035', 'averages': '￥131', 'styles': '老北京火锅', 'addrs': '国贸/建外', 'recommends': '麻酱小料|自制烧饼|鲜羊肉', 'group': 0, 'discounts': 0}, 
{'title': '蘇飯', 'href': 'https://www.dianping.com/shop/FgiEMOYJ7kJYn7cs', 'comments': '3814', 'averages': '￥99', 'styles': '私房菜', 'addrs': '三里屯/工体', 'recommends': '赛螃蟹|红烧肉|自制坚果酸奶', 'group': 0, 'discounts': 0}, 
{'title': 'Bada kitchen 和风洋食(中关村店)', 'href': 'https://www.dianping.com/shop/j6rTOedDbGNsLVFd', 'comments': '13746', 'averages': '￥125', 'styles': '日本料理', 'addrs': '中关村', 'recommends': '嫩滑蛋包咖喱饭|猪肉奶酪紫苏卷|奶酪厚蛋烧', 'group': 0, 'discounts': 0}, 
{'title': '南门涮肉(东单店)', 'href': 'https://www.dianping.com/shop/G3ZxMJTDLITGsxLX', 'comments': '17045', 'averages': '￥127', 'styles': '老北京火锅', 'addrs': '王府井/东单', 'recommends': '小料双拼|自制烧饼|糖蒜', 'group': 1, 'discounts': 0}, 
{'title': '第六季自助餐厅(王府井店)', 'href': 'https://www.dianping.com/shop/Gal9XcTwxoOi24CH', 'comments': '37166', 'averages': '￥349', 'styles': '自助餐', 'addrs': '王府井/东单', 'recommends': '鲜活鲍鱼|海南空运水果|香煎三文鱼', 'group': 1, 'discounts': 0}, 
{'title': 'THE TACO BAR(三里屯店)', 'href': 'https://www.dianping.com/shop/l7F7wWC2wuZEFVwA', 'comments': '8529', 'averages': '￥135', 'styles': '西餐', 'addrs': '三里屯/工体', 'recommends': '玉米片牛油果|外国佬taco|牛肉Taco', 'group': 1, 'discounts': 1}, 
{'title': '泓0871臻选云南菜', 'href': 'https://www.dianping.com/shop/l3DBZMWaKcU0BmaV', 'comments': '3938', 'averages': '￥292', 'styles': '云南菜|滇菜', 'addrs': '双桥', 'recommends': '招牌破酥包|三年金钱火腿配大理手撕乳扇|腾冲土锅子', 'group': 1, 'discounts': 1}]
'''