# StudyPython
This is my code of Study Python.

```python
html = open("jobPage.html", "r")

bs = BeautifulSoup(html,"html.parser")

jnames = bs.select(".cn > h1")
for name in jnames:
print(name)


joinfo  jhafa0](““)3 88:时和地区 1成餐(家限)1历1招人布

cnameList = bs.select(".cname a")#公司名称

jobMsgList = bs.select(".job_msg > p") # 工作描过
jobMsgStr = ""
for str in jobMsgList:
  jobMsgStr = jobMsgStr + str.text
days = bs.select(".itype")
# print(days[0].text.strip())
info = days[0]["title"].split("|")
# for inf in info:
#  print(inf.strip())
print(info[0].strip())
print(info[1].strip()[0:-2])
```

模板推荐:
https://bootstrapmade.com/
https://colorlib.com/wp/templates/
https://colorlib.com/wp/free-bootstrap-admin-dashboard-templates/
视频里面的模板:
https://startbootstrap.com/themes/sb-admin-2/



### 什么是异步加载的数据?

表现形式:6个例子
1. NHK新闻:https://www3.nhk.orjp/news/special/coronavirus/latest-news!
2. 人民网:http://liuyan.people.com.cn/threads/list?fid=5062&position=1
3. B站评论区:https://www.bilibili.com/video/BV1Mf4v197ci
4. 百度地图:https://map.baidu.com/@11585725.3557560.15.71z
5. 网易邮箱注册:https://mail.163.com/register/index.htm
6. 花瓣网:https://huaban.com/search/?g=%E7%BE%8E%E9%A3%9F

什么是异步加载的数据?

#### 辅助工具

- Chrome浏览器调试工具

- Postman

#### 应用场景

- 优化用户体验
- 用户行为分析
- 提升开发效率
