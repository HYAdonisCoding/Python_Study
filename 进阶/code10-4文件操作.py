import os
# 获取脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
    
def open_file():
    # 打开文件
    filename = script_dir + '/test.txt'
    f = open(filename, mode='r', encoding='utf-8')
    # 读取文件
    context = f.read()
    # context = f.read(5)
    # context = f.readline()
    # context = f.readlines()
    print(context)
    # 关闭文件    # 
    f.close()
    print('打开完成')
    
def append_file():
    write_file('a')
    
def write_file(mode='w', context = ['hello', 'world', 'I\'m a hero', 'Who are you?']):
    # print(f'当前工作目录: {os.getcwd()}')
    
    # print(f'脚本所在的目录: {script_dir}')
    try:
        # 打开文件
        filename = script_dir + '/test.txt'
        f = open(filename, mode=mode, encoding='utf-8')
        try:
            # 读取文件
            f.write('你好，我是Eason\n')
            f.write('你是哪个？\n')
            
            for i in context:
                f.write(i+'\n')
            print('写入完成')
        finally:
            # 关闭文件
            f.close()
    except Exception as e:
        print(f'发生错误: {e}')
    # # 打开文件
    # filename = 'test.txt'
    # f = open(filename, mode='w', encoding='utf-8')
    # # 读取文件
    # f.write('你好，我是Eason\n')
    # f.write('你是哪个？\n')
    # # 关闭文件    # 
    # f.close()
    # print('写入完成')

def with_open():
    with open(script_dir + '/test.txt', mode='r', encoding='utf-8') as f:
        context = f.read()
        print(context)
if __name__ == '__main__':
    # open_file()
    # write_file()
    # append_file()
    with_open()
    pass