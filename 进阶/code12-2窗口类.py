import wx

def onclick(event):
    print("onclick")

class MyFrame(wx.Frame):
    def __init__(self):
        # 创建窗口
        wx.Frame.__init__(self, None, title='Python 学习系统')
      

        # 创建面板
        p1 = wx.Panel(self)
      
        # 创建静态文本
        staticText = wx.StaticText(p1, label='欢迎学习Python')
        

        # 创建按钮
        btn = wx.Button(p1, label='OK', pos=(100,200))
        
        # 给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, onclick, btn)

# 创建应用程序对象
app = wx.App()

# 创建窗口
frm = MyFrame()
# 显示窗口
frm.Show()
# 进入主循环，让窗口一直显示
app.MainLoop()