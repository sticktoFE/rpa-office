from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor,QFont,QGuiApplication,QCursor
class TipsShower(QLabel):
    def __init__(self, text, targetarea=(0, 0, 0, 0), parent=None, fontsize=60, timeout=1000):
        super().__init__(parent)
        self.parent = parent
        self.area = targetarea
        self.timeout = timeout
        self.rfont = QFont('微软雅黑', fontsize)
        self.setFont(self.rfont)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)
        self.setText(text)
        self.show()
        self.setStyleSheet("color:red;background-color:rgb(200,200,100);")
        
    def setText(self, text, autoclose=True, font: QFont = None, color: QColor = None) -> None:
        super(TipsShower, self).setText(text)
        self.adjustSize()
        x, y, w, h = self.area
        if x < QGuiApplication.primaryScreen().availableGeometry().width() - x - w:
            self.move(x + w + 5, y)
        else:
            self.move(x - self.width() - 5, y)
        # print(self.parent.x(),self.parent.y())
        # self.move(self.parent.pos().x(),self.parent.pos().y())
        # 也可以把提示信息放在鼠标附近
        # self.move(QCursor.pos().x(),QCursor.pos().y())
        self.show()
        if autoclose:
            self.timer.start(self.timeout)
        if font is not None:
            self.setFont(font)
        if color is not None:
            self.setStyleSheet(f"color:{color.name()}")

    def hide(self) -> None:
        super(TipsShower, self).hide()
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