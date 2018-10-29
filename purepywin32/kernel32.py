import ctypes
from ctypes import wintypes

import purepywin32.common as common

kernel32 = ctypes.windll.kernel32


def pyOpenProcess(access, pid, inherit_handles=False):
    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = (wintypes.DWORD,
                            wintypes.BOOL,
                            wintypes.DWORD)
    OpenProcess.restype = wintypes.HANDLE
    ret = OpenProcess(access, inherit_handles, pid)
    if not ret:
        raise ctypes.WinError()
    return ret

def pyCloseHandle(handle):
    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = (wintypes.HANDLE,)
    CloseHandle.restype = wintypes.BOOL

    if not handle:
        return

    CloseHandle(handle)

def pyGetCurrentProcessId():
    GetCurrentProcessId = kernel32.GetCurrentProcessId
    GetCurrentProcessId.argtypes = ()
    GetCurrentProcessId.restype = wintypes.DWORD
    return GetCurrentProcessId()
