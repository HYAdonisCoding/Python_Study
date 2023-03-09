# 需求：根据创建顺序给每一条狗设置一个编号

class Dog:
    __count = 0
    def __init__(self, name):
        self.__name = name


        Dog.__count += 1
        self.__no = Dog.__count
    
    def __str__(self):
        return f'第{self.__no}号狗: {self.__name}'
        

d1 = Dog('旺财')
print(d1)
d1 = Dog('宝哥')
print(d1)
d1 = Dog('拆哥')
print(d1)

Dog.count = 10
for _ in range(3):
    Dog('qw')
d1 = Dog('牧羊犬')
print(d1)
d1 = Dog('金毛')
print(d1)