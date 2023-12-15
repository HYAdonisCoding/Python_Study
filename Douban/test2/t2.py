# -*- coding: utf-8 -*-

# from .. import Test
# from ..test1 import t1
# from ...Test import Calumny
import sys


import os

def addPath():
    # # 获取当前脚本所在目录的上级目录，加入到 sys.path 中
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
    sys.path.insert(0, parent_dir)

if __name__ == '__main__':
    # print(t1.add(2, 10))
    print('t2 main')
    print(1,sys.path)
    # addPath()
    print(2, sys.path)
    # print(current_dir)
    # print(parent_dir)