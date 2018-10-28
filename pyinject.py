import argparse
import os
import platform

import purepywin32.kernel32 as pyk32


class PyInjectorInvalidDLL(Exception):
    pass

class PyDLLInjector(object):
    def __init__(self, dllname, pid=None, process=None):
        self.pid = pid
        self.process = process
        self.dllname = dllname

        if not os.path.isfile(self.dllname):
            raise PyInjectorInvalidDLL('dll not found on disk')

    def get_proc_handle(self):
        pass

    def check_perms(self):
        pass


def main(args):
    if args.pid and args.dll:
        pyinject = PyDLLInjector(args.dll, pid=args.pid)

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
