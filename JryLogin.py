# https://www.cnblogs.com/franknihao/p/6591689.html
# https://blog.51cto.com/laomomo/1957342

import sys, paramiko, ConfigParser, os
from MyExceptions import *
from MainFrame import MainFrame
# 上面这些都是辅助的模块，不是这篇的重点可以忽略 #
from wx import *
from threading import Thread

LOGIN_EVENT_ID = NewId()  # 所有事件都有一个固有的ID，自定义事件也不例外。这句为我自定义的事件分配一个ID（wx内部用的一个ID）。

class LoginEvent(PyEvent):
    """自定义一个事件类，用PyEvent做基类，在其构造方法中通过SetEventType来为这类事件分配一个ID。
    message参数是为了每次构建事件时都可以通过这个message指出这个事件的一些信息，方便事件处理函数来做出相应的操作
    """
    def __init__(self, message):
        PyEvent.__init__(self)
        self.SetEventType(LOGIN_EVENT_ID)
        self.data = message

class LoginThread(Thread):
    """自定义一个继承自Thread类的类，构造方法中一般有个wxObject用来指代一个组件对象（大多数情况是Frame本身）
    重载run方法，做具体的操作，在操作中适当的地方用wx.PostEvent方法手动引发一个事件，事件源是wxObject，事件是前面自定义事件类的一个实例
    """
    def __init__(self, server, user, password, wxObject):
        Thread.__init__(self)
        self.server = server
        self.user = user
        self.password = password
        self.wxObject = wxObject

    def run(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server, 22, self.user, self.password, timeout=15)
            PostEvent(self.wxObject, LoginEvent("success"))
        except TimeOutException:
            PostEvent(self.wxObject, LoginEvent(u"连接超时"))
        except AuthenticationException:
            PostEvent(self.wxObject, LoginEvent(u"密码验证失败"))
        except SocketError:
            PostEvent(self.wxObject, LoginEvent(u"Socket错误导致连接失败"))
        except Exception, e:
            PostEvent(self.wxObject, LoginEvent(str(e)))


class MyFrame(Frame):
    def __init__(self):
        #详细的构造方法略去#
        self.btn.Bind(EVT_BUTTON,self._login)  #点击按钮确定，开始登录操作
        self.Connect(-1,-1,LOGIN_EVENT_ID,self._loginHandler) # Connect方法和xxx.Bind很像，就是把一个对象和某种事件联系起来，并给予一个处理事件的函数，
        # 和Bind不同的是Connect方法用的是EVENT的ID来绑定的。EVENT的ID可以通过EVT_BUTTON.typeID来查看，别的wx自带的event，在获取到其ID之后也可以转化成Connect方法来做
        # 这个self应该要和后文中自定义线程类初始化时传进去的wxObject参数一致（保证出事件的组件和监听的组件是一样的

    def _login(self,event):
        #略过了一些冻结界面的操作，比如self.btn.Disable()等。这样的话按下登录之后可以保证用户不会在有线程在登录中的时候再按登录出现混乱
        #还有做一些输入值的检查，获取输入值等等
        t = LoginThread(server,user,password,self)
　　　　 t.setDaemon(True)　　#设置t为守护进程的原因是如果用户按下确定开始登录，然后又想按取消的话，主线程可以在守护线程没完成前就退出。否则按了取消还是要等登录完成才有反应
        t.start()　　　　# 开启一个线程，当线程还在运行且没有触发你的自定义事件的这段时间里，主框架不会再被阻塞了。
        # 且由于之前调用了Disable，主框架内部的组件也是不可互动的。当线程触发一个事件（在这个例子里就是登录出错或者成功了）那么就调用之前在框架的构造方法里提到的绑定自定义事件的处理函数
        # 然后在_loginHandler里面对事件的data属性做个判断，如果是成功的data那么就做成功之后该做的操作，如果是失败了就做失败之后的操作。
　　　　　
    def _loginHandler(self,event):
        if event.data != "success":    #之前自定义事件类中的辅助信息参数data的价值在这里体现出来了。可以对触发的事件做判断，根据判断结果确定要做的是失败处理还是成功处理
            MessageBox(event.data,u"登录错误")
            self.okButton.SetLabel(u"确定")
            self.okButton.Enable()
            for item in [self.serverInput, self.userInput, self.passInput]:
                item.SetEditable(True)    #失败的情况就把之前所有冻结的界面组件解冻，因为要期待用户再输入
        else:
            server = self.serverInput.GetValue()
            user = self.userInput.GetValue()
            password = self.passInput.GetValue()
            self.Close()    
            MainFrame(server, user, password).Show()    #登录成功的话就关闭这个窗口然后Show出新的下一个窗口就行了



