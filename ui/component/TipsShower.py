from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QFont, QGuiApplication, QCursor


class TipsShower(QLabel):
    def __init__(
        self, text, targetarea=(0, 0, 50, 30), parent=None, fontsize=18, timeout=1000
    ):
        super().__init__(parent)
        self.parent = parent
        self.area = targetarea
        self.timeout = timeout
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.setWordWrap(True)  # 启用自动换行
        # 设置大小区域 (x, y, width, height)
        self.setGeometry(*self.area)
        self.setText(
            text,
            stylesheet=f"background-color:rgb(200,200,100);font: {fontsize}pt;color:red;font-family: '微软雅黑';",
        )
        self.show()

    def setText(
        self,
        text,
        stylesheet=None,
        pos=None,
        autoclose=True,
    ) -> None:
        super(TipsShower, self).setText(text)
        self.adjustSize()
        if pos is not None:
            # if x < QGuiApplication.primaryScreen().availableGeometry().width() - x - w:
            #     self.move(x + w + 5, y)
            # else:
            # 设置大小区域 (x, y, width, height)
            self.move(*pos)
        if autoclose:
            self.timer.start(self.timeout)
        if stylesheet is not None:
            self.setStyleSheet(stylesheet)
        self.show()

    def hide(self) -> None:
        super().hide()
        self.timer.stop()
        # self.setFont(self.rfont)
        # self.setStyleSheet("color:red")

    def textAreaChanged(self, minsize=0):
        self.document.adjustSize()
        newWidth = self.document.size().width() + 25
        newHeight = self.document.size().height() + 15
        if newWidth != self.width():
            if newWidth < minsize:
                self.setFixedWidth(minsize)
            else:
                self.setFixedWidth(newWidth)
        if newHeight != self.height():
            if newHeight < minsize:
                self.setFixedHeight(minsize)
            else:
                self.setFixedHeight(newHeight)
