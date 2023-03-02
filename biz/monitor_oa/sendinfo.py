import sys
import time
from mytools.auto_app.AppActionExecThread import AppExec
from myutils.ScreenShot import ScreenShot
from pynput.mouse import Controller
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)
from ui.OCRResult_event import TotalMessage
from Form import Ui_Form


class MainWindow(QMainWindow):
    t_temp = time.perf_counter()
    delay_time = 500

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 对imageLabel读图片的路径进行初始化
        self.ui.screenLabel.setImagePath("biz/infoTracing/image/resized_screen.png")
        # self.ui.screenLabel.resize(self.src_width/3,self.src_heigth/3)
        self.ui.screenLabel.setPixmap(QPixmap("biz/infoTracing/image/1.jpg"))
        # self.ui.screenLabel.mousePressSignal.connect(self.imageLabelPressSlot)
        # self.ui.screenLabel.mouseDragSignal.connect(self.imageLabelDragSlot)
        # self.ui.screenLabel.wheelEvent().connect(self.imageLabelDragSlot)
        self.ss = ScreenShot()
        self.mouse = Controller()

    # 获取截屏并显示
    @Slot()
    def on_getScreenShotPushButton_clicked(self):
        time.sleep(0.5)
        (
            self.top_hwnd,
            pixmap_img,
            self.target_window_x,
            self.target_window_y,
        ) = self.ss.shot_screen_locate_window("WeChatMainWndForPC", "微信")
        self.ui.screenLabel.clear()
        self.ui.screenLabel.setPixmap(pixmap_img)

    # 点击开始
    @Slot()
    def on_actionStartPushButton_clicked(self):
        # name_list = []
        # for item in self.ui.taskTreeWidget.findItems("", Qt.MatchFlag.MatchStartsWith):
        #     name_list.append(item.text(0))
        for_pics = [
            "biz/monitor_oa/image/search.png",
            "biz/monitor_oa/image/selectfile.png",
            "biz/monitor_oa/image/send.png",
        ]
        self.ae = AppExec(
            class_name="WeChatMainWndForPC", window_name="微信", for_pics=for_pics
        )
        # self.ae.setFileNames(name_list)
        self.ae.signal.connect(self.ocrResult)
        self.ae.start()

    def ocrResult(self, result):
        self.aemg = TotalMessage("".join(result))
        self.aemg.show()

    # 点击任务终止

    @Slot()
    def on_taskStopPushButton_clicked(self):
        self.ae.terminate()


def send_webchat():
    for_pics = [
        "biz/monitor_oa/image/search.png",
        "biz/monitor_oa/image/selectfile.png",
        "biz/monitor_oa/image/send.png",
    ]
    ae = AppExec(class_name="WeChatMainWndForPC", window_name="微信", for_pics=for_pics)
    # self.ae.setFileNames(name_list)
    # self.ae.signal.connect(self.ocrResult)
    ae.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
