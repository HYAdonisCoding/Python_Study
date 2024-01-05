# -*- coding: utf-8 -*-
import re
import json
import ssl
import urllib.request, urllib.parse, urllib.error

import certifi
import requests


def main():
    print('Hello, World!')

def getData() :
    # url = 'https://we.51job.com/api/job/search-pc?api_key=51job&timestamp=1703576335&keyword=Python&searchType=2&function=&industry=&jobArea=010000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum=2&requestId=51da10f28a7ef27acf6f2ba865254f9f&pageSize=20&source=1&accountId=44930433&pageCode=sou%7Csou%7Csoulb'
    # url = "https://search.51job.com/list/090200,000000,0000,0,9,99,python,2,3.html?lang=c&postchannel=0000Gworkyear=99&"
    #url ="https://www3.nhk.or.jp/news/json16/word/0000967_002.json'
    # #askURL(url)
    # result = open('result.html','r', encoding='utf-8')
    # data = re.findall(r"\"engine_search_result\":(.+?),\"jobid_count\"", str(result.readlines()))
    # print(data[0])
    # jsonObj = json.Loads(data[0])
    # for item in jsonObj:
    #     print(item['job_name'] + ':'+ item['company_name'])
    url = "https://we.51job.com/api/job/search-pc?api_key=51job&timestamp=1703578583&keyword=python&searchType=2&function=&industry=&jobArea=010000&jobArea2=&landmark=&metro=&salary=&workYear=&degree=&companyType=&companySize=&jobType=&issueDate=&sortType=0&pageNum=3&requestId=eb633f0044b5a0da780a52e5308a8ec5&pageSize=20&source=1&accountId=44930433&pageCode=sou%7Csou%7Csoulb"
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json?scene=1&query=python&city=101010100&experience=&payType=&partTime=&degree=&industry=&scale=&stage=&position=&jobType=&salary=&multiBusinessDistrict=&multiSubway=&page=2&pageSize=30"
    getJson(url)

def getJson(url):
    headers = {
        # "User-Token": "e986beb236d7c133bdfaf1cbbacf1035658a827e",     
        # "Uuid": "65b9e377939dcf739aa00f19a38bcd96",     
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        # "Accept": "application/json, text/plain, */*",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        # "Account-Id": "44930433",
        # "Connection": "keep-alive",
        "Cookie": "lastCity=101010100; __zp_seo_uuid__=003f1a24-b8c2-4bfb-8608-b8a54586904c; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1703578938; wd_guid=75c39bb5-8523-4285-b6df-9a4c521674fc; historyState=state; _bl_uid=Falaqq9ama12kpxhs292x2wom372; __zp_stoken__=8c4afw4%2FCucOeEkAMZxFjEl5zdsK7e8K%2Bw4BodmfDg8K2Y3JoZ8KGwrZ1wqfCuVTDh8OFc8OAd8KMUMKlcsKMwq3Co8KqwrLCq8SIwr%2FCuE7Cp8OGwpnEnsO5xIDDmFFLw4bCozo3DhQMCRANEwsKDw4UFxYTFwkRFBUWDBQRGD8qw77DqMKKPURHPyxTTVUNWGRbTmJMCmFNTjpAYBZbX0AtM8K%2Fw748RsOHw7vCvcKmwr3CvsK8w7TDg8OGwroXOkRGPsK5w4ovNcK7w7Epwr19CsK%2Fwp0Qw4MsC8K6w5Jhw45mw4jCqcKDwrxeNj5Dwr1GPxpAOzpBPUNGOj8qRMK7QcOKYcK8wq96w4BjMz4aRz1DRDw%2FPUNCOkEpQ0N8KT1GLkYPERAWEjBCw4Jawr%2FDnj1D; __l=r=https%3A%2F%2Fwww.google.com.hk%2F&l=%2Fwww.zhipin.com%2Fweb%2Fcommon%2F404.html&s=3&g=&friend_source=0&s=3&friend_source=0; __c=1703578937; __a=29932763.1703578937..1703578937.4.1.4.4; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1703579020",
    }

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        req = urllib.request.Request(url, headers=headers)
        
        response = urllib.request.urlopen(req, context=ssl_context)
        
        json = response.read().decode('utf-8', errors='replace')
        print(json)
        # 处理响应的代码
    except Exception as e:
        print(f"Error: {e}")
def askURL() :
    pass

