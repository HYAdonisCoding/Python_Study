import requests
post_url = 'http://fanyi.baidu.com/sug'
post_url = 'https://fanyi.baidu.com/v2transapi?'

headers = {
    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
    # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    # 'X-Requested-With': 'XMLHttpRequest',
}


data = {
    # 'kw': 'man',
    'from': 'en',
    'to': 'zh',
    'query': 'cavern',
    'transtype': 'enter',
    'simple_means_flag': '3',
    'sign': '834358.546823',
    'token': '05a1bfdc838e5296a22a6240829ac981',
    'domain': 'common',
    'ts': '1718696060859',
} 
response = requests.post(url=post_url, data=data, headers=headers)

# 以字符串形式来返回网页的源码
content = response.text
import json
obj = json.loads(content)
print(obj)
print(response.status_code)