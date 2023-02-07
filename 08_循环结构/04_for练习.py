n=0
while n < 1 or n > 100:
    n = int(input('请输入[1, 20]的数: '))
line = '💜' * n
for i in range(n):
    print(line)
    
# for i in range(n):
#     print('🖤' * i)

# for i in range(1, n*n+1):
#     end = '' if i % n else '\n'
#     print('🖤', end=end)

# for i in range(1, n * n + 1):
#     # print('%02d' % i, end= ' ')
#     print('🖤', end="")
#     if i % n == 0:
#         print('')

for i in range(n * n):
    # print('%02d' % i, end= ' ')
    print('🖤', end="")
    if(i + 1) % n == 0:
        print('')
        
line = '🤎' * n
for _ in range(n):
    print(line)
    
#