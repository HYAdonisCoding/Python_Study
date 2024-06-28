# -*- coding: utf-8 -*-

import urllib.parse  
import json
import AboutDB

class ScrapySpiderPracticeItem(dict):
    def __init__(self, *args, **kwargs):
        super(ScrapySpiderPracticeItem, self).__init__(*args, **kwargs)
        self.__dict__ = self
# import xzqh

def encoded(chinese_text):
    # 要编码的汉字字符串  
    
    # 使用quote函数进行URL编码  
    # 使用 urllib.parse.quote 进行编码
    encoded_string = urllib.parse.quote(chinese_text.encode("gb2312"))
    # print(encoded_string)
    return encoded_string

def decode(encoded_text):
    # 先进行 URL 解码
    decoded_bytes = urllib.parse.unquote_to_bytes(encoded_text)
    # 再用 GB2312 解码
    decoded_text = decoded_bytes.decode("gb2312")

    print(decoded_text)
    return decoded_text

def city_urls():
    
    
    cities = [
        "北京市（京）",
        "天津市（津）",
        "河北省（冀）",
        "山西省（晋）",
        "内蒙古自治区（内蒙古）",
        "辽宁省（辽）",
        "吉林省（吉）",
        "黑龙江省（黑）",
        "上海市（沪）",
        "江苏省（苏）",
        "浙江省（浙）",
        "安徽省（皖）",
        "福建省（闽）",
        "江西省（赣）",
        "山东省（鲁）",
        "河南省（豫）",
        "湖北省（鄂）",
        "湖南省（湘）",
        "广东省（粤）",
        "广西壮族自治区（桂）",
        "海南省（琼）",
        "重庆市（渝）",
        "四川省（川、蜀）",
        "贵州省（黔、贵）",
        "云南省（滇、云）",
        "西藏自治区（藏）",
        "陕西省（陕、秦）",
        "甘肃省（甘、陇）",
        "青海省（青）",
        "宁夏回族自治区（宁）",
        "新疆维吾尔自治区（新）",
        "香港特别行政区（港）",
        "澳门特别行政区（澳）",
        "台湾省（台）",
    ]
    print(len(cities))
    urls = []
    for city in cities:
        enc = encoded(city)
        # 使用三引号字符串来处理换行符，并添加注释
        URL = f'"http://xzqh.mca.gov.cn/defaultQuery?shengji={enc}&diji=-1&xianji=-1", # {city}\n'
        urls.append(URL)
    # 使用join方法将列表中的URL连接成一个字符串，并在每个URL后添加换行符
    result = "".join(urls)

    # 打印结果
    print(result)
    """
    "http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%A3%A8%BE%A9%A3%A9&diji=-1&xianji=-1 # 北京市（京）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%EC%BD%F2%CA%D0%A3%A8%BD%F2%A3%A9&diji=-1&xianji=-1 # 天津市（津）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1 # 河北省（冀）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%BD%CE%F7%CA%A1%A3%A8%BD%FA%A3%A9&diji=-1&xianji=-1 # 山西省（晋）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C4%DA%C3%C9%B9%C5%D7%D4%D6%CE%C7%F8%A3%A8%C4%DA%C3%C9%B9%C5%A3%A9&diji=-1&xianji=-1 # 内蒙古自治区（内蒙古）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C1%C9%C4%FE%CA%A1%A3%A8%C1%C9%A3%A9&diji=-1&xianji=-1 # 辽宁省（辽）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BC%AA%C1%D6%CA%A1%A3%A8%BC%AA%A3%A9&diji=-1&xianji=-1 # 吉林省（吉）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%DA%C1%FA%BD%AD%CA%A1%A3%A8%BA%DA%A3%A9&diji=-1&xianji=-1 # 黑龙江省（黑）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%CF%BA%A3%CA%D0%A3%A8%BB%A6%A3%A9&diji=-1&xianji=-1 # 上海市（沪）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BD%AD%CB%D5%CA%A1%A3%A8%CB%D5%A3%A9&diji=-1&xianji=-1 # 江苏省（苏）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%D5%E3%BD%AD%CA%A1%A3%A8%D5%E3%A3%A9&diji=-1&xianji=-1 # 浙江省（浙）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B0%B2%BB%D5%CA%A1%A3%A8%CD%EE%A3%A9&diji=-1&xianji=-1 # 安徽省（皖）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B8%A3%BD%A8%CA%A1%A3%A8%C3%F6%A3%A9&diji=-1&xianji=-1 # 福建省（闽）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BD%AD%CE%F7%CA%A1%A3%A8%B8%D3%A3%A9&diji=-1&xianji=-1 # 江西省（赣）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%BD%B6%AB%CA%A1%A3%A8%C2%B3%A3%A9&diji=-1&xianji=-1 # 山东省（鲁）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%C4%CF%CA%A1%A3%A8%D4%A5%A3%A9&diji=-1&xianji=-1 # 河南省（豫）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%FE%B1%B1%CA%A1%A3%A8%B6%F5%A3%A9&diji=-1&xianji=-1 # 湖北省（鄂）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%FE%C4%CF%CA%A1%A3%A8%CF%E6%A3%A9&diji=-1&xianji=-1 # 湖南省（湘）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%E3%B6%AB%CA%A1%A3%A8%D4%C1%A3%A9&diji=-1&xianji=-1 # 广东省（粤）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%E3%CE%F7%D7%B3%D7%E5%D7%D4%D6%CE%C7%F8%A3%A8%B9%F0%A3%A9&diji=-1&xianji=-1 # 广西壮族自治区（桂）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%A3%C4%CF%CA%A1%A3%A8%C7%ED%A3%A9&diji=-1&xianji=-1 # 海南省（琼）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%D6%D8%C7%EC%CA%D0%A3%A8%D3%E5%A3%A9&diji=-1&xianji=-1 # 重庆市（渝）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%CB%C4%B4%A8%CA%A1%A3%A8%B4%A8%A1%A2%CA%F1%A3%A9&diji=-1&xianji=-1 # 四川省（川、蜀）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B9%F3%D6%DD%CA%A1%A3%A8%C7%AD%A1%A2%B9%F3%A3%A9&diji=-1&xianji=-1 # 贵州省（黔、贵）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%D4%C6%C4%CF%CA%A1%A3%A8%B5%E1%A1%A2%D4%C6%A3%A9&diji=-1&xianji=-1 # 云南省（滇、云）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%CE%F7%B2%D8%D7%D4%D6%CE%C7%F8%A3%A8%B2%D8%A3%A9&diji=-1&xianji=-1 # 西藏自治区（藏）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C9%C2%CE%F7%CA%A1%A3%A8%C9%C2%A1%A2%C7%D8%A3%A9&diji=-1&xianji=-1 # 陕西省（陕、秦）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B8%CA%CB%E0%CA%A1%A3%A8%B8%CA%A1%A2%C2%A4%A3%A9&diji=-1&xianji=-1 # 甘肃省（甘、陇）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C7%E0%BA%A3%CA%A1%A3%A8%C7%E0%A3%A9&diji=-1&xianji=-1 # 青海省（青）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%C4%FE%CF%C4%BB%D8%D7%E5%D7%D4%D6%CE%C7%F8%A3%A8%C4%FE%A3%A9&diji=-1&xianji=-1 # 宁夏回族自治区（宁）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%D0%C2%BD%AE%CE%AC%CE%E1%B6%FB%D7%D4%D6%CE%C7%F8%A3%A8%D0%C2%A3%A9&diji=-1&xianji=-1 # 新疆维吾尔自治区（新）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%CF%E3%B8%DB%CC%D8%B1%F0%D0%D0%D5%FE%C7%F8%A3%A8%B8%DB%A3%A9&diji=-1&xianji=-1 # 香港特别行政区（港）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%B0%C4%C3%C5%CC%D8%B1%F0%D0%D0%D5%FE%C7%F8%A3%A8%B0%C4%A3%A9&diji=-1&xianji=-1 # 澳门特别行政区（澳）",
"http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%A8%CD%E5%CA%A1%A3%A8%CC%A8%A3%A9&diji=-1&xianji=-1 # 台湾省（台）",
"""
    directlyCitys = ["北京市（京）", "天津市（津）","上海市（沪）","重庆市（渝）",]
    directlyCitysList = []
    for city in directlyCitys:
        enc = encoded(city)
        # 使用三引号字符串来处理换行符，并添加注释
        item = f'"{enc}", # {city}\n'
        directlyCitysList.append(item)
    result = "".join(directlyCitysList)

    # 打印结果
    print(result)
    """"%B1%B1%BE%A9%CA%D0%A3%A8%BE%A9%A3%A9", # 北京市（京）
"%CC%EC%BD%F2%CA%D0%A3%A8%BD%F2%A3%A9", # 天津市（津）
"%C9%CF%BA%A3%CA%D0%A3%A8%BB%A6%A3%A9", # 上海市（沪）
"%D6%D8%C7%EC%CA%D0%A3%A8%D3%E5%A3%A9", # 重庆市（渝）"""

