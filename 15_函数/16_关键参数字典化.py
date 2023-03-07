# 编写一个函数：可以打印个人信息（姓名、年龄、城市等，且这些信息都是可选的）
def show_info(**info):
    if 'name' in info:
        print('姓名 =', info['name'])
    if 'age' in info:
        print('年龄 =', info['age'])
    if 'city' in info:
        print('城市 =', info['city'])
    
    print(info)
    
show_info(name='Eason', age=18, city='北京', weight=120, height=180)


# show_info(name='Eason', city='北京')
# show_info(name='Eason', age=18)
# show_info(age=18, city='北京')
# show_info(name='Eason')
# show_info(city='北京')
# show_info(age=18)
