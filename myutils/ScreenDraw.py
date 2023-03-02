from PySide6.QtGui import QKeySequence, QPen, QPainter, QPixmap, QColor, QShortcut
from PySide6.QtWidgets import QLabel, QMessageBox
from PySide6.QtCore import QRect, Qt, Signal


class Bbox(object):
    def __init__(self):
        self._x1, self._y1 = 0, 0
        self._x2, self._y2 = 0, 0

    @property
    def point1(self):
        return self._x1, self._y1

    @point1.setter
    def point1(self, position: tuple):
        self._x1 = position[0]
        self._y1 = position[1]

    @property
    def point2(self):
        return self._x2, self._y2

    @point2.setter
    def point2(self, position: tuple):
        self._empty = False
        self._x2 = position[0]
        self._y2 = position[1]

    @property
    def bbox(self):
        if self._x1 < self._x2:
            x_min, x_max = self._x1, self._x2
        else:
            x_min, x_max = self._x2, self._x1

        if self._y1 < self._y2:
            y_min, y_max = self._y1, self._y2
        else:
            y_min, y_max = self._y2, self._y1
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def __str__(self):
        return str(self.bbox)


class ScreenDraw(QLabel):
    signal = Signal(tuple)

    def __init__(self, width, height):
        super().__init__()
        self._press_flag = False
        self._pen = QPen(Qt.white, 2, Qt.DashLine)
        self._painter = QPainter()
        self._bbox = Bbox()
        self._pixmap = QPixmap(width, height)
        self._pixmap.fill(QColor(255, 255, 255))
        self.setPixmap(self._pixmap)
        self.setWindowOpacity(0.4)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置背景颜色为透明
        QShortcut(QKeySequence("esc"), self, self.escevent)

    def escevent(self):
        self.close()
        self.signal.emit(('esc', 'esc'))

    def _draw_bbox(self):
        pixmap = self._pixmap.copy()
        self._painter.begin(pixmap)
        self._painter.setPen(self._pen)  # 设置pen必须在begin后
        rect = QRect(*self._bbox.bbox)
        self._painter.fillRect(rect, Qt.SolidPattern)  # 区域不透明
        self._painter.drawRect(rect)  # 绘制虚线框
        self._painter.end()
        self.setPixmap(pixmap)
        self.update()
        self.showFullScreen()
        # print(rect)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            # print("鼠标左键：", [QMouseEvent.x(), QMouseEvent.y()])
            self._press_flag = True
            self._bbox.point1 = [QMouseEvent.x(), QMouseEvent.y()]

    def mouseMoveEvent(self, QMouseEvent):
        if self._press_flag:
            # print("鼠标移动：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._draw_bbox()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton and self._press_flag:
            # print("鼠标释放：", [QMouseEvent.x(), QMouseEvent.y()])
            self._bbox.point2 = [QMouseEvent.x(), QMouseEvent.y()]
            self._press_flag = False
            reply = QMessageBox.Yes
            # 本想着可以在画方框时可以调整方框大小，即微调，后面需要再实现这部分功能
            # QMessageBox.question(
            #     self,
            #     "退出提示",
            #     "<font color=gray>是否需要调整区域？</font>",
            #     QMessageBox.Yes | QMessageBox.No,
            #     QMessageBox.No,
            # )
            if reply == QMessageBox.Yes:
                self.signal.emit(self._bbox.bbox)
