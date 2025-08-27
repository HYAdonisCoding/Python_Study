n = int(input('请输入秒数：'))
hour = n // 3600
minute = n % 3600 // 60
second = n % 60
print(f'{n}秒等于{hour}时{minute}分{second}秒')