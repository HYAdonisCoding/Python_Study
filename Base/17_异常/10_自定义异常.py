class AgeError(Exception):
    """ 自定义的异常类型，表示age有问题 """
    def __str(self):
        if len(self.args) == 1:
            return f'{self.args[0]}'
        return f'{self.args}'
    
class Person:
    def __init__(self):
        self.__age = 1
        
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, age):
        if age < 1:
            raise AgeError("Age must be greater than 1", )
        if age > 120:
            raise AgeError("Age must not be greater than 120", age)
        self.__age = age
        
        
try:
    p = Person()
    p.age = 200
except AgeError as e:
    print('出现了异常', e.args[0])
    print('出现了异常', e.args[1])
    print('出现了异常', e)