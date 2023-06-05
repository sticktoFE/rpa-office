import json
import subprocess
import sys
import time
import cv2
import pyautogui
from mytools.auto_app.AppActionExecThread import AppExec
from myutils.ScreenShot import ScreenShot
from pynput.mouse import Button, Controller
from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QInputDialog,
    QMainWindow,
    QTreeWidgetItem,
)
from ui.OCRResult_event import TotalMessage
from Form import Ui_Form
from myutils import image_convert


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
        self.ui.screenLabel.mousePressSignal.connect(self.imageLabelPressSlot)
        self.ui.screenLabel.mouseDragSignal.connect(self.imageLabelDragSlot)
        self.ss = ScreenShot()
        self.mouse = Controller()

    # 获取截屏并显示
    @Slot()
    def on_getScreenShotPushButton_clicked(self):
        time.sleep(0.8)
        # 通过huawei管家直接截屏
        # 通过BlueStacks虚拟机直接截屏
        # BlueStacks 版本4.280以上是“损汴圮湩潤w楬㙢4”，当前 4.200是_ctl.Window
        # BlueStacks-(_ctl.Window or 损汴圮湩潤w楬㙢4)
        #  window_name ="_ctl.Window",top_window_name="BlueStacks"
        # 不用到子窗口window_name='Loading..'，否则下面的三个键“返回，桌面，查看打开的应用”  就没了
        cv2_img, self.target_window_x, self.target_window_y = self.ss.shot_screen(
            top_window_name="多屏协同"
        )
        self.resizeRatio_x = 1  # 0.867*1.5#1.2
        self.resizeRatio_y = 1  # 0.359*1.5#0.8
        # 2、通过adb命令来截屏
        # sp = self.ss.shot_screen_adb()
        # #对象截屏，获取相关参数的类
        # #应该理解成 当前屏幕密度/被截屏屏幕密度，至于这个2/5咋来的，我只能说试出来的
        # self.resizeRatio =2/5
        # src_width,src_heigth = self.ss.get_src_screen_size()

        # src_width= sp.size().width()*self.resizeRatio_x
        # src_heigth = sp.size().height()*self.resizeRatio_y
        cv2_img = cv2.resize(
            cv2_img,
            None,
            fx=self.resizeRatio_x,
            fy=self.resizeRatio_y,
            interpolation=cv2.INTER_AREA,
        )
        sp = image_convert.cv2pixmap(cv2_img)
        # sp = sp.scaled(src_width,src_heigth,Qt.KeepAspectRatio,Qt.SmoothTransformation)
        # self.ui.screenLabel.resize(src_width,src_heigth)
        self.ui.screenLabel.clear()
        self.ui.screenLabel.setPixmap(sp)

    # 处理屏幕点击事件
    def imageLabelPressSlot(self, x, y):
        x = x / self.resizeRatio_x
        y = y / self.resizeRatio_y
        # 1、通过adb命令来实现点击
        # subprocess.run(f'adb shell input tap {x} {y}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        # 2、左键点击屏幕上的这个位置
        tagCenterX, tagCenterY = self.target_window_x + x, self.target_window_y + y
        self.old_pos = self.mouse.position
        self.mouse.position = (tagCenterX, tagCenterY)
        self.mouse.click(Button.left, 1)
        # 实现点击完后鼠标还回到原来位置
        self.mouse.position = self.old_pos
        # 点击新加载的屏幕
        self.on_getScreenShotPushButton_clicked()

    # 处理屏幕滑动事件
    def imageLabelDragSlot(self, x1, y1, x2, y2, t):
        x1 = x1 / self.resizeRatio_x
        y1 = y1 / self.resizeRatio_y
        x2 = x2 / self.resizeRatio_x
        y2 = y2 / self.resizeRatio_y
        # print('从({x1},{y1}) 拖到({x2},{y2}) ，时间({t})'.format(x1=x1, y1=y1,x2=x2, y2=y2,t=t))
        # 1、adb实现
        # subprocess.run(f'adb shell input swipe {x1} {y1} {x2} {y2} {t}')
        # 2、利用pynpt实现
        # 单击的另一种实现,先点击后释放
        s_CenterX, s_tagCenterY = self.target_window_x + x1, self.target_window_y + y1
        e_CenterX, e_tagCenterY = self.target_window_x + x2, self.target_window_y + y2
        self.old_pos = (
            self.mouse.position
        )  # (self.mouse.position[0]-x1,self.mouse.position[0]-y1)
        self.mouse.position = (s_CenterX, s_tagCenterY)
        # pynput模拟不出拖拽，所以用pyautogui
        pyautogui.dragTo(e_CenterX, e_tagCenterY, 0.2)
        self.mouse.position = (self.old_pos[0] + x2 - x1, self.old_pos[1] + y2 - y1)
        self.on_getScreenShotPushButton_clicked()

    # 点击添加文件
    @Slot()
    def on_fileAddPushButton_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "../mobile_action", "(*.json)"
        )
        filename = path.split("/")[-1].split(".")[0]
        print(filename)
        item = QTreeWidgetItem(self.ui.taskTreeWidget)
        item.setText(0, filename)

    # 点击移除
    @Slot()
    def on_fileRemovePushButton_clicked(self):
        root = self.ui.taskTreeWidget.invisibleRootItem()
        for item in self.ui.taskTreeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    # 执行动作组，输入是文件名的list，不包含扩展名
    def mobile_action_exec(self, name):
        try:
            with open("../mobile_action/" + name + ".json") as f:
                action_data = json.load(f)
                print("action set name:{}".format(action_data["action set name"]))
                for action in action_data["action set"]:
                    if action["action name"] == "delay":
                        time.sleep(float(action["param"]) / 1000)
                    else:
                        subprocess.run(action["cmd"])
        except:
            print("打开文件{}失败".format(name))

    @Slot()
    def on_autoClickScreenShot_clicked(self):
        for_pics = [
            "utils/AppCrawler/image/app_manager.png",
            "utils/AppCrawler/image/clear.png",
            "utils/AppCrawler/image/vphone.png",
            "utils/AppCrawler/image/skip_one.png",
            "utils/AppCrawler/image/skip_two.png",
            "utils/AppCrawler/image/shutdownad.png",
            # utilsiAppCrawlerng/image/upslip.png",
            "utils/AppCrawler/image/zy.png",
            "utils/AppCrawler/image/workstation.png",
            "utils/AppCrawler/image/notice.png",
            "utils/AppCrawler/image/import_notice.png",
            "utils/AppCrawler/image/all_news.png",
        ]
        self.OCR = AppExec(window_name="多屏协同", for_pics=for_pics)
        self.OCR.signal.connect(self.ocrResult)
        self.OCR.start()

    def ocrResult(self, result):
        self.ocrmg = TotalMessage("".join(result))
        self.ocrmg.show()


if __name__ == "__main__":
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
