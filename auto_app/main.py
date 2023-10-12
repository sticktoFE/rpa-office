import re
import sys
from PySide6.QtCore import QThreadPool
from auto_app.get_licai import get_app_info
from model.OCRServer import startup_ocrserver
from auto_app.AppActionExecThread import AppExec
from mytools.screen_shot.OCRThread import ScreenShotTasks
from myutils.DateAndTime import get_date
from myutils.GeneralQThread import Worker
from pynput.mouse import Controller
from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTreeWidgetItem,
)
from myutils.info_out_manager import dump_json_table, get_temp_folder
from ui.OCRResult_event import TotalMessage
from Form import Ui_Form


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.mouse = Controller()
        self.content_out_folder = get_temp_folder(
            execute_file_path=__file__, is_clear_folder=True
        )
        self.content_out_file = f"{self.content_out_folder}/product_info.txt"

        self.screenshot = ScreenShotTasks()
        self.screenshot.result.connect(self.after_auto_roll)
        # 直接启动拼接线程才启动
        self.screenshot.start()
        self.worker = Worker(get_app_info, self.screenshot)

        self.temp_product_list = {"date": get_date()}

    @Slot()
    def on_actionStartPushButton_clicked(self):
        QThreadPool.globalInstance().start(self.worker)

    def after_auto_roll(self, result):
        content = " ".join(result[2])
        content = re.sub(r"\n", " ", content)
        content = re.sub(r"\d+:\d+|C?\s*<?\s*理财详情[\s<]*|关注|立即购买", "", content).strip()
        content = re.sub(r"^D |查看更多√|查看更多V", "", content).strip()
        # 产品名称默认格式为中文 英文 下划线 数字
        match_result = re.search(
            r"[\u4e00-\u9fa5a-zA-Z0-9_-]+(?:\s*[（(][\s\u4e00-\u9fa5a-zA-Z0-9_-]+[)）]\s*[\u4e00-\u9fa5a-zA-Z0-9_-]*)*\s+",
            content,
        )
        product_name = match_result.group()
        product_name = re.sub(r"\s", "", product_name)
        self.temp_product_list[product_name] = content
        print(
            f"-----------------------------------------------{self.temp_product_list}"
        )

    @Slot()
    def on_taskStopPushButton_clicked(self):
        self.screenshot.stop_thread()

    def closeEvent(self, event) -> None:
        self.screenshot.stop_thread()
        dump_json_table(self.temp_product_list, self.content_out_file, False)
        return super().closeEvent(event)

    # 点击添加文件
    @Slot()
    def on_fileAddPushButton_clicked(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "../mobile_action", "(*.json)"
        )
        filename = path.split("/")[-1].split(".")[0]
        print(filename)
        item = QTreeWidgetItem(self.ui.taskTreeWidget)
        item.setText(0, filename)

    # 点击移除
    @Slot()
    def on_fileRemovePushButton_clicked(self):
        root = self.ui.taskTreeWidget.invisibleRootItem()
        for item in self.ui.taskTreeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    @Slot()
    def on_autoClickScreenShot_clicked(self):
        for_pics = [
            "utils/AppCrawler/image/app_manager.png",
            "utils/AppCrawler/image/clear.png",
            "utils/AppCrawler/image/vphone.png",
            "utils/AppCrawler/image/skip_one.png",
            "utils/AppCrawler/image/skip_two.png",
            "utils/AppCrawler/image/shutdownad.png",
            # utilsiAppCrawlerng/image/upslip.png",
            "utils/AppCrawler/image/zy.png",
            "utils/AppCrawler/image/workstation.png",
            "utils/AppCrawler/image/notice.png",
            "utils/AppCrawler/image/import_notice.png",
            "utils/AppCrawler/image/all_news.png",
        ]
        self.OCR = AppExec(window_name="多屏协同", for_pics=for_pics)
        self.OCR.signal.connect(self.ocrResult)
        self.OCR.start()

    def ocrResult(self, result):
        self.ocrmg = TotalMessage("".join(result))
        self.ocrmg.show()


if __name__ == "__main__":
    QThreadPool.globalInstance().setMaxThreadCount(3)
    # 最先启动ocr服务，比较慢，尽量早启动
    startup_ocrserver()
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
