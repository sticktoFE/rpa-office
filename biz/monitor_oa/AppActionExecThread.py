import time
from PySide6.QtCore import QThread, Signal
from myutils.DateAndTime import clock
from myutils.ScreenShot import ScreenShot
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
            self.class_name, self.window_name
        )
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

    def cad_turn(self, cad_file="D:\\六十四卦.jpg", outd=None, purpos_window_pos=None):
        # __sizex__, __sizey__ =  pag.size()  # 获得屏幕尺寸
        """
        cad_file  :  要操作的CAD文件
        outd      :  文件输出路径
        """
        # 打开图标，图标事先截图保存
        # 搜索联系人或群名
        c = pag.locateCenterOnScreen(self.__icon_search__, region=purpos_window_pos)
        pag.moveTo(*c, duration=1)
        pag.click(clicks=2, button="left")  # 点击打开按钮
        # 录入搜索的信息
        self._workaround_write("文件传输助手")
        pag.press("enter")

        # 选择发送的文件图标
        c = pag.locateCenterOnScreen(self.__icon_selectfile__, region=purpos_window_pos)
        pag.moveTo(*c, duration=2)
        pag.click(clicks=1, interval=1, button="left")
        # 输入信息
        self._workaround_write(cad_file)
        pag.press("enter")
        # 点击发送
        # c = pag.locateCenterOnScreen(
        #     self.__icon_send__, region=purpos_window_pos)
        # pag.moveTo(*c, duration=0.2)
        # pag.click(button="left")
        # 一般都可以通过回车来发送信息，代替上面寻找发送按钮，增加泛化能力
        pag.press("enter")

        # 关闭所有可能存在的窗口，避免占用太多内存
        while True:
            try:
                c = pag.locateCenterOnScreen(
                    self.__icon_close__, region=purpos_window_pos
                )
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
        pag.hotkey("ctrl", "v")
        pyperclip.copy("")
