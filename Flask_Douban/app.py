# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import datetime
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    # return 'Hello, Eason!'
    return home()

@app.route('/movie')
def movie_default():
    # 获取参数
    start = request.args.get('start', default=0, type=int)

    dataList = []
    conn = sqlite3.connect("movietop250.db")
    print('Open database connection')
    c = conn.cursor() # 获取游标
    sql = 'select * from movie250 limit 25 offset ' + str(start) + ';'
    cursor = c.execute(sql)
    i = 0
    data = []
    for row in cursor:
        data = list(row)
        i = i + 1
        data.insert(0, start+i)
        dataList.append(data)
    c.close()
    conn.close()
    print('查询 successfully')
    return render_template('movie.html', datas = dataList)


if __name__ == '__main__':
     app.run(debug=True)