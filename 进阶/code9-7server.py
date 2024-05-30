import socket

# 创建socket对象
sk = socket.socket()
# 绑定ip和端口号
sk.bind(('127.0.0.1', 8999))
# 设置监听
sk.listen(5)

# 等待客户端连接
conn, addr = sk.accept()

print(conn, addr)

while True:
    accept_data = conn.recv(1024)
    print(f'收到客户端发的消息{accept_data.decode('utf8')}')
    send_data = '收到了！'
    conn.send(send_data.encode('utf8'))