from random import choice, randint
import string
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import QMenu, QSystemTrayIcon


class MSystemTray(QSystemTrayIcon):
    def __init__(self, parent, iconpath):
        super().__init__(QIcon(iconpath), parent)
        self.ui = parent
        self.init()

    def init(self):
        # 托盘行为
        self.action_quit = QAction(
            self.get_icon(), "退出", self, triggered=self.quit)
        self.action_show = QAction(
            self.get_icon(), "主窗口", self, triggered=self.show_window)
        self.menu_tray = QMenu()
        self.menu_tray.addAction(self.action_quit)
        # 增加分割线
        self.menu_tray.addSeparator()
        self.menu_tray.addAction(self.action_show)

        # self.tray.activated.connect(self.freeShot)  # 设置托盘点击事件处理函数
        self.setContextMenu(self.menu_tray)
        self.setToolTip("我是内控机器人")
        # 把鼠标点击图标的信号和槽连接
        self.activated.connect(self.onIconClicked)
        # 快捷键

    def get_icon(self):
        # 测试模拟图标
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(QFont('思源字体', 11))
        painter.setPen(Qt.GlobalColor(randint(4, 18)))
        painter.drawText(0, 0, 16, 16, Qt.AlignCenter,choice(string.ascii_letters))
        painter.end()
        return QIcon(pixmap)

    def quit(self):
        self.ui.close()
        QtWidgets.QApplication.quit()

    def show_window(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        # self.ui.showNormal()
        # self.ui.activateWindow()
        self.ui.show()
    # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击

    def onIconClicked(self, reason):
        if reason == 3:
            # self.showMessage("Message", "skr at here")
            if not self.ui.isVisible():  # self.ui.isMinimized() or
                # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
                # self.ui.showNormal()
                # self.ui.activateWindow()
                self.ui.show()
            else:
                # 若不是最小化，则最小化
                # self.ui.showMinimized()
                # self.ui.setWindowFlags(Qt.SplashScreen)
                self.ui.hide()
