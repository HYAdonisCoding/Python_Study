#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

# tcp
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
# s.connect(('127.0.0.1', 9999))
# # 接收欢迎消息:
# print(s.recv(1024).decode('utf-8'))
# for data in [b'Michael', b'Tracy', b'Sarah']:
#     # 发送数据:
#     s.send(data)
#     print(s.recv(1024).decode('utf-8'))
# s.send(b'exit')
# s.close()

# 客户端使用UDP时，首先仍然创建基于UDP的Socket，然后，不需要调用connect()，直接通过sendto()给服务器发数据：

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()