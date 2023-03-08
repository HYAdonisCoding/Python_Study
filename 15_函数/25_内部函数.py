def len(v):
    return 10

def test():
    def len(s):
        return 20
    
    print(len([11, 22, 33]))
    
test()

print(len([11, 22, 33]))