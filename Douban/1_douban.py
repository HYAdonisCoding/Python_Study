# -*- coding: utf-8 -*-

# https://movie.douban.com/top250
from bs4 import BeautifulSoup # 网页解析，获取数据
import re # 正则表达式，进行文字匹配
import urllib.request, urllib.error # 制定URL，获取网络数据
import xlwt # 进行Excel操作
import sqlite3
import certifi
import ssl

def main():
    baseurl = 'https://movie.douban.com/top250?start='
    # 1. 爬取网页
    dataList = getData(baseurl)
    savePath = "top250.xlsx"
    savePathDB = "movietop250.db"
    
    
    # 3.保存数据
    saveData(dataList, savePath)
    # saveData2DB(dataList,savePathDB)
    
# 影片详情的规则
findLink = re.compile(r'<a href="(.*?)">')
# 影片图片的规则
findImgSrc = re.compile(r'<img .*? src="(.*?)".*?/>', re.S)
# 影片片名的规则
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片评分的规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 影片评价人数的规则
findNum = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况的规则
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 影片相关内容的规则
findComment = re.compile(r'<p class="">(.*?)</p>', re.S)

def getData(baseurl):
    dataList = []
    for i in range(0, 10):
        url = baseurl + str(i*25)
        html = askURL(url)
        
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='item'):
            data = []
            item = str(item)
            # print(item)
            link = re.findall(findLink, item)[0]
            data.append(link)
            
            img = re.findall(findImgSrc, item)[0]
            data.append(img)
            
            title = re.findall(findTitle, item)
            if len(title) > 1:
                data.append(title[0])
                t = title[1].replace('/', '')
                data.append(configSpace(t))
            else:
                data.append(title[0])
                data.append("")
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            num = re.findall(findNum, item)[0]
            data.append(num)
            ing = re.findall(findInq, item)
            if len(ing) > 0:
                data.append(configSpace(ing[0]))
            else:
                data.append("")
            c = re.findall(findComment, item)[0]
            c = c.replace('<br/>', '')
            c = c.replace('/', ' ')
            c = c.replace("\n", ' ')
            c = configSpace(c)
            data.append(c)
            
            print(data)
            dataList.append(data)   
    return dataList

def configSpace(str):
    pattern = re.compile(r"\s+")
    str1 = re.sub(pattern, " ", str)
    return str1
def saveData2DB(datalist, dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] ='"'+data[index]+'"'
        sql = '''
            insert into movie250 
            (info_link,pic_link,cname,ename, score,rated, instrodction, info)
            values(%s)'''%",". join(data)
        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()   
        
def init_db(dbpath):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    sql = '''
            create table movie250 
            (info_link text,
            pic_link text,
            cname text,
            ename text, 
            score real,
            rated real, 
            instrodction text, 
            info text);
        '''
    print(sql)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def askURL(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        req = urllib.request.Request(url, headers=headers)
        
        response = urllib.request.urlopen(req, context=ssl_context)
        return response.read().decode('utf-8', errors='replace')
        # 处理响应的代码
    except Exception as e:
        print(f"Error: {e}")
        return ""
    finally:
        print(f"完成: {url}")

def saveData(dataList, path):
    # 创建一个Workbook对象
    workbook = xlwt.Workbook()
    # 添加一个sheet
    sheet = workbook.add_sheet('sheet1')

    # 写入表头
    titles = ['info_link', 'pic_link', 'cname', 'ename', 'score', 'rated', 'instrodction', 'info']
    for i in range(0, len(titles)):
        sheet.write(0, i, titles[i])

    # 写入表格数据
    for i in range(0, len(dataList)):
        item = dataList[i]
        for j in range(0, len(item)):
            sheet.write(i+1, j, item[j])

    # 保存文件
    workbook.save(path)
if __name__ == '__main__':
    print("Starting Spiders")
    # init_db('movie.db')
    main()
    print("Spiders successfully")
