import win32api, win32con, win32gui
def get_window_pos(name):
      name = name
      handle = win32gui.FindWindow(0, name)
      # 获取窗口句柄
      if handle == 0:
            return None
      else:
            # 返回坐标值和handle
            return win32gui.GetWindowRect(handle), handle
(x1, y1, x2, y2), handle = get_window_pos('多屏协同')
print(handle)
# 发送还原最小化窗口的信息
win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE,0)
# 设为高亮
win32gui.SetForegroundWindow(handle)

from PIL import Image, ImageGrab
img_ready = ImageGrab.grab((x1, y1, x2, y2))
# 截图
img_ready.show()
# 展示 