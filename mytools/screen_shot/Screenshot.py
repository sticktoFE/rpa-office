import math
import operator
import random
import sys
from functools import reduce
import cv2
from numpy import asarray
from PIL import Image
from PySide6.QtCore import Qt, Signal, QObject, QThread
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListenner
from pynput import mouse
import pyperclip
from mytools.screen_shot.OCRScrollOut import TasksThread
from myutils import image_convert
import pyautogui as pg
from ui.component.TipsShower import TipsShower

# pg.PAUSE = 1  # 所有指令间隔1秒


# import pyautogui as pg
class roller_mask(QLabel):  # 滚动截屏遮罩层
    def __init__(self, area):
        super(roller_mask, self).__init__()
        transparentpix = QPixmap(
            QGuiApplication.primaryScreen().availableGeometry().size()
        )
        transparentpix.fill(Qt.transparent)
        self.area = area
        self.tips = TipsShower("单击自动滚动;\n或手动下滚;", area)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setPixmap(transparentpix)
        self.showFullScreen()

    def settext(self, text: str, autoclose=True):  # 设置提示文字
        self.tips.setText(text, autoclose)

    def paintEvent(self, e):  # 绘制遮罩层
        super().paintEvent(e)
        x, y, w, h = self.area
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(x - 1, y - 1, w + 2, h + 2)
        painter.setPen(Qt.NoPen)
        # 把除了划定区域外的部分变成黑色，突出截屏区域
        painter.setBrush(QColor(0, 0, 0, 120))
        painter.drawRect(0, 0, x, self.height())
        painter.drawRect(x, 0, self.width() - x, y)
        painter.drawRect(x + w, y, self.width() - x - w, self.height() - y)
        painter.drawRect(x, y + h, w, self.height() - y - h)
        painter.end()


