# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import datetime
import sqlite3
import re # 正则表达式，进行文字匹配

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    # return 'Hello, Eason!'
    return home()

# 词云
@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/score')
def score():
    scores = []
    nums = []
    conn = sqlite3.connect("movietop250.db")
    print('Open database connection')
    c = conn.cursor() # 获取游标
    sql = 'select score, count(score) from movie_top250 group by score'
    
    cursor = c.execute(sql)

    for row in cursor:
        scores.append(str(row[0]))
        nums.append(row[1])
    
    sql = 'select year, count(year) from movie_top250 group by year'
    cursor = c.execute(sql)
    yearData=[]
    for row in cursor:
        print(row[0], row[1])
        yearData.append({ 'value': row[1], 'name': row[0] })
    sql = 'select nation, count(nation) from movie_top250 group by nation'
    cursor = c.execute(sql)
    nationDatas = []
    for row in cursor:
        # { value: 40, name: 'rose 1' },
        nationDatas.append({ 'value': row[1], 'name': row[0] })
    # print(nationDatas)
    c.close()
    conn.close()
    print('查询 successfully')
    # [{ value: 40, name: 'rose 1' },]
    return render_template('score.html', scores = scores, nums = nums, nationDatas=nationDatas,yearData=yearData)


@app.route('/movie')
def movie_default():
    # 获取参数
    start = request.args.get('start', default=0, type=int)
    dataList = get_data_privite(start)
    return render_template('movie.html', datas = dataList)

@app.route('/get_data')
def get_data():
    start = 0
    # 通过 request.args 获取 URL 中的查询参数
    page = request.args.get('page', default=-1, type=int)
    print('page', page)
    if page != -1 and page<=10:
        start = page * 25;
    return get_data_privite(start)

def get_data_privite(start):
    
    dataList = []
    conn = sqlite3.connect("movietop250.db")
    print('Open database connection')
    c = conn.cursor() # 获取游标
    sql = 'select * from movie_top250 limit 25 offset ' + str(start) + ';'
    cursor = c.execute(sql)
    # i = 0
    # data = []
    for row in cursor:
        # data = list(row)
        # i = i + 1
        # data.insert(0, start+i)
        # dataList.append(data)
        dataList.append(row)
    c.close()
    conn.close()
    print('查询 successfully')
    return dataList

if __name__ == '__main__':
     app.run(debug=True)