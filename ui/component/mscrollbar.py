from PySide6.QtCore import QAbstractAnimation, QEvent, QSize, QVariantAnimation, Qt
from PySide6.QtWidgets import  QScrollBar

    # //varAnima: 变量动画
    # //preferWidth: 临时记录动态的滚动条宽度
    # //maxWidth: 滚动条最大宽度
class AnimatedScrollBar(QScrollBar):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.maxWidth = 20
        self.varAnima =  QVariantAnimation(self); #创建动画
        self.varAnima.setDuration(100)
        self.varAnima.valueChanged.connect(self.noticeValueChange)
        self.nowheel = False
    def setDisabledWheel(self,nowheel=True):
        self.nowheel = nowheel
    def noticeValueChange(self,val):
         # //valueChanged时，动画不一定在运行,需要约束
        if self.varAnima.state() == QAbstractAnimation.Running :
            self.preferWidth = val
            # //通知变化
            self.updateGeometry()
# 要实现布局的动态调整，需要在手动更新sizeHint后通知布局。
# Qt提供了QWidget::updateGeometry()来通知布局，该接口会触发QEvent::LayoutRequest，之后布局会重新调用QWidget::sizeHint()。
    def sizeHint(self) :
        # //样式指定的宽度值，可以通过默认的sizeHint获取
        tmp = super().sizeHint()
        if self.orientation() == Qt.Horizontal:
            # //仅改变宽度,实际由于布局的存在，长度值并不重要
            return QSize(tmp.width(), self.preferWidth)
        return QSize(self.preferWidth, tmp.height())
    def event(self,e):
        if e.type() == QEvent.Polish:
            # //初始化preferWidth，也可以在第一次sizeHint()被调用时初始化
            tmp = super().sizeHint()
            self.preferWidth = tmp.height() if self.orientation() == Qt.Horizontal else tmp.width()
        elif e.type() == QEvent.HoverEnter:
            if self.varAnima.state() == QAbstractAnimation.Running:
                self.varAnima.stop()
            self.varAnima.setStartValue(self.preferWidth)
            self.varAnima.setEndValue(self.maxWidth)
            self.varAnima.start()
        elif e.type() == QEvent.HoverLeave:
            if self.varAnima.state() == QAbstractAnimation.Running:
                self.varAnima.stop()
            tmp = super().sizeHint()
            normalWidth = tmp.height() if self.orientation() == Qt.Horizontal else tmp.width()
            self.varAnima.setStartValue(self.preferWidth)
            self.varAnima.setEndValue(normalWidth)
            self.varAnima.start()
        elif e.type() == QEvent.Wheel and self.nowheel:
            return True
        return super().event(e)
