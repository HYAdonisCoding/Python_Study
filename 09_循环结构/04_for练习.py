n=0
while n < 1 or n > 100:
    n = int(input('请输入[1, 100 ]的数: '))
line = '💜' * n
for i in range(n):
    print(line)
    
# for i in range(n):
#     print('💜' * n)