from random import choice, randint
import string
from win32clipboard import *
from PySide6.QtGui import QCursor, QFont, QIcon, QKeySequence, QMovie, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    QMenu,
    QSystemTrayIcon,
    QShortcut,
    QFileDialog,
)
from PySide6.QtCore import Qt, QEvent, QSize, QTimer

# from biz.shotscreen.DrawShot import ScreenLabel
from utils.ScreenShot import ScreenShot

# from util.TimeShot import TimeShot
from functools import partial
from ui.Ui_mainwindow import Ui_MainWindow

from ui.Ui_screendrawdialog_event import ShotDialog

# from .ManagerConfig import ManagerConfig
from ui.Ui_manage_config_event import ManagerConfig


def get_icon():
    # 测试模拟图标
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    painter = QPainter()
    painter.begin(pixmap)
    painter.setFont(QFont("思源字体", 11))
    painter.setPen(Qt.GlobalColor(randint(4, 18)))
    painter.drawText(0, 0, 16, 16, Qt.AlignCenter, choice(string.ascii_letters))
    painter.end()
    return QIcon(pixmap)


class BaseWindow(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.screenwidth = width
        self.screenheight = height
        # self.adjustSize()
        self.setupUi(self)
        # 这一行就是来设置窗口始终在顶端的。
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )  # 保持界面在最上层且无边框（去掉窗口标题）
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 托盘行为
        self.action_quit = QAction("退出", self, triggered=self.stopScreenshot)
        self.action_show = QAction("主窗口", self, triggered=self.show)
        self.menu_tray = QMenu(self)
        self.menu_tray.addAction(self.action_quit)
        # 增加分割线
        self.menu_tray.addSeparator()
        self.menu_tray.addAction(self.action_show)
        # 设置最小化托盘
        self.tray = QSystemTrayIcon(QIcon("./icon/ai.png"), self)  # 创建系统托盘对象
        # self.tray.activated.connect(self.freeShot)  # 设置托盘点击事件处理函数
        self.tray.setContextMenu(self.menu_tray)
        # 快捷键
        QShortcut(QKeySequence("F1"), self, self.freeShot)

        ##右键菜单设置
        self.context_menu = QMenu(self)
        self.init_menu()

        # 启动定时器检测记事本的位置大小和是否关闭
        self.checkTimer = QTimer(self, timeout=self.checkWindow)
        # action.setEnabled(0)
        # 两个可弹出的子窗口
        self.mc = None
        self.rcwindow = None
        # 如果已经识别这个图片，就不用再输出到界面上
        self.hasOCRSamePageID = None
        self.initFirst()
        self.anchorHasClicked = False

        self.xleave = 20
        self.yleave = 13

    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())

    def init_menu(self):
        # 背景透明
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        # 无边框、去掉自带阴影
        self.context_menu.setWindowFlags(
            self.context_menu.windowFlags()
            | Qt.FramelessWindowHint
            | Qt.NoDropShadowWindowHint
        )
        self.context_menu.addAction(get_icon(), "关闭", self.close)
        self.context_menu.addSeparator()
        action = self.context_menu.addAction(get_icon(), "选项", self.managerConfig)

    def managerConfig(self):
        self.mc = ManagerConfig()
        rect = self.frameGeometry().getRect()
        self.mc.move(rect[0] + rect[2], rect[1])
        self.mc.show()
        # self.checkTimer.start(10)  # 10毫秒比较流畅

    def checkWindow(self):
        # 查找
        # hwnd = win32gui.FindWindow(None,'配置OCR参数')
        if not self.mc and not self.rcwindow:
            # 表示记事本关闭了
            self.checkTimer.stop()
            # self.close()  # 关闭自己
            return
        # 获取位置
        rect = self.frameGeometry().getRect()
        if self.mc:
            self.mc.move(rect[0] + rect[2], rect[1])
        if self.rcwindow:
            self.rcwindow.move(rect[0] + rect[2], rect[1])

    ##手工画范围截图
    def freeShot(self, width, height):
        """开始截图"""
        self.hide()
        # self.label = ScreenLabel(width, height)
        self.label.showFullScreen()
        self.label.signal.connect(self.callback)

    def callback(self, pixmap):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        # 截完图做啥操作
        dialog = ShotDialog(pixmap[0])
        dialog.exec_()
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口

    # 对当前激活的窗口进行截图
    def shootScreen(self):
        if self.delaySpinBox.value() != 0:
            QApplication.beep()
        self.originalPixmap = ScreenShot().shot_screen()
        # self.updateScreenshotLabel()
        if self.hideThisWindowCheckBox.isChecked():
            self.show()

    # 手工截当前屏幕
    def newScreenshot(self):
        if self.hideThisWindowCheckBox.isChecked():
            self.hide()
        self.pushButton_shotCurrentWin.setDisabled(True)
        Qt.QTimer.singleShot(self.delaySpinBox.value() * 1000, self.shootScreen)
        self.pushButton_shotCurrentWin.setDisabled(False)

    # 手工截当前屏幕内容保存
    def saveScreenshot(self):
        format = "png"
        initialPath = Qt.QDir.currentPath() + "/untitled." + format
        fileName, filetype = QFileDialog.getSaveFileName(
            self,
            "Save As",
            initialPath,
            "%s Files (*.%s);;All Files (*)" % (format.upper(), format),
        )
        if fileName:
            self.originalPixmap.save(fileName, format)
            print("file saved as  %s" % fileName)

    # 手工划区启动截屏
    def startHandScreenshot(self):
        """开始截图"""
        self.hide()
        # self.label = ScreenLabel(self.screenwidth, self.screenheight)
        self.label.showFullScreen()
        # self.label.signal.connect(self.callback)
        self.label.signal.connect(self.afterDraw)

    def afterDraw(self, box):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口
        if box[0] == "esc":
            return
        # self.PO = TimeShot(main_win=self,box=box[1])
        # self.PO.start()
        # self.PO.signal.connect(self.refresh)

    # 上面离开后再鼠标放到小程序上时触发
    def enterEvent(self, evt):
        self.activateWindow()
        if self.x() == self.xleave - self.width():
            self.move(-self.xleave, self.y())
        elif self.y() == self.yleave - self.height() + self.y() - self.geometry().y():
            self.move(self.x(), -self.yleave)
        # 只要鼠标放到窗口就停止扫描识别
        if self.PO.runCon:
            self.PO.stop()

    # 上面鼠标移动窗口结束并鼠标离开窗口时执行下面函数
    def leaveEvent(self, evt):
        if self.anchorHasClicked:
            return
        cx, cy = (
            QCursor.pos().x(),
            QCursor.pos().y(),
        )  # QCursor.pos()效果等同于event.globalPos()
        if (
            cx >= self.x()
            and cx <= self.x() + self.width()
            and cy >= self.y()
            and cy <= self.geometry().y()
        ):
            return  # title bar
        elif self.x() < 0 and QCursor.pos().x() > 0:
            self.move(self.xleave - self.width(), self.y())
        elif self.y() < 0 and QCursor.pos().y() > 0:
            self.move(
                self.x(), self.yleave - self.height() + self.y() - self.geometry().y()
            )
        # 只要鼠标离开窗口就开始扫描识别
        if not self.PO.runCon and not self.anchorHasClicked:
            self.PO.runCon = True
            self.PO.start()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.isMinimized():
            self.tray.showMessage("通知", "已最小化到托盘，点击开始截图")
            self.tray.show()
            self.hide()


# if __name__ == "__main__":
#     app = QApplication(argv)
#     width = QGuiApplication.primaryScreen().availableGeometry().screenGeometry().width()
#     height = QGuiApplication.primaryScreen().availableGeometry().screenGeometry().height()
#     window = Main()
#     window.show()
#     exit(app.exec())
