# -*- coding: utf-8 -*-
'''
Created on 30 сент. 2013 г.

@author: prolubnikovda
'''

import wx
import wx.aui
import wx.grid
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
        self.SetStatusText(u"Готов")
        self.Bind(wx.EVT_CLOSE, self.OnDoClose)

    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "Сканер\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Варианты\tCtrl-M")
        self.Bind(wx.EVT_MENU, self.OnVariantView, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        menu.AppendSeparator()
        item = menu.Append(-1, "Exit\tAlt-X")
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
        
    def OnVariantView(self, evt):
        self.count += 1
        child = VariantViewFrame(self, self.count)
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
                                         title="Сканер: %d" % count)
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

class VariantViewFrame(wx.aui.AuiMDIChildFrame):
    def __init__(self, parent, count):
        wx.aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title="Варианты: %d" % count)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button( self, wx.ID_ANY, u"Обновить", wx.DefaultPosition, wx.DefaultSize, 0 )
        button.Bind(wx.EVT_BUTTON, self.onRefresh)
        sizer_h.Add(button, 0, wx.ALL, 5)
        button = wx.Button( self, wx.ID_ANY, u"Удалить", wx.DefaultPosition, wx.DefaultSize, 0 )
        button.Bind(wx.EVT_BUTTON, self.onDelete)
        sizer_h.Add(button, 0, wx.ALL, 5)
        button = wx.Button( self, wx.ID_ANY, u"Оптимизировать", wx.DefaultPosition, wx.DefaultSize, 0 )
        button.Bind(wx.EVT_BUTTON, self.onVacuum)
        sizer_h.Add(button, 0, wx.ALL, 5)
        
        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_v.Add(sizer_h, 0, wx.EXPAND, 5)
        #SELECT t1.id, t1.path, t1.dt, t1.start, t1.stop, t2.cnt  FROM variant as t1, (select variant_id, count(*) as cnt from files group by variant_id) as t2 where t1.id=t2.variant_id
        #SELECT t1.id, t1.path, t1.dt, t1.start, t1.stop, t2.cnt  FROM variant as t1 left join (select variant_id, count(*) as cnt from files group by variant_id) as t2 on t1.id=t2.variant_id
        self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        # Grid
        app.pf.PushStatusText(u"Чтение данных...")
        t = time.time()
        self.conn = openDb()
        self.table = VariantTable(self.conn)
        self.m_grid1.SetTable(self.table, True, wx.grid.Grid.wxGridSelectRows)
        app.pf.PushStatusText(u"Запрос выполнен за " + time.strftime("%M:%S", time.localtime(time.time()-t)))
#         self.m_grid1.CreateGrid( 5, 5 )
#         self.m_grid1.EnableEditing( True )
#         self.m_grid1.EnableGridLines( True )
#         self.m_grid1.EnableDragGridSize( False )
#         self.m_grid1.SetMargins( 0, 0 )
#         
#         # Columns
#         self.m_grid1.EnableDragColMove( False )
#         self.m_grid1.EnableDragColSize( True )
#         self.m_grid1.SetColLabelSize( 30 )
#         self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
#         
#         # Rows
#         self.m_grid1.EnableDragRowSize( True )
#         self.m_grid1.SetRowLabelSize( 80 )
#         self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        
        # Label Appearance
        
        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        self.m_grid1.AutoSize()
        self.m_grid1.EnableEditing(False)
        sizer_v.Add( self.m_grid1, 1, wx.ALL|wx.EXPAND, 5 ) 
        
        self.SetSizer(sizer_v)
        self.Layout()      
        
    def __del__( self ):
        self.conn.close()

    def onRefresh(self, evt):
        app.pf.PushStatusText(u"Обновление данных...")
        t = time.time()
        self.table = VariantTable(self.conn)
        self.m_grid1.SetTable(self.table, True, wx.grid.Grid.wxGridSelectRows)
        app.pf.PushStatusText(u"Запрос выполнен за " + time.strftime("%M:%S", time.localtime(time.time()-t)))
        self.m_grid1.ForceRefresh()
        self.m_grid1.AutoSize()
        
    def onDelete(self, evt):
        rows = self.m_grid1.GetSelectedRows()
        t = time.time()
        app.pf.PushStatusText(u"Удаление строк...")
        for i in rows:
            with self.conn:
                id = self.table.data[i][0]
                self.conn.execute("""delete from files where variant_id=?""", (id,))
                self.conn.execute("""delete from variant where id=?""", (id,))
        app.pf.PushStatusText(u"Обновление данных...")
        self.table = VariantTable(self.conn)
        self.m_grid1.SetTable(self.table, True, wx.grid.Grid.wxGridSelectRows)
        app.pf.PushStatusText(u"Запрос выполнен за " + time.strftime("%M:%S", time.localtime(time.time()-t)))
        self.m_grid1.ForceRefresh()
        self.m_grid1.AutoSize()
        
    def onVacuum(self, evt):
        app.pf.PushStatusText(u"Оптимизация базы данных...")
        t = time.time()
        self.conn.execute("""VACUUM""")
        app.pf.PushStatusText(u"Запрос выполнен за " + time.strftime("%M:%S", time.localtime(time.time()-t)))

#----------------------------------------------------------------------

