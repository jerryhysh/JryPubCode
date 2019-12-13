import wx
'''
    多选框
'''
class Example(wx.Frame):
    def __init__(self,parent,title):
        super(Example,self).__init__(parent,title = title,size = (300,200))
        self.InitUI()
        
    def InitUI(self):
        pnl = wx.Panel(self)

        # 创建多选框对象
        self.cb1 = wx.CheckBox(pnl,label = 'Value A',pos = (10,10))
        self.cb2 = wx.CheckBox(pnl,label = 'Value B',pos = (10,40))
        self.cb3 = wx.CheckBox(pnl,label = 'Value C',pos = (10,70))
        # 绑定事件
        self.Bind(wx.EVT_CHECKBOX,self.onChecked)

        self.Centre()
        self.Show()

    def onChecked(self,e):
        cb = e.GetEventObject()
        print(cb.GetLabel(),'is clicked',cb.GetValue())


def main():
    ex = wx.App()
    Example(None,'CheckBox Demo')
    ex.MainLoop()

if __name__ == "__main__":
    main()


