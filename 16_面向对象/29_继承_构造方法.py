class Person:
    def __init__(self):
        print('Person.__init__')
        # 初始化属性
        self.name = 'Eason'
        self.age = 20
    
class Student(Person):
    def __init__(self):
        super().__init__()
        print('Student.__init__')
        self.no = 9
        
s = Student()
print(s.__dict__)