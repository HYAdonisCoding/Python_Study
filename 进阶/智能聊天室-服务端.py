import wx
from socket import *
import threading
from concurrent.futures import ThreadPoolExecutor
from 千帆模型 import gpt

class Server(wx.Frame):
    def __init__(self):
        # 实例属性
        self.isOn = False # 客户端是否连接服务器
        # self.server_socket = socket()
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Allow reuse of addresses
            

        self.server_socket.bind(('0.0.0.0',8999))
        
        # 监听
        self.server_socket.listen(5)
        # 保存所有的客户端
        self.client_thread_dict = {}
        self.main_thread = None
        self.stop_event = threading.Event()
        # 创建线程池
        self.pool = ThreadPoolExecutor(max_workers=10)
        
        
        wx.Frame.__init__(self, None, title='AI聊天室', size=(430, 660), pos=(0,100))
        # 界面布局
        # 创建面板
        self.pl = wx.Panel(self)
        
        # 创建按钮
        self.start_server_btn = wx.Button(self.pl, label='启动服务器', pos=(10,10), size=(200, 40))
        self.save_text_btn = wx.Button(self.pl, label='保存聊天记录', pos=(220,10), size=(200, 40))
        
        self.stop_server_btn = wx.Button(self.pl, label='停止服务器', pos=(10,530), size=(410, 40))
        
        # 创建聊天内容文本框
        self.text = wx.TextCtrl(self.pl, size=(410,450), pos=(10, 60), style=wx.TE_READONLY|wx.TE_MULTILINE)
        
        # 按钮事件绑定
        self.Bind(wx.EVT_BUTTON, self.save_text, self.save_text_btn)
        self.Bind(wx.EVT_BUTTON, self.start_server, self.start_server_btn)
        self.Bind(wx.EVT_BUTTON, self.stop_server, self.stop_server_btn)
    
    def save_text(self, event):
        print('save_text', event)
        record = self.text.GetValue()
        with open('record.log', 'a+', encoding='utf8') as f:
            f.write(record)
        print('save success')
    def stop_server(self, event):
        print('stop_server', event)
        if self.isOn:
            self.isOn = False
            self.stop_event.set()
            for client in self.client_thread_dict.values():
                if client.isOn:
                    client.client_socket.close()
                    client.isOn = False
            if self.main_thread:
                self.main_thread.join()
            self.stop_event.clear()  # Reset the event for future use
    def start_server(self, event):
        print('start_server', event)
        if self.isOn == False:
            self.isOn = True
            # 创建线程
            self.main_thread = threading.Thread(target=self.main_thread_fun)
            self.main_thread.daemon = True
            self.main_thread.start()
            
        
    def main_thread_fun(self):
        while self.isOn:
            client_socket, client_address = self.server_socket.accept()
            client_name = client_socket.recv(1024).decode('utf-8')
            client_thread = ClientThead(client_socket, client_name, self)
            # 保存客户端
            self.client_thread_dict[client_name] = client_thread
            self.pool.submit(client_thread.run)
            self.send(f'【服务器消息】：欢迎{client_name}({client_address})进入聊天室')
        
    def send(self, text):
        self.text.AppendText(text + '\n')
        print(self.text.GetValue())
        for client in self.client_thread_dict.values():
            if client.isOn:
                result = gpt(text)
                client.client_socket.send(result.encode('utf-8'))
                self.text.AppendText(result + '\n')
        
class ClientThead(threading.Thread):
    def __init__(self, socket, name, server):
        threading.Thread.__init__(self)
        self.client_socket = socket
        self.client_name = name
        self.server = server
        self.isOn = True
    def run(self):
        while self.isOn:
            text = self.client_socket.recv(1024).decode('utf-8')
            if text == '断开连接':
                self.isOn = False
                self.server.send('【服务器消息】：%s离开了聊天室'%self.client_name)
            else:
                self.server.send('【%s】：%s'%(self.client_name, text))
        self.client_socket.close()
        
    
        
        
        

if __name__ == '__main__':
    app = wx.App()
    server = Server()
    server.Show()
    app.MainLoop()
    print("Starting")