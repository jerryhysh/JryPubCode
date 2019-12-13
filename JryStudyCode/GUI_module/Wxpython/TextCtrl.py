import wx

'''
    文本框
'''

class Mywin(wx.Frame):
    def __init__(self,parent,title):
        super(Mywin,self).__init__(parent,title = title,size = (350,250))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # '''
        # ====================================================
        # 创建hbox1盒子
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        # 创建StaticText对象
        l1 = wx.StaticText(panel,-1,"文本域")
        # 将StaticText对象加入盒子hbox1
        hbox1.Add(l1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        # 创建TextCtrl对象
        self.t1 = wx.TextCtrl(panel)
        # TextCtrl对象绑定事件OnKeyTyped
        self.t1.Bind(wx.EVT_TEXT,self.OnKeyTyped)
        # 将TextCtrl对象加入盒子hbox1
        hbox1.Add(self.t1,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        # hbox1盒子加入vbox盒子
        vbox.Add(hbox1)
        # ====================================================
        # '''

        # '''
        # ====================================================
        # 创建hbox2盒子
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        # 创建StaticText对象
        l2 = wx.StaticText(panel, -1, "密码文本")
        # 将StaticText对象加入盒子hbox2
        hbox2.Add(l2,1,wx.ALIGN_LEFT|wx.ALL,5)

        # 创建TextCtrl对象
        self.t2 = wx.TextCtrl(panel,style= wx.TE_PASSWORD)
        # 设置最大长度
        self.t2.SetMaxLength(5)
        # TextCtrl对象绑定事件OnMaxLen
        self.t2.Bind(wx.EVT_TEXT_MAXLEN,self.OnMaxLen)
        # 将TextCtrl对象加入盒子hbox2
        hbox2.Add(self.t2,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)
        
        # hbox2盒子加入vbox盒子
        vbox.Add(hbox2)
        # ====================================================
        # '''
        # '''
        # ====================================================
        # 创建hbox3盒子
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # 创建StaticText对象
        l3 = wx.StaticText(panel,-1,"多行显示")
        # 将StaticText对象加入盒子hbox3
        hbox3.Add(l3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        # 创建TextCtrl对象
        self.t3 = wx.TextCtrl(panel,size=(200,100),style = wx.TE_MULTILINE)
        # TextCtrl对象绑定事件OnEnterPressed
        self.t3.Bind(wx.EVT_TEXT_ENTER,self.OnEnterPressed)  
        # 将TextCtrl对象加入盒子hbox3
        hbox3.Add(self.t3,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        # hbox3盒子加入vbox盒子
        vbox.Add(hbox3)
        # ====================================================
        # '''

        # ====================================================
        # 创建hbox4盒子
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        # 创建StaticText对象
        l4 = wx.StaticText(panel, -1, "只读取文本")
        # 将StaticText对象加入盒子hbox4
        hbox4.Add(l4, 1, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        # 创建TextCtrl对象
        self.t4 = wx.TextCtrl(panel, value = "只读文本",style = wx.TE_READONLY|wx.TE_CENTER)
        # 将TextCtrl对象加入盒子hbox4
        hbox4.Add(self.t4,1,wx.EXPAND|wx.ALIGN_LEFT|wx.ALL,5)

        # hbox4盒子加入vbox盒子
        vbox.Add(hbox4)
        # ====================================================



        panel.SetSizer(vbox)
        self.Centre()
        self.Show()
        self.Fit()

    def OnKeyTyped(self, event): 
        print(event.GetString())

    def OnMaxLen(self,event): 
        print("Maximum length reached")

    def OnEnterPressed(self,event): 
        print ("Enter pressed")


def main():
    app = wx.App() 
    Mywin(None,  'TextCtrl实例')
    app.MainLoop()

if __name__ == "__main__":
    main()