import json
import os
# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + "/"
# 假设文件路径为 "data.json"
all_file_path = current_directory+  "allArea.json"
def read_json(file_path=all_file_path):
    # 打开文件并加载内容
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 现在可以操作 data，它包含了 JSON 文件中的内容
    # print(data)  # 打印整个 JSON 内容


    # 如果是列表，可以按索引访问特定元素
    # print(data[0], data[-1])  # 例如，假设 JSON 文件中是一个列表，这里访问第一个元素
    return data

from urllib.parse import urlparse, parse_qs
# def dispose_of_url(url):
#     # url = "http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1"
#     # url = "http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%A8%CD%E5%CA%A1%A3%A8%CC%A8%A3%A9&diji=-1&xianji=-1"
#     parsed_url = urlparse(decode(url))
#     query_params = parse_qs(parsed_url.query)
#     print(query_params)
#     if "shengji" in query_params:
#         shengji_value = query_params["shengji"][0]
        
#         # print(f"shengji value: {shengji_value}")
#         # 用括号分割
#         parts = shengji_value.split("（")[0]  # 使用括号（作为分隔符

#         # 输出分割后的结果
#         # print(parts)
#         list = read_json()
#         # 在数据中找到"cName":"河北省"的对象
#         desired_obj = next(item for item in list if item["cName"] == parts)
#         # print(desired_obj)
#         return desired_obj
#     else:
#         print("shengji parameter not found in the URL.")
#         return None

