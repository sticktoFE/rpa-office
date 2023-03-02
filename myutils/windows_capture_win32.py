import time
import win32gui
import win32ui,win32api
import win32con
import numpy as np
import cv2
from PIL import Image
def get_hwnd(window_name: str):
    process_list = []
    def callback(handle, _):
        process_list.append(win32gui.GetWindowText(handle))
    win32gui.EnumWindows(callback, None)
    # ターゲットウィンドウ名を探す
    for process_name in process_list:
        if window_name in process_name:
            hnd = win32gui.FindWindow(None, process_name)
            break
    else:
        print("没找到指定窗口，使用整个桌面")
        hnd = win32gui.GetDesktopWindow()
    x0, y0, x1, y1 = win32gui.GetWindowRect(hnd)
    return hnd,x0, y0, x1, y1
def WindowCapture(window_name: str, bgr2rgb: bool = False):
    hnd,x0, y0, x1, y1 = get_hwnd(window_name) 
    width = x1 - x0 
    height = y1 - y0 
    # win32gui.SetForegroundWindow(hnd)
    # time.sleep(1.0)
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
     # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # saveBitMap.SaveBitmapFile(saveDC, 'biz/InfoTracing/image/screenshot12.bmp')

    # 1、获取图像
    img = np.frombuffer(saveBitMap.GetBitmapBits(True), np.uint8).reshape(height, width, 4)
    if bgr2rgb is True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("biz/InfoTracing/image/xxxx.png",img)
    cv2.imshow("result_view", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #2、获取位图信息
    # bmpinfo = saveBitMap.GetInfo()
    # bmpstr = saveBitMap.GetBitmapBits(True)
    # ###生成图像
    # im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    # im_PIL.show()  # 显示
    # im_PIL.save("biz/InfoTracing/image/xxxx.png", "JPEG", quality=100)  # 保存
    # im_PIL.show()  # 显示
    # 内存释放
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hnd, hwndDC)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    return img
if __name__ == '__main__':
    beg = time.time()
    img = WindowCapture("多屏协同",bgr2rgb=False) # 部分一致  多屏协同
    end = time.time()
    print(end - beg)