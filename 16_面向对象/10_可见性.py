class Student:
    def __init__(self, name, age):
        self.__age = None
        self.__name = None
        self.set_name(name)
        self.set_age(age)
        
    def __str__(self):
        return f'{self.__age}岁{self.__name}'
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name
    
    def get_age(self):
        return self.__age
    
    def set_age(self, age):
        self.__age = age if age > 0 else 1
        
    

s = Student('Eason', 18)

print(s)
print(s.get_name())
print(s.get_age())

# 目的：允许外界修改对象内部的属性，但是不允许它乱改
# 1.隐藏属性：让属性对外不可见
# 2.提供操作属性的方法：访问（读取）、修改