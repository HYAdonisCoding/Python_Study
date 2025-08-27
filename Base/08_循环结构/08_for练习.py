high = 0 # 初始值要比所有分数都底
low = 100 # 初始值要比所有分数都高

for i in range(1, 6):
    score = int(input(f'请输入第{i}位学员的分数：'))
    
    high = max(score, high)
    
    low = min(score, low)

print(f'最高分是：{high}, 最低分是：{low}')