import functools
import re
import subprocess
import sys
import time
from win32 import win32api, win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics
from pathlib import Path


# '获取手机屏幕大小'
def get_src_screen_size(self):
    completedProcess = subprocess.run(
        "adb shell wm size",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if completedProcess.returncode == 0:
        if result := re.search(r"(\d+)x(\d+)", completedProcess.stdout):
            # print(int(result.group(1)),int(result.group(2)) )
            return (int(result.group(1)), int(result.group(2)))
    else:
        print(f"{completedProcess.stderr}")
        return None


# 截图展示区缩放比例，这个数字和分辨率，DIP等都有关系，还没摸清规律
# 3*3/4 #通过直接屏幕截屏时 dip 240调整成320时，写成3/4# 缩放比例
# '获取手机屏幕密度'
def get_src_screen_density(self):
    completedProcess = subprocess.run(
        "adb shell wm density",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if completedProcess.returncode == 0:
        if result := re.search(r"(\w+): (\d+)", completedProcess.stdout):
            # print(f"源系统显示密度：{result.group(2)}")
            return int(result.group(2))
    else:
        print(f"{completedProcess.stderr}")
        sys.exit()


# 本来想寻找一个公式来识别两个屏幕的对一张图片的缩放比例，无奈没找到，此处暂时存档
def get_resize_ratio(self, img):
    # 当前主机屏显示密度
    curent_density = self.screen.physicalDotsPerInch()
    print(f"当前屏显示密度{curent_density}")
    src_density = self.get_src_screen_density()
    print(f"源系统显示密度{src_density}")
    # 为了让显示图像和源屏大小一致，做相应缩放
    self.scaleRatio = curent_density / (src_density)
    src_width, src_heigth = self.get_src_screen_size()
    width = src_width * self.scaleRatio / self.resizeRatio
    height = src_heigth * self.scaleRatio / self.resizeRatio
    print(img.width(), img.height())
    return img.scaled(width, height)


# 在屏幕上截屏相应程序窗口时，计算其宽和高 单位像素，显然的
def get_pic_size(self):
    # 注释的和未注释的两种方式，都没用上
    # try:
    #     f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    # except WindowsError:
    #     f = None
    # if f:
    #     rect = ctypes.wintypes.RECT()
    #     DWMWA_EXTENDED_FRAME_BOUNDS = 9
    #     f(ctypes.wintypes.HWND(self.top_hwnd),
    #       ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
    #       ctypes.byref(rect),
    #       ctypes.sizeof(rect)
    #       )
    #     # return (rect.right - rect.left, rect.bottom - rect.top)
    self.childRec = win32gui.GetClientRect(self.purpose_hwnd)  # 目标子句柄窗口的坐标
    print(self.childRec)
    return (
        self.childRec[2] - self.childRec[0],
        self.childRec[3] - self.childRec[1],
    )


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    print(f"物理分辨率={w,h}")
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(win32con.SM_CXSCREEN)
    h = GetSystemMetrics(win32con.SM_CYSCREEN)
    print(f"缩放后分辨率={w,h}")
    return w, h


def getdpi():
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    screen_scale_rate = screen_scale_rate * 100
    print(f"缩放倍数={screen_scale_rate}%")
    return screen_scale_rate


# 装饰器，用于调整系统缩放比例
def handle_screen(func):
    # 如果识别到系统分辨率进行了缩放，为了截图，先恢复到不缩放，再回到原来状态
    @functools.wraps(func)
    def adjust_dpi():
        userdpi = getdpi()
        print(f"当前系统缩放率为:{userdpi}")
        if userdpi == 100:
            print(" 程序直接运行")
            func()
        else:
            print("正在调整为100%缩放率")
            location = f"{Path(__file__).parent}/SetDpi.exe"
            win32api.ShellExecute(0, "open", location, " 100", "", win32con.SW_HIDE)
            print("运行中 请等待")
            func()
            print("运行完成 缩放自动调回初始")
            userdpi = str(userdpi)
            win32api.ShellExecute(0, "open", location, userdpi, "", win32con.SW_HIDE)

    return adjust_dpi


# screen_scale_rate = getdpi()
# print(screen_scale_rate)
getdpi()
