class Dog:
    __count = 0
    
    def __init__(self, name):
        self.__name = name
        self.__class__.__count +=1
        self.__no = self.__class__.__count
        
    def __str__(self):
        return f'第{self.__no}号狗: {self.__name}'
    
    def run(self):
        print(self, 'run')
        
    def sleep(self):
        print(self, 'sleep')
        
    @classmethod
    def get_count(cls):
        return cls.__count

    @staticmethod
    def get_avg_weight():
        return 10
        
print(Dog.get_avg_weight())

d1 = Dog('旺财')
d1.run()
d1.sleep()

d2 = Dog('宝哥')
d2.run()
d2.sleep()

print(Dog.get_count())
print(Dog.get_avg_weight())