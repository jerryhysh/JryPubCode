import wx


class JryWin(wx.Frame):
    def __init__(self,parent,title):
        super(JryWin,self).__init__(parent,title = title,size = (600,200))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.HORIZONTAL)

        self.IpPortAddrBox = wx.BoxSizer(wx.HORIZONTAL)

        self.IpAddrLabel = wx.StaticText(panel,label = "IpAddress:",style = wx.ALIGN_CENTRE)
        self.IpPortAddrBox.Add(self.IpAddrLabel,0,wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,20)

        # 创建TextCtrl对象
        self.IpPortTextCtrl = wx.TextCtrl(panel,size=(200,100),style = wx.TE_MULTILINE)
        self.IpPortAddrBox.Add(self.IpPortTextCtrl,0,wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,20)

        self.IpPortConnButton = wx.Button()

        box.Add(self.IpPortAddrBox,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,20)
        
        panel.SetSizer(box)

        self.Centre()
        self.Show()


def main():
    app = wx.App()
    JryWin(None,"StaticTezt demo")
    app.MainLoop()

if __name__ == "__main__":
    main()
    




