n=0
while n < 1 or n > 100:
    n = int(input( '请输入[1, 100 ]的数: ' ))
#1+2+3+ 4
ret = 0
for i in range(1, n + 1):
    ret += i
print(f'结果是{ret}')

# 1-2+3-4+...+ n (所有的奇数相加，减去所有的偶数)
ret = 0
for i in range(1,n+1):
    ret += i if i % 2 else -i
print(f'结果是{ret}')
#1+3+5+7+...+ n (所有的奇数相加)
ret = 0
for i in range(1, n + 1, 2):
 ret += i
print(f'结果是{ret}')