from myutils.GeneralQThread import Worker
from myutils import image_convert, globalvar
from route.OCRRequest import get_ocr_result
from ui.component.TipsShower import TipsShower
import numpy as np
from PySide6.QtCore import Qt, Signal, QStandardPaths, QThreadPool
from PySide6.QtGui import (
    QCursor,
    QGuiApplication,
    QPixmap,
    QPainter,
    QIcon,
    QFont,
)
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QGroupBox
from .MaskLayer import MaskLayer
from .SAIFinder import Finder
from .Screenshot import Screenshot
from pynput.mouse import Controller

# 导入图片资源以便使用,不能删除
import mytools.screen_shot.imagefiles.jamresourse_rc


class MainLayer(QLabel):  # 区域截图功能
    showm_signal = Signal(str)
    recorder_recordchange_signal = Signal()
    close_signal = Signal()
    screen_shot_pic_signal = Signal(object)

    # progress_signal = Signal(float)
    def __init__(self):
        super().__init__()
        # self.parent = parent
        # self.ready_flag = False
        # self.pixmap()=QPixmap()
        self.setup()

    # 初始化界面
    def setup(self):
        self.on_init = True
        self.mask = MaskLayer(self)  # 遮罩层，其实就是基于当前背景窗口的操作层，在上面可以作划区域等操作
        self.setMouseTracking(True)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        # 1、截屏时绘图工具箱,可移动
        # 2、智能选区的寻找器
        self.finder = Finder(self)
        # 左上角的大字提示
        self.Tipsshower = TipsShower("  ", targetarea=(100, 70, 0, 0), parent=self)
        tipsfont = QFont("Microsoft YaHei", 35)
        # tipsfont.setBold(True)
        self.Tipsshower.setFont(tipsfont)
        self.Tipsshower.hide()
        # 3、截屏后的行为操作框，比如锁定截图在原位置，保存图片等
        self.init_slabel_ui()
        self.init_parameters()
        self.on_init = False
        # 滚动截屏操作
        self.rollSS = Screenshot(draw=True)
        self.rollSS.showm_signal.connect(self.in_roll_shot)
        self.rollSS.finish_signal.connect(self.after_roll_shot)

    # 初始化界面的参数
    def init_slabel_ui(self):
        self.setToolTip("左键框选，右键返回")
        self.botton_box = QGroupBox(self)

        self.save_botton = QPushButton(self.botton_box)
        self.save_botton.setToolTip("另存为文件")
        self.save_botton.setGeometry(0, 0, 40, 35)
        self.save_botton.setIcon(QIcon(":/saveicon.png"))
        self.save_botton.clicked.connect(self.save_pic)

        self.rollshot_botton = QPushButton(self.botton_box)
        self.rollshot_botton.setToolTip("滚动截屏")
        self.rollshot_botton.setGeometry(
            self.save_botton.x() + self.save_botton.width(), 0, 40, 35
        )
        self.rollshot_botton.setIcon(QIcon(":/scroll_icon.png"))
        self.rollshot_botton.clicked.connect(self.roll_shot)

        self.confirm_botton = QPushButton(self.botton_box)
        self.confirm_botton.setToolTip("截屏")
        self.confirm_botton.setGeometry(
            self.rollshot_botton.x() + self.rollshot_botton.width(), 0, 60, 35
        )
        self.confirm_botton.setIcon(QIcon(":/screenshot.png"))
        self.confirm_botton.clicked.connect(self.screen_shot_ocr)
        self.botton_box.resize(
            +self.save_botton.width()
            + self.rollshot_botton.width()
            + self.confirm_botton.width(),
            self.confirm_botton.height(),
        )
        self.botton_box.hide()

    # 初始化参数
    def init_parameters(self):
        # 智能选区开关
        # self.smartcursor_on = True
        # 正在自动寻找选取的控制变量,就进入截屏之后会根据鼠标移动到的位置自动选取,
        self.finding_rect = True
        self.drawing_rect = (
            self.choicing
        ) = (
            self.move_rect
        ) = self.move_y0 = self.move_x0 = self.move_x1 = self.move_y1 = False
        self.x0 = (
            self.y0
        ) = (
            self.rx0
        ) = self.ry0 = self.x1 = self.y1 = self.mouse_posx = self.mouse_posy = -50
        self.bx = self.by = 0
        self.tool_width = 5

    # 后台初始化截屏线程,用于寻找所有智能选区
    def init_ss_thread_fun(self, get_pix):
        self.mouse_posx = self.mouse_posy = -150
        self.qimg = get_pix.toImage()
        temp_shape = (self.qimg.height(), self.qimg.width(), 4)
        ptr = self.qimg.bits()
        # ptr.setsize(self.qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)[..., :3]
        self.finder.img = result
        self.finder.find_contours_setup()
        QApplication.processEvents()

    # 1、截屏函数,功能有二:当有传入pix时直接显示pix中的图片作为截屏背景,否则截取当前屏幕作为背景;前者用于重置所有修改
    def screen_shot(self):
        self.finding_rect = True

        # 寻找合适屏幕
        def search_in_which_screen():
            mousepos = Controller().position
            screens = QApplication.screens()
            # 默认是主屏幕，屏幕坐标原点是 0，0
            getscreen = None, None, None, None, None
            # 识别多少个屏幕，并选择当前鼠标所在的屏幕来截屏
            for screen in screens:
                rect = screen.geometry().getRect()
                screen_x_begin, screen_x_end = rect[0], rect[0] + rect[2]
                screen_y_begin, screen_y_end = rect[1], rect[1] + rect[3]
                # print(f"窗口位置：{self.x(),self.y()}；屏幕位置及大小：{rect}；鼠标的位置：{mousepos}")
                mouse_x, mouse_y = mousepos[0], mousepos[1]
                if mouse_x in range(screen_x_begin, screen_x_end) and mouse_y in range(
                    screen_y_begin, screen_y_end
                ):
                    getscreen = (
                        screen,
                        screen_x_begin,
                        screen_y_begin,
                        screen_x_end,
                        screen_y_end,
                    )
                    break
            return getscreen

        (
            self.purpose_screen,
            self.x0,
            self.y0,
            self.x1,
            self.y1,
        ) = search_in_which_screen()
        self.move(self.x0, self.y0)
        get_pix = self.purpose_screen.grabWindow(0)  # 截取屏幕
        # 1、画一个图片
        pixmap = QPixmap(get_pix.width(), get_pix.height())
        pixmap.fill(Qt.GlobalColor.transparent)  # 填充透明色,不然没有透明通道
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.drawPixmap(0, 0, get_pix)
        painter.end()  # 一定要end
        # 2、主背景设置图片，并全屏，不透明
        self.setPixmap(pixmap)
        # 1表示完全不透明，设置主背景不透明，通过mask层实现透视划区
        self.setWindowOpacity(1)
        self.showFullScreen()
        self.originalPix = pixmap.copy()
        self.botton_box.hide()
        # 设置蒙层并在上面划线选区
        self.mask.setGeometry(0, 0, get_pix.width(), get_pix.height())
        self.mask.show()
        self.init_ss_thread_fun(get_pix)
        # 以下设置样式
        self.setStyleSheet(
            "QPushButton{color:black;background-color:rgb(239,239,239);padding:1px 4px;}"
            "QPushButton:hover{color:green;background-color:rgb(200,200,100);}"
            "QGroupBox{border:none;}"
        )
        self.setFocus()
        self.setMouseTracking(True)
        self.activateWindow()
        self.raise_()
        self.update()

    # 6、划完截图区域后，显示动作按钮
    def choice(self):
        self.choicing = True
        botton_box_x = self.x1 + 5
        botton_box_y = self.y1 + 5
        dx = abs(self.x1 - self.x0)
        dy = abs(self.y1 - self.y0)
        x = globalvar.get_var("SCREEN_WIDTH")
        y = globalvar.get_var("SCREEN_HEIGHT")
        if dx < self.botton_box.width() + 10:
            botton_box_x = (
                min(self.x0, self.x1) - self.botton_box.width() - 5
                if max(self.x1, self.x0) + self.botton_box.width() > x
                else max(self.x1, self.x0) + 5
            )
        elif self.x1 > self.x0:
            botton_box_x = self.x1 - self.botton_box.width() - 5
        if dy < self.botton_box.height() + 105:
            botton_box_y = (
                min(self.y0, self.y1) - self.botton_box.height() - 5
                if max(self.y1, self.y0) + self.botton_box.height() + 20 > y
                else max(self.y0, self.y1) + 5
            )
        elif self.y1 > self.y0:
            botton_box_y = self.y1 - self.botton_box.height() - 5
        self.botton_box.move(botton_box_x, botton_box_y)
        self.botton_box.show()

    # 仅仅保存图片
    def save_pic(self):
        backupgroud_big_pix = self.pixmap().copy()
        x0 = min(self.x0, self.x1)
        y0 = min(self.y0, self.y1)
        x1 = max(self.x0, self.x1)
        y1 = max(self.y0, self.y1)
        w = x1 - x0
        h = y1 - y0
        if x1 - x0 < 1 or y1 - y0 < 1:
            self.Tipsshower.setText("范围过小<1")
            return
        self.final_get_img = backupgroud_big_pix.copy(x0, y0, w, h)

        path, l = QFileDialog.getSaveFileName(
            self,
            "保存为",
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.PicturesLocation
            )
            + "/未命名",
            "img Files (*.PNG *.jpg *.JPG *.JPEG *.BMP *.ICO);;all files(*.*)",
        )
        if path:
            backupgroud_big_pix.save(path)
        else:
            return
        self.manage_data()

    # 7、划完截图区域后，截图识别内容
    def screen_shot_ocr(self):
        backupgroud_big_pix = self.pixmap().copy()
        x0 = min(self.x0, self.x1)
        y0 = min(self.y0, self.y1)
        x1 = max(self.x0, self.x1)
        y1 = max(self.y0, self.y1)
        w = x1 - x0
        h = y1 - y0
        if x1 - x0 < 1 or y1 - y0 < 1:
            self.Tipsshower.setText("范围过小<1")
            return
        self.final_get_img = backupgroud_big_pix.copy(x0, y0, w, h)

        get_ocr_result(
            image_convert.pixmap2cv(self.final_get_img),
            self.after_roll_shot,
            ocr_method="ocr",
        )
        self.manage_data()

    # """8、点击滚动截屏"""
    def roll_shot(self):
        x0 = min(self.x0, self.x1)
        y0 = min(self.y0, self.y1)
        x1 = max(self.x0, self.x1)
        y1 = max(self.y0, self.y1)
        print(x0, y0, x1, y1)
        if x1 - x0 < 50 or y1 - y0 < 50:
            self.showm_signal.emit("过小!")
            self.Tipsshower.setText("划定滚动区域面积过小!")
            return
        self.botton_box.hide()
        print("roller begin")
        self.rollSS.auto_roll(self.purpose_screen, (x0, y0, x1 - x0, y1 - y0))

    # 在滚动截屏时，隐藏覆盖层及弹出相应信息
    def in_roll_shot(self, x):
        self.hide()
        self.Tipsshower.setText(x)

    def after_roll_shot(self, result):
        print("图片识别完成")
        if result is None:
            print("未完成滚动截屏,用户退出")
            self.clear_and_hide()
            return
        self.screen_shot_pic_signal.emit(result)
        self.manage_data()

    """截屏完之后善后工作"""

    def manage_data(self):
        self.clear_and_hide()
        # self.close()

    # 清理退出
    def clear_and_hide(self):
        self.hide()
        self.botton_box.hide()
        worker = Worker(
            self.clear_and_hide_thread
        )  # Any other args, kwargs are passed to the run function
        # worker.signals.finished.connect(self.after_auto_roll)
        QThreadPool.globalInstance().start(worker)

    # 后台等待线程
    def clear_and_hide_thread(self):
        self.close_signal.emit()
        # try:
        #     self.save_data_thread.wait()
        # except Exception:
        #     print(sys.exc_info(), 2300)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # 先储存起鼠标位置,用于画笔等的绘图计算
        mouse_posx = event.position().x()
        mouse_posy = event.position().y()
        if event.button() == Qt.MouseButton.LeftButton:
            # 按下了左键，说明正在选区或移动选区
            r = 0
            x0 = min(self.x0, self.x1)
            x1 = max(self.x0, self.x1)
            y0 = min(self.y0, self.y1)
            y1 = max(self.y0, self.y1)
            my = (y1 + y0) // 2
            mx = (x1 + x0) // 2
            # 以下为判断点击在哪里
            if (
                not self.finding_rect
                and (self.x0 - 8 < mouse_posx < self.x0 + 8)
                and (
                    my - 8 < mouse_posy < my + 8
                    or y1 - 8 < mouse_posy < y1 + 8
                    or y0 - 8 < mouse_posy < y0 + 8
                )
            ):
                self.move_x0 = True
                r = 1
            elif (
                not self.finding_rect
                and (self.x1 - 8 < mouse_posx < self.x1 + 8)
                and (
                    my - 8 < mouse_posy < my + 8
                    or y0 - 8 < mouse_posy < y0 + 8
                    or y1 - 8 < mouse_posy < y1 + 8
                )
            ):
                self.move_x1 = True
                r = 1
            elif (
                not self.finding_rect
                and (self.y0 - 8 < mouse_posy < self.y0 + 8)
                and (
                    mx - 8 < mouse_posx < mx + 8
                    or x0 - 8 < mouse_posx < x0 + 8
                    or x1 - 8 < mouse_posx < x1 + 8
                )
            ):
                self.move_y0 = True
            elif (
                not self.finding_rect
                and self.y1 - 8 < mouse_posy < self.y1 + 8
                and (
                    mx - 8 < mouse_posx < mx + 8
                    or x0 - 8 < mouse_posx < x0 + 8
                    or x1 - 8 < mouse_posx < x1 + 8
                )
            ):
                self.move_y1 = True
            elif (
                not self.finding_rect
                and (x0 + 8 < mouse_posx < x1 - 8)
                and (y0 + 8 < mouse_posy < y1 - 8)
            ):
                self.move_rect = True
                self.setCursor(Qt.CursorShape.SizeAllCursor)
                self.bx = abs(max(self.x1, self.x0) - mouse_posx)
                self.by = abs(max(self.y1, self.y0) - mouse_posy)
            else:
                # 要开始拖动鼠标选区
                self.drawing_rect = True
                # 记录下点击位置
                self.rx0 = mouse_posx
                self.ry0 = mouse_posy
                if self.x1 == -50:
                    self.x1 = mouse_posx
                    self.y1 = mouse_posy
            if r and x0 - 8 < mouse_posx < x1 + 8:  # 判断是否点击四个角上
                if self.y0 - 8 < mouse_posy < self.y0 + 8:
                    self.move_y0 = True
                elif self.y1 - 8 < mouse_posy < self.y1 + 8:
                    self.move_y1 = True
            self.finding_rect = False
            self.botton_box.hide()
            self.update()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if not self.isVisible():
            return
        # 先储存起鼠标位置,用于画笔等的绘图计算
        self.mouse_posx = event.position().x()
        self.mouse_posy = event.position().y()
        # 处在划定目标区域状态，鼠标形状为十字架
        if self.finding_rect:
            self.x0, self.y0, self.x1, self.y1 = self.finder.find_targetrect(
                (self.mouse_posx, self.mouse_posy)
            )
            self.setCursor(
                QCursor(
                    QPixmap(":/smartcursor.png").scaled(
                        32, 32, Qt.AspectRatioMode.KeepAspectRatio
                    ),
                    16,
                    16,
                )
            )
        else:  # 已经划定区域
            minx = min(self.x0, self.x1)
            maxx = max(self.x0, self.x1)
            miny = min(self.y0, self.y1)
            maxy = max(self.y0, self.y1)  # 以上取选区的最小值和最大值
            my = (maxy + miny) // 2
            mx = (maxx + minx) // 2  # 取中间值
            #
            if (
                (minx - 8 < self.mouse_posx < minx + 8)
                and (miny - 8 < self.mouse_posy < miny + 8)
            ) or (
                (maxx - 8 < self.mouse_posx < maxx + 8)
                and (maxy - 8 < self.mouse_posy < maxy + 8)
            ):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)  # 左上右下移动选定区域边框线的鼠标形状
            elif (
                (minx - 8 < self.mouse_posx < minx + 8)
                and (maxy - 8 < self.mouse_posy < maxy + 8)
            ) or (
                (maxx - 8 < self.mouse_posx < maxx + 8)
                and (miny - 8 < self.mouse_posy < miny + 8)
            ):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)  # 左下右上移动选定区域边框线的鼠标形状
            elif (
                self.x0 - 8 < self.mouse_posx < self.x0 + 8
                or self.x1 - 8 < self.mouse_posx < self.x1 + 8
            ) and (
                my - 8 < self.mouse_posy < my + 8
                or miny - 8 < self.mouse_posy < miny + 8
                or maxy - 8 < self.mouse_posy < maxy + 8
            ):
                self.setCursor(Qt.CursorShape.SizeHorCursor)  # 左右移动选定区域边框线的鼠标形状
            elif (
                self.y0 - 8 < self.mouse_posy < self.y0 + 8
                or self.y1 - 8 < self.mouse_posy < self.y1 + 8
            ) and (
                mx - 8 < self.mouse_posx < mx + 8
                or minx - 8 < self.mouse_posx < minx + 8
                or maxx - 8 < self.mouse_posx < maxx + 8
            ):
                self.setCursor(Qt.CursorShape.SizeVerCursor)  # 上下移动选定区域边框线的鼠标形状
            elif (minx + 8 < self.mouse_posx < maxx - 8) and (
                miny + 8 < self.mouse_posy < maxy - 8
            ):
                self.setCursor(Qt.CursorShape.SizeAllCursor)  # 挪动整个选择框的鼠标形状
            elif (
                self.move_x1 or self.move_x0 or self.move_y1 or self.move_y0
            ):  # 拖动选定区域的边框移动时鼠标形状
                b = (self.x1 - self.x0) * (self.y1 - self.y0) > 0
                if (self.move_x0 and self.move_y0) or (self.move_x1 and self.move_y1):
                    if b:
                        self.setCursor(Qt.CursorShape.SizeFDiagCursor)  # 左上 右下方向拉动的鼠标形状
                    else:
                        self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                elif (self.move_x1 and self.move_y0) or (self.move_x0 and self.move_y1):
                    if b:
                        self.setCursor(Qt.CursorShape.SizeBDiagCursor)  # 左下 右上方向拉动的鼠标形状
                    else:
                        self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                elif self.move_x0 or self.move_x1:
                    self.setCursor(Qt.CursorShape.SizeHorCursor)  # 左右选定边框横向拉动的鼠标形状
                elif self.move_y0 or self.move_y1:
                    self.setCursor(Qt.CursorShape.SizeVerCursor)  # 上下选定边框横向拉动的鼠标形状
                elif self.move_rect:
                    self.setCursor(Qt.CursorShape.SizeAllCursor)  # 移动整个选定区域框的鼠标形状
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)  # 选定区域外面的鼠标形状
            # 以上几个ifelse都是判断鼠标移动的位置和选框的关系然后设定光标形状
            # 选区,移动鼠标更新选区右下角的坐标值
            if self.drawing_rect:
                self.x1 = self.mouse_posx  # 储存当前位置到self.x1下同
                self.y1 = self.mouse_posy
                self.x0 = self.rx0  # 鼠标按下时记录的坐标,下同
                self.y0 = self.ry0
                if self.y1 > self.y0:  # 下面是边界修正,由于选框占用了一个像素,否则有误差
                    self.y1 += 1
                else:
                    self.y0 += 1
                if self.x1 > self.x0:
                    self.x1 += 1
                else:
                    self.x0 += 1
            else:  # 下面是处理移动/拖动选区
                if self.move_x0:
                    self.x0 = self.mouse_posx
                elif self.move_x1:
                    self.x1 = self.mouse_posx
                if self.move_y0:
                    self.y0 = self.mouse_posy
                elif self.move_y1:
                    self.y1 = self.mouse_posy
                elif self.move_rect:  # 拖动选框
                    dx = abs(self.x1 - self.x0)
                    dy = abs(self.y1 - self.y0)
                    if self.x1 > self.x0:
                        self.x1 = self.mouse_posx + self.bx
                        self.x0 = self.x1 - dx
                    else:
                        self.x0 = self.mouse_posx + self.bx
                        self.x1 = self.x0 - dx
                    if self.y1 > self.y0:
                        self.y1 = self.mouse_posy + self.by
                        self.y0 = self.y1 - dy
                    else:
                        self.y0 = self.mouse_posy + self.by
                        self.y1 = self.y0 - dy
        self.update()  # 刷新界面

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.drawing_rect = False  # 选区结束标志置零
            self.move_rect = (
                self.move_y0
            ) = self.move_x0 = self.move_x1 = self.move_y1 = False
            self.choice()
            # self.confirm_botton.show()
        elif event.button() == Qt.MouseButton.RightButton:  # 右键
            self.setCursor(Qt.CursorShape.ArrowCursor)
            if self.choicing:  # 退出选定的选区
                self.botton_box.hide()
                self.choicing = False
                self.finding_rect = True
                self.x0 = self.y0 = self.x1 = self.y1 = -50
            else:  # 退出截屏
                self.clear_and_hide()
            self.update()
