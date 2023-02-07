n = 0
k = 3
while n < k or n > 20:
    n = int(input(f'请输入[{k},20]范围内的整数：'))

for i in range(n):
    c = '💚' if 0 < i < n-1 else '🤎'
    print('🤎' + c * (n - 2) + '🤎')
    
# for i in range(n):
#     if i == 0 or i == n - 1:
#         print('🤎' * n)
#     else:
#         print('🤎' + '💚' * (n - 2) + '🤎')