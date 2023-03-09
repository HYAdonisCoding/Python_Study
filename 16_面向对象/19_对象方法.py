class Dog:
    __count = 0
    def __init__(self, name):
        self.__name = name


        Dog.__count += 1
        self.__no = Dog.__count
    
    def __str__(self):
        return f'第{self.__no}号狗: {self.__name}'
    
    def test1(self, text):
        print('对象方法', id(self), text, self)
       
    @classmethod 
    def test2(cls, text):
        print('类方法', id(cls), text)
        

d1 = Dog('旺财')
d2 = Dog('宝哥')

# 对象方法
print(d1)
d1.test1('d1')
Dog.test1(d1, 'Dog')
d1.__class__.test1(d1, 'd1.__class__')
d2.__class__.test1(d1, 'd2.__class__')

print('-' * 30)

print(d2)
d2.test1('d2')
Dog.test1(d2, 'Dog')
d1.__class__.test1(d2, 'd1.__class__')
d2.__class__.test1(d2, 'd2.__class__')

print('-' * 30)

# 类方法
Dog.test2('Dog')
d1.__class__.test2('d1.__class__')
d2.__class__.test2('d2.__class__')
d1.test2('d1')
d2.test2('d2')


print('-' * 30)