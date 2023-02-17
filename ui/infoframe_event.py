from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from ui.infoframe import Ui_InfoWidget


# import requests
class InfoFrame(QWidget, Ui_InfoWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.adjustSize()
        self.setWindowFlags(self.windowFlags()
                            | Qt.FramelessWindowHint)  # 没有窗口栏
        # 窗口无边框后，周边增加一层阴影，以和周边环境做区分
        shadow_effect = QGraphicsDropShadowEffect(self
                                                  # self, blurRadius=9.0, color=QColor(116, 116, 116), offset=QPointF(0, 0)
                                                  )
        shadow_effect.setOffset(0, 0)  # 偏移
        shadow_effect.setColor(QColor(116, 116, 116))  # 阴影颜色 Qt.gray
        shadow_effect.setBlurRadius(8)  # 阴影半径
        self.label_3.setGraphicsEffect(shadow_effect)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        # self.label_3.resize(self.scrollAreaWidgetContents.size())
        # /* 让横向滚动条高度为0，实际上隐藏了滚动条 */
        # self.scrollArea.horizontalScrollBar().setStyleSheet("""
        #             height:0px;
        # """)
        # self.scrollArea.verticalScrollBar().setStyleSheet("""
        #          QScrollBar {
        #             width:0px;
        #             }

        # """)
        # self.verticalLayout.addStretch(1)
        # self.scrollAreaWidgetContents.setMinimumSize(380, 1000)
        self.scrollArea.installEventFilter(self)
        self.last_time_move = 0

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if self.last_time_move == 0:
                self.last_time_move = event.position().x()
            distance = self.last_time_move - event.position().x()
            # self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + distance)
            self.scrollArea.horizontalScrollBar().setValue(
                self.scrollArea.horizontalScrollBar().value() + distance)
            self.last_time_move = event.position().x()

        elif event.type() == QEvent.MouseButtonRelease:
            self.last_time_move = 0
        return QWidget.eventFilter(self, source, event)
