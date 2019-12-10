import logging
import wx
from JrySemDatAnlyz import TboxAndPlatProtolAnlyz

# wxFormbuilder图形开发界面工具
# https://www.yiibai.com/wxpython/wxpython_hello_world.html




'''
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    TboxAndPlatProtolAnlyz(int(3))
    input("wait close")
'''

# 创建窗口类
class myWindowClass(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'SEM东南TBOX与TSP数据解析工具',size=(800,600))

        # 创建面板
        # Panel是窗口的容器，通常其大小与Frame一样，在其上放置各种控件，这样可将窗口内容与工具栏及状态栏区分开
        MainPanel = wx.Panel(self)
        
        # 创建多行输入文本框
        self.InputStaticTxtHandle = wx.StaticText(MainPanel,-1,"输入解析数据:")
        self.InputTextCtrlHandle = wx.TextCtrl(MainPanel,size = (300,100),style = wx.TE_MULTILINE)

        # 创建解析控制组件
        self.AnalyzeBttnHandle = wx.Button(MainPanel,-1,"解析")
        self.AnalyzeBttnHandle.Bind(wx.EVT_BUTTON,self.AnalyzeClicked)

        # 创建解析解析数据显示
        self.OutputStaticTxtHandle = wx.StaticText(MainPanel,-1,"数据解析结果:")
        self.OutputTextCtrlHandle = wx.TextCtrl(MainPanel,-1,size = (400,200),style = wx.TE_MULTILINE|wx.TE_READONLY)
        
        # ======界面布局======
        # 创建输入文本框容器
        InputDatBoxSizer = wx.BoxSizer(wx.VERTICAL)
        InputDatBoxSizer.Add(self.InputStaticTxtHandle)
        InputDatBoxSizer.Add(self.InputTextCtrlHandle)

        # 创建控件容器
        CtrlBoxSizer = wx.BoxSizer(wx.VERTICAL)
        CtrlBoxSizer.Add(self.AnalyzeBttnHandle)

        # 创建解析结果显示容器
        OutputDatBoxSizer = wx.BoxSizer(wx.VERTICAL)
        OutputDatBoxSizer.Add(self.OutputStaticTxtHandle)
        OutputDatBoxSizer.Add(self.OutputTextCtrlHandle)

        # 创建数据及控制水平容器
        DatAndCtrlBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        DatAndCtrlBoxSizer.Add(InputDatBoxSizer,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL,20)
        DatAndCtrlBoxSizer.Add(CtrlBoxSizer,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL,20)

        # 创建垂直容器
        MainBoxSizer = wx.BoxSizer(wx.VERTICAL)
        MainBoxSizer.Add(DatAndCtrlBoxSizer,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL,20)
        MainBoxSizer.Add(OutputDatBoxSizer,0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL,20)

        MainPanel.SetSizer(MainBoxSizer)

        self.Centre()
        self.Show()

    def AnalyzeClicked(self,event):
        self.OriginStr = self.InputTextCtrlHandle.GetValue()
        # print(type(self.OriginStr))
        self.OutputStr = TboxAndPlatProtolAnlyz(3,self.OriginStr)
        self.OutputTextCtrlHandle.SetValue(self.OutputStr)
    
        

def main():
    # 先创建一个App
    App = wx.App()
    # 创建顶层窗口类的对象
    myWinFrame = myWindowClass()
    # 激活窗口显示
    myWinFrame.Show()
    # 应用程序对象的主事件循环
    App.MainLoop()

if __name__ == "__main__":
    main()    
