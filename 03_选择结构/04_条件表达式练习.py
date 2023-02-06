n = 30
k = 8 # 每页的数据量

# if n % k == 0:
#     v = n // k
# else:
#     v = n // k + 1
    
# print(f'需要的页数为{v}页')

# v = n // k
# if n % k != 0:
#     v += 1
    
# print(f'需要的页数为{v}页')


# v = n // k + (1 if n % k else 0)

v = (n + k - 1) // k
    
print(f'需要的页数为{v}页')