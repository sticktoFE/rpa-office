# -*- coding: utf-8 -*-
import ast
import re
import subprocess
import time

import mss
import numpy
import win32con
import win32com.client
import win32gui
import win32process
import win32api
from myutils import image_compare, image_convert
from PIL import Image, ImageQt
from PySide6.QtGui import QGuiApplication, QPixmap

from myutils.window_run import get_hwnd

# from PySide6.QtCore import QThread


class ScreenShot:
    def __init__(self) -> None:
        self.top_hwnd = None
        self.screen = QGuiApplication.primaryScreen()
        self.mss_mss = mss.mss()
        self.use_mss_mss = None  # 默认不适用mss ，使用pyside6的截屏sdk

    # 在屏幕上截屏相应程序窗口
    # 利用直接截屏，通过截图定位程序中的位置，两边总是位置不一致，后来发现是操作系统有缩放的缘故，改成100%就好了，整了两天才发现
    # 统一返回 cv2格式图像，即nump.array
    def shot_screen(self, **kwargs):
        box = kwargs.get("box")
        if box is not None:
            # 1、根据起始位置和宽度、高度来截屏
            # 对起点位置和形状进行截屏   box=(x,y,width,heigth)
            # winId为根窗口，即整个桌面（屏幕），用0来表示
            # 1、使用pyqt截图（快一点）
            # print(f"ScreenShot in  {QThread.currentThread()}线程中")
            pixmap = self.screen.grabWindow(0, *box)
            cv2_img = image_convert.pixmap2cv_2(pixmap)
            # cv2_img = numpy.array(pixmap)
            # 2、使用mss截图
            # mss_mss_img = self.mss_mss.grab({"top":box[1],"left":box[0],"width":box[2],"height":box[3]})
            # img = Image.frombytes("RGB", mss_mss_img.size, mss_mss_img.bgra, "raw", "BGRX")
            # end = time.time()
            # print(f"shot_screen--mss用时：{end - beg}")
            return cv2_img

    # 通过寻找窗口来截屏

    def shot_screen_locate_window(self, class_name=None, window_name=None):
        if window_name is None:
            print("窗口名称不能为空")
            return (None, None, None)
        # self.top_hwnd = win32gui.FindWindow(None, window_name)
        self.top_hwnd = get_hwnd(class_name, window_name)
        # 十六进制转成成十进制
        # self.top_hwnd = ast.literal_eval('00B10F30')
        if self.top_hwnd == 0:
            print("没有获取到窗口")
            return (None, None, None)
        (x1, y1, x2, y2) = win32gui.GetWindowRect(self.top_hwnd)
        pixmap = self.screen.grabWindow(self.top_hwnd)
        return (self.top_hwnd, pixmap, x1, y1)
        # 用mss截图
        # mss_mss_img = self.mss_mss.grab(
        #     {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        # )
        # cv2_img = numpy.array(mss_mss_img, dtype=numpy.uint8)
        # return (cv2_img, x1, y1)

    def locate_window(self, class_name=None, window_name=None):
        if window_name is None:
            print("窗口名称不能为空")
            return (None, None, None)
        # self.top_hwnd = win32gui.FindWindow(None, window_name)
        self.top_hwnd = get_hwnd(class_name, window_name)
        # 十六进制转成成十进制
        # self.top_hwnd = ast.literal_eval('00B10F30')
        if self.top_hwnd == 0:
            print("没有获取到窗口")
            return (None, None, None)
        (x1, y1, x2, y2) = win32gui.GetWindowRect(self.top_hwnd)
        # pixmap = self.screen.grabWindow(self.top_hwnd)
        return (x1, y1, x2 - x1, y2 - y1)
        # 用mss截图
        # mss_mss_img = self.mss_mss.grab(
        #     {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        # )
        # cv2_img = numpy.array(mss_mss_img, dtype=numpy.uint8)
        # return (cv2_img, x1, y1)

    # 通过adb利用手机截屏功能截屏

    def shot_screen_adb(self):
        # bluestacks 之前连接端口总是变化，所以需要执行一次连接
        # 后来window11做了一次更新，默认端口是5555，所以不需要执行连接了，因为系统默认会连这个端口
        # os.system('adb connect 127.0.0.1:5555')
        # 获取操作对象（虚拟机上的android或手机）
        subprocess.run(
            "adb devices",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # subprocess.run("adb shell input keyevent 82")#亮屏手机
        subprocess.run(
            "adb shell /system/bin/screencap -p /sdcard/screen.png",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        time.sleep(0.1)
        subprocess.run(
            "adb pull /sdcard/screen.png biz/infoTracing/image/screen.png",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        img = QPixmap("biz/infoTracing/image/screen.png")
        return img
