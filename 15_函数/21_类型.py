def test(a: int | list, b: str) -> tuple | int:
    print(a, b)
    return 40

d = test(50, 'kkk')
print(d)
# print(d[0])
# print(d[1])