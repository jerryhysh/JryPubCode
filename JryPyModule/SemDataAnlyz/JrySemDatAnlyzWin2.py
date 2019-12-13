# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from JrySemDatAnlyz import TboxAndPlatProtolAnlyz
###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 800,600 ), style = wx.HSCROLL|wx.TAB_TRAVERSAL|wx.VSCROLL )
		
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"原始数据：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer5.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 400,200 ), wx.TE_MULTILINE )
		bSizer5.Add( self.m_textCtrl1, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"平台数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
		
		bSizer6.Add( self.m_checkBox1, 0, wx.ALL, 10 )
		
		m_radioBox1Choices = [ u"车控请求数据", u"车控应答数据" ]
		self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, u"数据解析方式", wx.DefaultPosition, wx.Size( 300,100 ), m_radioBox1Choices, 1, wx.RA_SPECIFY_ROWS )
		self.m_radioBox1.SetSelection( 1 )
		self.m_radioBox1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer6.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"数据解析", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer6.Add( self.m_button1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"数据解析结果：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 600,200 ), wx.TE_MULTILINE|wx.TE_READONLY )
		self.m_textCtrl2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		
		bSizer3.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.AnalyzeData )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def AnalyzeData( self, event ):
		self.OriginStr = self.m_textCtrl1.GetValue()
		if(True == self.m_checkBox1.GetValue()):
			self.OutputStr = TboxAndPlatProtolAnlyz(1,self.OriginStr)
			self.m_textCtrl2.SetValue(self.OutputStr)
		else:
			if("车控请求数据" == self.m_radioBox1.GetStringSelection()):
				self.OutputStr = TboxAndPlatProtolAnlyz(2,self.OriginStr)
				self.m_textCtrl2.SetValue(self.OutputStr)
			elif("车控应答数据" == self.m_radioBox1.GetStringSelection()):
				self.OutputStr = TboxAndPlatProtolAnlyz(3,self.OriginStr)
				self.m_textCtrl2.SetValue(self.OutputStr)
			else:
				pass
		event.Skip()






if __name__ == "__main__":
    App = wx.App()
    frame = MyFrame1(None) 
    panel = MyPanel1(frame)
    frame.Show(True) 
    App.MainLoop()
