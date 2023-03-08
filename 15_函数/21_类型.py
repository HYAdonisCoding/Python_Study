def test(a: int | list, b: str) -> tuple | int:
    print(a, b)
    return 40

d = test(50, 'kkk')
print(d)
# print(d[0])
# print(d[1])

age: int | None = 20
age += 10

age = None

age = '7656'
age += '5443'
age = [11, 22, 33]

print(age)