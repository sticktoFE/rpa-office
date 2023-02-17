from pathlib import Path

from ss_pyside6 import Ui_MainWindow
from ss_selenium import SeleniumManager
from myutils.window_handle.window_info import handle_screen

def shotCallback(res):
    pass
    # print("file_path", res)


url = "https://www.maigoo.com/top/408298.html"
# url = 'https://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html'
# 1、使用selenium来请求网页并截图
# SeleniumManager(url,
#                 shot_driver=SeleniumManager.shot_selenium_driver_Chromedriver,
#                 image_path=save_path,
#                 callback=shotCallback).shotScreen("天气预报")
# 2、使用pyside6来请求网页并截图
@handle_screen
def mw():
    Ui_MainWindow(url, callback=shotCallback).shotScreen()


mw()