def getGithub():
    url = "https://github.com/HYAdonisCoding"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        # "Cookie": "_gh_sess=WTV6mMzvEVi15Tl0yvTTWT8jnxLAxQm9JOvw3SXEnDIli8bwCRaSeHcnu3cTB4C0wMhIWPLZpsWu4bhHSapBT3avcdP5eHwxmeT2n8IcPmgZSC4DYfOfdj%2BQZoOeV94%2ButBwOzYGIFtlG58UyM%2FKYenUQ69z2ClVOJdzy4Z8F6OkD53PDg3FooQNlYxe%2FCA%2FUojyGffjAo1IMT%2FD%2BFn6phjE8DI8%2B54zQnEqIZNzaFEPnB1bPP8gegk1iVd0h6sEDfG1HIyIVJquEhgrdkFuLTndbXz63lZaKIuEz5VswhskoB9UiLD2FfqXT0WhwLl8S3LydXfeeH6XhSrrcxAj%2BeXHDxbREEm%2Fl2kCqA%3D%3D--knYvrSxR2%2Bj6MiT6--tS%2FIbpZ7GMp9htJgld46jg%3D%3D; has_recent_activity=1; preferred_color_mode=light; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; __Host-user_session_same_site=-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; user_session=-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; dotcom_user=HYAdonisCoding; logged_in=yes; saved_user_sessions=17538734%3A-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; _device_id=648221f4ac44895e5d728de16d3dbf02; _octo=GH1.1.390781214.1686124449"
    }
    temp = '_gh_sess=WTV6mMzvEVi15Tl0yvTTWT8jnxLAxQm9JOvw3SXEnDIli8bwCRaSeHcnu3cTB4C0wMhIWPLZpsWu4bhHSapBT3avcdP5eHwxmeT2n8IcPmgZSC4DYfOfdj%2BQZoOeV94%2ButBwOzYGIFtlG58UyM%2FKYenUQ69z2ClVOJdzy4Z8F6OkD53PDg3FooQNlYxe%2FCA%2FUojyGffjAo1IMT%2FD%2BFn6phjE8DI8%2B54zQnEqIZNzaFEPnB1bPP8gegk1iVd0h6sEDfG1HIyIVJquEhgrdkFuLTndbXz63lZaKIuEz5VswhskoB9UiLD2FfqXT0WhwLl8S3LydXfeeH6XhSrrcxAj%2BeXHDxbREEm%2Fl2kCqA%3D%3D--knYvrSxR2%2Bj6MiT6--tS%2FIbpZ7GMp9htJgld46jg%3D%3D; has_recent_activity=1; preferred_color_mode=light; tz=Asia%2FShanghai; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; __Host-user_session_same_site=-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; user_session=-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; dotcom_user=HYAdonisCoding; logged_in=yes; saved_user_sessions=17538734%3A-XIQ57jEbUtrVyy8moRHrhLMUed_uNJzT_FRJJNSkHVGpPSv; _device_id=648221f4ac44895e5d728de16d3dbf02; _octo=GH1.1.390781214.1686124449'
    # 稳妥方案
    cookie_list = temp.split("; ")
    cookies = {cookie.split('=')[0]: cookie.split('=')[0]for cookie in cookie_list}
    # cookies = {}
    # for cookie in cookie list:cookies [cookie.split('=') [0Y= cookie.split('=')[-1]
    print(cookies)
    response = requests.get(url,headers=headers)
    with open("51Job/Spider/github_without_cookies.html","wb")as f:
        f.write(response. content)

