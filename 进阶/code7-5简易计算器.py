while 1:
    try:
        op = input('请输入一个四则运算算式（例如：1+2）：')
        if '+' in op:
            a = op.split('+')
            result = float(a[0]) + float(a[1])
            print(f'{op}={result}')
        elif '-' in op:
            a = op.split('-')
            result = float(a[0]) - float(a[1])
            print(f'{op}={result}')
        elif '*' in op:
            a = op.split('*')
            result = float(a[0]) * float(a[1])
            print(f'{op}={result}')
        elif '/' in op:
            a = op.split('/')
            result = float(a[0]) / float(a[1])
            print(f'{op}={result}')
        elif op=='C' or op == 'c':
            print('感谢您使用本计算器！再见！')
            break
        else:
            raise Exception('请按照1+2这个格式输入算式')
    except ZeroDivisionError as e:
        print(f'{op}--{e}-----注意除法运算，除数不能为0！')
    except ValueError as e:
        print(f'{op}-------{e}-----请确保输入的是有效的数字和运算符！')
    except Exception as e:
        print(f'{op}-------{e}')
        