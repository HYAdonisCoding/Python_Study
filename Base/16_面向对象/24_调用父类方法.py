class Animail:
    def sleep(self):
        print(self, id(self), 'Animail sleep')

        
        
class Dog(Animail):
    pass
    def sleep(self):
        print(self, id(self), 'Dog sleep')
        
class RobotDog(Dog):
    def sleep(self):
        print(self, id(self), 'RobotDog sleep')  
        
    def fly(self):
        print(self, id(self), 'RobotDog fly')  
        
        
        
d = RobotDog()
d.sleep()
d.fly()

print('-' * 30)