def test_json(jsonString):
    if not jsonString:
        jsonString = '''{"code": "130000", "jp": "hbs", "name": "河北省", "py": "Hebei Sheng", "qp": "HebeiSheng", "subList": [{"area": "14530", "code": "130100", "name": "石家庄市", "population": "989", "resident": "长安区", "subList": [{"area": "138", "areaCode": "0311", "code": "130102", "name": "长安区", "population": "67", "postalCode": "050011", "resident": "育才街道"},{"area": "69", "areaCode": "0311", "code": "130104", "name": "桥西区", "population": "68", "postalCode": "050091", "resident": "振头街道"},{"area": "97", "areaCode": "0311", "code": "130105", "name": "新华区", "population": "51", "postalCode": "050051", "resident": "革新街道"},{"area": "76", "areaCode": "0311", "code": "130107", "name": "井陉矿区", "population": "9", "postalCode": "050100", "resident": "矿市街道"},{"area": "101", "areaCode": "0311", "code": "130108", "name": "裕华区", "population": "65", "postalCode": "050031", "resident": "裕兴街道"},{"area": "836", "areaCode": "0311", "code": "130109", "name": "藁城区", "population": "87", "postalCode": "052160", "resident": "廉州镇"},{"area": "603", "areaCode": "0311", "code": "130110", "name": "鹿泉区", "population": "45", "postalCode": "050200", "resident": "获鹿镇"},{"area": "326", "areaCode": "0311", "code": "130111", "name": "栾城区", "population": "36", "postalCode": "051430", "resident": "栾城镇"},{"area": "951", "areaCode": "0311", "code": "130181", "name": "辛集市", "population": "64", "postalCode": "052300", "resident": "辛集镇"},{"area": "619", "areaCode": "0311", "code": "130183", "name": "晋州市", "population": "58", "postalCode": "052200", "resident": "晋州镇"},{"area": "525", "areaCode": "0311", "code": "130184", "name": "新乐市", "population": "52", "postalCode": "050700", "resident": "长寿街道"},{"area": "1381", "areaCode": "0311", "code": "130121", "name": "井陉县", "population": "33", "postalCode": "050300", "resident": "微水镇"},{"area": "468", "areaCode": "0311", "code": "130123", "name": "正定县", "population": "51", "postalCode": "050800", "resident": "正定镇"},{"area": "1025", "areaCode": "0311", "code": "130125", "name": "行唐县", "population": "46", "postalCode": "050600", "resident": "龙州镇"},{"area": "1066", "areaCode": "0311", "code": "130126", "name": "灵寿县", "population": "35", "postalCode": "050500", "resident": "灵寿镇"},{"area": "222", "areaCode": "0311", "code": "130127", "name": "高邑县", "population": "20", "postalCode": "051330", "resident": "高邑镇"},{"area": "296", "areaCode": "0311", "code": "130128", "name": "深泽县", "population": "26", "postalCode": "052500", "resident": "深泽镇"},{"area": "1210", "areaCode": "0311", "code": "130129", "name": "赞皇县", "population": "28", "postalCode": "051230", "resident": "赞皇镇"},{"area": "524", "areaCode": "0311", "code": "130130", "name": "无极县", "population": "54", "postalCode": "052400", "resident": "无极镇"},{"area": "2648", "areaCode": "0311", "code": "130131", "name": "平山县", "population": "51", "postalCode": "050400", "resident": "平山镇"},{"area": "675", "areaCode": "0311", "code": "130132", "name": "元氏县", "population": "45", "postalCode": "051130", "resident": "槐阳镇"},{"area": "674", "areaCode": "0311", "code": "130133", "name": "赵县", "population": "62", "postalCode": "051530", "resident": "赵州镇"}]},{"area": "13829", "code": "130200", "name": "唐山市", "population": "756", "resident": "路北区", "subList": [{"area": "168", "areaCode": "0315", "code": "130203", "name": "路北区", "population": "85", "postalCode": "063000", "resident": "乔屯街道"},{"area": "118", "areaCode": "0315", "code": "130202", "name": "路南区", "population": "35", "postalCode": "063000", "resident": "学院南路街道"},{"area": "249", "areaCode": "0315", "code": "130204", "name": "古冶区", "population": "33", "postalCode": "063100", "resident": "京华街道"},{"area": "251", "areaCode": "0315", "code": "130205", "name": "开平区", "population": "25", "postalCode": "063021", "resident": "开平街道"},{"area": "1262", "areaCode": "0315", "code": "130207", "name": "丰南区", "population": "54", "postalCode": "063300", "resident": "青年路街道"},{"area": "1234", "areaCode": "0315", "code": "130208", "name": "丰润区", "population": "81", "postalCode": "064000", "resident": "太平路街道"},{"area": "1281", "areaCode": "0315", "code": "130209", "name": "曹妃甸区", "population": "21", "postalCode": "063200", "resident": "唐海镇"},{"area": "1509", "areaCode": "0315", "code": "130281", "name": "遵化市", "population": "75", "postalCode": "064200", "resident": "遵化镇"},{"area": "1227", "areaCode": "0315", "code": "130283", "name": "迁安市", "population": "78", "postalCode": "064400", "resident": "永顺街道"},{"area": "1027", "areaCode": "0315", "code": "130284", "name": "滦州市", "population": "57", "postalCode": "063700", "resident": "滦河街道"},{"area": "1482", "areaCode": "0315", "code": "130224", "name": "滦南县", "population": "57", "postalCode": "063500", "resident": "友谊路街道"},{"area": "1417", "areaCode": "0315", "code": "130225", "name": "乐亭县", "population": "44", "postalCode": "063600", "resident": "乐安街道"},{"area": "1439", "areaCode": "0315", "code": "130227", "name": "迁西县", "population": "40", "postalCode": "064300", "resident": "兴城镇"},{"area": "1165", "areaCode": "0315", "code": "130229", "name": "玉田县", "population": "70", "postalCode": "064100", "resident": "无终街道"}]},{"area": "7813", "code": "130300", "name": "秦皇岛市", "population": "301", "resident": "海港区", "subList": [{"area": "713", "areaCode": "0335", "code": "130302", "name": "海港区", "population": "85", "postalCode": "066000", "resident": "建设大街街道"},{"area": "193", "areaCode": "0335", "code": "130303", "name": "山海关区", "population": "14", "postalCode": "066200", "resident": "路南街道"},{"area": "155", "areaCode": "0335", "code": "130304", "name": "北戴河区", "population": "13", "postalCode": "066100", "resident": "西山街道"},{"area": "1069", "areaCode": "0335", "code": "130306", "name": "抚宁区", "population": "35", "postalCode": "066300", "resident": "抚宁镇"},{"area": "1212", "areaCode": "0335", "code": "130322", "name": "昌黎县", "population": "56", "postalCode": "066600", "resident": "昌黎镇"},{"area": "961", "areaCode": "0335", "code": "130324", "name": "卢龙县", "population": "42", "postalCode": "066400", "resident": "卢龙镇"},{"area": "3510", "areaCode": "0335", "code": "130321", "name": "青龙满族自治县", "population": "57", "postalCode": "066500", "resident": "青龙镇"}]},{"area": "12047", "code": "130400", "name": "邯郸市", "population": "1061", "resident": "丛台区", "subList": [{"area": "387", "areaCode": "0310", "code": "130403", "name": "丛台区", "population": "83", "postalCode": "056002", "resident": "丛台西街道"},{"area": "416", "areaCode": "0310", "code": "130402", "name": "邯山区", "population": "77", "postalCode": "056001", "resident": "火磨街道"},{"area": "243", "areaCode": "0310", "code": "130404", "name": "复兴区", "population": "37", "postalCode": "056003", "resident": "胜利桥街道"},{"area": "374", "areaCode": "0310", "code": "130406", "name": "峰峰矿区", "population": "46", "postalCode": "056200", "resident": "滏阳东路街道"},{"area": "503", "areaCode": "0310", "code": "130407", "name": "肥乡区", "population": "41", "postalCode": "057550", "resident": "肥乡镇"},{"area": "760", "areaCode": "0310", "code": "130408", "name": "永年区", "population": "97", "postalCode": "057150", "resident": "临洺关镇"},{"area": "1806", "areaCode": "0310", "code": "130481", "name": "武安市", "population": "85", "postalCode": "056300", "resident": "武安镇"},{"area": "742", "areaCode": "0310", "code": "130423", "name": "临漳县", "population": "76", "postalCode": "056600", "resident": "临漳镇"},{"area": "482", "areaCode": "0310", "code": "130424", "name": "成安县", "population": "47", "postalCode": "056700", "resident": "成安镇"},{"area": "1053", "areaCode": "0310", "code": "130425", "name": "大名县", "population": "94", "postalCode": "056900", "resident": "大名镇"},{"area": "1509", "areaCode": "0310", "code": "130426", "name": "涉县", "population": "43", "postalCode": "056400", "resident": "平安街道"},{"area": "695", "areaCode": "0310", "code": "130427", "name": "磁县", "population": "49", "postalCode": "056500", "resident": "磁州镇"},{"area": "449", "areaCode": "0310", "code": "130430", "name": "邱县", "population": "26", "postalCode": "057450", "resident": "新马头镇"},{"area": "336", "areaCode": "0310", "code": "130431", "name": "鸡泽县", "population": "34", "postalCode": "057350", "resident": "鸡泽镇"},{"area": "314", "areaCode": "0310", "code": "130432", "name": "广平县", "population": "31", "postalCode": "057650", "resident": "广平镇"},{"area": "456", "areaCode": "0310", "code": "130433", "name": "馆陶县", "population": "36", "postalCode": "057750", "resident": "馆陶镇"},{"area": "864", "areaCode": "0310", "code": "130434", "name": "魏县", "population": "104", "postalCode": "056800", "resident": "魏城镇"},{"area": "677", "areaCode": "0310", "code": "130435", "name": "曲周县", "population": "54", "postalCode": "057250", "resident": "曲周镇"}]},{"area": "12143", "code": "130500", "name": "邢台市", "population": "801", "resident": "襄都区", "subList": [{"area": "318", "areaCode": "0319", "code": "130502", "name": "襄都区", "population": "53", "postalCode": "054001", "resident": "南长街街道"},{"area": "1894", "areaCode": "0319", "code": "130503", "name": "信都区", "population": "74", "postalCode": "054002", "resident": "钢铁路街道"},{"area": "431", "areaCode": "0319", "code": "130505", "name": "任泽区", "population": "39", "postalCode": "055150", "resident": "任城镇"},{"area": "405", "areaCode": "0319", "code": "130506", "name": "南和区", "population": "40", "postalCode": "054400", "resident": "和阳镇"},{"area": "861", "areaCode": "0319", "code": "130581", "name": "南宫市", "population": "51", "postalCode": "055750", "resident": "凤岗街道"},{"area": "859", "areaCode": "0319", "code": "130582", "name": "沙河市", "population": "46", "postalCode": "054100", "resident": "褡裢街道"},{"area": "797", "areaCode": "0319", "code": "130522", "name": "临城县", "population": "22", "postalCode": "054300", "resident": "临城镇"},{"area": "788", "areaCode": "0319", "code": "130523", "name": "内丘县", "population": "30", "postalCode": "054200", "resident": "内丘镇"},{"area": "268", "areaCode": "0319", "code": "130524", "name": "柏乡县", "population": "21", "postalCode": "055450", "resident": "柏乡镇"},{"area": "749", "areaCode": "0319", "code": "130525", "name": "隆尧县", "population": "57", "postalCode": "055350", "resident": "隆尧镇"},{"area": "1032", "areaCode": "0319", "code": "130528", "name": "宁晋县", "population": "87", "postalCode": "055550", "resident": "凤凰镇"},{"area": "631", "areaCode": "0319", "code": "130529", "name": "巨鹿县", "population": "43", "postalCode": "055250", "resident": "巨鹿镇"},{"area": "366", "areaCode": "0319", "code": "130530", "name": "新河县", "population": "18", "postalCode": "055650", "resident": "新河镇"},{"area": "504", "areaCode": "0319", "code": "130531", "name": "广宗县", "population": "34", "postalCode": "054600", "resident": "广宗镇"},{"area": "406", "areaCode": "0319", "code": "130532", "name": "平乡县", "population": "37", "postalCode": "054500", "resident": "中华路街道"},{"area": "994", "areaCode": "0319", "code": "130533", "name": "威县", "population": "65", "postalCode": "054700", "resident": "洺州镇"},{"area": "500", "areaCode": "0319", "code": "130534", "name": "清河县", "population": "45", "postalCode": "054800", "resident": "葛仙庄镇"},{"area": "542", "areaCode": "0319", "code": "130535", "name": "临西县", "population": "39", "postalCode": "054900", "resident": "临西镇"}]},{"area": "22135", "code": "130600", "name": "保定市", "population": "1090", "resident": "竞秀区", "subList": [{"area": "139", "areaCode": "0312", "code": "130602", "name": "竞秀区", "population": "52", "postalCode": "071051", "resident": "先锋街道"},{"area": "173", "areaCode": "0312", "code": "130606", "name": "莲池区", "population": "64", "postalCode": "071000", "resident": "五四路街道"},{"area": "629", "areaCode": "0312", "code": "130607", "name": "满城区", "population": "41", "postalCode": "072150", "resident": "满城镇"},{"area": "867", "areaCode": "0312", "code": "130608", "name": "清苑区", "population": "69", "postalCode": "071100", "resident": "清苑镇"},{"area": "723", "areaCode": "0312", "code": "130609", "name": "徐水区", "population": "64", "postalCode": "072550", "resident": "安肃镇"},{"area": "751", "areaCode": "0312", "code": "130681", "name": "涿州市", "population": "70", "postalCode": "072750", "resident": "双塔街道"},{"area": "1283", "areaCode": "0312", "code": "130682", "name": "定州市", "population": "124", "postalCode": "073000", "resident": "南城区街道"},{"area": "486", "areaCode": "0312", "code": "130683", "name": "安国市", "population": "41", "postalCode": "071200", "resident": "祁州路街道"},{"area": "618", "areaCode": "0312", "code": "130684", "name": "高碑店市", "population": "63", "postalCode": "074000", "resident": "兴华路街道"},{"area": "1658", "areaCode": "0312", "code": "130623", "name": "涞水县", "population": "36", "postalCode": "074100", "resident": "涞水镇"},{"area": "2496", "areaCode": "0312", "code": "130624", "name": "阜平县", "population": "23", "postalCode": "073200", "resident": "阜平镇"},{"area": "714", "areaCode": "0312", "code": "130626", "name": "定兴县", "population": "61", "postalCode": "072650", "resident": "定兴镇"},{"area": "1417", "areaCode": "0312", "code": "130627", "name": "唐县", "population": "60", "postalCode": "072350", "resident": "仁厚镇"},{"area": "495", "areaCode": "0312", "code": "130628", "name": "高阳县", "population": "36", "postalCode": "071500", "resident": "锦华街道"},{"area": "314", "areaCode": "0312", "code": "130629", "name": "容城县", "population": "28", "postalCode": "071700", "resident": "容城镇"},{"area": "2448", "areaCode": "0312", "code": "130630", "name": "涞源县", "population": "29", "postalCode": "074300", "resident": "涞源镇"},{"area": "370", "areaCode": "0312", "code": "130631", "name": "望都县", "population": "27", "postalCode": "072450", "resident": "望都镇"},{"area": "728", "areaCode": "0312", "code": "130632", "name": "安新县", "population": "48", "postalCode": "071600", "resident": "安新镇"},{"area": "2534", "areaCode": "0312", "code": "130633", "name": "易县", "population": "58", "postalCode": "074200", "resident": "易州镇"},{"area": "1084", "areaCode": "0312", "code": "130634", "name": "曲阳县", "population": "66", "postalCode": "073100", "resident": "恒州镇"},{"area": "652", "areaCode": "0312", "code": "130635", "name": "蠡县", "population": "55", "postalCode": "071400", "resident": "蠡吾镇"},{"area": "711", "areaCode": "0312", "code": "130636", "name": "顺平县", "population": "32", "postalCode": "072250", "resident": "蒲阳镇"},{"area": "331", "areaCode": "0312", "code": "130637", "name": "博野县", "population": "27", "postalCode": "071300", "resident": "博野镇"},{"area": "514", "areaCode": "0312", "code": "130638", "name": "雄县", "population": "40", "postalCode": "071800", "resident": "雄州镇"}]},{"area": "36303", "code": "130700", "name": "张家口市", "population": "465", "resident": "桥西区", "subList": [{"area": "218", "areaCode": "0313", "code": "130703", "name": "桥西区", "population": "29", "postalCode": "075000", "resident": "新华街街道"},{"area": "385", "areaCode": "0313", "code": "130702", "name": "桥东区", "population": "33", "postalCode": "075000", "resident": "红旗楼街道"},{"area": "2014", "areaCode": "0313", "code": "130705", "name": "宣化区", "population": "52", "postalCode": "075100", "resident": "建国街街道"},{"area": "315", "areaCode": "0313", "code": "130706", "name": "下花园区", "population": "6", "postalCode": "075300", "resident": "城镇街道"},{"area": "1162", "areaCode": "0313", "code": "130708", "name": "万全区", "population": "22", "postalCode": "076250", "resident": "孔家庄镇"},{"area": "2324", "areaCode": "0313", "code": "130709", "name": "崇礼区", "population": "13", "postalCode": "076350", "resident": "西湾子镇"},{"area": "3863", "areaCode": "0313", "code": "130722", "name": "张北县", "population": "38", "postalCode": "076450", "resident": "张北镇"},{"area": "3365", "areaCode": "0313", "code": "130723", "name": "康保县", "population": "27", "postalCode": "076650", "resident": "康保镇"},{"area": "3388", "areaCode": "0313", "code": "130724", "name": "沽源县", "population": "23", "postalCode": "076550", "resident": "平定堡镇"},{"area": "2601", "areaCode": "0313", "code": "130725", "name": "尚义县", "population": "19", "postalCode": "076750", "resident": "南壕堑镇"},{"area": "3220", "areaCode": "0313", "code": "130726", "name": "蔚县", "population": "50", "postalCode": "075700", "resident": "蔚州镇"},{"area": "1849", "areaCode": "0313", "code": "130727", "name": "阳原县", "population": "27", "postalCode": "075800", "resident": "西城镇"},{"area": "1698", "areaCode": "0313", "code": "130728", "name": "怀安县", "population": "24", "postalCode": "076150", "resident": "柴沟堡镇"},{"area": "1801", "areaCode": "0313", "code": "130730", "name": "怀来县", "population": "37", "postalCode": "075400", "resident": "沙城镇"},{"area": "2802", "areaCode": "0313", "code": "130731", "name": "涿鹿县", "population": "35", "postalCode": "075600", "resident": "涿鹿镇"},{"area": "5287", "areaCode": "0313", "code": "130732", "name": "赤城县", "population": "29", "postalCode": "075500", "resident": "赤城镇"}]},{"area": "39719", "code": "130800", "name": "承德市", "population": "383", "resident": "双桥区", "subList": [{"area": "667", "areaCode": "0314", "code": "130802", "name": "双桥区", "population": "39", "postalCode": "067000", "resident": "中华路街道"},{"area": "452", "areaCode": "0314", "code": "130803", "name": "双滦区", "population": "15", "postalCode": "067001", "resident": "双塔山镇"},{"area": "148", "areaCode": "0314", "code": "130804", "name": "鹰手营子矿区", "population": "6", "postalCode": "067200", "resident": "铁北路街道"},{"area": "3294", "areaCode": "0314", "code": "130881", "name": "平泉市", "population": "48", "postalCode": "067500", "resident": "平泉镇"},{"area": "3648", "areaCode": "0314", "code": "130821", "name": "承德县", "population": "43", "postalCode": "067400", "resident": "下板城镇"},{"area": "3123", "areaCode": "0314", "code": "130822", "name": "兴隆县", "population": "33", "postalCode": "067300", "resident": "兴隆镇"},{"area": "2993", "areaCode": "0314", "code": "130824", "name": "滦平县", "population": "33", "postalCode": "068250", "resident": "中兴路街道"},{"area": "5473", "areaCode": "0314", "code": "130825", "name": "隆化县", "population": "45", "postalCode": "068150", "resident": "安州街道"},{"area": "8765", "areaCode": "0314", "code": "130826", "name": "丰宁满族自治县", "population": "41", "postalCode": "068350", "resident": "大阁镇"},{"area": "1936", "areaCode": "0314", "code": "130827", "name": "宽城满族自治县", "population": "26", "postalCode": "067600", "resident": "宽城镇"},{"area": "9220", "areaCode": "0314", "code": "130828", "name": "围场满族蒙古族自治县", "population": "54", "postalCode": "068450", "resident": "围场镇"}]},{"area": "13488", "code": "130900", "name": "沧州市", "population": "787", "resident": "运河区", "subList": [{"area": "138", "areaCode": "0317", "code": "130903", "name": "运河区", "population": "37", "postalCode": "061001", "resident": "水月寺街道"},{"area": "89", "areaCode": "0317", "code": "130902", "name": "新华区", "population": "23", "postalCode": "061000", "resident": "建设北街街道"},{"area": "1009", "areaCode": "0317", "code": "130981", "name": "泊头市", "population": "63", "postalCode": "062150", "resident": "解放街道"},{"area": "1012", "areaCode": "0317", "code": "130982", "name": "任丘市", "population": "91", "postalCode": "062550", "resident": "新华路街道"},{"area": "1545", "areaCode": "0317", "code": "130983", "name": "黄骅市", "population": "58", "postalCode": "061100", "resident": "骅西街道"},{"area": "1333", "areaCode": "0317", "code": "130984", "name": "河间市", "population": "91", "postalCode": "062450", "resident": "瀛州路街道"},{"area": "1520", "areaCode": "0317", "code": "130921", "name": "沧县", "population": "74", "postalCode": "061000", "resident": "沧州市新华区"},{"area": "968", "areaCode": "0317", "code": "130922", "name": "青县", "population": "44", "postalCode": "062650", "resident": "清州镇"},{"area": "711", "areaCode": "0317", "code": "130923", "name": "东光县", "population": "39", "postalCode": "061600", "resident": "东光镇"},{"area": "919", "areaCode": "0317", "code": "130924", "name": "海兴县", "population": "24", "postalCode": "061200", "resident": "苏基镇"},{"area": "795", "areaCode": "0317", "code": "130925", "name": "盐山县", "population": "50", "postalCode": "061300", "resident": "盐山镇"},{"area": "516", "areaCode": "0317", "code": "130926", "name": "肃宁县", "population": "37", "postalCode": "062350", "resident": "肃宁镇"},{"area": "790", "areaCode": "0317", "code": "130927", "name": "南皮县", "population": "40", "postalCode": "061500", "resident": "南皮镇"},{"area": "583", "areaCode": "0317", "code": "130928", "name": "吴桥县", "population": "28", "postalCode": "061800", "resident": "桑园镇"},{"area": "1173", "areaCode": "0317", "code": "130929", "name": "献县", "population": "66", "postalCode": "062250", "resident": "乐寿镇"},{"area": "387", "areaCode": "0317", "code": "130930", "name": "孟村回族自治县", "population": "23", "postalCode": "061400", "resident": "孟村镇"}]},{"area": "6420", "code": "131000", "name": "廊坊市", "population": "483", "resident": "广阳区", "subList": [{"area": "384", "areaCode": "0316", "code": "131003", "name": "广阳区", "population": "50", "postalCode": "065000", "resident": "解放道街道"},{"area": "578", "areaCode": "0316", "code": "131002", "name": "安次区", "population": "38", "postalCode": "065000", "resident": "银河北路街道"},{"area": "802", "areaCode": "0316", "code": "131081", "name": "霸州市", "population": "66", "postalCode": "065700", "resident": "霸州镇"},{"area": "634", "areaCode": "0316", "code": "131082", "name": "三河市", "population": "75", "postalCode": "065200", "resident": "鼎盛东大街街道"},{"area": "703", "areaCode": "0316", "code": "131022", "name": "固安县", "population": "53", "postalCode": "065500", "resident": "固安镇"},{"area": "761", "areaCode": "0316", "code": "131023", "name": "永清县", "population": "41", "postalCode": "065600", "resident": "永清镇"},{"area": "448", "areaCode": "0316", "code": "131024", "name": "香河县", "population": "38", "postalCode": "065400", "resident": "淑阳镇"},{"area": "897", "areaCode": "0316", "code": "131025", "name": "大城县", "population": "54", "postalCode": "065900", "resident": "平舒镇"},{"area": "1037", "areaCode": "0316", "code": "131026", "name": "文安县", "population": "56", "postalCode": "065800", "resident": "文安镇"},{"area": "176", "areaCode": "0316", "code": "131028", "name": "大厂回族自治县", "population": "13", "postalCode": "065300", "resident": "大厂镇"}]},{"area": "8758", "code": "131100", "name": "衡水市", "population": "458", "resident": "桃城区", "subList": [{"area": "563", "areaCode": "0318", "code": "131102", "name": "桃城区", "population": "68", "postalCode": "053000", "resident": "中华大街街道"},{"area": "878", "areaCode": "0318", "code": "131103", "name": "冀州区", "population": "35", "postalCode": "053200", "resident": "冀州镇"},{"area": "1245", "areaCode": "0318", "code": "131182", "name": "深州市", "population": "57", "postalCode": "053800", "resident": "深州镇"},{"area": "905", "areaCode": "0318", "code": "131121", "name": "枣强县", "population": "41", "postalCode": "053100", "resident": "枣强镇"},{"area": "832", "areaCode": "0318", "code": "131122", "name": "武邑县", "population": "32", "postalCode": "053400", "resident": "武邑镇"},{"area": "443", "areaCode": "0318", "code": "131123", "name": "武强县", "population": "22", "postalCode": "053300", "resident": "武强镇"},{"area": "572", "areaCode": "0318", "code": "131124", "name": "饶阳县", "population": "29", "postalCode": "053900", "resident": "饶阳镇"},{"area": "496", "areaCode": "0318", "code": "131125", "name": "安平县", "population": "34", "postalCode": "053600", "resident": "安平镇"},{"area": "941", "areaCode": "0318", "code": "131126", "name": "故城县", "population": "53", "postalCode": "053800", "resident": "郑口镇"},{"area": "1188", "areaCode": "0318", "code": "131127", "name": "景县", "population": "55", "postalCode": "053500", "resident": "景州镇"},{"area": "695", "areaCode": "0318", "code": "131128", "name": "阜城县", "population": "35", "postalCode": "053700", "resident": "阜城镇"}]}]}'''
    print("--------------------------------")
    try:
        # 将 JSON 字符串解析为字典
        item_dict = json.loads(jsonString)
        
        # 创建 ScrapySpiderPracticeItem 对象
        item = ScrapySpiderPracticeItem()
        
        # 将字典中的值赋值给 ScrapySpiderPracticeItem 对象
        for key, value in item_dict.items():
            item[key] = value
            
        return item
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    print("test_json")

