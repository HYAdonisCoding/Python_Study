import random as r

n = r.randint(0, 1000)
k = -1# 猜测的答案
x = 0 # 猜测的次数

# 如果回答错误，就提示再次输入答案
while k != n:
    if x:
        print('猜大了' if k > n  else '猜小了')
    k = int(input('请输入你的答案：'))
    x += 1
    
    
# while k != n:
#     if x:
#         print('猜大了') if k > n else print('猜小了')
#     k = int(input('请输入你的答案：'))
#     x += 1
    

# while k != n:
#     if x:
#         if k > n:
#             print('猜大了')
#         else:
#             print('猜小了')
#     k = int(input('请输入你的答案：'))
#     x += 1

# 回答正确

print(f'经过{x}次猜测，恭喜回答正确，答案是{n}')