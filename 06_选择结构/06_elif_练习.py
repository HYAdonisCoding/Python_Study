a = 1111
b = 22
c = 333

if a > b:
    if b > c:#a > b > c
        print(f'中间值是{b}')
    elif a > c:#a > b且 c >= b 且 a > c => a > c >= b
        print(f'中间值是{c}')
    else:
        print(f'中间值是{a}')
else: # b >= a
    if c > b: # c > b >= a
        print(f'中间值是{b}')
    elif a > c: # b >= a, b >= c 且  a > c => b >= a > c 
        print(f'中间值是{a}')
    else:
        print(f'中间值是{c}')