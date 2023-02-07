n = 0
while n < 1 or n > 20:
    n = int(input('请输入[1,20]范围内的整数：'))
# n 行
for i in range(1, n + 1):
    print('🤎' * i)