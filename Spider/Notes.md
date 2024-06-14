### 2.JsonPath

```
jsonpath的安须及使用方式:
pip安装:


pip install jsonpath


jsonpath的使用:
obj = json.load(open("json文件”，"r”, encoding 'utf-8'))
ret = jsonpath.isonpath(obj，“jsonpath语法')
收程连授(htto/blox.csdn.netuxidevao/article/details/77802389)

练习淘票票
作业:1.股票信息提取 (http://quore.stockstar.com/)
2.boos直聘
3.中华英才
4.汽车之家
```



### 3.BeautifulSoup

1.简介

```
1.Beautifulsoup简称bs4
2.什么是Beatifulsoup?
Beautifulsoup，和1xml一样，是一个html的释折器，主要功能也导解析和提取数据

3.优缺点?
缺点:效率没有lxml的效率高
优气:接口设计人性化，使用方便
```

2,安装以及创建

```
1.安装
pip install bs4
2.导入
from bs4 import Beautifulsoup
3.创建对象
服务器响应的文件生成对象
soup = Beautifulsoup(response.read().decode()，"1xm1')本地文件生成对象
soup = Beautifulsoup(open('1.htmi'),'lxml')注意;默认打开文件的编巧格式gbk所以需要指定打开编码格式
```

3.节点定位

```
1.根据标签名查找节点
soup.a [注] 只能找到第一个a
soup.a.name
soup.a.attrs
2.函数
	（1）.find（返回一个对象）
    find('a'):只找到第一个a标签
    find('a', title=‘名字'）
    find('a', class=‘名字'）
（2）.find_a11（返回一个列表）
  find_al1('a') 直找到所有的a
  find_all(['a'，'span']) 返回所有的a和spanfind_al1('a'，1imit=2) 只找前两个a
  （3）.select（根据选择器得到节点对象）【推荐】
  1. element
    eg: p
  2. class
    eg: .firstname
  3. #id
    eg: #firstname
4.属性性选择器
	[attribute]
		eg:li = soup. select('li[class]')
	[attribute=value]
		eg:li = soup. select ('li [class="hengheng1"]')
5.层级选择器
	element element
		div p
	element>element
		div>p 
	element, element
		div,p
	eg: soup = soup. select ('a, span')
```

4.节点信息

```
（1）.获取节点内容：适用于标签中嵌套标签的结构
  obj.string
  obj.get_text()【推荐】
```

今日任务：

- 爬虫
