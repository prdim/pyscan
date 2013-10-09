# -*- coding: utf-8 -*-
'''
Created on 30 сент. 2013 г.

@author: prolubnikovda
'''

import wx
import wx.aui

#----------------------------------------------------------------------


class ParentFrame(wx.aui.AuiMDIParentFrame):
    def __init__(self, parent):
        wx.aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title=u"Главное окно",
                                          size=(640,480),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()
        self.PushStatusText(u"Готов")
        self.Bind(wx.EVT_CLOSE, self.OnDoClose)

    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "Exit")
        self.Bind(wx.EVT_MENU, self.OnDoExit, item)
        mb.Append(menu, "&File")

        menu = wx.Menu()
        item = menu.Append(-1, "About")
        self.Bind(wx.EVT_MENU, self.OnDoAbout, item)
        mb.Append(menu, "&Help")
        return mb

    def OnNewChild(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count)
        child.Activate()

    def OnDoClose(self, evt):
        # Close all ChildFrames first else Python crashes
        for m in self.GetChildren():
            if isinstance(m, wx.aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    if isinstance(k, ChildFrame):
                        k.Close()
        evt.Skip()

    def OnDoExit(self, evt):
        wx.Exit()

    def OnDoAbout(self, evt):
        info = wx.AboutDialogInfo()
        info.Copyright = u"(c) Spec, 2013"
        info.Description = u"Это тестовая программа"
        info.Developers = (u"Spec",)
        info.Name = "PyScan"
        info.Version = "0.1"
        wx.AboutBox(info);

#----------------------------------------------------------------------

class ChildFrame(wx.aui.AuiMDIChildFrame):
    def __init__(self, parent, count):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title="Child: %d" % count)
#         mb = parent.MakeMenuBar()
#         menu = wx.Menu()
#         item = menu.Append(-1, "This is child %d's menu" % count)
#         mb.Append(menu, "&Child")
#         self.SetMenuBar(mb)

##        p = wx.Panel(self)
        p = MyPanel1(self)
#         wx.StaticText(p, -1, "This is child %d" % count, (10,10))
#         p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Bind( wx.EVT_CLOSE, p.onClosePane )

        wx.CallAfter(self.Layout)
        
#     def onClosePane( self, event ):
#         print(u"Закрываю панель")
#         event.Skip()        

#----------------------------------------------------------------------

class MyPanel1 ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,154 ), style = wx.TAB_TRAVERSAL )
        
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Выбор каталога", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        bSizer2.Add( self.m_staticText3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_dirPicker2 = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Выбор каталога", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer2.Add( self.m_dirPicker2, 1, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
        
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Статус...", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer3.Add( self.m_staticText4, 1, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
        
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_gauge2 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge2.SetValue( 0 ) 
        bSizer4.Add( self.m_gauge2, 1, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        bSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Запуск", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button2, 0, wx.ALL, 5 )
        
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"Остановка", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_button3, 0, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer5, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer1 )
        self.Layout()
        
        # Connect Events
#         self.Bind( wx.EVT_CLOSE, self.onClosePane )
        self.m_button2.Bind( wx.EVT_BUTTON, self.onStart )
        self.m_button3.Bind( wx.EVT_BUTTON, self.onStop )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def onClosePane( self, event ):
        print(u"Закрываю панель2")
        event.Skip()
    
    def onStart( self, event ):
        if self.m_dirPicker2.Path == u"":
#             self.Parent.Parent.Parent.PushStatusText(u"Нужно выбрать каталог!")
            app.pf.PushStatusText(u"Нужно выбрать каталог!")
        else:
            print("Start")
        event.Skip()
    
    def onStop( self, event ):
        print("Stop")
        event.Skip()

#----------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        self.pf = ParentFrame(None)
        self.pf.Show(True)
        self.SetTopWindow(self.pf)
        return True

    def OnExit(self):
        print("exit")

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()