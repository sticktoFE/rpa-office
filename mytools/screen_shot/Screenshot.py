import random
import sys
from PIL import Image
from PySide6.QtCore import Signal, QObject, QThread
from PySide6.QtWidgets import QApplication
from pynput.mouse import Listener as MouseListenner
from pynput import mouse
import pyperclip
from mytools.screen_shot.OCRThread import ScreenShotTasks
import pyautogui as pg
from myutils.image_compare import is_same


class Screenshot(QObject):  # 滚动截屏主类
    showm_signal = Signal(str)
    finish_signal = Signal(tuple)

    def __init__(self, draw=False):
        super().__init__()
        self.finalimg = None
        self.img_list = []
        self.final_cv2_draw = None
        self.final_info = []
        self.final_html_content = []

    # 1、自动滚动模式--采取多线程提高速度，还未完成
    def auto_roll(self, screen, area):
        in_rolling = True
        self.showm_signal.emit("开始截屏-----------")  # 让mainlayer隐藏掉
        x, y, w, h = area
        # 拖动的鼠标落脚点选择很重要，最好选择有文字内容，但对于网页可以选中的区域，这样下面才能判断时滚动鼠标还是拖动
        # 下面使用随机数来随机落到下半区域位置
        (
            mouse_pos_x,
            mouse_pos_y,
        ) = screen.geometry().x() + x + w / 2, screen.geometry().y() + y + h * random.uniform(
            0.4, 0.8
        )
        # 控制鼠标点击到滚动区域中心,靠下的位置（3/4）
        # ！！！特别注意，如果鼠标不在可滚动区域，会导致滚动停止，进而截图退出，
        pg.moveTo(
            mouse_pos_x,
            mouse_pos_y,
        )
        mouse_scroll_distance = int(h * 2 / 4)  # 每次滚动的距离
        # 启动多线程把图片拼接成长图并ocr识别
        worker = ScreenShotTasks()
        worker.result.connect(self.after_auto_roll)
        # 直接启动拼接线程才启动
        worker.start()

        # 点击退出的函数句柄
        def onclick(x, y, button, pressed):
            if button == mouse.Button.middle:
                listener.stop()
                in_rolling = False
                # 停止多线程的图片处理任务
                worker.stop_thread()
                self.showm_signal.emit(
                    "middle click to stop---正在识别中........"
                )  # 告诉调用者，退出了
                self.finish_signal.emit(None)

        # 鼠标监听器
        listener = MouseListenner(on_click=onclick)
        listener.start()
        isDrag = None
        i = 1
        oldimg = Image.fromqpixmap(screen.grabWindow(0, x, y, w, h))
        worker.add_img(oldimg)
        # 拖动后，清空剪贴板，为了判断是拖动页面还是滑动页面
        pyperclip.copy("")
        while in_rolling:
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
            # 0、开始截图
            i += 1
            newimg = Image.fromqpixmap(screen.grabWindow(0, x, y, w, h))
            if is_same(oldimg, newimg):
                print(f"第{i}次，图片一样，截图结束。")
                # 停止多线程的图片处理任务
                worker.stop_thread()
                break
            # 保留上一次的图片，便于比较
            oldimg = newimg
            # 4、增加到列表中用于线程的拼接
            # 图片数据加入到后台的拼接线程中
            worker.add_img(newimg)
            # 通过sleep控制自动滚动速度
            QThread.sleep(random.randint(2, 3))
        print("结束滚动,共截屏{}张".format(i - 1))

    # 如果正在滚动状态或self.img_list还有图片没有处理完就一直处理
    def after_auto_roll(self, result):
        self.finish_signal.emit(result)
        print("处理完返回图片")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = Screenshot()
    # s.img_list = [cv2.imread(f"{Path(__file__).parent}/tmp/{}.png".format(name)) for name in range(45, 51)]
    # s.match_and_merge()
    s.auto_roll((400, 60, 500, 600))
    # t = TipsShower("按下以开始")
    sys.exit(app.exec())
