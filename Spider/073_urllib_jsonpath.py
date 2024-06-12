# https://blog.csdn.net/luxideyao/article/details/77802389
import os
import json
import jsonpath

# 获取当前文件所在目录
current_directory = os.path.dirname(os.path.abspath(__file__)) + '/'
json_file = current_directory + '073_jsonpath.json'

obj = json.load(open(json_file, 'r', encoding='utf-8'))

# 书点所有书的作者
ret = jsonpath.jsonpath(obj, '$.store.book[*].author')
print(ret)
# 所有的作者
# ret = jsonpath.jsonpath(obj, '$..author')
# print(ret)

	
# store的所有元素。所有的bookst和bicycle
# ret = jsonpath.jsonpath(obj, '$.store.*')
# print(ret)
# store里面所有东西的price
# ret = jsonpath.jsonpath(obj, '$.store..price')
# print(ret)
# 第三个书
# ret = jsonpath.jsonpath(obj, '$..book[2]')
# print(ret)
# 最后一本书
# ret = jsonpath.jsonpath(obj, '$..book[(@.length-1)]')
# print(ret)
# 前面的两本书。
# ret = jsonpath.jsonpath(obj, '$..book[0,1]')
# ret = jsonpath.jsonpath(obj, '$..book[:2]')
# print(ret)
# 过滤出所有的包含isbn的书。
# ret = jsonpath.jsonpath(obj, '$..book[?(@.isbn)]')
# print(ret)
# 过滤出价格低于10的书。
# ret = jsonpath.jsonpath(obj, '$..book[?(@.price<10)]')
# print(ret)
# 所有元素。
# ret = jsonpath.jsonpath(obj, '$..*')
# print(ret)