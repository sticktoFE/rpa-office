from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMovie, QPainter
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class GifSplashScreen(QWidget):
    play_signal = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        )  # 保持界面在最上层且无边框（去掉窗口标题）
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 设置透明度
        self.setWindowOpacity(0.8)
        # 设置背景色为淡蓝色
        self.setStyleSheet("background-color: rgb(55, 135, 215);")
        self.main_lot = QVBoxLayout(self)  # 垂直布局，主布局
        self.main_lot.setContentsMargins(0, 0, 0, 0)
        self.backgroud_movie_zoomout_x = 0  # 背景动画x方向缩小像素
        self.backgroud_movie_zoomout_y = 0  # 背景动画y方向缩小像素
        self.movie = QMovie()
        # self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(200)
        self.movie.frameChanged.connect(self.repaint)
        self.movie.frameChanged.connect(self.stopmovie)

    def setMovie(self, gif_path, info, gifAinfolayout, inwidget=None, play_once=False):
        # 背景的的长宽缩放 正值表示缩小
        self.backgroud_movie_zoomout_x = 0
        self.backgroud_movie_zoomout_y = 0
        self.play_once = play_once
        if self.movie.state() == QMovie.Running:
            self.movie.stop()
        self.movie.setFileName(gif_path)
        if self.main_lot is not None:
            self.deleteItemsOfLayout(self.main_lot)
        if info:
            # 默认文字显示位置居中
            self.infolabel = QLabel()
            self.infolabel.setText(info)
            self.infolabel.setAlignment(Qt.AlignCenter)
            self.infolabel.setScaledContents(True)
            if gifAinfolayout == "v":  # 文字靠下
                self.spacelabel = QLabel()
                # self.backgroundlabel.setScaledContents(True)
                # self.backgroundlabel.setMovie(self.movie)
                # self.backgroundlabel.resize(480,480)
                # border:2px solid rgb(0, 255, 0);
                # self.backgroundlabel.setStyleSheet("QLabel{background-color:transparent;border:6px solid rgb(0, 255, 0);}")
                self.main_lot.addWidget(self.spacelabel)
                self.main_lot.addStretch(30)
                self.main_lot.addWidget(self.infolabel)
                self.main_lot.setStretch(0, 9)
                self.main_lot.setStretch(1, 1)
                self.backgroud_movie_zoomout_x = 20
                self.backgroud_movie_zoomout_y = 30
            else:
                self.main_lot.addWidget(self.infolabel)
        elif inwidget is not None:
            self.main_lot.addWidget(inwidget)
        self.movie.start()

    def paintEvent(self, event):
        display_rect = self.rect()
        display_rect.setWidth(display_rect.width() - self.backgroud_movie_zoomout_x)
        display_rect.setHeight(display_rect.height() - self.backgroud_movie_zoomout_y)
        currentPM = self.movie.currentPixmap()
        # 反锯齿
        currentPM = currentPM.scaled(
            display_rect.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation
        )
        currentPMRect = currentPM.rect()
        if currentPMRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.setRenderHints(
                QPainter.SmoothPixmapTransform | QPainter.Antialiasing
            )  # 消锯齿
            painter.translate(
                self.backgroud_movie_zoomout_x / 2, 0
            )  # x方向如果缩小，即往左边减少10，开始画图x方向位置为 10/2 = 5
            painter.drawPixmap(display_rect, currentPM)
            painter.end()
        event.accept()
        # 下面可以把gif动态图拆出来
        # self.movie.currentPixmap().save(f"ui/icon/123/{self.movie.currentFrameNumber()}.jpg","Q_NULLPTR",quality=100)

    def stopmovie(self, frameNumber):
        if self.play_once and frameNumber == self.movie.frameCount() - 1:
            self.play_signal.emit()
            self.movie.stop()

    # 迭代删除xlayout中删除布局中的widget内容
    # 光删layout，里面的widget其实还存在，只是没布局了
    def deleteItemsOfLayout(self, xlayout):
        if xlayout is not None and (
            type(xlayout) is QVBoxLayout or type(xlayout) is QHBoxLayout
        ):
            while xlayout.count():
                item = xlayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    # widget.deleteLater()
                    widget.setParent(None)
                else:
                    del item

    # 删除xlayout中的类型如QVBoxLayout类型的box

    def boxdelete(self, xlayout, toDeleteLayout):
        for i in range(xlayout.count()):
            layout_item = xlayout.itemAt(i)
            if type(layout_item.layout()) is toDeleteLayout:
                self.deleteItemsOfLayout(layout_item.layout())
                xlayout.removeItem(layout_item)
                break

    def stopMovieSetPath(self, gif_path):
        self.movie.stop()
        self.backgroundlabel.setStyleSheet(f"border-image:{gif_path}")
        if not gif_path:
            self.backgroundlabel.hide()


# if __name__ == '__main__':
#     pass
