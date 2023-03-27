class Person:
    def __init__(self, name, age):
        print('Person.__init__')
        # 初始化属性
        self.name = name
        self.age = age
        
    def __str__(self):
        return f'{self.name}_{self.age}'
    
class Student(Person):
    def __init__(self, name, age, no):
        super().__init__(name, age)
        print('Student.__init__')
        self.no = no
      
    def __str__(self):
        return f'{self.no}_{super().__str__()}'  
s = Student('Eason', 19, 1)
print(s.__dict__)
print(s)