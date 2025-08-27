class Person:
    __count = 10
    
    @classmethod
    def get_count(cls):
        return cls.__count
class Student(Person):
    @classmethod
    def show(cls):
        # 访问父类
        # print(cls._Person__count)
        print(cls.get_count())
        
Student.show()