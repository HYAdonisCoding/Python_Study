class Animail:
    def run(self):
        print(self, id(self), 'Animail run')

        
        
class Dog(Animail):
    
    def run(self):
        print(self, id(self), 'Dog run')
        
class Cat(Animail):
    def run(self):
        print(self, id(self), 'Cat run')  
        
        
def test(obj: Animail):
    obj.run()  

a = Animail()
b = Dog()
c = Cat()

test(a)
test(b)
test(c)

# test(10)
# test('12345678')