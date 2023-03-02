import win32gui
import win32con
import re
import traceback
from time import sleep
import win32com.client


class cWindow:
    def __init__(self, hwnd=None, class_name=None):
        self._hwnd = hwnd
        self._class_name = class_name

    def SetAsForegroundWindow(self):
        # First, make sure all (other) always-on-top windows are hidden.
        self.hide_always_on_top_windows()
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._hwnd)
        # 强行显示窗口才好截图
        win32gui.SendMessage(
            self._hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)

    def Maximize(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def _window_enum_callback(self, hwnd, regex):
        '''Pass to win32gui.EnumWindows() to check all open windows'''
        if self._hwnd is None and re.match(regex, str(win32gui.GetWindowText(hwnd))) is not None:
            className = win32gui.GetClassName(hwnd)
            if self._class_name is None and not (className == 'Button' or className == 'Shell_TrayWnd' or className == 'TrayNotifyWnd') or self._class_name == className:
                self._hwnd = hwnd

    def find_window_regex(self, regex):
        if self._hwnd is None:
            win32gui.EnumWindows(self._window_enum_callback, regex)

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self._hwnd:  # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)

    def get_hwnd(self):
        return self._hwnd
# 获取顶层窗口parent_hwnd下的名称为wnd_name的窗口
# EnumWindows()的回调函数
        # hwnd: 在枚举每个顶层窗口而调用该函数的过程中传递给该函数的顶层窗口的句柄 如果作为EnumChildWindows的回调函数，则是子窗口的句柄
        # lParam: 即EnumWindows()函数的第二个参数。
        # Return Value:
        # 返回TRUE，则EnumWindows()函数在系统中继续调用EnumWindowsProc()函数；返回FALSE，则停止枚举。


def get_hwnd(class_name, wind_name):
    cW = cWindow(class_name=class_name)
    # sleep(1)
    try:
        regex = f".*{wind_name}.*"
        cW.find_window_regex(regex)
        # cW.Maximize()
        cW.SetAsForegroundWindow()
    except:
        f = open("log.txt", "w")
        f.write(traceback.format_exc())
        print(traceback.format_exc())
    return cW.get_hwnd()


# get_hwnd('微信')
