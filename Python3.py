#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Fibonacci series: 斐波纳契数列
# 两个元素的总和确定了下一个数
#a, b = 0, 1
#while b < 1000:
#     print(b, end=',')
#     a, b = b, a+b #1 1 2 3 5 8

#Python 3支持int、float、bool、complex（复数）。
a, b, c, d = 20, 5.5, True, 4+3j
print(type(a), type(b), type(c), type(d))

#String（字符串）Python中的字符串str用单引号(' ')或双引号(" ")括起来，同时使用反斜杠(\)转义特殊字符。
s = 'Yes,he doesn\'t'
print(s, type(s), len(s))

#如果你不想让反斜杠发生转义，可以在字符串前面添加一个r，表示原始字符串：
print('C:\some\name')
print(r'C:\some\name')

#另外，反斜杠可以作为续行符，表示下一行是上一行的延续。还可以使用"""..."""或者'''...'''跨越多行。字符串可以使用 + 运算符串连接在一起，或者用 * 运算符重复：
print('str'+'ing', 'my'*3)

#Python中的字符串有两种索引方式，第一种是从左往右，从0开始依次增加；第二种是从右往左，从-1开始依次减少。
#注意，没有单独的字符类型，一个字符就是长度为1的字符串。
word = 'Python'
print(word[0], word[5])
print(word[-1], word[-6])

#还可以对字符串进行切片，获取一段子串。用冒号分隔两个索引，形式为变量[头下标:尾下标]。
#截取的范围是前闭后开的，并且两个索引都可以省略：
word = 'ilovepython'
print(word[1:5])
print(word[:])
print(word[5:])
print(word[-10:-6])

#List（列表）
a = ['him', 25, 100, 'her']
print(a)
#列表还支持串联操作，使用+操作符：
a = [1, 2, 3, 4, 5]
a = a + [6, 7, 8]
print(a)

#列表中的元素是可以改变的
a[0] = 9
a[2:5] = [13, 14, 15]
print(a)
a[2:5] = []   # 删除
print(a)

#Tuple（元组）

#元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号里，元素之间用逗号隔开。
#元组中的元素类型也可以不相同
a = (1991, 2014, 'physics', 'math')
print(a, type(a), len(a))

tup1 = () # 空元组
tup2 = (20,) # 一个元素，需要在元素后添加逗号

#元组也支持用+操作符：
tup1, tup2 = (1, 2, 3), (4, 5, 6)
print(tup1+tup2)

#Sets（集合）
#集合（set）是一个无序不重复元素的集。
student = {'Tom', 'Jim', 'Mary', 'Tom', 'Jack', 'Rose'}
print(student)   # 重复的元素被自动去掉

print('Rose' in student)  # membership testing（成员测试）

a = set('abracadabra')
b = set('alacazam')
print(a)

print( a - b )    # a和b的差集

print(a | b )    # a和b的并集

print(a & b)     # a和b的交集

print(a ^ b)     # a和b中不同时存在的元素


#Dictionaries（字典）
dic = {}  # 创建空字典
tel = {'Jack':1557, 'Tom':1320, 'Rose':1886}
print(tel)

print(tel['Jack'] )  # 主要的操作：通过key查询
# 删除一个键值对
#del tel['Rose']
print(tel) 


print(list(tel.keys()) ) # 返回所有key组成的list



sorted(tel.keys()) # 按key排序
 # 成员测试
print('Tom' in tel)
print('Mary' not in tel) 

#dict=dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
#print(dict)

print({x: x**2 for x in (2, 4, 6)})
#dict=dict(sape=4139, guido=4127, jack=4098)
print(dict(sape=4139, guido=4127, jack=4098))












