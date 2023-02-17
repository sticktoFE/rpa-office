import time
import cv2
from pynput.mouse import Button, Controller
from PySide6.QtCore import QThread, Signal
from myutils.DateAndTime import clock
from myutils.image_convert import pixmap2cv
from myutils.window_handle.ScreenShot import ScreenShot
import os
import pyautogui as pag
import pyperclip
__sizex__, __sizey__ = pag.size()  # 获得屏幕尺寸


class AppExec(QThread):
    """
    # 实现自动截图特定窗口，并根据目标对象列表，按顺序自动连续点击
    """

    signal = Signal(tuple)

    def __init__(self, **kwargs):
        super().__init__()
        self.runCon = False
        self.class_name = kwargs.get("class_name")
        self.window_name = kwargs.get("window_name")
        self.for_pics = kwargs.get("for_pics")
        self.shotscreen = ScreenShot()
        self.purpos_window_pos = self.shotscreen.locate_window(
            self.class_name, self.window_name)
        # self.purpos_window_pos = kwargs.get("purpos_window_pos")

        # 连接数据库
        # self.conn = None
        # self.signal.connect(self.refresh)
        self.__icon_search__ = "biz/monitor_oa/image/search.png"
        self.__icon_selectfile__ = "biz/monitor_oa/image/selectfile.png"
        self.__icon_send__ = "biz/monitor_oa/image/send.png"
        self.__icon_selected__ = "biz/monitor_oa/image/selected.png"
        self.__icon_close__ = "biz/monitor_oa/image/close.png"

    def stop(self):
        self.runCon = False
        # self.wait() 没弄清楚当初为啥有这个，先注释

    def start(self):
        if not self.runCon:
            super().start()
            self.runCon = True
        # self.wait() 没弄清楚当初为啥有这个，先注释

    @clock
    def run(self):
        time.sleep(2)
        self.cad_turn(purpos_window_pos=self.purpos_window_pos)

    @clock
    def run1(self):
        # 实例化Controller得到一个可以操作鼠标的对象
        mouse = Controller()
        for forPic in self.for_pics:
            _, pixmap, x1, y1 = self.shotscreen.shot_screen_locate_window(self.class_name,
                                                                          self.window_name)
            cv2_img = pixmap2cv(pixmap)
            pos = self.searchPicCenterPos(cv2_img, forPic)
            if pos is None:
                continue
            # 屏幕左上角坐标为(0, 0) 右下角为(屏幕宽度, 屏幕高度)
            # 给mouse.position赋值等于移动鼠标，这里相当于移动到(100, 100)的位置
            # 如果坐标小于0，那么等于0。如果超出屏幕范围，那么等于最大范围
            # 鼠标定位到
            # 此方法等价于mouse.move(100, 100)
            mouse.position = (x1 + pos[0], y1 + pos[1])
            # 该函数接收两个参数：点击鼠标的哪个键、以及点击次数
            # 这里连续点击两次，等于双击
            time.sleep(1)
            mouse.click(Button.left, 1)
            time.sleep(4)  # 延迟一会儿，等新窗口加载完再截屏和寻找
        self.signal.emit(("00", "成功"))
        # time.sleep(0.1)  # 制造阻塞

    def searchPicCenterPos(self, source_cv2_img, forPic):
        # cv2.imwrite("biz/InfoTracing/image/xxxx.png",source_cv2_img)
        # cv2.imshow("result_view", source_cv2_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 屏幕缩放系数 mac缩放是2 windows一般是1
        screenScale = 1
        # 事先对按钮截图
        target = cv2.imread(forPic, cv2.IMREAD_COLOR)
        # print("****")
        # print(target.shape)
        # print(source_cv2_img.shape)
        # 先截图
        # screenshot=pyscreeze.screenshot('screenshot.png')
        # 读取图片 灰色会快
        # temp = cv2.imread(r'biz/infoTracing/image/screenshot.png',cv2.IMREAD_GRAYSCALE)
        source_cv2_img = cv2.cvtColor(source_cv2_img, cv2.COLOR_BGR2RGB)
        tempheight, tempwidth = source_cv2_img.shape[:2]
        # 先缩放搜索图 INTER_LINEAR INTER_AREA
        scale_source = cv2.resize(
            source_cv2_img,
            (int(tempwidth / screenScale), int(tempheight / screenScale)),
        )
        stempheight, stempwidth = scale_source.shape[:2]
        # 在搜索图中寻找目标图
        res = cv2.matchTemplate(scale_source, target, cv2.TM_CCOEFF_NORMED)
        mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(f"**************max_val={max_val}")
        if max_val >= 0.5:
            print(f"{forPic}找到")
            # 计算出中心点
            theight, twidth = target.shape[:2]
            # 目标图标中心点(x,y)
            # max_loc表示目标图标左上点(x,y)
            tagCenterX, tagCenterY = max_loc[0] + int(twidth / 2), max_loc[1] + int(
                theight / 2
            )
            # self.imageLabelPressSlot(tagCenterX,tagCenterY)
            return (tagCenterX, tagCenterY)
        else:
            print(f"{forPic}没找到")
            return None

    def cad_turn(self, cad_file='D:\\六十四卦.jpg', outd=None, purpos_window_pos=None):
        # __sizex__, __sizey__ =  pag.size()  # 获得屏幕尺寸
        '''
        cad_file  :  要操作的CAD文件
        outd      :  文件输出路径
        '''
        # 打开图标，图标事先截图保存
        # 搜索联系人或群名
        c = pag.locateCenterOnScreen(
            self.__icon_search__, region=purpos_window_pos)
        pag.moveTo(*c, duration=1)
        pag.click(clicks=2, button="left")  # 点击打开按钮
        # 录入搜索的信息
        self._workaround_write('文件传输助手')
        pag.press('enter')

        # 选择发送的文件图标
        c = pag.locateCenterOnScreen(
            self.__icon_selectfile__, region=purpos_window_pos)
        pag.moveTo(*c, duration=2)
        pag.click(clicks=1, interval=1, button="left")
        # 输入信息
        self._workaround_write(cad_file)
        pag.press('enter')
        # 点击发送
        # c = pag.locateCenterOnScreen(
        #     self.__icon_send__, region=purpos_window_pos)
        # pag.moveTo(*c, duration=0.2)
        # pag.click(button="left")
        # 一般都可以通过回车来发送信息，代替上面寻找发送按钮，增加泛化能力
        pag.press('enter')

        # 关闭所有可能存在的窗口，避免占用太多内存
        while (True):
            try:
                c = pag.locateCenterOnScreen(
                    self.__icon_close__, region=purpos_window_pos)
                pag.moveTo(*c, duration=0.1)  # 移到“x”按钮
                pag.click(button="left")  # 点击“x”按钮
            except TypeError:
                break

    def _workaround_write(self, text):
        """
        This is a work-around for the bug in pyautogui.write() with non-QWERTY keyboards
        It copies the text to clipboard and pastes it, instead of typing it.
        """
        pyperclip.copy(text)
        pag.hotkey('ctrl', 'v')
        pyperclip.copy('')
