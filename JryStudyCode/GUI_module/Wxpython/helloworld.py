# 导入wx模块
import wx
# https://stackoverflow.com/questions/28437071/pylint-1-4-reports-e1101no-member-on-all-c-extensions
def main():
    # 定义应用程序类的一个对象
    app = wx.App()
    # 创建一个顶层窗口。
    window = wx.Frame(None, title = "wxPython",size = (400,300))
    # 
    panel = wx.Panel(window)
    # 添加一个静态文本对象
    label = wx.StaticText(panel, label = "Hello world",pos = (100,100))
    # 通过show()方法激活框架窗口。
    window.Show(True)
    # 输入应用程序对象的主事件循环
    app.MainLoop()

if __name__ == "__main__":
    main()



