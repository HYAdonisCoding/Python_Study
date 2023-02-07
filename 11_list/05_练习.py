s = [56 , 78, 100, 89, 0, 96]


# while True:
#     print(s)
    
#     s[int(input('请输入索引：'))] = int(input('请输入分数：'))
#     print()
    
while True:
    print(s)
    
    index = int(input('请输入索引：'))
    score = int(input('请输入分数：'))
    s[index] = score
    print()