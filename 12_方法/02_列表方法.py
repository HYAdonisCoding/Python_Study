brands = []

while True:
    s = input('请输入汽车品牌：')
    if s == '0':
        break
    if s in brands:
        continue
    brands.append(s)
    
print('-' * 30)
print(f'一共{len(brands)}中汽车品牌：')
print(brands)