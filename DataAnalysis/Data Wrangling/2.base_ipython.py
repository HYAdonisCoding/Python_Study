#!/usr/bin/env python3
# filepath: /Users/adam/Documents/Developer/MyGithub/Python_Study/Proficient/recursion.py
# coding: utf-8
speter = "-" * 10

# 利用Python进行数据分析
# Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython

# 第二章 Python 语言基础
def control_condition():
    x = 5
    print('Non-negative' if x > 0 else 'negative')
from datetime import datetime, date, time, timedelta
# import datetime  # 导入整个模块
def test_date():
    dt = datetime(2026, 10, 29, 20, 30, 21)
    print(dt.day)
    print(dt.minute)
    print(dt.strftime("%Y-%m-%d %H:%M"))
    print(datetime.strptime("20091031", "%Y%m%d"))
    dt2 = datetime(2026, 11, 29, 20, 30, 21)
    delta = dt2 - dt
    
    print(delta)
    print(type(delta))
    print(timedelta(17, 7197))
    
def add_and_maybe_mutiply(a, b, c=None):
    result = a + b
    if c is not None:
        result = result * c
    return result
def unicode():
    val = "español"
    print(val)
    val_utf8 = val.encode("utf-8")
    print(val_utf8)
    print(type(val_utf8))
    val1 = val_utf8.decode("utf-8")
    print(val1)
    
def formatte():
    template = "{0:.2f} {1:s} are worth US${2:d}"
    print(template.format(88.46, "Argentine Pesos", 1))
    print(template.format(88.4123236, "Argentine Pesos", 9))

def duck_type():
    def isiterable(obj):
        try:
            iter(obj)
            return True
        except TypeError: # not iterable
            return False
    print(isiterable("a string"))
    print(isiterable([1, 2, 3]))
    print(isiterable(5))

def test():
    pass
if __name__ == "__main__":
    print(f"{speter*2}Starting{speter*2}")
    try:
        control_condition()
    except KeyboardInterrupt:
        print(f"{speter*2}手动退出程序{speter*2}")
    finally:

        print(f"{speter*2}Finished{speter*2}")


