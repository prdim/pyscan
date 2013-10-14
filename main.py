# -*- coding: utf-8 -*-
'''
Created on 30 сент. 2013 г.

@author: prolubnikovda
'''

import wx
import wx.aui
import os
import finfo
import threading
import datetime
import time
import sqlite3 as db

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
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer3.Add( self.m_staticText4, 1, wx.ALL, 5 )
        
        
        bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )
        
        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
        self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )
        bSizer3.Add( self.m_staticText41, 1, wx.ALL, 5 )
                
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
        
        self.isStart = False
        self.t_files = 0
        self.s_files = 0
        self.s_files_e = 0
        self.t_time = 0
        self.s_time = 0
#         self.d_time = 0
        self.conn = None
    
    def __del__( self ):
        print("закрываюся...")
        if self.isStart:
            self.isStart = False
            self.th.join()
    
    def progress(self):
        self.t_files = 0
        self.s_files = 0
        self.t_time = time.time()
        self.s_time = self.t_time
        test = finfo.disk_usage(self.m_dirPicker2.Path)
        self.s_files_e = test.used
        print finfo.bytes2human(test.total)
        print finfo.bytes2human(test.used)
        print finfo.bytes2human(test.free)
        self.conn = openDb()
        id = addVariant(self.conn, self.m_dirPicker2.Path)
        self.walk(self.m_dirPicker2.Path, id)
        self.isStart = False
        self.conn.close()
        self.m_staticText4.SetLabel(u"Завершено успешно.")
        
    def progressUpdate(self, path):
        if (time.time() - self.t_time) > 1:
            self.m_staticText4.SetLabel(path)
            self.m_staticText41.SetLabel(u"Обработано файлов: %i, скорость: %i файлов/сек, время: " % 
                                             (self.t_files,
                                              self.t_files/(time.time()-self.s_time)) +
                                            time.strftime("%M:%S", time.localtime(time.time()-self.s_time)))
            self.m_gauge2.SetValue((self.s_files*100)/self.s_files_e)
            self.t_time = time.time()
#             self.d_files = self.t_files

    def walk(self, d, id):
        try:
            lst = os.listdir(d)
        except os.error:
            return
        for name in lst:
            if self.isStart == False:
                return
            pname = os.path
            path = os.path.join(d, name)
            if os.path.isfile(path):
#                 func(path)
                stat = os.stat(path)
                addFile(self.conn,(id, path, name, pname, stat.st_size, 
                                   stat.st_atime, stat.st_mtime, stat.st_ctime))
                self.s_files += stat.st_size
                self.t_files += 1
#                 self.m_staticText4.SetLabelText(path)
#                 self.m_staticText41.SetLabelText(u"Обработано файлов: %i" % self.t_files)
                self.progressUpdate(path)
            else:
                self.walk(path, id)
          
    # Virtual event handlers, overide them in your derived class
    def onClosePane( self, event ):
        print(u"Закрываю панель2")
        event.Skip()
    
    def onStart( self, event ):
        if self.isStart:
            app.pf.PushStatusText(u"Процесс уже запущен!")
            return
        if self.m_dirPicker2.Path == u"":
#             self.Parent.Parent.Parent.PushStatusText(u"Нужно выбрать каталог!")
            app.pf.PushStatusText(u"Нужно выбрать каталог!")
        else:
            self.th = threading.Thread(target=self.progress)
            self.isStart = True
            self.th.start()
        event.Skip()
    
    def onStop( self, event ):
        self.isStart = False
        print("Stop")
        event.Skip()

#----------------------------------------------------------------------

def openDb():
    conn = db.connect("db\\files.db")
#     c = conn.cursor()
#     rows = c.execute("""select * from sqlite_master where type = 'table'""").fetchall()
#     if len(rows) == 0:
    conn.execute("""create table if not exists variant (
        id int primary key not null,
        path text not null,
        dt text not null,
        start int,
        stop int);""")
    conn.execute("""create table if not exists files (
        variant_id int not null,
        path text,
        fname text,
        fparent text,
        size int,
        atime int,
        mtime int,
        ctime int);""")
    return conn

def addVariant(conn, basePath):
    c = conn.cursor()
    rows = c.execute("""select max(id) from variant""").fetchone()
    if rows[0] == None:
        id = 1
    else:
        id = rows[0] + 1
    print rows, id
    c.execute("""insert into variant(id, path, dt, start) values(?,?,?,?);""",
              (id,
               basePath,
               db.Date.today(),
               time.time()))
    conn.commit()
    c.close
    return id

def addFile(conn, dt):
    c = conn.cursor()
    c.execute("""insert into files
        (variant_id, path, fname, fparent, size, atime, mtime, ctime) 
        values (?,?,?,?,?,?,?,?);""", dt)
    conn.commit()

def checkFile(path):
    stat = os.stat(path)
#     print path, stat.st_size, stat.st_atime, stat.st_mtime, stat.st_ctime

#----------------------------------------------------------------------

class MyApp(wx.App):
    def OnInit(self):
        self.pf = ParentFrame(None)
        self.pf.Show(True)
        self.SetTopWindow(self.pf)
        return True

    def OnExit(self):
        print("exit")

#----------------------------------------------------------------------

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
