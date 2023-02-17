import sys
import traceback
from PIL import Image
from PySide6.QtCore import Qt, QTimer, QUrl, QRect
from PySide6.QtGui import QGuiApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QApplication, QMainWindow
from ...myutils.image_convert import pixmap2cv_1
from myutils.image_merge import ImageMerge, merge
from WebShotScreen import ShotScreenManager
from myutils.window_handle.ScreenShot import ScreenShot
import cv2


class Ui_MainWindow(QMainWindow, ShotScreenManager):
    def __init__(self, url, x=30, y=0, width=1500, height=800, callback=None):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self)
        ShotScreenManager.__init__(self, url, x, y, width, height, callback)
        # 当两个不同分辨率不同的设备运行同一个由Qt开发的程序时，会出现控件大小不一致甚至无法正常显示等问题。解决这个问题的方法是在主函数（程序入口）最前面添加一行代码
        #  效果待验证，如果可以，别忘了 rpa相应也加一下
        # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        self.setWindowTitle("截图")
        # self.temp_height = 0
        self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, False)  # 禁用最大化，最小化
        # self.setWindowFlag(Qt.WindowStaysOnTopHint, True) # 窗口顶置
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)  # 窗口无边框
        # 创建浏览器实例
        self.browser = QWebEngineView()
        # 隐藏滚动条
        self.browser.page().settings().setAttribute(
            QWebEngineSettings.WebAttribute.ShowScrollBars, False
        )
        # 加载页面
        self.browser.load(QUrl(self.win_url))
        # 设置中心窗口
        self.setCentralWidget(self.browser)
        # 设置窗口位置和大小
        self.set_window_geometry()
        self.shotscreen = ScreenShot()

    # 设置桌面窗口
    def set_window_geometry(self):
        print("MainWindow->set_window_geometry")
        # 设置窗口的宽度和高度
        screen_array = QGuiApplication.screens()
        screen_count = len(screen_array)
        for i in range(screen_count):
            rect = screen_array[i].availableGeometry()
            screen_width, screen_height = rect.width(), rect.height()
            # 如果调用时设置了展示的窗口width height 则只要找到屏幕能容纳此窗口的即可，故break
            if self.win_width and self.win_height:
                if self.win_width < screen_width and self.win_height < screen_height:
                    if not self.win_x and not self.win_y:
                        self.win_x, self.win_y = rect.left(), rect.top()
                    break
            else:
                # 如果调用时没有设置展示的窗口width height 则找到最大的屏幕作为窗口来展示，故没有break
                if not self.win_width or screen_width > self.win_width:
                    self.win_width = screen_width
                if not self.win_height or screen_height > self.win_height:
                    self.win_height = screen_height
        self.bbox = (self.win_x, self.win_y, self.win_width, self.win_height)
        self.setGeometry(self.win_x, self.win_y, self.win_width, self.win_height)

    # 截一次屏并缓存起来，为了最后做拼接
    # over_flow_size非完整尾页，上面重复的部分
    def screen_shot_tocache(self, is_rest_page=False):
        print("MainWindow->screen_shot")
        # 创建 截图工具实例
        # cv2_img = self.shotscreen.shot_screen(box=self.bbox)
        mPixmap = self.browser.grab(QRect(*self.bbox))
        cv2_img = pixmap2cv_1(mPixmap)
        self.image_list.append(cv2_img)
        # 下面是保存截图，为了调试 如果都没问题，没必要保存，因为拼接时用的是list（缓存）中的图片
        # 截图保存路径
        # cv2.imencode(".jpg", cv2_img)[1].tofile(f"{self.temp_path}/{self.shotPage}_{ self.image_name}")

    def start_shot(self):
        self.scroll_end = False
        self.image_list = []
        # 获取web页面的高
        content_total_height = self.browser.page().contentsSize().height()
        # 创建截图合并实例
        # self.image_merge = ImageMerge(save_path=self.image_path)
        # 创建定时器
        self.timer = QTimer(self)
        # 定时执行 exe_command 回调
        self.timer.timeout.connect(self.exe_command)
        # 设置定时间隔，单位：ms
        self.timer.setInterval(500)
        # 启动定时器
        self.timer.start()

    # 执行截图判断
    def exe_command(self):
        print("MainWindow->exe_command")
        if not self.scroll_end:
            # 截图后 滚动页面至下一页
            self.screen_shot_tocache()
            self.scroll_page_run_js()
        else:
            # 关闭定时器
            self.timer.stop()
            # 关闭窗口
            self.close()
            # 合并所有截图，
            fianle_img = merge(
                self.image_list, draw_match_output=self.temp_path, drop_head_tail=True
            )
            cv2.imencode(".jpg", fianle_img)[1].tofile(
                f"{self.image_path}/final_img.jpg"
            )
            self.checkShotCallback(file=fianle_img, error=None)

    def js_callback(self, result):
        print("----------")
        print(result)
        self.scroll_end = result

    # 执行js代码，模拟滚动条滑动web页面
    def scroll_page_run_js(self):
        # scrollHeight 内容最顶部到最底部的长度,即完整页面内容的高度，T+M+B
        # 包括因为滚动条而显示的M中间部分和上段T、下段B隐藏的部分
        # scrollTop 滚动条顶部位置距内容最顶部的位置，即显示页面上面因为滚动而隐藏的部分高度，即T
        # clientHeight =document.documentElement.clientHeight 等于 dHeight，  页面内容 显示部分的高度，即M
        # window.scrollTo(xpos,ypos) 要在窗口文档显示区左上角显示的文档的 x 坐标, y 坐标。
        # 减去20是为了滚动时适当重叠，面对丢失数据
        script = """
            var scroll = function (dScrollSteps) {
            var h = document.documentElement.scrollHeight
            var t = document.documentElement.scrollTop
            var clientHeight = document.documentElement.clientHeight
            dScrollSteps = dScrollSteps || 0
            var current = t + clientHeight
            //// 页面滚动到底了
            if (current >= h) {
                return 1
            } else {
                    window.scrollBy({top: dScrollSteps,left: 0,behavior: "smooth"})
                    return 0
                }
            }
        """
        # window.scrollTo(0, current)
        # 负数向上滚动
        # window.scrollBy({
        #         top: -100,
        #         left: 0,
        #         behavior: "smooth"
        #         })
        command = f"{script}\n scroll(200)"
        # script = script + "\n document.getElementById('head').style.display='none'"
        self.browser.page().runJavaScript(command, 0, self.js_callback)

    # 启动截图--入口
    def shotScreen(self):
        try:
            print("MainWindow->shotScreen", f"url={self.win_url}")
            # 页面加载完成后执行 start_shot回调
            self.browser.loadFinished.connect(self.start_shot)
            self.show()
            self.app.exit(self.app.exec())
        except Exception:
            self.checkShotCallback(file=None, error=traceback.format_exc())