def get51JobData(args=""):
    url = "https://we.51job.com/pc/search?jobArea=090200&keyword=python&searchType=2&sortType=0&metro="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # "Cookie": "partner=sem_pcbaidupz_2; guid=65b9e377939dcf739aa00f19a38bcd96; ps=needv%3D0; 51job=cuid%3D44930433%26%7C%26cusername%3DqhY%252BWyZ%252BDqDzqpibTUqdOw%253D%253D%26%7C%26cpassword%3D%26%7C%26cname%3DvUExO%252BFmfosnxo92vX64Kg%253D%253D%26%7C%26cemail%3D7bo6NiJ6WNbnz8TH8H4T8hPEhjdvJ4kroRHglssL31s%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.05M%252FOG03ICwI%26%7C%26cconfirmkey%3Dho..ODtl3HoJk%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3Dho8z7Z4hF8Ndk%26%7C%26to%3De986beb236d7c133bdfaf1cbbacf1035658a827e%26%7C%26; sensor=createDate%3D2010-02-26%26%7C%26identityType%3D1; NSC_ohjoy-bmjzvo-200-159=ffffffffc3a0d61845525d5f4f58455e445a4a423660; sajssdk_2015_cross_new_user=1; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20231226%26%7C%26securetime%3DUm5WYgNlBWJTNFZvXWANZ1VvUGQ%253D; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2244930433%22%2C%22first_id%22%3A%2218ca50dc9d6838-01fd9cb0b4ebb3e-1f525637-2073600-18ca50dc9d71d8b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThjYTUwZGM5ZDY4MzgtMDFmZDljYjBiNGViYjNlLTFmNTI1NjM3LTIwNzM2MDAtMThjYTUwZGM5ZDcxZDhiIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNDQ5MzA0MzMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2244930433%22%7D%2C%22%24device_id%22%3A%2218ca50dc9d6838-01fd9cb0b4ebb3e-1f525637-2073600-18ca50dc9d71d8b%22%7D; Hm_lvt_1370a11171bd6f2d9b1fe98951541941=1703576758; Hm_lpvt_1370a11171bd6f2d9b1fe98951541941=1703577072; acw_tc=ac11000117035826104962044e00e0a79bcafd63bb73563dfca087cd2bdf9a; acw_sc__v2=658a9b9288d1cdf10d1d54c71d2cc12559ddc5db; search=jobarea%7E%60010000%7C%21recentSearch0%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60090200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60090200%2C010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAPython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAiOS%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; JSESSIONID=DADE23F9DDD73508D118FF26A37E07A4; ssxmod_itna=iqGOY5BK7K0IxYqeBcDeunIYdi=DCG8YtjSbfj0jDBuC4iNDnD8x7YDvIA5/YIGiDb54sb0+B+Q54SfYxH1GnSwKFqw+g0eD=xYQDwxYoDUxGtDpxG6osIDYYCDt4DTD34DYDig=DBSLK8D04z2aHzChIOzEKzDYP8mxDOAxGCF4GtP/HGB2Pee4iamx0CZhK7DmKDIp38b+5DFOoEE40kmxi3jYv6940O1FK7DBRz/xY8g4nDH=0eVDhk1BR4Fl2xPB0uHmiqxcrxN5UYFnGPOvxnLTDDiOxxLj+DD=; ssxmod_itna2=iqGOY5BK7K0IxYqeBcDeunIYdi=DCG8YtjSbfjjD8kPfu+DGNdPGaStGj6K88jYqidi/0k02hit7uApN3O+jvR1FB17ApP9YmW7vU75+nLpK8TY/g0KLTA6QNn4=8KUiUIh49K2XQZ5kfm0te1xNCnr5RD24CayrsQwH4Obba8haB1piQraz/ZosK/o1iKw=iGvhKr5bFSF=3gH7IYTpFpppXhLsHrpHygLG0oQNipgCekP8aSewafKeulvpI2AiUre0n6ZTwgEsWL3e8pkyqOmpTuHfe2PkFVO9p+jF/gnUK8kRc+gBBhgjI34yy8IS/P9K+8+ecAastq2jPvlw8UPX4pK0vG+98YG2/p=KDwURtbi444b/mgI+HGiiUA63gzBxwCbliuPXAtaP0GbfCDNGunmP84udK8wWatZPBUpOiRq=TTgcFFIK64sI44PHNUHsmPv7brjEFCwwWfpYdPc4OT5riMWtpopcUF0dpgiF0nBoOYMvULTnkzl+EWRaUYE9r7F0D050FD/zOc924N9KuBaF0DMe09ca+35M93D07dBq0GKz22b1q9DcfUG6FaXtKbta0D6o0oeYKnB3SU9ZtYgt6zG2sD=Pjq5Xgl0xL9Kl/3=BqBCaDsSsASHstdvfeiFKh80DArFlYkt0xX9BDp0KwD7IGDD7=DYKxeD=",
    }
    temp = 'partner=sem_pcbaidupz_2; guid=65b9e377939dcf739aa00f19a38bcd96; ps=needv%3D0; 51job=cuid%3D44930433%26%7C%26cusername%3DqhY%252BWyZ%252BDqDzqpibTUqdOw%253D%253D%26%7C%26cpassword%3D%26%7C%26cname%3DvUExO%252BFmfosnxo92vX64Kg%253D%253D%26%7C%26cemail%3D7bo6NiJ6WNbnz8TH8H4T8hPEhjdvJ4kroRHglssL31s%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.05M%252FOG03ICwI%26%7C%26cconfirmkey%3Dho..ODtl3HoJk%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3Dho8z7Z4hF8Ndk%26%7C%26to%3De986beb236d7c133bdfaf1cbbacf1035658a827e%26%7C%26; sensor=createDate%3D2010-02-26%26%7C%26identityType%3D1; NSC_ohjoy-bmjzvo-200-159=ffffffffc3a0d61845525d5f4f58455e445a4a423660; sajssdk_2015_cross_new_user=1; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20231226%26%7C%26securetime%3DUm5WYgNlBWJTNFZvXWANZ1VvUGQ%253D; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2244930433%22%2C%22first_id%22%3A%2218ca50dc9d6838-01fd9cb0b4ebb3e-1f525637-2073600-18ca50dc9d71d8b%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThjYTUwZGM5ZDY4MzgtMDFmZDljYjBiNGViYjNlLTFmNTI1NjM3LTIwNzM2MDAtMThjYTUwZGM5ZDcxZDhiIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNDQ5MzA0MzMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2244930433%22%7D%2C%22%24device_id%22%3A%2218ca50dc9d6838-01fd9cb0b4ebb3e-1f525637-2073600-18ca50dc9d71d8b%22%7D; Hm_lvt_1370a11171bd6f2d9b1fe98951541941=1703576758; Hm_lpvt_1370a11171bd6f2d9b1fe98951541941=1703577072; acw_tc=ac11000117035826104962044e00e0a79bcafd63bb73563dfca087cd2bdf9a; acw_sc__v2=658a9b9288d1cdf10d1d54c71d2cc12559ddc5db; search=jobarea%7E%60010000%7C%21recentSearch0%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch1%7E%60090200%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60090200%2C010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAPython%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60010000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAiOS%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; JSESSIONID=DADE23F9DDD73508D118FF26A37E07A4; ssxmod_itna=iqGOY5BK7K0IxYqeBcDeunIYdi=DCG8YtjSbfj0jDBuC4iNDnD8x7YDvIA5/YIGiDb54sb0+B+Q54SfYxH1GnSwKFqw+g0eD=xYQDwxYoDUxGtDpxG6osIDYYCDt4DTD34DYDig=DBSLK8D04z2aHzChIOzEKzDYP8mxDOAxGCF4GtP/HGB2Pee4iamx0CZhK7DmKDIp38b+5DFOoEE40kmxi3jYv6940O1FK7DBRz/xY8g4nDH=0eVDhk1BR4Fl2xPB0uHmiqxcrxN5UYFnGPOvxnLTDDiOxxLj+DD=; ssxmod_itna2=iqGOY5BK7K0IxYqeBcDeunIYdi=DCG8YtjSbfjjD8kPfu+DGNdPGaStGj6K88jYqidi/0k02hit7uApN3O+jvR1FB17ApP9YmW7vU75+nLpK8TY/g0KLTA6QNn4=8KUiUIh49K2XQZ5kfm0te1xNCnr5RD24CayrsQwH4Obba8haB1piQraz/ZosK/o1iKw=iGvhKr5bFSF=3gH7IYTpFpppXhLsHrpHygLG0oQNipgCekP8aSewafKeulvpI2AiUre0n6ZTwgEsWL3e8pkyqOmpTuHfe2PkFVO9p+jF/gnUK8kRc+gBBhgjI34yy8IS/P9K+8+ecAastq2jPvlw8UPX4pK0vG+98YG2/p=KDwURtbi444b/mgI+HGiiUA63gzBxwCbliuPXAtaP0GbfCDNGunmP84udK8wWatZPBUpOiRq=TTgcFFIK64sI44PHNUHsmPv7brjEFCwwWfpYdPc4OT5riMWtpopcUF0dpgiF0nBoOYMvULTnkzl+EWRaUYE9r7F0D050FD/zOc924N9KuBaF0DMe09ca+35M93D07dBq0GKz22b1q9DcfUG6FaXtKbta0D6o0oeYKnB3SU9ZtYgt6zG2sD=Pjq5Xgl0xL9Kl/3=BqBCaDsSsASHstdvfeiFKh80DArFlYkt0xX9BDp0KwD7IGDD7=DYKxeD='
    # 稳妥方案
    cookie_list = temp.split("; ")
    cookies = {cookie.split('=')[0]: cookie.split('=')[0]for cookie in cookie_list}
    # cookies = {}
    # for cookie in cookie list:cookies [cookie.split('=') [0Y= cookie.split('=')[-1]
    print(cookies)
    response = requests.get(url,headers=headers, cookies=cookies)
    with open("51Job/Spider/51_with_cookies.html","wb")as f:
        f.write(response. content)

def getCookies():
    url = 'http://www.baidu.com'
    response = requests.get(url)
    print(response.cookies)
    dict_cookies = requests.utils.dict_from_cookiejar(response.cookies)
    print('dict_cookies',dict_cookies)
    jar_cookies = requests.utils.cookiejar_from_dict(dict_cookies)
    print('jar_cookies',jar_cookies)
    
if __name__ == '__main__':
    # getData()
    # getGithub()
    getCookies()
    main()