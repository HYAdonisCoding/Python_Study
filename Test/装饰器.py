from ctypes import cdll, c_char, c_char_p, c_int, c_void_p, \
    pythonapi, py_object, PYFUNCTYPE, CFUNCTYPE
import os
#
# Global
#
_pytransform = None
HT_HARDDISK, HT_IFMAC, HT_IPV4, HT_IPV6, HT_DOMAIN = range(5)
# 定义了一个装饰器
def dllmethod(func):
    print('dllmethod called')
    def wrap(*args, **kwargs):
        print('wrap called')
        return func(*args, **kwargs)
    return wrap


@dllmethod
def test_method():
    print('test_method called')
    prototype = PYFUNCTYPE(c_int, c_int, c_int, c_int, c_int)
    _init_runtime = prototype(('init_runtime', _pytransform))
    return _init_runtime(0, 0, 0, 0)

@dllmethod
def test_method1():
    print('test_method1 called')
    

print(HT_HARDDISK, HT_IFMAC, HT_IPV4, HT_IPV6, HT_DOMAIN)
print(c_int, c_int, c_int, c_int, c_int)