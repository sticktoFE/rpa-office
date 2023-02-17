

from PySide6.QtCore import Qt, QStandardPaths
from PySide6.QtGui import QGuiApplication
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QApplication, QLabel, QFileDialog, QMenu

# 固定截图区在原来位置，方便原滋原味检视
class Freezer(QLabel):
    def __init__(self, parent=None, img=None, x=0, y=0, listpot=0):
        super().__init__()
        self.imgpix = img
        self.listpot = listpot
        self.setPixmap(self.imgpix)
        self.settingOpacity = False
        self.setWindowOpacity(0.95)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.drawRect = True
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setGeometry(x, y, self.imgpix.width(), self.imgpix.height())
        self.show()
        self.drag = self.resize_the_window = False
        self.on_top = True
        self.p_x = self.p_y = 0
        self.setToolTip("Ctrl+滚轮可以调节透明度")
        # self.setMaximumSize(QGuiApplication.primaryScreen().availableGeometry().size())

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quitAction = menu.addAction("退出")
        copyaction = menu.addAction('复制')
        saveaction = menu.addAction('另存为')
        topaction = menu.addAction('(取消)置顶')
        rectaction = menu.addAction('(取消)边框')
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            self.clear()
        elif action == saveaction:
            img = self.imgpix
            path, l = QFileDialog.getSaveFileName(self, "另存为", QStandardPaths.writableLocation(
                QStandardPaths.PicturesLocation), "png Files (*.png);;"
                                                  "jpg file(*.jpg);;jpeg file(*.JPEG);; bmp file(*.BMP );;ico file(*.ICO);;"
                                                  ";;all files(*.*)")
            if path:
                img.save(path)
        elif action == copyaction:
            clipboard = QApplication.clipboard()
            try:
                clipboard.setPixmap(self.imgpix)
            except Exception:
                print('复制失败')
        elif action == topaction:
            if self.on_top:
                self.on_top = False
                self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
                self.setWindowFlag(Qt.Tool, False)
                self.show()
            else:
                self.on_top = True
                self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
                self.setWindowFlag(Qt.Tool, True)
                self.show()
        elif action == rectaction:
            self.drawRect = not self.drawRect
            self.update()

    def wheelEvent(self, e):
        if not self.isVisible():
            return
        angleDelta = e.angleDelta() / 8
        dy = angleDelta.y()
        if self.settingOpacity:
            if dy > 0:
                if self.windowOpacity() <= 1 - 0.1:
                    self.setWindowOpacity(self.windowOpacity() + 0.1)
                else:
                    self.setWindowOpacity(1)
            elif dy < 0 and self.windowOpacity() >= 0.21000000000000002:
                self.setWindowOpacity(self.windowOpacity() - 0.1)
        elif 2 * QGuiApplication.primaryScreen().availableGeometry().width() >= self.width() >= 50:
            self._extracted_from_wheelEvent_15(dy, e)
        self.update()

    # TODO Rename this here and in `wheelEvent`
    def _extracted_from_wheelEvent_15(self, dy, e):
        w = self.width() + dy * 5
        w = max(w, 50)
        if w > 2 * QGuiApplication.primaryScreen().availableGeometry().width():
            w = 2 * QGuiApplication.primaryScreen().availableGeometry().width()
        scale = self.imgpix.height() / self.imgpix.width()
        h = w * scale
        s = self.width() / w
        mdx = e.x() * s - e.x()
        mdy = e.y() * s - e.y()
        self.setPixmap(self.imgpix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.setGeometry(self.x() + mdx, self.y() + mdy, w, h)
        QApplication.processEvents()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.x() > self.width() - 20 and event.y() > self.height() - 20:
                self.resize_the_window = True
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.SizeAllCursor)
                self.drag = True
                self.p_x, self.p_y = event.x(), event.y()
            # self.resize(self.width()/2,self.height()/2)
            # self.setPixmap(self.pixmap().scaled(self.pixmap().width()/2,self.pixmap().height()/2))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)
            self.drag = self.resize_the_window = False

    def mouseMoveEvent(self, event):
        if self.isVisible():

            if self.drag:
                self.move(event.x() + self.x() - self.p_x, event.y() + self.y() - self.p_y)
            elif self.resize_the_window:
                if event.x() > 10 and event.y() > 10:
                    w = event.x()
                    scale = self.imgpix.height() / self.imgpix.width()
                    h = w * scale
                    self.resize(w, h)
                    self.setPixmap(self.imgpix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            elif event.x() > self.width() - 20 and event.y() > self.height() - 20:
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.clear()
        elif e.key() == Qt.Key_Control:
            self.settingOpacity = True

    def keyReleaseEvent(self, e) -> None:
        if e.key() == Qt.Key_Control:
            self.settingOpacity = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.drawRect:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.green, 1, Qt.SolidLine))
            painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
            painter.end()

    def clear(self):
        self.clearMask()
        self.hide()
        del self.imgpix
        super().clear()
        # jamtools.freeze_imgs[self.listpot] = None

    def closeEvent(self, e):
        self.clear()
        e.ignore()
