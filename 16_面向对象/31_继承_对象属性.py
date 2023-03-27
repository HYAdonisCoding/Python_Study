class Person:
    def __init__(self, name, age):
        print('Person.__init__')
        # 初始化属性
        self.__name = name
        self.__age = age
        
    @property
    def name(self):
        return self.__name
    @property
    def age(self):
        return self.__age
    
    def __str__(self):
        return f'{self.name}_{self.age}'
    
class Student(Person):
    def __init__(self, name, age, no):
        super().__init__(name, age)
        print('Student.__init__')
        self.__no = no
      
    def __str__(self):
        return f'no: {self.__no}_name: {self.name}_age: {self.age}'  
s = Student('Eason', 19, 1)
print(s.__dict__)
print(s)