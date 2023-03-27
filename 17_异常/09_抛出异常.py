class Person:
    def __init__(self):
        self.__age = 1
        
    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, age):
        if age < 1:
            raise ValueError("Age must be greater than 1")
        if age > 120:
            raise ValueError("Age must not be greater than 120")
        self.__age = age
        
p = Person()

try:
    p.age = -10
except ValueError as e:
    print('出现了异常', e.args[0])

print(p.__dict__)
print(p.age)


p2 = Person()
p2.age = -10
print(p2.age)