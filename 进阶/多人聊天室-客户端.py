import wx
from socket import *
import threading
from faker import Faker

class Client(wx.Frame):
    def __init__(self):
        # 实例属性
        self.name = Faker('zh_CN').name() # 用户的名字
        self.isConnected = False # 客户端是否连接服务器
        self.client_socket = None #
        
        wx.Frame.__init__(self, None, title=self.name+'聊天室', size=(430, 660), pos=(100,100))
        # 界面布局
        # 创建面板
        self.pl = wx.Panel(self)
        
        # 创建按钮
        self.conn_btn = wx.Button(self.pl, label='加入聊天室', pos=(10,10), size=(200, 40))
        self.dis_conn_btn = wx.Button(self.pl, label='离开聊天室', pos=(220,10), size=(200, 40))
        
        self.clear_btn = wx.Button(self.pl, label='清空', pos=(10,580), size=(200, 40))
        self.send_btn = wx.Button(self.pl, label='发送', pos=(220,580), size=(200, 40))
        
        # 创建聊天内容文本框
        self.text = wx.TextCtrl(self.pl, size=(410,400), pos=(10, 60), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.input_text = wx.TextCtrl(self.pl, size=(410, 100), pos=(10, 470), style=wx.TE_MULTILINE)
        
        # 按钮事件绑定
        self.Bind(wx.EVT_BUTTON, self.clear, self.clear_btn)
        self.Bind(wx.EVT_BUTTON, self.conn, self.conn_btn)
        self.Bind(wx.EVT_BUTTON, self.dis_conn, self.dis_conn_btn)
        self.Bind(wx.EVT_BUTTON, self.send, self.send_btn)
    
    def clear(self, event):
        print('clear', event)
        self.input_text.clear()
    
    def conn(self, event):
        print('conn', event)
        if self.isConnected == False:
            self.isConnected = True
            self.client_socket = socket()
            self.client_socket.connect(('127.0.0.1', 8999))
            # 发送用户名
            self.client_socket.send(self.name.encode('utf8'))
            
            main_thread = threading.Thread(target=self.receive_data)
            main_thread.setDaemon(True)
            main_thread.start()
            
        
    def dis_conn(self, event):
        print('dis_conn', event)
        self.client_socket.send('断开连接'.encode('utf-8'))
        self.isConnected = False
        
    def send(self, event):
        print('send', event)
        if self.isConnected:
            text = self.input_text.GetValue()
            if text != '':
                self.client_socket.send(text.encode('utf-8'))
                self.input_text.Clear()
        
    def receive_data(self):
        print('receive_data', self)
        while self.isConnected:
            text = self.client_socket.recv(1024).decode('utf8')
            print('receive_data', text)
            self.text.AppendText(text+'\n')
            print(self.text.GetValue())
        
    
        
        
        

if __name__ == '__main__':
    app = wx.App()
    frm = Client()
    frm.Show()
    app.MainLoop()
    print("Starting")