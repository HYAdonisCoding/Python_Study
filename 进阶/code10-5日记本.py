import os
from easy_package    import easy_tools

# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 打开文件
filename = script_dir + '/Notes.txt'
# 使用非打印字符作为分隔符
separator = '\x1E'

def read_note(day=-1):
    
    f = open(filename, mode='r', encoding='utf-8')
    # 读取文件
    try:
        context = f.read()
        if day != '-1':
            lista = context.split(separator)
            for i in lista:
                if i[:(len(day))] == day:
                    print(f'日记：\n{i}')
                    return True
            else:
                return False
        else:
            context = context.replace(separator, '')
            print(context)
            return True
    except Exception as e:
        print(f'发生错误: {e}')
        return False
    finally:
        f.close()
    
    
def write_Note():
    date = input('请输入今天的日期(当前日期请输入-1)：')
    text = input('请输入日记内容：' )
    try:
        # 打开文件
        f = open(filename, mode='a', encoding='utf-8')
        try:
            if date == '-1':
                date = easy_tools.get_time()
            # 写入文件
            f.write(separator)
            f.write(date+'\n')
            f.write(text+'\n')
        finally:
            # 关闭文件
            f.close()
            return True
    except Exception as e:
        print(f'发生错误: {e}')
        return False

def menu():
    print('*'*30)
    print('''欢迎使用Python日记本系统
    1: 记日记
    2: 阅读日记
    3: 退出系统''')
    print('*'*30)
def quit():
    print('*'*30)
    print('欢迎下次使用Python日记本系统，再见！')
    print('*'*30)
if __name__ == '__main__':
    menu()
    while True:
        op = input('请输入您的选择：')
        if op == '1':
            if write_Note():
                print('日记保存成功！')
        elif op == '2':
            day = input('请输入您查询的日期（全部请输入-1）：')
            if read_note(day):
                print('日记已加载完成！')
            else:
                print('未查询到日记信息，请重试！')
        elif op == '3':
            quit()
            break
        else:
            print('请重试')

                   