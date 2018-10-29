import ctypes
from ctypes import wintypes

import purepywin32.common as common

psapi = ctypes.WinDLL('psapi.dll')

def pyEnumProcesses():
    EnumProcesses = psapi.EnumProcesses
    EnumProcesses.argtypes = (wintypes.PDWORD,
                              wintypes.DWORD,
                              wintypes.PDWORD)
    EnumProcesses.restype = wintypes.BOOL
    pid_count = wintypes.DWORD * 2048
    pid_array = pid_count()
    cb = ctypes.sizeof(pid_array)
    cb_needed = wintypes.DWORD()

    ret = EnumProcesses(ctypes.cast(pid_array, wintypes.PDWORD),
                        cb,
                        ctypes.byref(cb_needed))
    if not ret:
        raise ctypes.WinError(ret)
    returned_pids = int(cb_needed.value / ctypes.sizeof(wintypes.DWORD))
    return [pid for pid in pid_array][1:returned_pids]

def pyEnumProcessModules(handle):
    EnumProcessModules = psapi.EnumProcessModules
    EnumProcessModules.argtypes = (wintypes.HANDLE,
                                   wintypes.LPHANDLE,
                                   wintypes.DWORD,
                                   wintypes.LPDWORD)
    EnumProcessModules.restypes = wintypes.BOOL

    hmod = wintypes.HANDLE()
    cb_needed = wintypes.DWORD()

    ret = EnumProcessModules(handle,
                             ctypes.byref(hmod),
                             ctypes.sizeof(hmod),
                             ctypes.byref(cb_needed))
    if not ret:
        raise ctypes.WinError()

    return hmod

def pyGetModuleBaseNameW(hproc, hmod):
    GetModuleBaseNameW = psapi.GetModuleBaseNameW
    GetModuleBaseNameW.argtypes = (wintypes.HANDLE,
                                   wintypes.HMODULE,
                                   wintypes.LPWSTR,
                                   wintypes.DWORD)
    GetModuleBaseNameW.restype = wintypes.DWORD
    buf = ctypes.create_unicode_buffer(1024)
    ret = GetModuleBaseNameW(hproc, hmod, buf, 1024)

    if not ret:
        raise ctypes.WinError()
    
    return buf.value