def dispose_of_url(url):
    # url = 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1'
    url = 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%CC%A8%CD%E5%CA%A1%A3%A8%CC%A8%A3%A9&diji=-1&xianji=-1'
    parsed_url = urlparse(decode(url))
    query_params = parse_qs(parsed_url.query)
    print(query_params)
    if 'shengji' in query_params:
        shengji_value = query_params['shengji'][0]
        
        print(f"shengji value: {shengji_value}")
        # 用括号分割
        arr = shengji_value.split("（")  # 使用括号（作为分隔符
        parts = arr[0]
        shorter = arr[1].split("）")[0] 
        # 输出分割后的结果
        print(parts)
        list = read_json()
        # 在数据中找到"cName":"河北省"的对象
        desired_obj = next(item for item in list if item["cName"] == parts)
        # 向desired_obj中插入shorter属性
        desired_obj['shorter'] = shorter
        print(desired_obj)
        return desired_obj
    else:
        print("shengji parameter not found in the URL.")
        return None

def dispose_of_data():
    data = [['java 高级', 'JAVA 工程师', 'Java 工程师', 'java 魏公村', 'Java 工程师', 'java 工程师', 'java web', 'JAVA 开发', 'Java 工程师', 'Java 工程师', 'Java Developers', 'JAVA 开发', 'Java 开发工程师', 'JAVA 开发工程师', 'Seinor Java Engineer', 'Java 资深/专家工程师', 'JAVA 开发工程师', 'Java 中级工程师', 'java 开发工程师', 'Java 工程师', 'Java 中级工程师', 'java web 工程师', 'Java 研发工程师', 'Java 研发工程师', 'JAVA web工程师', 'Java 开发', 'java 工程师', 'Java 工程师', 'Java 高级开发工程师', '致远互联 java 开发'], ['北京·朝阳区·三元桥', '北京·朝阳区·高碑店', '北京·海淀区·上地', '北京·海淀区·万柳', '北京·通州区·九棵树', '北京·朝阳区·广渠门', '北京·海淀区·中关村', '北京·朝阳区·来广营', '北京·丰台区·北大地', '北京·丰台区·刘家窑', '北京·朝阳区·国贸', '北京·昌平区·天通苑', '北京·海淀区·白石桥', '北京·海淀区·上地', '北京·海淀区·人民大学', '北京·海淀区·安宁庄', '北京·丰台区·世界公园', '北京·海淀区·西二旗', '北京·丰台区·宋家庄', '北京·朝阳区·朝外', '北京·朝阳区·四惠东', '北京·海淀区·五道口', '北京·大兴区·大兴经济开发区', '北京·朝阳区·大望路', '北京·丰台区·南苑', '北京·朝阳区·望京', '北京', '北京·海淀区·知春路', '北京·朝阳区·东大桥', '北京·海淀区·万柳'], ['20-30K', '15-25K·13薪', '10-15K', '15-16K', '10-15K', '11-20K', '9-14K', '8-12K', '25-40K·14薪', '11-22K', '20-30K·13薪', '10-15K', '15-25K·14薪', '10-13K', '18-19K', '25-50K·14薪', '8-13K', '11-18K', '12-15K', '9-12K', '12-20K', '8-13K', '12-18K', '14-20K·13薪', '18-23K·13薪', '16-32K', '15-25K', '10-15K·13薪', '20-40K', '7-12K'], ['5-10年|本科', '3-5年|本科', '3-5年|本科', '3-5年|本科', '5-10年|大专', '3-5年|本科', '3-5年|本科', '5-10年|大专', '5-10年|硕士', '3-5年|本科', '5-10年|本科', '3-5年|本科', '1-3年|本科', '1-3年|本科', '3-5年|本科', '5-10年|本科', '经验不限|学历不限', '3-5年|本科', '1-3年|本科', '5-10年|本科', '3-5年|本科', '1-3年|本科', '1-3年|本科', '3-5年|大专', '3-5年|本科', '3-5年|本科', '5-10年|本科', '经验不限|学历不限', '3-5年|本科', '经验不限|学历不限'], ['Oracle|微服务架构|SpringBoot|SpringCloud|MySQL|||', 'Spring|MySQL|Python|微服务架构|搜索引擎技术||', 'Linux|HTML/CSS|Java', 'Java|SpringCloud|MySQL', '全栈开发', 'Java', 'Java|HTML5|Javascript', '微服务架构|后端开发', '后端工程师|Spring|MyBatis|计算机/软件工程相关经验||', 'MySQL|Redis|Java|后端工程师|SpringBoot||', '软件工程师|java|AWS|DevOps|English|Agile', 'IM|即时通讯', 'Java|后端开发', 'Java|Linux|数据库', '软件工程师', '后端工程师|Java|Java开发经验|分布式系统开发经验|', '全栈工程师|Java', '数据库|springboot|Java', 'Java|Spring', 'Java|Nginx|不接受居家办公|SpringCloud|MySQL|||', 'HTML/CSS|Linux|Javascript', 'SpringBoot|全栈开发|Angular|Ionic|前后端分离|', '后端工程师|Java|Spring|MyBatis|Java开发经验||', 'Java', 'HTML|CSS|服务器配置|Spring|SpringMVC|MySQL||', 'Java|Javascript|JS', 'Java|JavaScript|Shell', 'Hibernate', 'Java|后端开发', 'Java|Spring|Tomcat|JVM|MongoDB|MySQL|'], ['', '节日福利，定期体检，团建聚餐，带薪年假，保底工资，包吃，员工旅游，五险一金，绩效奖金，零食下午茶，橙长培训', '', '定期体检，节日福利，带薪年假，员工旅游，五险一金，加班补助，年终奖', '', '五险一金，年终奖，带薪年假，零食下午茶', '', '', '补充医疗保险，餐补，交通补助，企业年金，五险一金，通讯补贴，带薪年假，定期体检', '团建聚餐，底薪加提成，年终奖', '五险一金，补充医疗保险，通讯补贴，不打卡，年终奖，英语环境，定期体检，员工旅游，带薪年假，零食下午茶，加班补助，节日福利，扁平化管理，瑞典公司', '', '带薪年假，五险一金，年终奖', '员工旅游，通讯补贴，年终奖，五险一金，节日福利，补充医疗保险，定期体检，带薪年假，绩效奖金，免费班车，团建聚餐，餐补，交通补助，住房补贴，生日福利', '定期体检，五险一金，补充医疗保险，带薪年假', '带薪年假，餐补，定期体检，股票期权，年终奖，节日福利，补充医疗保险，五险一金，12%公积金', '', '', '五险一金', '五险一金，节日福利，年终奖，员工旅游，带薪年假，股票期权，加班补助', '电脑补助，交通补助，餐补，五险一金', '', '补充医疗保险，通讯补贴，股票期权，年终奖，员工旅游，交通补助，节日福利，五险一金', '加班补助，五险一金，定期体检，年终奖，带薪年假，员工旅游，股票期权，餐补', '项目奖金，节日福利，带薪年假，年终奖，餐补，绩效奖金，五险一金，十三薪', '', '定期体检，五险一金，包吃，带薪年假，节日福利，全勤奖，年终奖', '', '', ''], ['https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20160418/31656ffbae01e1260ddb9cce6be2e36625d4d77513bbdf88b8bdcf31d5160bac.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20160629/6008a527f7d56db27dc5c6154b29974215448da25be9de63b43b4741dfde78f2.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/workfeel/20210729/632c878df933402c0eed8478b5fb014eb4454daec2082508b74c592e07be4f9c.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20200906/547e2cbd0ca6e78489f95c667895ba2c5834926bf4ffff11fb08e5baf949a5f8_s.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20210125/82d9c7824a98f218f608efc9a19f708395035a3a8abfebeaba483cc6c645d01f_s.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/logo/20200902/516037f3461e85a009972ed6fe6d3f7bc213f85b57749b1d080148326f75b003.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20190401/105e45a28b585a8eacc688603e3e044ff9551cee2739490faff3eaf3a36d7cd1_s.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20200111/3c3f6aba86aa649738ae9decf1dbb901ee9a5c297470d5a9f16c235691d04ef0_s.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://c-res.zhipin.com/jrs/0da9edf124b739758b6f04569e9a7359.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20170227/c67dd0d2dcc69b5082c593da0bc9441cd4bfc94849ece8a60a231aa51958b2c0.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20180412/5e9adb3ecb9ec4990054de1e67df96b8.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/banner/71f4ee09b9a2abfb675b5c705fc46c9dcfcd208495d565ef66e7dff9f98764da.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20180408/a8d3b7bba05f41f906a22c7d90dc4ef319beb939baf28337f5ce992042660dc1.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/logo/20230218/7b5b554d84f9729c1e7de0f6120a0ae762f883a6253352769302459af10b1e3f9d10d9ff4fc961f6.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20190922/2a6e0e4955f1d59ffcef8c6c9ae1c550d16e91211ebdb0f990024587eaf82564_s.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/logo/20191218/cf5c3b16af9098b6320c6a8c82f772e8abd9bfb32891588baba1d632695509fc.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/app/mobile/normal-0e3f1e4441a21d4874cece3a3d81f0fe.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/workfeel/20221216/7bf6f160950405e952c777481029b3be438a8c334bd422a28b1228d0cd43e189300947f276948f7e.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20190318/cf56054c04049290a8387c119e3baa90a984f2c003b6f0f41cad366e6931ee3d.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20190219/0d106ebddafa2d9030da738abfd07d758d9ab79ca86c07f38b95f72abb206153.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/mcs/chatphoto/20180404/a01e032f8cd2c835f3197f2f445e9d46cfcd208495d565ef66e7dff9f98764da.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/upload/com/logo/20190729/10221667efa8c632880a04cb83b4b07087506d655a47f8bd4fb893e30ade0ae1.jpg?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/app/mobile/normal-0e3f1e4441a21d4874cece3a3d81f0fe.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0', 'https://img.bosszhipin.com/beijin/icon/894ce6fa7e58d64d57e7f22d2f3a9d18afa7fcceaa24b8ea28f56f1bb14732c0.png?x-oss-process=image/resize,w_100,limit_0'], ['https://www.zhipin.com/gongsi/8f70ee824b1fff371nx_3dW7F1I~.html', 'https://www.zhipin.com/gongsi/92e05e7431035db003Jz29U~.html', 'https://www.zhipin.com/gongsi/29bfc503d24a7f301HV73Nu7.html', 'https://www.zhipin.com/gongsi/91677364ad3685761nN409u7FVc~.html', 'https://www.zhipin.com/gongsi/5304dc14c960865f0Xxy09S1EQ~~.html', 'https://www.zhipin.com/gongsi/4d50ebe968d0320f1nRz3Nm1Eg~~.html', 'https://www.zhipin.com/gongsi/fb976c9f7c2f02fc03Z42921Eg~~.html', 'https://www.zhipin.com/gongsi/4353fb49826a5cf933dy3dm9FQ~~.html', 'https://www.zhipin.com/gongsi/800c197ae38b8e821XR80t64FFY~.html', 'https://www.zhipin.com/gongsi/90ed4bcbfb97b0bf1XR8290~.html', 'https://www.zhipin.com/gongsi/ffafaf122196c10903R70tm-Fg~~.html', 'https://www.zhipin.com/gongsi/f5ce733aa65f81681n152tS9GA~~.html', 'https://www.zhipin.com/gongsi/b338d3bc864eeea303N539S9EA~~.html', 'https://www.zhipin.com/gongsi/962b3c4e4f1165691nV90tq1.html', 'https://www.zhipin.com/gongsi/bc5bd8ee49cc5be81XBy0tq9.html', 'https://www.zhipin.com/gongsi/6f1aa1d6b1d033ad33B43N0~.html', 'https://www.zhipin.com/gongsi/3c6df403656eb7851XJ_3Ni1FFQ~.html', 'https://www.zhipin.com/gongsi/d4eb5e346294bc3b1nN5092_FA~~.html', 'https://www.zhipin.com/gongsi/f1b3660c674345891H172t28Fg~~.html', 'https://www.zhipin.com/gongsi/6d458930fc80ec1b1XVy0t28Eg~~.html', 'https://www.zhipin.com/gongsi/1a977d7ef12241491HR-0ty4Ew~~.html', 'https://www.zhipin.com/gongsi/bb98a7a2843d76fd0HZ72ty0FA~~.html', 'https://www.zhipin.com/gongsi/8a656add2f7ff4741XB43t68EVE~.html', 'https://www.zhipin.com/gongsi/a881e00dc670f2891Hx63Nm0FQ~~.html', 'https://www.zhipin.com/gongsi/ab8562645e2cac7d1nx62NS8EA~~.html', 'https://www.zhipin.com/gongsi/1e82e61fd7ffe1161nJ90961Ew~~.html', 'https://www.zhipin.com/gongsi/ee9c3d5d8b355cb11HF53tm_FQ~~.html', 'https://www.zhipin.com/gongsi/9a4773aa78f6684a3nF-39W9GA~~.html', 'https://www.zhipin.com/gongsi/829099aa4a41e90c0nR93N28Fg~~.html', 'https://www.zhipin.com/gongsi/4beecc871d28755c1HV729W0E1A~.html'], ['北京奥海科技有限公司', '新橙科技', '鼎创力维', '柯锐特', '北京尚廷科技有限公司', '和风互联', '空曌科技', '微象限', '冶金自动化研究设计院', '拍立返', 'WirelessCar', '时空感应科技', '汇联信通', '中科院信工所', 'IGT', '小米', '北京市弘洁蓝天科技', '兴达智成', '星云互动', '三只肥猴', '滴度传媒', '北京创芯互联科技', '游美华夏', '卓越智视科技', '万方电子技术', '符代企业管理咨询', '中安智讯', '优迹网络科技', '国安建工', '北京江辽科技有限公司'], ['计算机软件|0-20人', '计算机软件|不需要融资|500-999人', '计算机软件|未融资|0-20人', '互联网|未融资|100-499人', '计算机软件|A轮|100-499人', '大数据|不需要融资|0-20人', '计算机软件|0-20人', '计算机软件|0-20人', '企业服务|100-499人', '互联网|A轮|20-99人', '计算机软件|未融资|100-499人', '社交网络|未融资|20-99人', '计算机软件|A轮|0-20人', '信息安全|不需要融资|1000-9999人', '计算机软件|已上市|100-499人', '互联网|已上市|10000人以上', '环保|100-499人', '计算机软件|未融资|20-99人', '广告营销|不需要融资|0-20人', '互联网|未融资|0-20人', '广告/公关/会展|天使轮|20-99人', '其他行业|1000-9999人', '旅游|A轮|20-99人', '计算机服务|不需要融资|20-99人', '铁路/船舶/航空/航天制造|未融资|', '计算机服务|未融资|1000-9999人', '计算机软件|不需要融资|20-99人', '互联网|20-99人', '工程施工|100-499人', '互联网|0-20人']]
    # 定义一个空列表，用于存放最终的对象
    result = []

    # 遍历每个元素的索引位置
    for i in range(len(data[0])):
        # 创建一个新的对象字典
        obj = {
            'title': data[0][i],  # 使用第一个子数组的元素作为'title'
            'locations': data[1][i],  # 使用第二个子数组的元素作为'locations'
            'salaries': data[2][i], # 使用第二个子数组的元素作为'salaries'
            'experience_education': data[3][i], # 使用第二个子数组的元素作为'locations'
            'skills': data[4][i], # 使用第二个子数组的元素作为'locations'
            'benefits': data[5][i], # 使用第二个子数组的元素作为'locations'
            'company_logos': data[6][i], # 使用第二个子数组的元素作为'locations'
            'company_href': data[7][i], # 使用第二个子数组的元素作为'locations'
            'company_name': data[8][i], # 使用第二个子数组的元素作为'locations'
            'company_info': data[9][i], # 使用第二个子数组的元素作为'locations'
        }
        # 将创建的对象添加到结果列表中
        result.append(obj)

    # 打印最终的对象列表
    data_tuples = [('JAVA', obj['title'], obj['locations'], obj['salaries'], obj['experience_education'], obj['skills'], obj['benefits'], obj['company_logos'], obj['company_href'], obj['company_name'], obj['company_info']) for obj in result]
    # print(data_tuples)
    return data_tuples


