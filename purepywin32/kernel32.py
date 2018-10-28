import ctypes
from ctypes import wintypes

kernel32 = ctypes.windll.kernel32

def pyGetLastError():
    GetLastError = kernel32.GetLastError
    GetLastError.argtypes = ()
    GetLastError.restype = wintypes.DWORD
    return GetLastError()


def pyOpenProcess(access, pid, inherit_handles=False):
    OpenProcess = kernel32.OpenProcess
    OpenProcess.argtypes = (wintypes.DWORD,
                            wintypes.BOOL,
                            wintypes.DWORD)
    OpenProcess.restype = wintypes.HANDLE
    return OpenProcess(access, pid, inherit_handles)
