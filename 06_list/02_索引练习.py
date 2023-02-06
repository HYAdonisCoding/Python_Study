day = int(input('请输入整数：'))

# 0用来占位
days = [0, '一', '二', '三', '四', '五', '六', '日']

if 1 <= day <= 7:
    print(f'星期{days[day]}')
else:
    print('非法输入')
    

# days = ['一', '二', '三', '四', '五', '六', '日']

# if 1 <= day <= 7:
#     print(f'星期{days[day-1]}')
# else:
#     print('非法输入')