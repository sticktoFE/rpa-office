#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QListWidget
from ui.manage_config import Ui_ManagerConfig


class ManagerConfig(QWidget, Ui_ManagerConfig):
    close_signal = Signal()

    def __init__(self, *args, **kwargs):
        super(ManagerConfig, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 保持界面在最上层且无边框（去掉窗口标题） |Qt.FramelessWindowHint
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.adjustSize()
        self.setWindowTitle("配置OCR参数")
        self.initUi()

    def initUi(self):
        # 初始化界面
        # 通过QListWidget的当前item变化来切换QStackedWidget中的序号
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.Shape.NoFrame)
        # 隐藏滚动条
        self.listWidget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.listWidget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # 这里就用一般的文本配合图标模式了(也可以直接用Icon模式,setViewMode)
        # self.listWidget.itemClicked.connect(self.onItemClicked)
        self.listWidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

        # self.Option = Option()
        # self.stackedWidget.addWidget(self.Option)

    # def donothing(self, int):
    #     print(int)
    #     pass
    # def onItemClicked(self, item):
    #     # print('Clicked', item.text(), self.listWidget.row(item))
    #     self.stackedWidget.setCurrentIndex(self.listWidget.row(item))
    def closeEvent(self, event):
        self.close_signal.emit()


# if __name__ == '__main__':
#     import sys
#     from PySide6.QtWidgets import QApplication
#     app = QApplication(sys.argv)
#     # app.setStyleSheet(Stylesheet)
#     w = ManagerConfig()
#     w.show()
#     sys.exit(app.exec())
