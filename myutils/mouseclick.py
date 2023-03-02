import os
import time

import pyscreeze
from PIL import Image, ImageDraw
from pynput import mouse
from pynput.mouse import Button

import win32gui
import win32con
import win32api
import time
import os
import ctypes 
#需要用到pywin32的库
# import pyautogui
# from pyscreeze import (center, grab, locate, locateAll, locateAllOnScreen,
#         locateCenterOnScreen, locateOnScreen, pixel, pixelMatchesColor,
#         screenshot)

def picture_draw(path, locate):
    oriImg = pyscreeze.screenshot()
    maskImg = Image.new('RGBA', oriImg.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(maskImg)
    draw.ellipse(locate, fill=(255, 255, 0, 100))

    final = Image.composite(maskImg, oriImg, maskImg)
    final.save(path)


def on_move(x, y):
    # pass
    print(f'Pointer moved to {(x,y)}')

i = 1
def on_click(x, y, button, pressed):
    global i
    # button_name = ''
    # print(button)
    if button == Button.left:
        button_name = 'Left Button'
    elif button == Button.middle:
        button_name = 'Middle Button'
    elif button == Button.right:
        button_name = 'Right Button'
    else:
        button_name = 'Unknown'
    if pressed:
        if button == Button.left:
            button_name = 'Left Button'
            picture_path = os.path.abspath('.') + '\\picture%s.png' % str(i)
            picture_draw(picture_path, (int(x) - 25, int(y) - 25, int(x) + 25, int(y) + 25))
            i += 1
        print('{0} Pressed at {1} at {2}'.format(button_name, x, y))
    else:
        # print('{0} Released at {1} at {2}'.format(button_name, x, y))
        pass
    if not pressed:
        return False


def on_scroll(x, y, dx, dy):
    # print('scrolled {0} at {1}'.format(
    #     'down' if dy < 0 else 'up',
    #     (x, y)))
    pass
#对鼠标操作进行监听，可以记录鼠标点击位置 x,y
# 如果利用机器学习能识别出图像中我们关注的目标 Y，再利用opencv识别出目标Y在图像中的位置范围(x1,y1,x2,y2)，x,y和其作对比就知道鼠标是不是点了Y
# 这是可以做用户行为分析的逻辑
while True:
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll, suppress=False) as listener:
        listener.join()



times = 6
wdname = u'多屏协同'  # 窗口名
handle = win32gui.FindWindow(0, wdname)  # 窗口句柄
if handle == 0:
    for i in range(10):
       print("没有获取到多屏协同窗口")
else:
    left, top, right, bot = win32gui.GetWindowRect(handle)  # 梦幻窗口所在位置的坐标
    #鼠标定位到
    win32api.SetCursorPos([left+130,top+260])
    #执行左单键击，若需要双击则延时几毫秒再点击一次即可 time.sleep(1)
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # #右键单击
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    # win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,0,0,-250)#滚动鼠标轮
   