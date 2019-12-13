import wx

class Mywin(wx.Frame):
    def __init__(self,parent,title):
        super(Mywin,self).__init__(parent,title = title,size = (300,200))

        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # 创建StaticText对象
        self.label = wx.StaticText(panel,label = "Your choice:",style = wx.ALIGN_CENTRE)
        # 将对象添加至box
        box.Add(self.label,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,20)

        languages = ['C', 'C++', 'Python', 'Java', 'Perl'] 

        # ======================================================
        # 创建StaticText对象
        cblbl = wx.StaticText(panel,label = "Combo box",style = wx.ALIGN_CENTRE)
        # 将对象添加至box
        box.Add(cblbl,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)

        self.combo = wx.ComboBox(panel,choices = languages)
        self.combo.Bind(wx.EVT_COMBOBOX, self.OnCombo) 
        box.Add(self.combo,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        # ======================================================

        # ======================================================
        # 创建StaticText对象
        chlbl = wx.StaticText(panel,label = "Choice control",style = wx.ALIGN_CENTRE)
        # 将对象添加至box
        box.Add(chlbl,0,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        # 创建Choice对象
        self.choice = wx.Choice(panel,choices = languages)
        
        self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)
        box.Add(self.choice,1,wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL,5)
        # ======================================================

        box.AddStretchSpacer() 

        panel.SetSizer(box)
        self.Centre()
        self.Show()

    def OnCombo(self, event): 
        self.label.SetLabel("You selected"+self.combo.GetValue()+" from Combobox") 

    def OnChoice(self,event): 
        self.label.SetLabel("You selected "+ self.choice.GetString(self.choice.GetSelection())+" from Choice") 

def main():
    app = wx.App()
    Mywin(None,'ComboBox & Choice demo')
    app.MainLoop()

if __name__ == "__main__":
    main()