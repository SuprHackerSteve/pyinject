import argparse
import os
import platform

import purepywin32.common as pycommon
import purepywin32.kernel32 as k32
import purepywin32.winutils as utils


class PyInjectorInvalidDLL(Exception):
    pass

class PyDLLInjector(object):
    def __init__(self, dllname, pid=None, process=None):
        self.pid = pid
        self.process = process
        self.dllname = dllname
        self.mypid = k32.pyGetCurrentProcessId()

        if not os.path.isfile(self.dllname):
            raise PyInjectorInvalidDLL('dll not found on disk')

    def get_proc_handle(self):
        proc_handle = k32.pyOpenProcess(pycommon.PROCESS_CREATE_THREAD | pycommon.PROCESS_VM_WRITE,
                                          self.pid)
        proc_list = utils.get_all_procs()
        self.process = proc_list[self.pid]
        print('* Injecting into %s (%d)' % (self.process, self.pid))

    def inject(self):
        self.get_proc_handle()

def main(args):
    if args.pid and args.dll:
        pyinject = PyDLLInjector(args.dll, pid=args.pid)
        pyinject.inject()

    if args.process and args.process:
        pyinject = PyDLLInjector(args.dll, process=args.process)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Userland process injection utility')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pid', type=int, help='pid to inject payload')
    group.add_argument('--process', help='process name to inject payload')
    parser.add_argument('--dll', help='dll name to be injected')
    args = parser.parse_args()
    main(args)
