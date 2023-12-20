# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/index')
def helloEason():
    return 'Hello, Eason!'

@app.route('/user/<username>')
def helloEvery(username):
    return 'Hello, %s!'%username

@app.route('/user/<int:id>')
def helloEvery2(id):
    return 'Hello, %d 号的会员!'%id

@app.route('/user/<float:id>')
def helloEvery3(id):
    return 'Hello, 身高%f 米的会员!'%id

@app.route('/today')
def hello1():
    time = datetime.date.today()
    names = ['Eason', 'Jack', 'John', 'Mike']
    task = {'name': 'clean room', 'time': '1 hour'}
    return render_template('index_today.html', var = time, names = names, tasks = task)

#  向页面传递变量

@app.route('/user/register')
def user_register():
    time = datetime.date.today()
    return render_template('users/register.html', var = time)

@app.route('/user/result', methods=['POST','GET'], endpoint='user_result')
def user_register_result():
    print('user_register_result() ：', request.method)
    if request.method == 'POST':
        results = request.form
        print(results)
        return render_template('users/result.html', result = results)
    else:
        return 'Error registering'

if __name__ == '__main__':
     app.run(debug=True)