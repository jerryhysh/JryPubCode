import wx
'''
    标签
'''

class Mywin(wx.Frame):
    def __init__(self,parent,title):
        super(Mywin,self).__init__(parent,title = title,size = (600,200))
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # ====================================================
        # 创建staticText对象lbl
        lbl = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER)
        txt1 = "Python GUI development"
        txt2 = "using wxPython"
        txt3 = "Python port of wxWidget"
        txt = txt1+"\n"+txt2+"\n"+txt3

        font = wx.Font(18,wx.ROMAN,wx.ITALIC,wx.NORMAL)
        # 设置字体
        lbl.SetFont(font)
        # 设置内容
        lbl.SetLabel(txt)

        box.Add(lbl,0,wx.ALIGN_CENTER)
        # ====================================================
        
        '''
        # ====================================================
        # 创建staticText对象lblwrap
        lblwrap = wx.StaticText(panel,-1,style=wx.ALIGN_RIGHT)
        txt = txt1+txt2+txt3
        # 设置标签内容
        lblwrap.SetLabel(txt)
        # 设置宽
        lblwrap.Wrap(200)

        box.Add(lblwrap,0,wx.ALIGN_LEFT)
        # ====================================================
        '''
        '''
        # ====================================================
        # 创建StaticText对象lb11
        lbl1 = wx.StaticText(panel,-1,style = wx.ALIGN_LEFT|wx.ST_ELLIPSIZE_MIDDLE)
        # 设置标签内容
        lbl1.SetLabel(txt)
        # 设置前景色为红色
        lbl1.SetForegroundColour((255,0,0))
        # 设置背景色为黑色
        lbl1.SetBackgroundColour((0,0,0))

        font = self.GetFont()
        # font.SetFont(20)
        lbl1.SetFont(font)

        box.Add(lbl1,0,wx.ALIGN_LEFT)
        # ====================================================
        '''

        panel.SetSizer(box)
        self.Centre()
        self.Show()

def main():
    app = wx.App()
    Mywin(None,"StaticTezt demo")
    app.MainLoop()

if __name__ == "__main__":
    main()


