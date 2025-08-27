# # 提示用户输入2个整数，最后打印证书的商
# try:
#     a = int(input('请输入第一个整数：'))#ValueError
#     print(1)
    
#     b = int(input('请输入第二个整数：'))#ValueError
#     print(2)
    
#     print(f'{a}除以{b}等于{a/b}') # ZeroDivisionError
#     print(3)
    
#     d = [10, 20]
#     print(s[5])
# except ValueError:
#     print('出现了异常, 输入的数据无法转换成整数')
# except ZeroDivisionError:
#     print('出现了异常， 0不能作为除数')
# except:
#     print('出现了异常，其他')
# else:
#     print('没有出现异常')
# finally:
#     print('执行完毕')
# print(4)


# try:
#     a = int(input('请输入第一个整数：'))#ValueError
#     print(1)
    
#     b = int(input('请输入第二个整数：'))#ValueError
#     print(2)
    
#     print(f'{a}除以{b}等于{a/b}') # ZeroDivisionError
#     print(3)
    
#     d = [10, 20]
#     print(s[5])
# except (ValueError, ZeroDivisionError) as e:
#     print(f'出现了异常, 输入的数据无法转换成整数或0不能作为除数, {e.args[0]}')
# except:
#     print('出现了异常，其他')
# else:
#     print('没有出现异常')
# finally:
#     print('执行完毕')
# print(4)


try:
    a = int(input('请输入第一个整数：'))#ValueError
    print(1)
    
    b = int(input('请输入第二个整数：'))#ValueError
    print(2)
    
    print(f'{a}除以{b}等于{a/b}') # ZeroDivisionError
    print(3)
    
    d = [10, 20]
    print(d[5])
except BaseException as e:
    print(f'出现了异常, {e.args[0]}')
else:
    print('没有出现异常')
finally:
    print('执行完毕')
print(4)