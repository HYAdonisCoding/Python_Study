import wx

def onclick(event):
    print("onclick")
    
# 创建应用程序对象
app = wx.App()

# 创建窗口
frm = wx.Frame(None, title='Python 学习系统',size=(800, 600), pos=(200,200))
# 显示窗口
frm.Show()

# 创建面板
p1 = wx.Panel(frm, size=(800, 600), pos=(200, 200))
# 显示面板
p1.Show()
# 创建静态文本
staticText = wx.StaticText(p1, label='欢迎学习Python',pos=(100, 100))
# 显示静态文本
staticText.Show()

# 创建按钮
btn = wx.Button(p1, label='OK')
# 显示按钮
btn.Show()
# 给按钮绑定事件
frm.Bind(wx.EVT_BUTTON, onclick, btn)

# 进入主循环，让窗口一直显示
app.MainLoop()