from myutils.GeneralQThread import Worker
from myutils import image_convert, globalvar
from ui.component.TipsShower import TipsShower
from .SFreezer import Freezer
import numpy as np
from PySide6.QtCore import Qt, Signal, QStandardPaths, QSettings, QThreadPool, QThread
from PySide6.QtGui import (
    QCursor,
    QGuiApplication,
    QPixmap,
    QPainter,
    QIcon,
    QFont,
)
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QGroupBox
from .SInfoWindow import FramelessEnterSendQTextEdit
from .MaskLayer import MaskLayer
from .SAIFinder import Finder
from .Screenshot import Screenshot
from pynput.mouse import Controller

# 导入图片资源以便使用
import mytools.screen_shot.imagefiles.jamresourse_rc


class MainLayer(QLabel):  # 区域截图功能
    showm_signal = Signal(str)
    recorder_recordchange_signal = Signal()
    close_signal = Signal()
    screen_shot_pic_signal = Signal(object)

    # progress_signal = Signal(float)
    def __init__(self):
        super().__init__()
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
        self.Tipsshower.hide()
        # 截屏后如果文字识别，结果展示窗口
        self.shower = FramelessEnterSendQTextEdit(self, enter_tra=True)
        self.shower.showm_signal.connect(self.Tipsshower.setText)
        # 3、截屏后的行为操作框，比如锁定截图在原位置，保存图片等
        self.init_slabel_ui()
        self.init_parameters()
        self.backup_ssid = 0  # 当前备份数组的id,用于确定回退了几步
        self.backup_pic_list = []  # 备份页面的数组,用于前进/后退
        self.on_init = False
        # 滚动截屏操作
        self.rollSS = Screenshot(draw=True)
        self.rollSS.showm_signal.connect(self.in_roll_shot)
        self.rollSS.finish_signal.connect(self.after_roll_shot)
        # self.rollSS.progress_signal.connect(self.progress_signal.emit)

    # 初始化界面的参数
    def init_slabel_ui(self):
        self.shower.hide()
        self.shower.setWindowOpacity(0.8)
        self.setToolTip("左键框选，右键返回")
        self.botton_box = QGroupBox(self)

        self.ssrec_botton = QPushButton(self.botton_box)
        self.ssrec_botton.setToolTip("开始录屏")
        self.ssrec_botton.setGeometry(0, 0, 40, 35)
        self.ssrec_botton.setIcon(QIcon(":/record.png"))
        self.ssrec_botton.clicked.connect(self.ssrec)

        self.save_botton = QPushButton(self.botton_box)
        self.save_botton.setToolTip("另存为文件")
        self.save_botton.setGeometry(
            self.ssrec_botton.x() + self.ssrec_botton.width(), 0, 40, 35
        )
        self.save_botton.setIcon(QIcon(":/saveicon.png"))
        self.save_botton.clicked.connect(lambda: self.cutpic(1))

        self.freeze_img_botton = QPushButton(self.botton_box)
        self.freeze_img_botton.setToolTip("固定图片于屏幕上")
        self.freeze_img_botton.setGeometry(
            self.save_botton.x() + self.save_botton.width(), 0, 40, 35
        )
        self.freeze_img_botton.setIcon(QIcon(":/freeze.png"))
        self.freeze_img_botton.clicked.connect(self.freeze_img)

        self.rollshot_botton = QPushButton(self.botton_box)
        self.rollshot_botton.setToolTip("滚动截屏")
        self.rollshot_botton.setGeometry(
            self.freeze_img_botton.x() + self.freeze_img_botton.width(), 0, 40, 35
        )
        self.rollshot_botton.setIcon(QIcon(":/scroll_icon.png"))
        self.rollshot_botton.clicked.connect(self.roll_shot)

        self.confirm_botton = QPushButton(self.botton_box)
        self.confirm_botton.setToolTip("截屏")
        self.confirm_botton.setGeometry(
            self.rollshot_botton.x() + self.rollshot_botton.width(), 0, 60, 35
        )
        self.confirm_botton.setIcon(QIcon(":/screenshot.png"))
        self.confirm_botton.clicked.connect(lambda: self.cutpic(3))
        self.botton_box.resize(
            self.ssrec_botton.width()
            + self.save_botton.width()
            + self.rollshot_botton.width()
            + self.freeze_img_botton.width()
            + self.confirm_botton.width(),
            self.confirm_botton.height(),
        )
        self.botton_box.hide()
        tipsfont = QFont("Microsoft YaHei", 35)
        # tipsfont.setBold(True)
        self.Tipsshower.setFont(tipsfont)

    # 初始化参数
    def init_parameters(self):
        # 智能选区开关
        # self.smartcursor_on = True
        # 正在自动寻找选取的控制变量,就进入截屏之后会根据鼠标移动到的位置自动选取,
        self.finding_rect = True
        self.NpainterNmoveFlag = (
            self.choicing
        ) = (
            self.move_rect
        ) = (
            self.move_y0
        ) = self.move_x0 = self.move_x1 = self.change_alpha = self.move_y1 = False
        self.x0 = (
            self.y0
        ) = (
            self.rx0
        ) = self.ry0 = self.x1 = self.y1 = self.mouse_posx = self.mouse_posy = -50
        self.bx = self.by = 0
        self.alpha = 255  # 透明度值
        self.tool_width = 5
        self.roller_area = (0, 0, 1, 1)

    def search_in_which_screen(self):
        mousepos = Controller().position
        screens = QApplication.screens()
        # 默认是主屏幕，屏幕坐标原点是 0，0
        getscreen = (QApplication.primaryScreen(), 0, 0)
        for screen in screens:
            rect = screen.geometry().getRect()
            screen_x_begin = rect[0]
            screen_x_end = rect[0] + rect[2]
            mouse_x = mousepos[0]
            screen_y_begin = rect[1]
            screen_y_end = rect[1] + rect[3]
            mouse_y = mousepos[1]
            print(f"窗口位置：{self.x(),self.y()}；一个窗口位置及大小：{rect}；鼠标的位置：{mousepos}")
            if mouse_x in range(screen_x_begin, screen_x_end) and mouse_y in range(
                screen_y_begin, screen_y_end
            ):
                getscreen = (screen, screen_x_begin, screen_y_begin)
                break
        return getscreen

    # 按键按下,每按一个键触发一次
    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        # self.pixmap().save(temp_path + '/aslfdhds.png')
        if e.key() == Qt.Key_Escape:  # 退出
            self.clear_and_hide()
        elif e.key() == Qt.Key_Control:  # 按住ctrl,更改透明度标志位置一
            print("cahnge")
            self.change_alpha = True
        elif self.change_alpha:  # 如果已经按下了ctrl
            if e.key() == Qt.Key_S:  # 还按下了s,说明是保存,ctrl+s
                self.cutpic(1)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # 先储存起鼠标位置,用于画笔等的绘图计算
        mouse_posx = event.position().x()
        mouse_posy = event.position().y()
        if event.button() == Qt.LeftButton:  # 按下了左键
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
                    or y0 - 8 < mouse_posy < y0 + 8
                    or y1 - 8 < mouse_posy < y1 + 8
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
                self.setCursor(Qt.SizeAllCursor)
                self.bx = abs(max(self.x1, self.x0) - mouse_posx)
                self.by = abs(max(self.y1, self.y0) - mouse_posy)
            else:
                # 没有绘图没有移动还按下了左键,说明正在选区,标志变量
                self.NpainterNmoveFlag = True
                self.rx0 = mouse_posx  # 记录下点击位置
                self.ry0 = mouse_posy
                if self.x1 == -50:
                    self.x1 = mouse_posx
                    self.y1 = mouse_posy
                if r:  # 判断是否点击在了对角线上
                    if (self.y0 - 8 < mouse_posy < self.y0 + 8) and (
                        x0 - 8 < mouse_posx < x1 + 8
                    ):
                        self.move_y0 = True
                        # print('y0')
                    elif self.y1 - 8 < mouse_posy < self.y1 + 8 and (
                        x0 - 8 < mouse_posx < x1 + 8
                    ):
                        self.move_y1 = True
                        # print('y1')
            if self.finding_rect:
                self.finding_rect = False
                # self.finding_rectde = True
            self.botton_box.hide()
            self.update()
        elif event.button() == Qt.RightButton:  # 右键
            self.setCursor(Qt.ArrowCursor)
            if self.choicing:  # 退出选定的选区
                self.botton_box.hide()
                self.choicing = False
                self.finding_rect = True
                self.shower.hide()
                self.x0 = self.y0 = self.x1 = self.y1 = -50
            else:  # 退出截屏
                self.clear_and_hide()
            self.update()

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if not self.isVisible():
            return
        # 先储存起鼠标位置,用于画笔等的绘图计算
        self.mouse_posx = event.position().x()
        self.mouse_posy = event.position().y()
        # 如果允许智能选取并且在选选区步骤
        if self.finding_rect:
            self.x0, self.y0, self.x1, self.y1 = self.finder.find_targetrect(
                (self.mouse_posx, self.mouse_posy)
            )
            self.setCursor(
                QCursor(
                    QPixmap(":/smartcursor.png").scaled(32, 32, Qt.KeepAspectRatio),
                    16,
                    16,
                )
            )
        else:  # 不在绘画
            minx = min(self.x0, self.x1)
            maxx = max(self.x0, self.x1)
            miny = min(self.y0, self.y1)
            maxy = max(self.y0, self.y1)  # 以上取选区的最小值和最大值
            my = (maxy + miny) // 2
            mx = (maxx + minx) // 2  # 取中间值
            if (
                (minx - 8 < self.mouse_posx < minx + 8)
                and (miny - 8 < self.mouse_posy < miny + 8)
            ) or (
                (maxx - 8 < self.mouse_posx < maxx + 8)
                and (maxy - 8 < self.mouse_posy < maxy + 8)
            ):
                self.setCursor(Qt.SizeFDiagCursor)
            elif (
                (minx - 8 < self.mouse_posx < minx + 8)
                and (maxy - 8 < self.mouse_posy < maxy + 8)
            ) or (
                (maxx - 8 < self.mouse_posx < maxx + 8)
                and (miny - 8 < self.mouse_posy < miny + 8)
            ):
                self.setCursor(Qt.SizeBDiagCursor)
            elif (self.x0 - 8 < self.mouse_posx < self.x0 + 8) and (
                my - 8 < self.mouse_posy < my + 8
                or miny - 8 < self.mouse_posy < miny + 8
                or maxy - 8 < self.mouse_posy < maxy + 8
            ):
                self.setCursor(Qt.SizeHorCursor)
            elif (self.x1 - 8 < self.mouse_posx < self.x1 + 8) and (
                my - 8 < self.mouse_posy < my + 8
                or miny - 8 < self.mouse_posy < miny + 8
                or maxy - 8 < self.mouse_posy < maxy + 8
            ):
                self.setCursor(Qt.SizeHorCursor)
            elif (self.y0 - 8 < self.mouse_posy < self.y0 + 8) and (
                mx - 8 < self.mouse_posx < mx + 8
                or minx - 8 < self.mouse_posx < minx + 8
                or maxx - 8 < self.mouse_posx < maxx + 8
            ):
                self.setCursor(Qt.SizeVerCursor)
            elif (self.y1 - 8 < self.mouse_posy < self.y1 + 8) and (
                mx - 8 < self.mouse_posx < mx + 8
                or minx - 8 < self.mouse_posx < minx + 8
                or maxx - 8 < self.mouse_posx < maxx + 8
            ):
                self.setCursor(Qt.SizeVerCursor)
            elif (minx + 8 < self.mouse_posx < maxx - 8) and (
                miny + 8 < self.mouse_posy < maxy - 8
            ):
                self.setCursor(Qt.SizeAllCursor)
            elif (
                self.move_x1 or self.move_x0 or self.move_y1 or self.move_y0
            ):  # 再次判断防止光标抖动
                b = (self.x1 - self.x0) * (self.y1 - self.y0) > 0
                if (self.move_x0 and self.move_y0) or (self.move_x1 and self.move_y1):
                    if b:
                        self.setCursor(Qt.SizeFDiagCursor)
                    else:
                        self.setCursor(Qt.SizeBDiagCursor)
                elif (self.move_x1 and self.move_y0) or (self.move_x0 and self.move_y1):
                    if b:
                        self.setCursor(Qt.SizeBDiagCursor)
                    else:
                        self.setCursor(Qt.SizeFDiagCursor)
                elif self.move_x0 or self.move_x1:
                    self.setCursor(Qt.SizeHorCursor)
                elif self.move_y0 or self.move_y1:
                    self.setCursor(Qt.SizeVerCursor)
                elif self.move_rect:
                    self.setCursor(Qt.SizeAllCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
            # 以上几个ifelse都是判断鼠标移动的位置和选框的关系然后设定光标形状
            if self.NpainterNmoveFlag:  # 如果没有在绘图也没在移动(调整)选区,在选区,则不断更新选区的数值
                # self.confirm_botton.hide()
                # self.rollshot_botton.hide()
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
            else:  # 说明在移动或者绘图,不过绘图没有什么处理的,下面是处理移动/拖动选区
                if self.move_x0:  # 判断拖动标志位,下同
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
        if event.button() == Qt.LeftButton:
            self.setCursor(Qt.ArrowCursor)
            self.NpainterNmoveFlag = False  # 选区结束标志置零
            self.move_rect = (
                self.move_y0
            ) = self.move_x0 = self.move_x1 = self.move_y1 = False
            self.choice()
            # self.confirm_botton.show()
            self.update()

    # 后台初始化截屏线程,用于寻找所有智能选区
    def init_ss_thread_fun(self, get_pix):
        self.x0 = self.y0 = 0
        self.x1 = globalvar.get_var("SCREEN_WIDTH")
        self.y1 = globalvar.get_var("SCREEN_HEIGHT")
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
    def screen_shot(self, pix=None):
        self.finding_rect = True
        self.sshoting = True
        if type(pix) is QPixmap:
            get_pix = pix
        else:
            if len(QGuiApplication.screens()) > 1:
                sscreen, s_coordi_x, scoordi_y = self.search_in_which_screen()
                self.move(s_coordi_x, scoordi_y)
            else:
                sscreen = QApplication.primaryScreen()
            get_pix = sscreen.grabWindow(0)  # 截取屏幕
        # 1、画一个图片
        pixmap = QPixmap(get_pix.width(), get_pix.height())
        pixmap.fill(Qt.transparent)  # 填充透明色,不然没有透明通道
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
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
        if type(pix) is not QPixmap:
            self.backup_ssid = 0
            self.backup_pic_list = [self.originalPix.copy()]
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

    # 6、划完截图区域后，显示选择按钮的函数
    def choice(self):
        self.choicing = True
        botton_boxw = self.x1 + 5
        botton_boxh = self.y1 + 5
        dx = abs(self.x1 - self.x0)
        dy = abs(self.y1 - self.y0)
        x = globalvar.get_var("SCREEN_WIDTH")
        y = globalvar.get_var("SCREEN_HEIGHT")
        if dx < self.botton_box.width() + 10:
            botton_boxw = (
                min(self.x0, self.x1) - self.botton_box.width() - 5
                if max(self.x1, self.x0) + self.botton_box.width() > x
                else max(self.x1, self.x0) + 5
            )
        elif self.x1 > self.x0:
            botton_boxw = self.x1 - self.botton_box.width() - 5
        if dy < self.botton_box.height() + 105:
            botton_boxh = (
                min(self.y0, self.y1) - self.botton_box.height() - 5
                if max(self.y1, self.y0) + self.botton_box.height() + 20 > y
                else max(self.y0, self.y1) + 5
            )
        elif self.y1 > self.y0:
            botton_boxh = self.y1 - self.botton_box.height() - 5
        self.botton_box.move(botton_boxw, botton_boxh)
        self.botton_box.show()

    # 7、划完截图区域后，点击确定获取裁剪图片
    def cutpic(self, save_as=0):
        self.sshoting = False
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

        def get_ocr_info(cv2_img):
            ocr_request = globalvar.get_var("ocrserver")
            while not ocr_request:
                QThread.msleep(1)
                ocr_request = globalvar.get_var("ocrserver")
            html_content = []
            cv2_img_draw, out_info, html_content = ocr_request.ocr_structure(cv2_img)
            return (0, (cv2_img, cv2_img_draw, out_info, html_content))

        if save_as:
            if save_as == 1:
                path, l = QFileDialog.getSaveFileName(
                    self,
                    "保存为",
                    QStandardPaths.writableLocation(QStandardPaths.PicturesLocation),
                    "img Files (*.PNG *.jpg *.JPG *.JPEG *.BMP *.ICO);;all files(*.*)",
                )
                if path:
                    backupgroud_big_pix.save(path)
                else:
                    return
            elif save_as == 2:
                return
            elif save_as == 3:
                worker = Worker(
                    get_ocr_info, image_convert.pixmap2cv(self.final_get_img)
                )
                worker.communication.result.connect(self.after_roll_shot)
                QThreadPool.globalInstance().start(worker)
        self.manage_data()

    # """8、点击滚动截屏"""
    def roll_shot(self):
        x0 = min(self.x0, self.x1)
        y0 = min(self.y0, self.y1)
        x1 = max(self.x0, self.x1)
        y1 = max(self.y0, self.y1)
        if x1 - x0 < 50 or y1 - y0 < 50:
            self.showm_signal.emit("过小!")
            self.Tipsshower.setText("滚动面积过小!")
            return
        self.botton_box.hide()
        print("roller begin")
        self.rollSS.roll_manager((x0, y0, x1 - x0, y1 - y0))

    # 在滚动截屏时，隐藏覆盖层及弹出相应信息
    def in_roll_shot(self, x):
        self.hide()
        self.Tipsshower.setText(x)

    def after_roll_shot(self, result):
        exi, final_result = result
        print("roller end")
        if exi:
            print("未完成滚动截屏,用户退出")
            self.clear_and_hide()
            return
        self.screen_shot_pic_signal.emit(final_result)
        self.manage_data()

    """截屏完之后善后工作"""

    def manage_data(self):
        self.clear_and_hide()
        # self.close()

    # 2、录屏函数
    def ssrec(self):
        self.parent.setingarea = True
        self.cutpic()
        self.recorder_recordchange_signal.emit()
        # recorder.recordchange()

    # 3、把截图区域固定在原地
    def freeze_img(self):
        self.cutpic(save_as=2)
        self.parent.freeze_imgs.append(
            Freezer(
                None,
                self.final_get_img,
                min(self.x0, self.x1),
                min(self.y0, self.y1),
                len(self.parent.freeze_imgs),
            )
        )
        if not QSettings("Fandes", "jamtools").value("S_SIMPLE_MODE", False, bool):
            self.parent.show()
        self.clear_and_hide()

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
