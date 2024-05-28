# 纸的厚度

# n = 0.1
# w = n
# for i in range(50):
#     w *= 2
#     print(w)

# 国王麦粒
# 1, 2, 4, 8, 16
g = 1 # 当前格子应该放的麦粒数
total = 0 # 总的麦粒数
a = 1 # 棋盘的格子数量

# while a<= 100:
#     total += g # 计算当前的总数
#     g *= 2 # 当前格子应该放的麦粒数*2
#     print('在放满了%d个格子后， 总的麦粒数是%d, 下一个格子的麦粒数是：%d'%(a, total, g))
#     a += 1 # 走到下一个格子
    
    

# print(total)

# 人生的复利 (1+0.01)
day = 0
result = 1
while day < 365:
    result = result * 1.01
    day += 1
    print(result)