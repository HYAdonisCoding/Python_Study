import os
import ssl
import certifi
import urllib.request
import json
import jsonpath

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'

url = 'https://dianying.taobao.com/cityAction.json?activityId&_ksTS=1718178619611_132&jsoncallback=jsonp133&action=cityAction&n_s=new&event_submit_doGetAllRegion=true'
zhipin_home = 'https://www.zhipin.com/wapi/zpgeek/suggest/searchhotword.json?historyQuery=ios%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88'
def send_get_request(url, headers):
    # 创建 SSL 上下文
    ssl_context = ssl.create_default_context()

    # 使用 certifi 提供的证书
    ssl_context.load_verify_locations(certifi.where())

    try:
        
        # 1.请求对象的定制
        request = urllib.request.Request(url=url, headers=headers)
        # context = ssl._create_unverified_context()
        response = urllib.request.urlopen(request)
        
        content = response.read().decode('utf-8')
        # 3.数据下载到本地
        # open默认gbk编码
        # fp = open(current_directory+'代理1.html', 'w', encoding='utf-8')
        # fp.write(content)
        # print(content)
        return content
    except urllib.error.HTTPError as e:
        print('系统正在升级...', e)
        return None
    except urllib.error.URLError as e:
        print('系统正在升级中...', e)
        return None
    
def spider_dianying(url, headers):
    content = send_get_request(url, headers=headers)
    json = content.split('(')[1].split(')')[0]
    return json

def spider(url, headers):
    
    content = send_get_request(url, headers=headers)
    return content

def downloadFile(json):
    with open(current_directory+'淘票票.json', 'w') as f:
        f.write(json)
def parse_local_file():
    obj = json.load(open(current_directory+'淘票票.json', 'r', encoding='utf-8'))
    print(obj)
    # 书点所有书的作者
    ret = jsonpath.jsonpath(obj, '$.returnValue..regionName')
    # ret = jsonpath.jsonpath(obj, '$.returnValue.A[*].regionName')
    print(ret)
def parse_netjson(json_data):
    obj = json.loads(json_data)
    ret = jsonpath.jsonpath(obj, '$.returnValue..regionName')
    print(ret)
if __name__ == '__main__':
    print ('Starting...')
    # headers = {'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Bx-V': '2.5.11',
    #     'Cookie': 't=363e0f60e552c8e074728829d15d34c5; cookie2=1dd24d39f277c223ebbebf941b9293f5; v=0; _tb_token_=e9e71ef3a5775; xlly_s=1; isg=BPv7imMyGWuqryXfjv3TEesWitllUA9ST0ZYA-24q_oRTBoudSISozhCZuwC7GdK',
    #     'Dnt': '1',
    #     'Referer': 'https://dianying.taobao.com/',
    #     'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    #     'Sec-Ch-Ua-Mobile': '?0',
    #     'Sec-Ch-Ua-Platform': '"macOS"',
    #     'Sec-Fetch-Dest': 'empty',
    #     'Sec-Fetch-Mode': 'cors',
    #     'Sec-Fetch-Site': 'same-origin',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    #     'X-Requested-With': 'XMLHttpRequest',}
    # content = spider_dianying(url, headers)
    # # print(content)
    # parse_netjson(content)
    # # parse_local_file()
    
    zhipin_headers ={ 
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'sid=sem_pz_bdpc_dasou_title; lastCity=101010100; __zp_seo_uuid__=729e5d20-53b4-496c-9290-572f5f0ffc97; __l=r=https%3A%2F%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&l=%2Fcitysite%2Fbeijing%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&s=1; __g=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1718182197; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1718182222; wd_guid=c4a344d6-a75d-455b-b784-d5ead84c40cf; historyState=state; __c=1718182197; __a=94460582.1718182197..1718182197.2.1.2.2; __zp_stoken__=9676fS0vDpsOEU8OMPjMdFRobFksvSEswR0ZLN0g%2FS0tLQkFNS0tKHz87LnJfbF7DmMKYw4RFNktCTERLQUI%2FSSZLRsOFREo1TW9kY17DkRDDnMOIbT3Cvy7CtsOLFcOiwr85wpbDgjUyf8OKQURHSBDDhcOEw4bDrsONw4HDjcKlw43Do8OFRD9nMzdAFhoPYkA%2FV1lkElFjWGpsXRZRWF0xSD9DP3JfxIg9QRQbGxIPFBsbEg8VGhoWGxQbGxIPFBsbEg88S8Kew4HClcOJxIXCp8SNxJ7Cnk%2FCl1bDh8K5wqtYwrhPwppWU1DCqcK3wrrCu8KlfU7CusK2cMOIw4vCn2HCtcOAeGR9woVOZsOKTm0XUlpfexodwocQHEAXGXDDjg%3D%3D',
        'Dnt': '1',
        'Referer': 'https://www.zhipin.com/web/geek/job?query=ios%E5%BC%80%E5%8F%91%E5%B7%A5%E7%A8%8B%E5%B8%88&city=101010100',
        'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',}
    # content = spider(zhipin_home, zhipin_headers)
    
    # obj = json.loads(content)
    # ret = jsonpath.jsonpath(obj, '$.zpData..name')
    # print(ret)