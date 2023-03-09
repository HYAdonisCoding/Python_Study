class Student:
    def __init__(self, name, age):
        self.__age = None
        self.__name = None
        self.name = (name)
        self.age = (age)
        
    def __str__(self):
        return f'{self.__age}岁{self.__name}'
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
    
    @name.deleter
    def name(self):
        del self.__name
        
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, age):
        self.__age = age if age > 0 else 1
        
    @age.deleter
    def age(self):
        del self.__age
    

s = Student('Eason', 18)
print(s.name)
print(s.age)
print(s.__dict__)

s.name = '燕云'
s.age = 16

print(s.name)
print(s.age)
print(s.__dict__)

del s.name
print(s.__dict__)

del s.age
print(s.__dict__)
# print(s)

