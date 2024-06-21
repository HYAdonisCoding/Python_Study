# 进入到scrapy shell的终端 直接在window的终端中输人scrapy shell 域名
# 如果想看到一些高亮 或者 自动补全 那么可以安装ipython pip install ipython

# scrapy shell www.baidu.com

'''
In [4]: response.status
Out[4]: 200

2024-06-21 09:07:40 [asyncio] DEBUG: Using selector: KqueueSelector
In [5]: response.xpath('//input[@id="su"]')
Out[5]: [<Selector query='//input[@id="su"]' data='<input type="submit" id="su" value="百...'>]

2024-06-21 09:08:33 [asyncio] DEBUG: Using selector: KqueueSelector
In [6]: response.xpath('//input[@id="su"]/@value')
Out[6]: [<Selector query='//input[@id="su"]/@value' data='百度一下'>]

2024-06-21 09:08:47 [asyncio] DEBUG: Using selector: KqueueSelector
In [7]: a = response.xpath('//input[@id="su"]/@value')

2024-06-21 09:09:02 [asyncio] DEBUG: Using selector: KqueueSelector
In [8]: a
Out[8]: [<Selector query='//input[@id="su"]/@value' data='百度一下'>]

2024-06-21 09:09:09 [asyncio] DEBUG: Using selector: KqueueSelector
In [9]: a.extract_first()
Out[9]: '百度一下'

2024-06-21 09:09:24 [asyncio] DEBUG: Using selector: KqueueSelector
In [10]: a.extract()
Out[10]: ['百度一下']

In [11]: b = response.css('#su::attr("value")')

2024-06-21 09:11:25 [asyncio] DEBUG: Using selector: KqueueSelector
In [12]: b
Out[12]: [<Selector query="descendant-or-self::*[@id = 'su']/@value" data='百度一下'>]

2024-06-21 09:11:28 [asyncio] DEBUG: Using selector: KqueueSelector
In [13]: b.extract_first()
Out[13]: '百度一下'
'''