class Screenshot(QObject):  # 滚动截屏主类
    showm_signal = Signal(str)
    choice_roll_signal = Signal(tuple)
    finish_signal = Signal(tuple)

    # progress_signal = Signal(float)
    def __init__(self, draw=False):
        super().__init__()
        self.screen = QApplication.primaryScreen()
        self.choice_roll_signal.connect(self.after_roll_manager)
        self.init_splicing_shots()

    def init_splicing_shots(self):
        self.finalimg = None
        self.img_list = []
        self.in_rolling = False
        self.final_cv2_draw = None
        self.final_info = []
        self.final_html_content = []

    def is_same(self, img1, img2):  # 判断两张图片的相似度,用于判断结束条件
        h1 = img1.histogram()
        h2 = img2.histogram()
        # 求所有像素点的协方差，似乎也是一种测量图片差异度的方式
        result = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1)
        )
        return result <= 5

    # 滚动截屏控制器,控制滚动截屏的模式(自动还是手动滚)
    # area表示截屏区域
    def roll_manager(self, area):
        self.mode = 1

        def on_click(x, y, button, pressed):  # 用户点击了屏幕说明用户想自动滚
            if button == mouse.Button.left:
                if (
                    area[0] < x < area[0] + area[2]
                    and area[1] < y < area[1] + area[3]
                    and not pressed
                ):
                    # 发送信息的同时，会让mainlayer隐藏掉
                    self.showm_signal.emit("选择自动滚动截屏")
                    self.mode = 1
                    self.choice_roll_signal.emit(area)
                    lis.stop()
            elif button == mouse.Button.right:
                self.mode = 2
                self.choice_roll_signal.emit(area)
                lis.stop()

        def on_scroll(x, y, button, pressed):  # 用户滚动了鼠标说明用户想要手动滚
            self.showm_signal.emit("选择手动滚动截屏")
            self.mode = 0
            self.choice_roll_signal.emit(area)
            lis.stop()

        self.rollermask = roller_mask(area)  # 滚动截屏遮罩层初始化
        # self.showrect.setGeometry(x, y, w, h)
        # self.showrect.show()
        lis = MouseListenner(on_click=on_click, on_scroll=on_scroll)  # 鼠标监听器初始化并启动
        lis.start()
        print("等待用户开始")
        # lis.join()

    def after_roll_manager(self, area):
        # 用户选择的模式
        if self.mode == 1:
            print("auto_roll")
            self.auto_roll(area)
        elif self.mode == 2:
            print("exit roller")
            self.finish_signal.emit((1, None))
        else:
            print("hand_roll")
            self.scroll_to_roll(area)
        self.showm_signal.emit("选择完毕，开始截屏-----------")
        self.rollermask.hide()

    # 1、自动滚动模式--采取多线程提高速度，还未完成
    def auto_roll(self, area):
        x, y, w, h = area
        # 拖动的鼠标落脚点选择很重要，最好选择有文字内容，但对于网页可以选中的区域，这样下面才能判断时滚动鼠标还是拖动
        # 下面使用随机数来随机落到下半区域位置
        mouse_pos_x, mouse_pos_y = x + w / 2, y + h * random.uniform(0.5, 0.99)
        mouse_scroll_distance = int(h * 2 / 4)  # 每次滚动的距离
        self.rollermask.tips.setText("正在自动滚动，单击中键停止")

        # 点击退出的函数句柄
        def onclick(x, y, button, pressed):
            if button == mouse.Button.middle:
                listener.stop()
                self.in_rolling = False
                # 停止多线程的图片处理任务
                self.worker.communication.thread_stop.emit()
                self.showm_signal.emit("middle click to stop---正在识别中........")

        # 鼠标监听器
        listener = MouseListenner(on_click=onclick)
        self.in_rolling = True  # 先设置再启动下面的事件，否则可能覆盖事件设置的状态
        listener.start()

        # 启动多线程把图片拼接成长图并ocr识别
        img_package_list = []
        self.worker = TasksThread(img_package_list)
        self.worker.communication.result.connect(self.after_merge_and_ocr)
        # 直接启动拼接线程才启动
        self.worker.start()
        # 控制鼠标点击到滚动区域中心,靠下的位置（3/4）
        # ！！！特别注意，如果鼠标不在可滚动区域，会导致滚动停止，进而截图退出，
        pg.moveTo(
            mouse_pos_x,
            mouse_pos_y,
        )
        img_list = []
        isDrag = None
        i = 0
        oldimg = Image.new("RGB", (128, 128), "#FF0f00")
        # 拖动后，清空剪贴板，为了判断是拖动页面还是滑动页面
        pyperclip.copy("")
        while self.in_rolling:
            i += 1
            # 0、开始截图
            pix = self.screen.grabWindow(0, x, y, w, h)  # 截屏
            # 1、滚动或拖动页面（类似指针移到下一位）
            if isDrag is None or isDrag == True:
                # 1、通过鼠标拖动控制鼠标滚动
                pg.dragRel(
                    0,
                    -mouse_scroll_distance,
                    duration=1.5,
                    button="left",
                    tween=pg.easeInOutQuad,
                )
                pg.moveRel(0, mouse_scroll_distance, 0.5)
            elif isDrag == False:
                # 2、通过鼠标滚轮控制鼠标滚动
                pg.scroll(-mouse_scroll_distance)
            # 2、开始时判断是拖动页面还是滑动页面
            # 拖动时，是否会选中一些数据，并能够拷贝到粘贴板
            # 看下有没有内容来判断是拖动页面还是滑动页面
            if isDrag is None:
                # 模拟键盘操作，将选中的内容复制到剪贴板中
                pg.hotkey("ctrl", "c")
                # 获取剪贴板中的内容
                content = pyperclip.paste()
                if len(content) > 0:
                    # 有内容，说明是网页，采用滚动模式
                    isDrag = False
                    # 既然有内容，鼠标点击下，清理选中的内容
                    # 并把之前的内容清理掉
                    pg.click()
                    continue
                else:
                    isDrag = True
            # 3、到最后时，判断是否到了尾页进而停止截屏
            # 把图片转化为pil的格式
            newimg = Image.fromqpixmap(pix)
            if self.is_same(oldimg, newimg):
                print(f"第{i}次，图片一样，截图结束。")
                if img_list:
                    img_package_list.append(img_list)
                # 停止多线程的图片处理任务
                self.worker.communication.thread_stop.emit()
                break
            # 保留上一次的图片，便于比较
            oldimg = newimg
            # 4、增加到列表中用于线程的拼接
            # 把图片转化为numpy的格式
            img = cv2.cvtColor(asarray(newimg), cv2.COLOR_RGB2BGR)
            # 图片数据存入self.img_list中被后台的拼接线程使用
            img_list.append(img)
            # #10张图片打一个包
            if len(img_list) == 10:
                img_package_list.append(img_list.copy())
                img_list.clear()
            # 通过sleep控制自动滚动速度
            QThread.sleep(random.randint(2, 3))
        print("结束滚动,共截屏{}张".format(i - 1))

    # 手动滚动模式
    def scroll_to_roll(self, area):
        x, y, w, h = area
        self.rollermask.tips.setText("手动向下滚动,单击结束")
        # id是滚动的最大次数 rid是当前滚动次数 向上 -1 向下 +1
        self.id = self.rid = 0
        self.a_step = 0
        img_package_list = []
        img_list = []
        pix = self.screen.grabWindow(0, x, y, w, h)
        img_list.append(image_convert.pixmap2cv(pix))

        # 点在区域中
        def inthearea(pos, area):
            return (
                area[0] < pos[0] < area[0] + area[2]
                and area[1] < pos[1] < area[1] + area[3]
            )

        def onclick(x, y, button, pressed):
            if pressed:
                pix = self.screen.grabWindow(0, x, y, w, h)
                img_list.append(image_convert.pixmap2cv(pix))
                self.id += 1
            else:
                print("click to stop", len(img_list))
                self.in_rolling = False

        def on_scroll(px, py, x_axis, y_axis):
            print(px, py, x_axis, y_axis)
            # if not inthearea((px,py),area):
            #     return
            self.a_step += 1
            if self.a_step < 2:
                return
            else:
                self.a_step = 0
            if y_axis < 0:
                # 当滚动id与真实id一样时说明在正常往下滚动
                if self.rid >= self.id:
                    pix = self.screen.grabWindow(0, x, y, w, h)  # 滚动段距离进行截屏
                    img_list.append(image_convert.pixmap2cv(pix))
                    # cv2.imwrite(f'{Path(__file__).parent}/tmp/{}.png'.format(self.id), img)
                    # 记录当前滚动的id
                    self.id += 1
                    self.rid = self.id
                    # #暂定20张图片打一个包
                    if len(img_list) == 10:
                        img_package_list.append((self.id, img_list.copy()))
                        img_list.clear()
                else:  # 不一样时说明用户往回滚了,跳过
                    print("跳过")
                    self.rid += 1
            else:  # 方向往回滚时id-1,以记录往回的步数
                self.rid -= 1
                print("方向错误")

        listener = MouseListenner(on_click=onclick, on_scroll=on_scroll)  # 鼠标监听器,传入函数句柄
        # 启动多线程把图片拼接成长图并ocr识别
        self.worker = TasksThread(img_package_list)
        self.worker.communication.result.connect(self.after_merge_and_ocr)
        self.in_rolling = True
        listener.start()  # 鼠标监听器启动
        # 拼接线程启动
        self.worker.start()
        while self.in_rolling:  # 等待结束滚动
            QThread.msleep(10)
        if img_list:
            img_package_list.append((self.id + 1, img_list))
        print(f"结束滚动,共截屏{self.id}张")
        listener.stop()
        # 停止多线程的图片处理任务
        self.worker.communication.thread_stop.emit()

    # 如果正在滚动状态或self.img_list还有图片没有处理完就一直处理
    def after_merge_and_ocr(self, result):
        self.finish_signal.emit((0, result))
        print("处理完返回图片")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = Screenshot()
    # s.img_list = [cv2.imread(f"{Path(__file__).parent}/tmp/{}.png".format(name)) for name in range(45, 51)]
    # s.match_and_merge()
    s.roll_manager((400, 60, 500, 600))
    # t = TipsShower("按下以开始")
    sys.exit(app.exec())
