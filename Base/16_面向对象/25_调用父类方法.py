class Animail:
    def run(self):
        print(self, id(self), 'Animail run')

        
        
class Dog(Animail):
    
    def run(self):
        # 调用父类的run方法
        # super(Dog, self).run()
        super().run()
        print(self, id(self), 'Dog run')
        
class RobotDog(Dog):
    def run(self):
        # 调用父类的run方法
        # super(RobotDog, self).run()
        super().run()
        print(self, id(self), 'RobotDog run')  
        
    def fly(self):
        self.run()
        print(self, id(self), 'RobotDog fly')  
        
        
        
d = RobotDog()
d.fly()

print('-' * 30)