def test():
    data = [['java 高级', 'java 魏公村', 'JAVA 工程师', 'Java 工程师', 'Java 工程师', 'java 工程师', 'JAVA 开发', 'java web', 'JAVA 开发', 'Java Developers', 'Seinor Java Engineer', 'Java 工程师', 'Java 工程师', 'Java 开发工程师', 'JAVA 开发工程师', 'Java 资深/专家工程师', 'JAVA 开发工程师', 'Java 中级工程师', 'java 开发工程师', 'JAVA web工程师', 'Java 工程师', 'java 工程师', 'JAVA 开发工程师', 'JAVA 研发工程师', 'JAVA 开发工程师', 'java 开发工程师', 'Java 开发', 'Java 高级开发工程师', '致远互联 java 开发', 'Java 中级工程师'], 
        ['北京·朝阳区·三元桥', '北京·海淀区·万柳', '北京·朝阳区·高碑店', '北京·海淀区·上地', '北京·通州区·九棵树', '北京·朝阳区·广渠门', '北京·朝阳区·来广营', '北京·海淀区·中关村', '北京·昌平区·天通苑', '北京·朝阳区·国贸', '北京·海淀区·人民大学', '北京·丰台区·北大地', '北京·丰台区·刘家窑', '北京·海淀区·白石桥', '北京·海淀区·上地', '北京·海淀区·安宁庄', '北京·丰台区·世界公园', '北京·海淀区·西二旗', '北京·丰台区·宋家庄', '北京·丰台区·南苑', '北京·朝阳区·朝外', '北京', '北京', '北京·朝阳区·亮马桥', '北京·海淀区·上地', '北京·朝阳区·朝外', '北京·朝阳区·望京', '北京·朝阳区·东大桥', '北京·海淀区·万柳', '北京·朝阳区·四惠东']]

    # 定义一个空列表，用于存放最终的对象
    result = []

    # 确定每个子数组的长度，假设它们都具有相同的长度
    num_items = len(data[0])

    # 遍历每个元素的索引位置
    for i in range(num_items):
        # 创建一个新的对象字典
        obj = {
            'title': data[0][i],  # 使用第一个子数组的元素作为'title'
            'locations': data[1][i]  # 使用第二个子数组的元素作为'locations'
        }
        # 将创建的对象添加到结果列表中
        result.append(obj)

    # 打印最终的对象列表
    print(result)

