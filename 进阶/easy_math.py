
auther = 'Jackson'

def add(a, b):
    return a + b

def total(*args):
    '''
    参数 接收一个列表
    return: 列表中每个元素的平方和
    '''
    result = 0
    for i in args:
        result += i**2
    return result