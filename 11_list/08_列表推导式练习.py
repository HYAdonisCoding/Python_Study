import random as r

# 统计每一个随机数的出现次数

edge = 10
size = 20

nos = [r.randrange(edge) for _ in range(size)]

all_times = [0 for _ in range(edge)]
for no in nos:
    all_times[no] += 1

print(nos)
for no, times in enumerate(all_times):
    print(f'{no}出现了{times}次')
    
print(all_times)


# 从小到大打印随机数
for no, times in enumerate(all_times):
    print(f'{no} ' * times, end='')

print()
print('-' * 30)

for no, times in enumerate(all_times):
    for _ in range(times):
        print(no, end=' ')