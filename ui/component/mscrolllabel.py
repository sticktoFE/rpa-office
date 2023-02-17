from functools import partial
from PySide6.QtCore import Qt, QTimer,Signal
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import QLabel

class ScrollLabel(QLabel):
    ready_signal = Signal(str,str)
    def __init__(self, parent):
        super().__init__(parent)
        self.list = []
        # 跑马灯切换间隔计时器
        self.pTimer = QTimer()
        self.pTimer.timeout.connect(self.display)
        self.autoScroll = False
        # 有一个潜在的flow_id
        self.linkActivated.connect(partial(self.onLinkActivated))
    def clearlist(self):
        # self.clear()
        self.pTimer.stop()

    def addList(self, rowlist: dict):
        self.rowlist = rowlist
        self.clear()
        if not rowlist:
            return
        innerHtmlTitle = f"<p><a href='' style='color:white;text-decoration:none;'>当前页面：{rowlist['page_name']}</a></p>"
        fontWidth = QFontMetrics(super().font())
        self.innerHtml = [
            f"""< p > <a href = '{str(item[0])}' style = 'color:white;text-decoration:none;' > {i}、{fontWidth.elidedText(str(item[1]), Qt.ElideRight, 300)} < /a > </p > """ for i, item in enumerate(rowlist["flows"])]
        self.setText(innerHtmlTitle+"".join(self.innerHtml))
        # 定时3000毫秒
        if self.autoScroll:
            self.nn = 1
            self.pTimer.start(1000)
    # 注意，connect过来时，潜在的参数总是最后一位，此处linkActivated潜在的入参为flow_id
    def onLinkActivated(self,flow_id):
        self.ready_signal.emit(self.rowlist["page_id"],flow_id)
    def enterEvent(self, event):
        if self.autoScroll:
            self.pTimer.stop()
            event.accept()

    def leaveEvent(self, event):
        if self.autoScroll:
            self.pTimer.start(1000)
            event.accept()
    # 按一定时间取列表中的5位，但跑马灯效果不好

    def display(self):
        if not self.list:
            self.setText("该页面未配置显示内容")
            return
        if self.nn <= len(self.list):
            if self.nn <= 4:
                self.setText("".join(self.innerHtml[: self.nn]))
                self.setAlignment(Qt.AlignBottom)
            else:
                self.setText("".join(self.innerHtml[self.nn-4: self.nn]))
                self.setAlignment(Qt.AlignTop)
            self.nn = self.nn+1
        else:
            # self.setText("".join(self.innerHtml[0]))
            self.nn = 1
    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #     # //先调用父类的paintEvent为了显示'背景'!!!
    #     super().paintEvent(a0)
    #     painter =QPainter(self);
    #     painter.setPen(QPen(Qt.red,2));
    #     painter.drawRect(QRect(x,y,w,h));
    #     #画线条
    #     painter.drawLine(QPoint,QPoint);
    #     return
