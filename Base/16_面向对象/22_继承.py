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
        
        
        
d = Dog()
d.sleep()
d.run()
d.wag_tail()

print('-' * 30)

c = Cat()
c.sleep()
c.run()
c.catch_mouse()