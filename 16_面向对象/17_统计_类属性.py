# 需求
# 实时统计程序中一共有多少条狗
# 比如：每创建一条狗就打印：创建了第XX条狗

class Dog:
    count = 0
    def __init__(self, name):
        self.__name = name


        Dog.count += 1
        print(f'创建了第{Dog.count}条狗{name}')
        

d1 = Dog('旺财')
d1 = Dog('宝哥')
d1 = Dog('拆哥')
d1 = Dog('牧羊犬')
d1 = Dog('金毛')