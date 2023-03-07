# 存放所有的出现次数
# 字符是key，次数是value
d = {}

# 接收用户的输入
# for c in input('请输入文字：'):
#     # 统计字符c出现的次数
#     d[c] = d.get(c, 0) + 1


# 接收用户的输入
for c in input('请输入文字：'):
    # 统计字符c出现的次数
    d[c] = d.get(c) + 1 if c in d else 1
    
# 接收用户的输入
# for c in input('请输入文字：'):
#     # 统计字符c出现的次数
#     if c in d:
#         d[c] = d.get(c) + 1
#     else:
#         d[c] =  1
    
# 打印
for k in d:
    print(f'【{k}】出现了{d[k]}次')