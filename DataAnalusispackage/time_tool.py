import datetime
import time
import functools

def log(func, content):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function '{func.__name__}' with arguments: {args} and keyword arguments: {kwargs}, content: {content}")
        # 记录函数执行时间
        
        time1 = datetime.datetime.now()
        func(*args, **kwargs)
        time2 = datetime.datetime.now()
        print(f"Function '{func.__name__}' 循环耗时: {(time2 - time1).seconds} seconds")
    return wrapper

def log_comment(content):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling function '{func.__name__}' with content: {content}")
            # 记录函数执行时间
            time1 = datetime.datetime.now()
            func(*args, **kwargs)
            time2 = datetime.datetime.now()
            print(f"Function '{func.__name__}' 循环耗时: {(time2 - time1).seconds} seconds")
        return wrapper
    return decorator