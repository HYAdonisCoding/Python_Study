# -*- coding: utf-8 -*-

# https://movie.douban.com/top250
from bs4 import BeautifulStoneSoup # 网页解析，获取数据
import re # 正则表达式，进行文字匹配
import urllib.request,urllib.error # 制定URL，获取网络数据
# import xlwt # 进行Excel操作
import sqlite3

def mian():
    baseurl = 'https://movie.douban.com/top250'
    # 1. 爬取网页
    dataList = getData(baseurl)
    savePath = ".\\top250.xlsx"
    # 2.获取数据
    
    # 3.保存数据
    saveData(savePath)

def getData(baseurl):
    dataList = []
    return dataList
    
def saveData(path):
    pass
if __name__ == '__main__':
    print("Starting douban1")
