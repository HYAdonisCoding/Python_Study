# 编写一个函数：可以向任意多个人打招呼
def hello(*names, title='Hi'):
    for n in names:
        print(f'{title}, {n}!')
        
hello('Eason', 'Jack', 'Rose', '燕云少君', title='您好')

hello('Eason', 'Jack', 'Rose')

print(11,22,33,44,55,66,sep='+', end='=')
max(10, 20, 30, 40)