class Student:
    count = 10
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def study(self):
        print(self.name)
        # 访问类变量
        print(Student.count)
        print(self.count)
        print(self.__class__.count)
        print(Student == self.__class__)
        
    @classmethod
    def my_func(self):
         pass

s = Student('Eason', 18)
s.study()


class Dog:
    pass

def run(dog: Dog):
    """
    让一只狗跑步
    :param name: 名字
    :param breed: 品种
    :param age: 年龄
   """
    print(f'一只名字叫{dog.name}的{dog.age}岁{dog.breed}跑起来了')
  
d1 = Dog()
d1.name = '宝哥' 
d1.breed = '柴犬'
d1.age = 5
run(d1)

d2 = Dog()
d2.name = '旺财' 
d2.breed = '中华田园犬'
d2.age = 3
run(d2)

d3 = Dog()
d3.name = '拆哥' 
d3.breed = '哈士奇'
d3.age = 3
run(d3)

