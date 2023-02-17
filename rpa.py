from functools import partial
from myutils.GeneralThread import Worker
from ui.mainwindow_event import MainWindow
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QThreadPool, QEvent, QObject
from myutils.LazyImport import lazy_import
from myutils import globalvar
# ocr服务较慢，程序一开始就运行起来


def startup_ocrserver():
    # Any other args, kwargs are passed to the run function
    worker_ocr_server = Worker(
        'OCRRequestProcess', module='route.OCRRequestProcess')
    worker_ocr_server.communication.result.connect(
        partial(globalvar.set_var, "ocrserver"))
    QThreadPool.globalInstance().start(worker_ocr_server)


class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.move(-1, 20)
        # print(f'Main thread name: {QThread.currentThread()}')
        # 1、能并行的单元单独开线程执行，加快启动速度
        worker = Worker(self.init_all_object, need_progress_signal=True)
        worker.communication.finished.connect(self.readyOcr)
        worker.communication.progress.connect(self.update_progress)
        QThreadPool.globalInstance().start(worker)
        # 2、初始化和窗口相关的内容
        self.init_all_gui()
    # 初始后台对象

    def init_all_object(self, progress_signal):
        super().init_all_object(progress_signal)
        # progress_signal.emit(100*2/2)
    # 对象放到init_all_gui还是init_all_object，要看此对象用不用主窗口对象

    def init_all_gui(self):
        # 先执行父类相应内容
        super().init_all_gui()
        # 任务栏显示
        from ui.component.msystemtray import MSystemTray
        self.systray = MSystemTray(self, "ui/icon/rpa.ico")
        # self.menuthread = QThread()
        # self.menuthread.setObjectName("I am a menuthread!")
        # 右键菜单设置 ---加载时非常耗时
        from ui.component.mmenu import MMenu
        self.context_menu: MMenu = MMenu()
        self.context_menu.show_signal.connect(self.menu_choice)
        # self.context_menu.moveToThread(self.menuthread)
        # self.menuthread.start()
        # 综合截屏界面
        from mytools.AIScreenshot.SMainLayer import SMainLayer
        self.screenshot = SMainLayer()
        self.screenshot.screen_shot_pic_signal.connect(self.ocrResult)
        # self.screenshot.progress_signal.connect(self.update_progress)

    def update_progress(self, n):
        self.progressBar.setVisible(True)
        self.progressBar.setValue(n)
        if n == 100:
            self.progressBar.setVisible(False)
    # 1、右键菜单设置区

    def contextMenuEvent(self, event):
        # print(event.type())
        # self.context_menu.exec(event.globalPos())
        # self.context_menu.popup(QCursor.pos())  # 菜单显示的位置,同上面注释
        # self.context_menu.show()
        # self.context_menu.popup_signal.connect(self.displayInfo)
        # self.context_menu.show_signal.emit()
        self.context_menu.show()
    # 打开配置选项

    def menu_choice(self, res):
        eval(res)

    def managerConfig(self):
        self.hide()
        self.PO.pause()
        self.mc = lazy_import('ui.manage_config_event').ManagerConfig()
        rect = self.frameGeometry().getRect()
        self.mc.move(rect[0] + rect[2], rect[1])
        self.mc.show()
        self.mc.close_signal.connect(self.close_manageConfig)
        # self.leaveTimer.start(10)  # 10毫秒比较流畅

    def close_manageConfig(self):
        self.show()
        self.PO.resume()

    def screen_shot_info(self):
        self.screenshot.screen_shot()

    # 识别内容展示
    def ocrResult(self, result):
        self.ocrmg = lazy_import('ui.OCRResult_event').TotalMessage(result)
        self.ocrmg.show()
    # 手工画范围截图

    def drawExtract(self):
        """开始截图"""
        self.hide()
        self.label = lazy_import('myutils.window_handle.ScreenDraw').ScreenDraw(
            globalvar.get_var("SCREEN_WIDTH"), globalvar.get_var("SCREEN_HEIGHT"))
        self.label.showFullScreen()
        self.label.signal.connect(self.ocr)

    # 划区域识别
    def ocr(self, box):
        self.label.close()
        del self.label  # del前必须先close
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口
        if box[0] != 'esc':
            self.OCR = lazy_import(
                'mytools.AIScreenshot.OCRScrollOut').OCRGeneral(box=box)
            self.OCR.signal.connect(self.ocrResult)
            self.OCR.start()

    def savePic(self, box):
        """截图完成回调函数"""
        self.label.close()
        del self.label  # del前必须先close
        # 截完图做啥操作
        originalPixmap = lazy_import(
            'myutils.window_handle.ScreenShot').ScreenShot().shot_screen(box=box)
        dialog = lazy_import(
            'ui.screendrawdialog_event').ShotDialog(originalPixmap)
        dialog.exec_()
        if not self.isMinimized():
            self.show()  # 截图完成显示窗口

    def pauseScan(self):
        self.PO.stop()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "退出提示",
            "<font color=gray>是否最小化至系统托盘？</font>",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.ignore()
            self.hide()
            self.systray.show()  # 显示最小化托盘图标
            self.systray.showMessage("通知", "已最小化到托盘")
        else:
            event.accept()
            self.systray.hide()
            if hasattr(self, "mc") and self.mc:
                self.mc.hide()  # 隐藏配置菜单
            if hasattr(self, "retail_info_window") and self.retail_info_window:
                self.retail_info_window.hide()  # 隐藏详情页
            if hasattr(self, "PO"):
                self.PO.stop()
# 扩展QApplication是为了捕获所有事件，看下什么在影响GUI主线程


class App(QApplication):
    def notify(self, eventobject: QObject, event: QEvent):
        """
        本次重写notify是为了截获应用的所有事件，并针对鼠标和键盘按下事件输出事件相关的信息
        :param eventobject: 事件接收对象
        :param event: 具体事件
        :return: True表示事件已经处理，False表示没有处理，需要继续往下传递
        """
        eventtype = event.type()
        print(
            f'所有事件类型{eventtype},事件接收者:{eventobject}，child={eventobject.children()}')
        flag = eventtype in [QEvent.Close,
                             QEvent.KeyPress, QEvent.MouseButtonPress]
        if flag:
            print("-----------------")
            print(
                f"In app notify:事件类型值={eventtype}，事件接收者:{eventobject},parent={eventobject.parent()},child={eventobject.children()}")

        ret = super().notify(eventobject, event)
        if flag:
            print("***************")
            print(
                f"App notify end,事件接收者:{eventobject}，事件返回值={ret},app={self},parent={eventobject.parent()}")
        return ret


if __name__ == "__main__":
    QThreadPool.globalInstance().setMaxThreadCount(3)
    # 最先启动ocr服务，比较慢，尽量早启动
    startup_ocrserver()
    # cgitb.enable(1, None, 5, "")
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(open("ui/style.qss", "rb").read().decode("utf-8"))
    SCREEN_WIDTH = QGuiApplication.primaryScreen().availableGeometry().width()
    SCREEN_HEIGHT = QGuiApplication.primaryScreen().availableGeometry().height()
    globalvar.set_var("SCREEN_WIDTH", SCREEN_WIDTH)
    globalvar.set_var("SCREEN_HEIGHT", SCREEN_HEIGHT)
    window = Main()
    window.show()
    sys.exit(app.exec())
