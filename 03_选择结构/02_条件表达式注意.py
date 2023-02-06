i = int(input('请输入数字：'))


if i % 2 == 0:
    print('偶数')
else:
    print('奇数')
    
print('-----等价写法------')

print('偶数') if i % 2 == 0 else print('奇数')