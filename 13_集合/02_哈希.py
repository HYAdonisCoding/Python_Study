# None
print(list.__hash__)

# <slot wrapper '__hash__' of 'int' objects>
print(int.__hash__)

# None
print(dict.__hash__)

# <slot wrapper '__hash__' of 'tuple' objects>
print(tuple.__hash__)

# None
print(set.__hash__)

s = { range(10), (10, 20), 10, 3.24, '545', False, {10, 20}}

print(len(s))