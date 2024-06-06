import wx

class CalculatorFrame(wx.Frame):
    pos_x, pos_y = 10, 70
    btn_w, btn_h = 50, 50
    
    def __init__(self):
        # 创建窗口
        wx.Frame.__init__(self, None, title='计算器', pos=(100, 100), size=(300,500))
        # 创建面板
        self.p1 = wx.Panel(self, pos=(0, 0), size=(300, 400))
        # 创建文本框
        self.entry = wx.TextCtrl(self.p1, pos=(10, 10), size=(280, 50), style=wx.TE_RIGHT)
        # 创建按钮
        w = self.pos_x+self.btn_w
        h = self.pos_x+self.btn_h
        # 第一行
        self.btn_clear = wx.Button(self.p1, label='C', pos=(self.pos_x, self.pos_y), size=(self.btn_w, self.btn_h))
        self.btn_div = wx.Button(self.p1, label='÷', pos=(self.pos_x+w, self.pos_y), size=(self.btn_w, self.btn_h))
        self.btn_mul = wx.Button(self.p1, label='×', pos=(self.pos_x+w*2, self.pos_y), size=(self.btn_w, self.btn_h))
        self.btn_back = wx.Button(self.p1, label='←', pos=(self.pos_x+w*3, self.pos_y), size=(self.btn_w, self.btn_h))
        
        # 第二行
        self.btn_7 = wx.Button(self.p1, label='7', pos=(self.pos_x, self.pos_y+h), size=(self.btn_w, self.btn_h))
        self.btn_8 = wx.Button(self.p1, label='8', pos=(self.pos_x+w, self.pos_y+h), size=(self.btn_w, self.btn_h))
        self.btn_9 = wx.Button(self.p1, label='9', pos=(self.pos_x+w*2, self.pos_y+h), size=(self.btn_w, self.btn_h))
        self.btn_sub = wx.Button(self.p1, label='-', pos=(self.pos_x+w*3, self.pos_y+h), size=(self.btn_w, self.btn_h))
        
        # 第三行
        self.btn_4 = wx.Button(self.p1, label='4', pos=(self.pos_x, self.pos_y+h*2), size=(self.btn_w, self.btn_h))
        self.btn_5 = wx.Button(self.p1, label='5', pos=(self.pos_x+w, self.pos_y+h*2), size=(self.btn_w, self.btn_h))
        self.btn_6 = wx.Button(self.p1, label='6', pos=(self.pos_x+w*2, self.pos_y+h*2), size=(self.btn_w, self.btn_h))
        self.btn_add = wx.Button(self.p1, label='+', pos=(self.pos_x+w*3, self.pos_y+h*2), size=(self.btn_w, self.btn_h))
        # 第四行
        self.btn_1 = wx.Button(self.p1, label='1', pos=(self.pos_x, self.pos_y+h*3), size=(self.btn_w, self.btn_h))
        self.btn_2 = wx.Button(self.p1, label='2', pos=(self.pos_x+w, self.pos_y+h*3), size=(self.btn_w, self.btn_h))
        self.btn_3 = wx.Button(self.p1, label='3', pos=(self.pos_x+w*2, self.pos_y+h*3), size=(self.btn_w, self.btn_h))
        self.btn_eq = wx.Button(self.p1, label='=', pos=(self.pos_x+w*3, self.pos_y+h*3), size=(self.btn_w, self.btn_h*2+10))
        
        # 第五行
        self.btn_0 = wx.Button(self.p1, label='0', pos=(self.pos_x, self.pos_y+h*4), size=(self.btn_w*2, self.btn_h))
        self.btn_point = wx.Button(self.p1, label='.', pos=(self.pos_x+w*2, self.pos_y+h*4), size=(self.btn_w, self.btn_h))
        
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_9)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_8)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_7)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_6)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_5)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_4)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_3)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_2)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_1)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_0)
        self.Bind(wx.EVT_BUTTON, self.On_btn_number, self.btn_point)
        
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_add)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_sub)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_mul)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_div)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_clear)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_back)
        self.Bind(wx.EVT_BUTTON, self.On_btn_Operation, self.btn_eq)
        
    def On_btn_Operation(self, event):
        # 获取触发事件的按钮对象  
        btn = event.GetEventObject()  
        # 获取按钮上的文本（标签）  
        text = btn.GetLabel()  
        print(text) 
        if text == 'C':
            print('清屏')
            self.entry.Clear()
        elif text == '+':
            print('加法')
            self.entry.AppendText("+")
        elif text == '-':
            print('减法')
            self.entry.AppendText("-")
        elif text == '×':
            print('乘法')
            self.entry.AppendText("*")
        elif text == '÷':
            print('除法')
            self.entry.AppendText("/")
        elif text == '←':
            print('删除一个')
            text = self.entry.GetValue()
            self.entry.SetValue(text[:-1])
        elif text == '=':
            print('等于')
            text = self.entry.GetValue()
            try:
                
                result = str(eval(text))
                self.entry.SetValue(result)
            except Exception as e:
                print('Exception', e)
                self.entry.SetValue('Error')
        else:
            print('Error: Invalid')
        
    def On_btn_number(self, event):
        # 获取触发事件的按钮对象  
        btn = event.GetEventObject()  
        # 获取按钮上的文本（标签）  
        text = btn.GetLabel()  
        print(text)  # 这将打印出 "1"  
        self.entry.AppendText(text)
        
        
if __name__ == '__main__':
    app = wx.App()
    frm = CalculatorFrame()
    frm.Show()
    app.MainLoop()
        
        
        
        
        
        