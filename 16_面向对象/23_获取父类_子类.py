class Animail:
    def sleep(self):
        print(self, 'sleep')
    
    def run(self):
        print(self, 'run')    
        
        
class Dog(Animail):
    def wag_tail(self):
        print(self, 'wag_tail')  
        
class Cat(Animail):
    def catch_mouse(self):
        print(self, 'catch_mouse')   
        
        
        
print(Dog.__base__)
print(Cat.__base__)


d = Dog()
# d.sleep()
# d.run()
# d.wag_tail()

print(d.__class__.__base__)

print(Dog.__bases__)

print(Animail.__subclasses__)

print('-' * 30)