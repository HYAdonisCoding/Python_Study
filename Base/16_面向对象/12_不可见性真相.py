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
s.__name = 'Tom'
s.__age = 20
print(s)
print(s.__dict__)
print(s.get_age())
print(s._Student__age)