brands = set()


while True:
    s = input('请输入汽车品牌：').strip()
    if not s:
        continue
    if s == '0':
        break
    brands.add(s)
    
print('-' * 30)
print(f'一共{len(brands)}中汽车品牌：')
print(brands)