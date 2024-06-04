import wx
import random



class MyFrame(wx.Frame):
    # 抽奖列表
    NameList = ['Jack', 'Eason', 'Tom']
    
    def __init__(self):
        # 创建窗口
        wx.Frame.__init__(self, None, title='抽奖器')
      

        # 创建面板
        self.p1 = wx.Panel(self)
        # 设置背景色
        # self.SetBackgroundColour(wx.YELLOW)
        self.SetBackgroundColour((200, 100, 200))
        # 创建静态文本
        self.staticText = wx.StaticText(self.p1, label=random.choice(self.NameList))
        # 创建字体
        font = wx.Font(48, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.staticText.SetFont(font)        

        # 创建按钮
        self.btn1 = wx.Button(self.p1, label='开始抽奖', pos=(100,200))
        self.btn2 = wx.Button(self.p1, label='结束抽奖', pos=(200,200))
        self.btn1.SetBackgroundColour((255,0,255))
        self.btn1.SetForegroundColour((255,0,255))
        # 给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.onclick, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.stop, self.btn2)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # 初始化 timer 属性  
        self.timer = None
        
    def on_close(self, event):  
        print ("on_close", event)
        # 处理窗口关闭事件的逻辑  
        if self.timer is not None:
            self.timer.Stop()
            self.timer.Destroy()
        self.Destroy()  
        
 


    def onclick(self, event):
        print("onclick")
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_name, self.timer)
        # 每隔100秒更新名字
        self.timer.Start(100) 
        
    
    def update_name(self, event):
        self.staticText.SetLabelText(random.choice(self.NameList))
        
    
    # 停止记时
    def stop(self, event):
        self.timer.Stop()
        print(self.staticText.GetLabelText())

if __name__ == '__main__':
    

    # 创建应用程序对象
    app = wx.App()

    # 创建窗口
    frm = MyFrame()
    # 显示窗口
    frm.Show()
    # 进入主循环，让窗口一直显示
    app.MainLoop()