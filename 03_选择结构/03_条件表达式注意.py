a = 30
b = 70


if a > b:
    print(f'最大值是{a}')
else:
    print(f'最大值是{b}')
    
print('-----等价写法------')

print(f'最大值是{a if a > b else b}')


print(f'最大值是：{max(a, b)}, 最小值是：{min(a, b)}')