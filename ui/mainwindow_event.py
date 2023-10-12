from functools import partial
from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtWidgets import QMainWindow
from myutils import globalvar
from biz.monitor_work_flow.OCRAndCompare import OCRAndCompare
from .mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.adjustSize()
        self.setupUi(self)
        # 这一行就是来设置窗口始终在顶端的。
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint
        )  # 保持界面在最上层且无边框（去掉窗口标题）
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 为窗口安装事件过滤器，所有事件在eventFilter里面统一处理
        # self.installEventFilter(self)
        self.anchorHasClicked = False
        # 控制靠边隐藏的参数
        self.xleave = 30  # 越大隐藏后显示的边越突出
        self.yleave = 25
        self.ready = False
        self.readyNum = 0
        self.sayHello()

    # 初始化后台对象
    def init_all_object(self, progress_signal):
        # 后台自动识别全屏并作规则识别提醒服务
        self.PO = OCRAndCompare(
            box=(
                0,
                0,
                globalvar.get_var("SCREEN_WIDTH"),
                globalvar.get_var("SCREEN_HEIGHT"),
            )
        )
        progress_signal.emit(100 * 1 / 2)
        self.PO.start()
        self.PO.signal.connect(self.displayInfo)
        progress_signal.emit(100 * 2 / 2)

    # 初始化窗口
    def init_all_gui(self):
        # 启动定时器检测记事本的位置大小和是否关闭
        self.leaveTimer = QTimer(self)
        # QTimer里面确实没有timeout
        self.leaveTimer.timeout.connect(partial(self.hide_auto_notice))
        self.leaveTimer.setSingleShot(True)  # **重要** 保证只执行一次计时
        # 初始化信息展示窗口（列表）
        from ui.infoframe_event import InfoFrame

        self.infoFrame = InfoFrame()
        self.infoFrame.label_3.ready_signal.connect(self.anchorClicked)
        self.infoFrame.resize(self.GSS.size())
        # 初始化信息展示窗口（详情）
        from biz.monitor_work_flow.ui.flow_remind_retail import FlowRemindRetail

        self.retail_info_window = FlowRemindRetail()
        self.retail_info_window.close_signal.connect(self.anchorClickedClose)

    def sayHello(self):
        self.GSS.setMovie("ui/icon/hello.gif", None, None, play_once=True)
        self.GSS.play_signal.connect(self.sayWelcome)
        # 直接在上面控制只轮播一次不成熟，还用下面的
        # self.canhello = GifPlay(gifplaywidget=self.GSS)
        # self.canhello.start()
        # self.canhello.signal.connect(self.sayWelcome)

    def sayWelcome(self):
        myString = """
                    <p>
                        &nbsp;欢迎使用
                    </p>
                    <p>
                        &nbsp;内控机器人
                    </p>
                    """
        self.GSS.setMovie("ui/icon/background.gif", myString, "f")
        QTimer.singleShot(1000, self.scanning)

    def scanning(self):
        myString = """
                    <p>
                        &nbsp;流程识别中
                    </p>
                    """
        self.GSS.setMovie("ui/icon/scanning12.gif", myString, "v")
        # 主线程发送准备好标识
        self.readyOcr()

    # 这是多个线程的汇合处，只有两个线程都准备好了，才会往下执行，是通过readyNum计数来识别是不是准备好了
    def readyOcr(self):
        self.readyNum = self.readyNum + 1
        if self.readyNum == 2:
            self.ready = True
            self.autoNotice = True
            self.hide_auto_notice()

    def displayInfo(self, result):
        if result["page_id"] == "NotExistsPageID":
            myString = """
                        <p>
                            &nbsp;流程识别中
                        </p>
                        """
            self.GSS.setMovie("ui/icon/scanning12.gif", myString, "v")
        else:
            self.infoFrame.label_3.addList(result)
            self.GSS.setMovie("ui/icon/background.gif", None, None, self.infoFrame)
            self.auto_notice()

    # 作为 Qlabel之linkActivated槽函数，在href中的字符串，传过来就是一个字符串，
    # 而且是作为最后一个参数传入的，下面即是flow_id，如果需要传多个入参，需要在上面的connect中传入
    def anchorClicked(self, page_id, flow_id):
        # self.retail_info_window.setWindowModality(Qt.ApplicationModal)
        rect = self.frameGeometry().getRect()
        self.retail_info_window.move(rect[0] + rect[2], rect[1])
        self.retail_info_window.displayData(flow_id, page_id)
        # 点击查看内容了，就不要再扫描了
        self.anchorHasClicked = True

    def anchorClickedClose(self):
        self.anchorHasClicked = False

    def enterEvent(self, a0: QEvent) -> None:
        # 鼠标放上去，暂停播放动画
        self.GSS.movie.setPaused(True)
        # 正在播放启动动画，不需要后面的操作
        if not self.ready:
            return

        # 手工还是自动触发窗口显示的表示
        self.autoNotice = False
        # 显示窗口
        self.showApp()
        # 停止扫描识别
        # self.PO.stop_signal.emit("")
        self.PO.pause()
        return super().enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:
        self.GSS.movie.setPaused(False)
        # 正在播放启动画面，即没有准备完毕，不要隐藏窗口，也不要开始工作
        if not self.ready:
            return
        # 打开详细界面看相关内容，不要隐藏主窗口
        if self.anchorHasClicked:
            return
        self.hideApp()
        # 离开重新启动识别
        # self.PO.start_signal.emit()
        self.PO.resume()
        return super().leaveEvent(a0)

    # 识别到内容，主动显示窗口并显示相应内容
    def auto_notice(self):
        # 1、打上识别成功通知的标识
        self.autoNotice = True
        self.showApp()
        # 2、停止扫描识别
        # self.PO.stop_signal.emit("0")
        self.PO.pause()
        # 3、显示后开启隐藏倒计时5s计时器
        if not self.leaveTimer.isActive():
            self.leaveTimer.start(5000)

    # 启动画面结束或者鼠标离开窗口时隐藏窗口
    def hide_auto_notice(self):
        # 非自动状态，即鼠标干预情况下，自动的行为无效
        if not self.autoNotice:
            return
        # 已经打开详情在浏览，就不要隐藏了
        if self.anchorHasClicked:
            return
        self.hideApp()
        # 离开重新启动识别
        # self.PO.start_signal.emit()
        self.PO.resume()
        # 关掉隐藏计时器
        if self.leaveTimer.isActive():
            self.leaveTimer.stop()

    def showApp(self):
        self.activateWindow()
        if self.x() == self.xleave - self.width():
            self.move(-self.xleave, self.y())
        elif self.y() == self.yleave - self.height() + self.y() - self.geometry().y():
            self.move(self.x(), -self.yleave)

    def hideApp(self):
        cx, cy = (
            QCursor.pos().x(),
            QCursor.pos().y(),
        )  # QCursor.pos()效果等同于event.globalPos()
        if (
            cx >= self.x()
            and cx <= self.x() + self.width()
            and cy >= self.y()
            and cy <= self.geometry().y()
        ):
            return  # title bar
        elif self.x() < 0 and QCursor.pos().x() > 0:
            self.move(self.xleave - self.width(), self.y())
        elif self.y() < 0 and QCursor.pos().y() > 0:
            self.move(
                self.x(), self.yleave - self.height() + self.y() - self.geometry().y()
            )

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.m_drag = True
            self.setCursor(QCursor(Qt.OpenHandCursor))
            # 获得鼠标的初始位置
            self.mouse_start_point_ = e.globalPosition()
            # 获得窗口的初始位置
            self.window_start_point_ = self.frameGeometry().topLeft()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self.m_drag = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            # 下面这个和 accept ignore之类有啥用，带深入研究事件模型，此处都不用好像也没关系
            # return super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent):
        if hasattr(self, "m_drag") and self.m_drag:
            # 获得鼠标移动的距离
            move_distance = e.globalPosition() - self.mouse_start_point_
            window_x = self.window_start_point_.x() + move_distance.x()
            window_y = self.window_start_point_.y() + move_distance.y()
            # //改变窗口的位置,
            # self.move(window_purpose_point)
            # 有的说下面这个能避免拖动时抖动，但感觉差不多
            self.setGeometry(window_x, window_y, self.width(), self.height())
