
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtWidgets import QLabel


class MaskLayer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.parent.on_init:
            print('oninit return')
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 正常显示选区
        rect = QRect(min(self.parent.x0, self.parent.x1), min(self.parent.y0, self.parent.y1),abs(self.parent.x1 - self.parent.x0), abs(self.parent.y1 - self.parent.y0))
        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        painter.drawRect(rect)
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setPen(QPen(QColor(0, 150, 0), 8, Qt.SolidLine))
        painter.drawPoint(QPoint(self.parent.x0, min(self.parent.y1, self.parent.y0) + abs(self.parent.y1 - self.parent.y0) // 2))
        painter.drawPoint(QPoint(min(self.parent.x1, self.parent.x0) + abs(self.parent.x1 - self.parent.x0) // 2, self.parent.y0))
        painter.drawPoint(QPoint(self.parent.x1, min(self.parent.y1, self.parent.y0) + abs(self.parent.y1 - self.parent.y0) // 2))
        painter.drawPoint(QPoint(min(self.parent.x1, self.parent.x0) + abs(self.parent.x1 - self.parent.x0) // 2, self.parent.y1))
        painter.drawPoint(QPoint(self.parent.x0, self.parent.y0))
        painter.drawPoint(QPoint(self.parent.x0, self.parent.y1))
        painter.drawPoint(QPoint(self.parent.x1, self.parent.y0))
        painter.drawPoint(QPoint(self.parent.x1, self.parent.y1))
        x = y = 100
        if self.parent.x1 > self.parent.x0:
            x = self.parent.x0 + 5
        else:
            x = self.parent.x0 - 72
        if self.parent.y1 > self.parent.y0:
            y = self.parent.y0 + 15
        else:
            y = self.parent.y0 - 5
        painter.setPen(QPen(Qt.darkRed, 2, Qt.SolidLine))
        painter.drawText(x, y,f'{abs(self.parent.x1 - self.parent.x0)}x{abs(self.parent.y1 - self.parent.y0)}')
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 120))
        painter.drawRect(0, 0, self.width(), min(self.parent.y1, self.parent.y0))
        painter.drawRect(0, min(self.parent.y1, self.parent.y0), min(self.parent.x1, self.parent.x0),self.height() - min(self.parent.y1, self.parent.y0))
        painter.drawRect(max(self.parent.x1, self.parent.x0), min(self.parent.y1, self.parent.y0),self.width() - max(self.parent.x1, self.parent.x0),self.height() - min(self.parent.y1, self.parent.y0))
        painter.drawRect(min(self.parent.x1, self.parent.x0), max(self.parent.y1, self.parent.y0),max(self.parent.x1, self.parent.x0) - min(self.parent.x1, self.parent.x0),self.height() - max(self.parent.y1, self.parent.y0))
        # 以下为鼠标放大镜
        painter.setPen(QPen(QColor(Qt.red), 2, Qt.SolidLine))
        if self.parent.mouse_posx > self.width() - 140:
            enlarge_box_x = self.parent.mouse_posx - 140
        else:
            enlarge_box_x = self.parent.mouse_posx + 20
        if self.parent.mouse_posy > self.height() - 140:
            enlarge_box_y = self.parent.mouse_posy - 120
        else:
            enlarge_box_y = self.parent.mouse_posy + 20
        enlarge_rect = QRect(enlarge_box_x, enlarge_box_y, 120, 120)
        painter.drawRect(enlarge_rect)
        painter.drawText(enlarge_box_x, enlarge_box_y - 8,f'({self.parent.mouse_posx}x{self.parent.mouse_posy})')
        try:
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            rpix = QPixmap(self.width() + 120, self.height() + 120)
            rpix.fill(QColor(0, 0, 0))
            rpixpainter = QPainter(rpix)
            rpixpainter.drawPixmap(60, 60, self.parent.pixmap())
            rpixpainter.end()
            larger_pix = rpix.copy(self.parent.mouse_posx, self.parent.mouse_posy, 120, 120).scaled(120 + self.parent.tool_width * 10, 120 + self.parent.tool_width * 10)
            pix = larger_pix.copy(larger_pix.width() // 2 - 60, larger_pix.height() // 2 - 60, 120, 120)
            painter.drawPixmap(enlarge_box_x, enlarge_box_y, pix)
            painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
            painter.drawLine(enlarge_box_x, enlarge_box_y + 60, enlarge_box_x + 120, enlarge_box_y + 60)
            painter.drawLine(enlarge_box_x + 60, enlarge_box_y, enlarge_box_x + 60, enlarge_box_y + 120)
        except Exception:
            print('draw_enlarge_box fail')
        painter.end()
