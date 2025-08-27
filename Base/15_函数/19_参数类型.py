def hello(name: str, times: int):
    for _ in range(times):
        print(f'Hi, {name}!')
        
hello("Eason", 2)

# hello(2, "Eason")

def test(a: list):
    a.append(a.count)
    
s = [1, 2, 3]
test(s)
print(s)