if __name__ == "__main__":
    # read_json()
    # city_urls()
    # obj = xzqh.dispose_of_url("http://xzqh.mca.gov.cn/defaultQuery?shengji=%BA%D3%B1%B1%CA%A1%A3%A8%BC%BD%A3%A9&diji=-1&xianji=-1")
    # print(obj)
    # item = test_json()
    # item_dict = dict(item)
    # json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
    # print(json_string)
    
    # 获取当前文件所在目录的绝对路径
    # current_dir = os.path.dirname(os.path.abspath(__file__))

    # # 获取当前文件所在目录的上一级目录的绝对路径
    # parent_dir = os.path.dirname(current_dir)
    # path = os.path.dirname(current_dir) + '/city.json'
    # print(path)
    # data = read_json(path)
    # print(type(data), len(data))
    # jsonstr = data.string()
    # item = test_json(jsonstr)
    # item_dict = dict(item)
    # json_string = json.dumps(item_dict, ensure_ascii=False, indent=4)
    # print(json_string[:1000])
    # print('****************************************************************')
    # print(json_string[:-1000])
    
    # dispose_of_url('')
    # datas = dispose_of_data()
    # AboutDB.insert_datas(datas)
    # test()
    
    max_pages = 10

    for page in range(2, max_pages + 1):
        url = f'https://www.zhipin.com/web/geek/job?query=JAVA&city=101010100&page={str(page)}'
        print(url)