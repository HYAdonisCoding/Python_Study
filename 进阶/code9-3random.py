import random

# 生成随机小数
a = random.random()
print(a)

# 生成随机整数
# for i in range(10):
    # a = random.randint(0, 100)
    # print(a)

a = random.randint(0, 100)
print(a)

#  获取列表中的随机元素
list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(list1[random.randint(0,len(list1)-1)])
print(random.choice(list1))
print(random.choice('hello_world'))

print(ord('A'), ord('Z'))
# 随机生成一个字母组成的列表
from easy_package import easy_tools, easy_games

print(easy_tools.random_string(5))

random.shuffle(list1)
print(list1)

# easy_games.rockPaperScissors()

easy_games.guess_number(0, 100)

