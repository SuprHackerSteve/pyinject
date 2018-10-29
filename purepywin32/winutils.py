import ctypes
from ctypes import wintypes

import purepywin32.common as common
import purepywin32.kernel32 as k32
import purepywin32.psapi as psapi


def get_win32_error():
    gle = ctypes.GetLastError()
    return '0x%x - %s' % (gle, ctypes.FormatError(gle))

# TODO: handle session 1 -> session 0
def get_all_procs():
    proc_list = {}
    for cpid in psapi.pyEnumProcesses():
        # some process opens will fail, like pid 0, 4, etc
        # most will be running in session 1, all session 0 pids are off limits
        try:
            proc = k32.pyOpenProcess(common.PROCESS_QUERY_INFORMATION | common.PROCESS_VM_READ, cpid)
            hmod = psapi.pyEnumProcessModules(proc)
            exe = psapi.pyGetModuleBaseNameW(proc, hmod)
            proc_list[cpid] = exe
            k32.pyCloseHandle(hmod)
            k32.pyCloseHandle(proc)
        except WindowsError as e:
            continue

    return proc_list
def get_current_session():
    return k32.kernel32.WTSGetActiveConsoleSessionId()
