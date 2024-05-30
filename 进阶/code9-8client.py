import socket

# 创建socket对象
sk = socket.socket()
# 连接服务器
sk.connect(('0.0.0.0', 8999))


while True:
    send_data = input('请输入您要发送的内容：')
    # 发送数据到服务器
    sk.send(send_data.encode('utf8'))
    # 等待服务器的响应
    accept_data = sk.recv(1024)
    str = accept_data.decode('utf8')
    print(f'收到服务器的响应： {str}')