from PIL import Image
from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel
from PySide6 import QtGui
import time

import cv2

from myutils.image_convert import cv2pixmap


class ImageLabel(QLabel):
    mousePressSignal = Signal(int, int)
    mouseDragSignal = Signal(int, int, int, int, int)

    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

    def setImagePath(self, imagePath):
        self.imagePath = imagePath

    def showImage(self):
        sp = QPixmap(self.imagePath)
        self.clear()
        self.setPixmap(sp)

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.pressX = ev.x()
        self.pressY = ev.y()
        self.currentTime = time.perf_counter()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        if self.pressX == ev.x() and self.pressY == ev.y():
            # 按下和松开是一个地方，点击事件
            self.mousePressSignal.emit(ev.x(), ev.y())
        else:
            # 按下和松开不是一个地方，拖拽事件
            clock = time.perf_counter()
            time_diff = int((clock - self.currentTime)*1000)  # 毫秒计时
            self.mouseDragSignal.emit(
                self.pressX, self.pressY, ev.x(), ev.y(), time_diff)

    def update_frame(self, img):
        frame = cv2.imread(img)
        if self.height() > self.width():
            width = self.width()
            height = int(frame.shape[0] * (width / frame.shape[1]))
        else:
            height = self.height()
            width = int(frame.shape[1] * (height / frame.shape[0]))
        frame = cv2.resize(frame, (width, height))
        self.setPixmap(cv2pixmap(frame))
