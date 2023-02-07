n = 0
k = 1
while n < k or n > 20:
    n = int(input(f'请输入[{k},20]范围内的整数：'))

for i in range(n):
    c = '🤎' * (n - i - 1)
    print(c + '💚' * (2 * i + 1) + c)