class VariantTable(wx.grid.PyGridTableBase):
    
    def __init__(self, conn):
        wx.grid.PyGridTableBase.__init__(self)
        c = conn.cursor()
        self.data = c.execute("""SELECT t1.id, t1.dt, t1.path, t1.start, 
            t1.stop, t2.cnt  
            FROM variant as t1 left join 
            (select variant_id, count(*) as cnt from files group by variant_id) as t2 
            on t1.id=t2.variant_id""").fetchall() 

    def GetNumberRows(self):
        return len(self.data)
    
    def GetNumberCols(self):
        return 5 #ID, Дата, Путь, Файлов, Время, Запущен
    
    def GetColLabelValue(self, col):
        return (u"Дата", u"Путь", u"Файлов", u"Время", u"Запущен")[col]
    
    def GetRowLabelValue(self, row):
        return self.data[row][0]
    
    def IsEmptyCell(self, row, col):
        return self.data[row][col] is not None
    
    def GetValue(self, row, col):
        value = self.data[row][col+1]
        if col==2:
            if self.data[row][5] is None:
                return ""
            else:
                return self.data[row][5]
        if col==4:
            if self.data[row][3] is None:
                return ""
            else:
                return time.strftime("%H:%M:%S", time.localtime(self.data[row][3]))
        if col==3:
            if self.data[row][4] is None or self.data[row][3] is None:
                return ""
            else:
                return time.strftime("%H:%M:%S", time.gmtime(self.data[row][4]-self.data[row][3]))
        if value is None:
            return ""
        return value
        
    def SetValue(self, row, col, value):
        pass
    
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
        self.max_files = 0
    
    def __del__( self ):
#         print("закрываюся...")
        if self.isStart:
            self.isStart = False
            self.th.join()
#             self.conn.close()
    
    def progress(self):
        self.m_gauge2.Pulse()
        self.m_staticText41.SetLabel(u"Подготовка...")
        self.t_files = 0
        self.s_files = 0
        global dt_list
        dt_list = []
        test = finfo.disk_usage(self.m_dirPicker2.Path)
        self.s_files_e = test.used
        print finfo.bytes2human(test.total)
        print finfo.bytes2human(test.used)
        print finfo.bytes2human(test.free)
        self.conn = openDb()
        self.max_files = getLastFileCount(self.conn, self.m_dirPicker2.Path)
        id = addVariant(self.conn, self.m_dirPicker2.Path)
        self.t_time = time.time()
        self.s_time = self.t_time
        self.walk(self.m_dirPicker2.Path, id)
        self.isStart = False
        addFileFlush(self.conn)
        updateVariant(self.conn, id, time.time())
        self.progressUpdateNow(self.m_dirPicker2.Path)
        self.conn.close()
        self.m_staticText4.SetLabel(u"Завершено успешно.")
        
    def progressUpdate(self, path):
        if (time.time() - self.t_time) > 1:
            self.progressUpdateNow(path)
            self.t_time = time.time()
#             self.d_files = self.t_files
    def progressUpdateNow(self, path):
        self.m_staticText4.SetLabel(path)
        self.m_staticText41.SetLabel(u"Обработано файлов: %i, скорость: %i файлов/сек, время: " % 
                                         (self.t_files,
                                          self.t_files/(time.time()-self.s_time)) +
                                        time.strftime("%M:%S", time.localtime(time.time()-self.s_time)))
        if self.max_files == 0:
            self.m_gauge2.SetValue((self.s_files*100)/self.s_files_e)
        elif self.t_files>0 and (self.t_files<self.max_files):
            self.m_gauge2.SetValue((self.t_files*100)/self.max_files)
            self.m_staticText41.SetLabel(self.m_staticText41.GetLabel() + u", осталось: " +
                                         time.strftime("%M:%S", 
                                                       time.localtime((time.time()-self.s_time)*
                                                                      (self.max_files-self.t_files)/self.max_files)))    

    def walk(self, d, id):
        try:
            lst = os.listdir(d)
        except os.error:
            return
        for name in lst:
            if self.isStart == False:
                return
            path = os.path.join(d, name)
            if os.path.isfile(path):
                stat = os.stat(path)
                addFile(self.conn,(id, path, name, d, stat.st_size, 
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
#         self.conn.close()
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
    conn.execute("""create index if not exists files_index on files (variant_id asc)""")
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

def updateVariant(conn, id, t):
    conn.execute("""update variant set stop=? where id=?""", (t, id))
    conn.commit()

dt_list = []
def addFile(conn, dt):
    global dt_list
#     c = conn.cursor()
    dt_list.append(dt)
    if len(dt_list) >1000:
        addFileFlush(conn)
    
def addFileFlush(conn):
    global dt_list
    conn.executemany("""insert into files
        (variant_id, path, fname, fparent, size, atime, mtime, ctime) 
        values (?,?,?,?,?,?,?,?);""", dt_list)
    conn.commit()
    dt_list = []
    
def getLastFileCount(conn, path):
    c = conn.cursor()
    row = c.execute("""SELECT max(id) FROM variant where path=?""", (path,)).fetchone()
    if row[0] == None:
        return 0
    id = row[0]
    return c.execute("""select count(*) from files where variant_id=?""", (id,)).fetchone()[0]

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
