# 编写一个函数：可以向任意多个人打招呼
def hello(*names):
    for n in names:
        print(f'Hi, {n}!')
        
hello('Eason', 'Jack', 'Rose', '燕云少君')

hello('Eason', 'Jack', 'Rose')

hello('Eason', 'Jack')

hello('Eason')

hello()