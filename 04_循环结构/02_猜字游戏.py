import random as r

left = 0
right = 1000
answer = r.randint(left, right)
guess = -1# 猜测的答案
times = 0 # 猜测的次数

# 如果回答错误，就提示再次输入答案
while answer != guess:
    if guess > answer:
        right = min(right, guess - 1) 
    else:
        left = max(guess + 1, left)
    guess = int(input(f'请输入[{left}, {right}]范围内的整数：'))
    times += 1
    
    
# 回答正确

print(f'经过{times}次猜测，恭喜回答正确，答案是{guess}')