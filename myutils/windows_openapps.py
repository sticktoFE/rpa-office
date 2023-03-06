import ctypes, time, shlex, subprocess
from ctypes.wintypes import DWORD, HWND
from ctypes import windll, byref


def get_windows(pid):
    current_window = 0
    pid_local = DWORD()
    while True:
        current_window = windll.User32.FindWindowExA(0, current_window, 0, 0)
        windll.user32.GetWindowThreadProcessId(current_window, byref(pid_local))
        if pid == pid_local.value:
            yield current_window
        if current_window == 0:
            return


def launch_apps_to_virtual_desktops_by_moving(command_lines, desktops=2):
    virtual_desktop_accessor = ctypes.WinDLL(
        "D:\\leichui\\workspace\\auto_mobile-master\\src\\VirtualDesktopAccessor.dll"
    )
    for i in range(desktops):
        pids = []
        for command_line in command_lines:
            if command_line:
                args = shlex.split(command_line)
                pids.append(subprocess.Popen(args).pid)
        time.sleep(3)
        for pid in pids:
            for window in get_windows(pid):
                window = HWND(window)
                print(i)


#     virtual_desktop_accessor.MoveWindowToDesktopNumber(window, i)
command_lines = r"""
                "D:\Program Files\Notepad++\notepad++.exe" "D:\Program Files\Notepad++\change.log"
                "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                """.splitlines()
launch_apps_to_virtual_desktops_by_moving(command_lines)
