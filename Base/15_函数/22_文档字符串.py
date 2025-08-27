def hello():
    print('hello')
    print('hello')
    print('hello')
    
# def avg(a: float, b: float) -> float:
#     """
#     计算两个数的平均值
#     :param a: 第一个数值
#     :param b: 第二个数值
#     :return 平均值
#     """
#     return (a + b) / 2

def avg(a: float, b: float) -> float:
    """
    计算两个数的平均值
    param a: 第一个数值
    param b: 第二个数值
    return 平均值
    """
    return (a + b) / 2

hello()
print(avg(13, 21))
print(avg.__doc__)
# help(avg)