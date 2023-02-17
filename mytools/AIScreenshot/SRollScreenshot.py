import math
import operator
import os
from pathlib import Path
import random
import sys
from functools import reduce
import cv2
from numpy import asarray
from PIL import Image
from PySide6.QtCore import Qt, Signal, QObject,QThread
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor,QGuiApplication
from PySide6.QtWidgets import QApplication, QLabel
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListenner
from pynput import mouse
from mytools.AIScreenshot.OCRScrollOut import TasksThread
from myutils.image_compare import PicMatcher
from myutils import image_convert
import pyautogui as pg
from ui.component.TipsShower import TipsShower
# import pyautogui as pg
class roller_mask(QLabel):  # 滚动截屏遮罩层
    def __init__(self, area):
        super(roller_mask, self).__init__()
        transparentpix = QPixmap(QGuiApplication.primaryScreen().availableGeometry().size())
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

class RollScreenshot(QObject):  # 滚动截屏主类
    showm_signal = Signal(str)
    choice_roll_signal = Signal(tuple)
    finish_signal = Signal(tuple)
    # progress_signal = Signal(float)
    def __init__(self, draw=False):
        super().__init__()
        self.choice_roll_signal.connect(self.after_roll_manager)
        self.init_splicing_shots()
    def init_splicing_shots(self):
        self.finalimg = None
        self.img_list = []
        self.roll_speed = 50
        self.in_rolling = False
        self.final_cv2_draw = None
        self.final_info = []
        self.final_html_content = []
    def is_same(self, img1, img2):  # 判断两张图片的相似度,用于判断结束条件
        h1 = img1.histogram()
        h2 = img2.histogram()
        # 求所有像素点的协方差，似乎也是一种测量图片差异度的方式
        result = math.sqrt( reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        # print(f'***********{result}')
        return result <= 5
    # 滚动截屏控制器,控制滚动截屏的模式(自动还是手动滚)
    def roll_manager(self, area):  
        x, y, w, h = area
        self.mode = 1
        def on_click(x, y, button, pressed):  # 用户点击了屏幕说明用户想自动滚
            if button == mouse.Button.left:
                if area[0] < x < area[0] + area[2] and area[1] < y < area[1] + area[3] and not pressed:
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
        QApplication.processEvents()
        lis = MouseListenner(on_click=on_click, on_scroll=on_scroll)  # 鼠标监听器初始化并启动
        lis.start()
        print("等待用户开始")
        # lis.join()
    def after_roll_manager(self, area):
        if self.mode == 1:  # 判断用户选择的模式
            print("auto_roll")
            self.auto_roll(area)
        elif self.mode == 2:
            print("exit roller")
            self.finish_signal.emit((1,None))
        else:
            print("hand_roll")
            self.scroll_to_roll(area)
        self.showm_signal.emit("选择完毕，开始截屏-----------")
        self.rollermask.hide()
    #1、自动滚动模式--采取多线程提高速度，还未完成
    def auto_roll(self, area):
        x, y, w, h = area
        self.rollermask.tips.setText("正在自动滚动，单击中键停止")
        speed = round(1 / self.roll_speed, 2)
        screen = QApplication.primaryScreen()
        winid = 0
        def onclick(x, y, button, pressed):  # 点击退出的函数句柄
            if button == mouse.Button.middle:
                listener.stop()
                self.in_rolling = False
                # 停止多线程的图片处理任务
                self.worker.communication.thread_stop.emit()
                self.showm_signal.emit("middle click to stop---正在识别中........")
        controler = MouseController()  # 鼠标控制器
        # 控制鼠标点击到滚动区域中心
        # ！！！特别注意，如果鼠标不在可滚动区域，会导致滚动停止，进而截图退出，
        # 如何在滚动截图时，不影响鼠标的使用，这是个课题
        controler.position = (area[0] + int(area[2] / 2), area[1] + int(area[3] / 2))
        oldimg = Image.new("RGB", (128, 128), "#FF0f00")
        listener = MouseListenner(on_click=onclick)  # 鼠标监听器
        self.in_rolling = True #先设置再启动下面的事件，否则可能覆盖事件设置的状态
        listener.start()
        print('main thread name: ', QThread.currentThread())
        # 启动多线程把图片拼接成长图并ocr识别
        isDrag = False
        i = 0
        img_package_list = []
        img_list = []
        self.worker = TasksThread(img_package_list) # Any other args, kwargs are passed to the run function
        self.worker.communication.result.connect(self.after_merge_and_ocr)
        # self.worker.communication.progress.connect(self.progress_signal.emit)
        while self.in_rolling:
            pix = screen.grabWindow(winid, x, y, w, h)  # 截屏
            newimg = Image.fromqpixmap(pix)  # 转化为pil的格式
            img = cv2.cvtColor(asarray(newimg), cv2.COLOR_RGB2BGR)
            img_list.append(img)  # 图片数据存入self.img_list中被后台的拼接线程使用
            # cv2.imshow("FSd", img)
            # cv2.waitKey(0)
            # let application process events each 5 steps.
            if not i % 5:
                QApplication.processEvents()
            # 如果第二次截图和第一次一样，去掉第二个重复的截图
            # 情况是滑动鼠标滚轮没有效果，所以尝试拖动鼠标
            if i == 2:
                if self.is_same(oldimg, newimg):
                    print(f"第{i+1}次，图片一样,尝试用拖动滑动方式。")
                    img_list.pop()
                    img_list.pop()
                    isDrag = True
                # 当截第二张图片时拼接线程才启动
                self.worker.start()
            # 每帧检查是否停止，这是另一个停止点，即页面滚动到最后了
            if i > 2 and self.is_same(oldimg, newimg):  
                print(f"第{i+1}次，图片一样,换用拖动滚动方式也是一样，所以退出了。")
                img_list.pop()
                self.in_rolling = False
                # 停止多线程的图片处理任务
                self.worker.communication.thread_stop.emit()
                i += 1
                if img_list:
                    img_package_list.append((i,img_list))
                break
            i += 1
            # #暂定10张图片打一个包
            if len(img_list) == 10:
                img_package_list.append((i,img_list.copy()))
                img_list.clear()
            oldimg = newimg
            if isDrag:
                # 2、通过鼠标拖动控制鼠标滚动
                scroll_value = random.randint(150,350)
                # controler.press(mouse.Button.left)
                # controler.move(0,-scroll_value)
                # # 用time.sleep会卡住
                # win32api.Sleep(1000)
                # controler.release(mouse.Button.left)
                # controler.move(0,scroll_value)
                #鼠标拖动上面是模拟，下面这个更逼真，而且是现成的
                pg.dragRel(0,-scroll_value, 1, button='left')
                pg.moveRel(0,scroll_value,1)
            else:
                # 1、通过鼠标滚轮控制鼠标滚动
                # controler.scroll(dx=0, dy=-2)
                pg.scroll(-random.randint(80,230))
            # 通过sleep控制自动滚动速度
            QThread.sleep(int(speed))
        print("结束滚动,共截屏{}张".format(i-1))
    # 手动滚动模式
    def scroll_to_roll(self, area):
        x, y, w, h = area
        self.rollermask.tips.setText("手动向下滚动,单击结束")
        screen = QApplication.primaryScreen()
        winid = 0
        # id是滚动的最大次数 rid是当前滚动次数 向上 -1 向下 +1
        self.id = self.rid = 0
        self.a_step = 0
        img_package_list = []
        img_list = []
        pix = screen.grabWindow(winid, x, y, w, h)
        img_list.append(image_convert.pixmap2cv(pix))
        # 点在区域中
        def inthearea(pos, area):
            return area[0] < pos[0] < area[0] + area[2] and area[1] < pos[1] < area[1] + area[3]
        def onclick(x, y, button, pressed):
            if pressed:
                pix = screen.grabWindow(winid, x, y, w, h)
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
                    # print(self.rid,self.id)
                    pix = screen.grabWindow(winid, x, y, w, h)  # 滚动段距离进行截屏
                    img_list.append(image_convert.pixmap2cv(pix))
                    # cv2.imwrite(f'{Path(__file__).parent}/tmp/{}.png'.format(self.id), img)
                    # 记录当前滚动的id
                    self.id += 1
                    self.rid = self.id
                    # #暂定20张图片打一个包
                    if len(img_list) == 10:
                        img_package_list.append((self.id,img_list.copy()))
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
            img_package_list.append((self.id+1,img_list))
        print(f"结束滚动,共截屏{self.id}张")
        listener.stop()
        # 停止多线程的图片处理任务
        self.worker.communication.thread_stop.emit()
    # 如果正在滚动状态或self.img_list还有图片没有处理完就一直处理
    def after_merge_and_ocr(self,result):
        self.finish_signal.emit((0,result))
        print("处理完返回图片")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = RollScreenshot()
    # s.img_list = [cv2.imread(f"{Path(__file__).parent}/tmp/{}.png".format(name)) for name in range(45, 51)]
    # s.match_and_merge()
    s.roll_manager((400, 60, 500, 600))
    # t = TipsShower("按下以开始")
    sys.exit(app.exec())
