import sys
import time
from PySide6.QtCore import (
    QThreadPool,
    Signal,
    QObject,
    QEventLoop,
    QTimer,
    QSettings,
    Qt,
)
from myutils.GeneralThread import Worker
from myutils.info_secure import dectry, enctry
from PySide6.QtCore import Slot
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QTableWidgetItem,
    QComboBox,
)
from ui.OCRResult_event import TotalMessage
from Form import Ui_Form


class Stream(QObject):
    """Redirects console output to text widget."""

    newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainWindow(QMainWindow, Ui_Form):
    t_temp = time.perf_counter()
    delay_time = 500

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 把标准输出展示到重定向窗口中
        redirect_out = Stream()
        redirect_out.newText.connect(self.onUpdateText)
        sys.stdout = redirect_out
        self.settings = QSettings("./config.ini", QSettings.Format.IniFormat)
        # 如果输入登录信息保存了，自动回显到输入框里
        userID = self.settings.value("userID")
        if userID is not None:
            self.userID.setText(userID)
            password = self.settings.value("password")
            self.password.setText(dectry(password))
        # 对imageLabel读图片的路径进行初始化
        # self.ui.screenLabel.setImagePath("biz/infoTracing/image/resized_screen.png")
        # # self.ui.screenLabel.resize(self.src_width/3,self.src_heigth/3)
        # self.ui.screenLabel.setPixmap(QPixmap("biz/infoTracing/image/1.jpg"))
        # self.ui.screenLabel.mousePressSignal.connect(self.imageLabelPressSlot)
        # self.ui.screenLabel.mouseDragSignal.connect(self.imageLabelDragSlot)

    # 展示任务进程
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.out_log.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.out_log.setTextCursor(cursor)
        self.out_log.ensureCursorVisible()

    # 点击添加文件
    @Slot()
    def on_fileAdd_clicked(self):
        row = self.taskTableWidget.rowCount()
        # 在末尾插入一空行
        self.taskTableWidget.insertRow(row)
        item_path = QTableWidgetItem("biz.monitor_oa.manager")
        item_path.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.taskTableWidget.setItem(row, 0, item_path)

        comBox_package = QComboBox()
        comBox_package.addItems(["RPAServer", "RPAClient"])
        self.taskTableWidget.setCellWidget(row, 1, comBox_package)

        comBox_method = QComboBox()
        comBox_method.addItems(["to_do", "have_done"])
        self.taskTableWidget.setCellWidget(row, 2, comBox_method)

    # 点击移除
    @Slot()
    def on_fileRemove_clicked(self):
        # root = self.taskTreeWidget.invisibleRootItem()
        # for item in self.taskTreeWidget.selectedItems():
        #     (item.parent() or root).removeChild(item)
        row_select = self.taskTableWidget.selectedItems()
        if len(row_select) == 0:
            return
        row_2 = self.taskTableWidget.currentRow()
        self.taskTableWidget.removeRow(row_2)

    # 点击任务终止
    @Slot()
    def on_taskStop_clicked(self):
        self.mt.terminate()

    # 点击任务开始
    @Slot()
    def on_taskStart_clicked(self):
        userID = self.userID.text()
        password = self.password.text()
        if len(userID) == 0 or len(password) == 0:
            QMessageBox.warning(self, "注意", "邮箱用户名或密码都不能为空")
        else:
            # 默认保存登录信息，快捷开始
            self.settings.setValue("userID", userID)
            self.settings.setValue("password", enctry(password))
            # 暂时支持一行，后面可以实现编排并增加优先级，按优先级顺序执行
            # row = self.taskTableWidget.currentRow()
            # if row == -1:
            # 获取第一行第一列单元格对象
            item = self.taskTableWidget.item(0, 0)
            # 检查单元格是否为空
            if item is not None:
                # 获取单元格文本
                path_ = item.text()
                package_ = self.taskTableWidget.cellWidget(0, 1).currentText()
                method_ = self.taskTableWidget.cellWidget(0, 2).currentText()
                worker_server = Worker(
                    package_,
                    classMethod=method_,
                    module=path_,
                    mail_userID=userID,
                    mail_passwd=password,
                )
                QThreadPool.globalInstance().start(worker_server)
                # 循环刷新界面，以显示最新日志内容
                loop = QEventLoop()
                QTimer.singleShot(2000, loop.quit)
                loop.exec()
            else:
                QMessageBox.warning(self, "注意", "请新增任务")
                return

    def ocrResult(self, result):
        self.ocrmg = TotalMessage("".join(result))
        self.ocrmg.show()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # reset stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
