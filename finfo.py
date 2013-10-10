# -*- coding: utf-8 -*-
'''
Created on 10.10.2013

@author: prolubnikovda
'''

import os
import collections

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

if hasattr(os, 'statvfs'):  # POSIX
    def disk_usage(path):
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)

elif os.name == 'nt':       # Windows
    import ctypes
    import sys

    def disk_usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                           ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return _ntuple_diskusage(total.value, used, free.value)
else:
    raise NotImplementedError("platform not supported")

disk_usage.__doc__ = __doc__

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

#----------------------------------------------------------------------

def getlocaldata(sms,dr,flst):
    for f in flst:
        fullf = os.path.join(dr,f)
        if os.path.islink(fullf): continue # don't count linked files
        if os.path.isfile(fullf):
            sms[0] += os.path.getsize(fullf)
            sms[1] += 1
        else:
            sms[2] += 1
            
def walk(d):
    for name in os.listdir(d):
        path = os.path.join(d, name)
        if os.path.isfile(path):
            print path
        else:
            walk(path)

def dtstat(dtroot):
    sums = [0,0,1] # 0 bytes, 0 files, 1 directory so far
    os.path.walk(dtroot,getlocaldata,sums)
    return sums


