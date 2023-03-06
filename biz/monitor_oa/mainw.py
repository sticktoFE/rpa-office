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
from biz.monitor_oa.manager import RPAClient, RPAServer
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
from Form import Ui_Form

"""Redirects console output to text widget."""


class Stream(QObject):
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
        userID_oa = self.settings.value("userID_oa")
        if userID_oa is not None:
            self.userID_oa.setText(userID_oa)
            password_oa = self.settings.value("password_oa")
            self.password_oa.setText(dectry(password_oa))
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run_command)

    @Slot()
    def on_start_clicked(self):
        interval = int(self.interval_edit.text())
        self.timer.start(interval * 1000)
        self.start.setEnabled(False)
        self.stop.setEnabled(True)

    @Slot()
    def on_stop_clicked(self):
        self.timer.stop()
        self.start.setEnabled(True)
        self.stop.setEnabled(False)

    def run_command(self):
        # 执行命令
        userID = self.userID.text()
        password = self.password.text()
        userID_oa = self.userID_oa.text()
        password_oa = self.password_oa.text()
        if len(userID) == 0 or len(password) == 0:
            QMessageBox.warning(self, "注意", "邮箱用户名或密码都不能为空")
        else:
            # 默认保存登录信息，快捷开始
            self.settings.setValue("userID", userID)
            self.settings.setValue("password", enctry(password))
            self.settings.setValue("userID_oa", userID_oa)
            self.settings.setValue("password_oa", enctry(password_oa))
            if self.RPAClient.isChecked():
                RPAClient(userID_oa, password_oa, userID, password).have_done()
            elif self.RPAServer.isChecked():
                RPAServer(userID, password).have_done()
            # 循环刷新界面，以显示最新日志内容
            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit)
            loop.exec()

    # 后期可以在界面添加编排任务，然后在此处解析循环执行
    def task_execute(self, userID, password, userID_oa, password_oa):
        # 默认保存登录信息，快捷开始
        self.settings.setValue("userID", userID)
        self.settings.setValue("password", enctry(password))
        self.settings.setValue("userID_oa", userID_oa)
        self.settings.setValue("password_oa", enctry(password_oa))
        # 暂时支持一行，后面可以实现编排并增加优先级，按优先级顺序执行
        # 获取第一行第一列单元格对象
        item = self.taskTableWidget.item(0, 0)
        # 检查单元格是否为空
        if item is not None:
            # 获取单元格文本
            module_ = item.text()
            object_ = self.taskTableWidget.cellWidget(0, 1).currentText()
            class_method_ = self.taskTableWidget.cellWidget(0, 2).currentText()
            worker_server = Worker(
                object_,
                classMethod=class_method_,
                module=module_,
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
        item_module = QTableWidgetItem("biz.monitor_oa.manager")
        item_module.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.taskTableWidget.setItem(row, 0, item_module)

        comBox_object = QComboBox()
        comBox_object.addItems(["RPAServer", "RPAClient"])
        self.taskTableWidget.setCellWidget(row, 1, comBox_object)

        comBox_class_method = QComboBox()
        comBox_class_method.addItems(["to_do", "have_done"])
        self.taskTableWidget.setCellWidget(row, 2, comBox_class_method)

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

    # 点击任务开始
    @Slot()
    def on_start_now_clicked(self):
        self.run_command()

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
