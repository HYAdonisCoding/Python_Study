import time
t = time.time() # 时间戳 1970
print(t)

t = time.localtime(t) # 结构化的时间
print(t)
print(f'{t.tm_year}-{t.tm_mon}-{t.tm_mday} {t.tm_hour}:{t.tm_min}:{t.tm_sec}')

s = time.strftime('%Y-%m-%d %H:%M:%S')
print(s)
from easy_package    import easy_tools

print(easy_tools.get_time())

