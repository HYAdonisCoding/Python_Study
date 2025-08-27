class Animail:
    def run(self):
        print(self, id(self), 'Animail run')

class Dog(Animail):
    
    def run(self):
        print(self, id(self), 'Dog run')
        
class Cat(Animail):
    def run(self):
        print(self, id(self), 'Cat run')  
        
class Pig(Animail):
    def run(self):
        print(self, id(self), 'Pig run')  
        
def run_animail(obj: Animail, times: int):
    for _ in range(times):
        obj.run()

run_animail(Dog(), 2)
run_animail(Cat(), 3)
run_animail(Pig(), 2)

# def run_dog(obj: Dog, times: int):
#     for _ in range(times):
#         obj.run()
        
# def run_cat(obj: Cat, times: int):
#     for _ in range(times):
#         obj.run()
        
# def run_pig(obj: Pig, times: int):
#     for _ in range(times):
#         obj.run()
        
        
# run_dog(Dog(), 2)
# run_cat(Cat(), 3)
# run_pig(Pig(), 2)