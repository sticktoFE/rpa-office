from functools import partial
from random import choice, randint
import string
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QFont, QIcon, QPainter, QPixmap, QCursor
from PySide6.QtWidgets import QMenu

import ui.pic_rc


class MMenu(QMenu):
    show_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.init_menu()

    def show(self):
        self.popup(QCursor.pos())
        super().show()

    def init_menu(self):
        # 背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.addAction(
            QIcon(f":icon/0{randint(1,8)}.ico"),
            "选项",
            partial(self.show_signal.emit, "self.managerConfig()"),
        )
        self.addSeparator()
        # self.addAction(QIcon(f":icon/0{randint(1,8)}.ico"), '范围抽取文本',partial(self.show_signal.emit,"self.drawExtract()"))
        # self.addSeparator()
        self.addAction(
            QIcon(f":icon/0{randint(1,8)}.ico"),
            "截图识别信息",
            partial(self.show_signal.emit, "self.screen_shot_info()"),
        )
        self.addSeparator()
        self.addAction(
            QIcon(f":icon/0{randint(1,8)}.ico"), "信息综合获取", self.displayInfoFetch
        )
        self.addSeparator()
        self.addAction(
            self.get_icon(), "暂停扫描", partial(self.show_signal.emit, "self.pauseScan()")
        )
        self.addSeparator()
        self.addAction(
            self.get_icon(), "关闭", partial(self.show_signal.emit, "self.close()")
        )

    def get_icon(self):
        # 测试模拟图标
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setFont(QFont("思源字体", 11))
        painter.setPen(Qt.GlobalColor(randint(4, 18)))
        painter.drawText(
            QRect(0, 0, 16, 16),
            Qt.AlignCenter,  # type: ignore
            choice(string.ascii_letters),
        )
        painter.end()
        return QIcon(pixmap)

    def displayInfoFetch(self):
        from ui.OCRResult_event import TotalMessage

        self.ocrmg = TotalMessage()
        rect = self.frameGeometry().getRect()
        self.ocrmg.move(rect[0] + rect[2], rect[1])
        self.ocrmg.show()
