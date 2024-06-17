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

### 4.selenium

1. 什么是selenium？

2. 为什么使用selenium？

模拟浏览器功能，自动执行网页中的js代码，实现动态加载

3. 如何安装selenium？

（1）换作谷歇浏览器驱动下载地址

http://chromedriver.storage.googleapis.com/index.html

（2）谷歌驱动和谷歇浏览器版本之间的映射表

http://blog.csdn.net/huilan_same/article/details/51896672

（3） 查看谷歇浏览器版本

谷歌浏览器右上角 ->帮助-->关于

(4) pip install selenium

4. selenium的使用步骤？

```
(1) 导入: from selenium import webdriver
(2) 创建谷歌浏览器操作对象：
path = 谷歌浏览器驱动文件路径
browser = webdriver .Chrome(path)
(3) 访问网址
ur1 = 要访问的网址
browser.get(url)
```

4-1: selenium的元素定位？

元素定位：自动化要做的就是模拟鼠标和键盘来操作来操作这些元素，点击、输入等等。操作这些元素前首先

要找到它们，webDriver提供很多定位元素的方法

方法：

```

1. find_element_by_id
	eg: button = browser.find_element_by_id('su')
2. find_elements_by_name
	eg: name = browser.find_element_by_name('wd')
3. find_elements_by_xpath
	eg: xpath1 = browser.find_elements_by_xpath('//input[@id="su"]')
4. find_elements_by_tag_name
	eg:names = browser.find_elements_by_tag_name('input')
5. find_elements_by_css_selector
	eg:my_input = browser.find_elements_by_css_selector ('#kw')[0]
6.find_elements_by_link_text
	eg:browser. find_element_by_link_text ("#Fil")



```

4-2：访问元素信息

```
获取元素厲性
	.get_attribute('class')
获取元素文本
	.text
获取标签名
	.tag_name
```

4-3：交互

```python
点击：click()
輸入：send_keys()
后退操作：browser.back()
前进操作：browser.forword()模拟JS滚动：
js = document. documentElement. scrollTop=100000'
browser.execute_script（js）执行js代码获取网页代码：page_source
退出：browser.quit()
```

2.Phantomjs

1. ﻿﻿什么是Phantomjs？

   ```
   （1）是一个无界面的浏览器
   （2）支持页面元素查找，js的执行等
   （3）由于不进行css和gui渲染，运行效率要比真实的浏览器要快很多
   ```

   

2. ﻿﻿如何使用Phantomjs？

   ```
   (1) 获取PhantomJS.exe文件路径path
   (2) browser = webdriver.PhantomJS(path)
   (3) browser.get(url)
   扩展：保存屏幕快照：browser.save_screenshot('baidu.png')
   ```

   

3.Chrome handless

```
1.系统要求：
  Chrome
		Unix/Linux 系統需要 chrome >= 59
		windows 系统需要 chrome >= 60

	Python3.6
	Selenium==3.4. *
	ChromeDriver==2.31
```



```
2.配置：
```

今日任务：

- 
- 5c:1b:f4:8a:a7:7e
