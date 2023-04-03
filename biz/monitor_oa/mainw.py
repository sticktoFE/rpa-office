import sys
from PySide6.QtCore import (
    QThreadPool,
    Signal,
    QObject,
    QSettings,
    Qt,
    Slot,
    QEventLoop,
    QTimer,
)
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QTableWidgetItem,
    QComboBox,
)
import keyring
from biz.monitor_oa.manager import RPAClient, RPAServer
from myutils.DateAndTime import get_date  # , start_ip_proxy
from myutils.GeneralThread import Worker
from Form import Ui_Form
import schedule

# 设置获取数据的日期
from datetime import date, datetime, timedelta

# import win32timezone
from keyring.backends import Windows

keyring.set_keyring(Windows.WinVaultKeyring())


class Stream(QObject):
    newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 把标准输出展示到重定向窗口中
        redirect_out = Stream()
        redirect_out.newText.connect(self.onUpdateText)
        sys.stdout = redirect_out
        self.config = QSettings("./config.ini", QSettings.Format.IniFormat)
        # 如果输入登录信息保存了，自动回显到输入框里
        # Load saved settings
        # 设置默认的密码存储后端 避免NoKeyringError异常
        # keyring.set_keyring(WinVaultKeyring())
        remember_me = self.config.value("remember_me", False, type=bool)
        self.remember_check.setChecked(remember_me)
        if remember_me:
            try:
                userID = keyring.get_password("myapp", "userID")
                passwd = keyring.get_password("myapp", userID)
                userID_oa = keyring.get_password("myapp", "userID_oa")
                passwd_oa = keyring.get_password("myapp", userID_oa)
            except keyring.errors.NoKeyringError:
                # 如果没有安装任何密钥环后端，使用默认密码
                userID = ""
                passwd = ""
                userID_oa = ""
                passwd_oa = ""
            self.userID.setText(userID)
            self.passwd.setText(passwd)
            self.userID_oa.setText(userID_oa)
            self.passwd_oa.setText(passwd_oa)

        today_str = get_date()
        yesterday_str = get_date(-1)
        self.data_start_date.setText(yesterday_str)
        self.data_end_date.setText(today_str)
        self.scheduled_jobs = []
        self.srapy_running = False
        self.set_time.setText("11:30~19:00~22:00")

    @Slot()
    def on_start_clicked(self):
        set_times = self.set_time.text()
        if len(set_times) == 0:
            QMessageBox.warning(
                self, "注意", "定时任务请在“每日定时中输入时间如16:00”,如多个，如16:00~19:00~24:00"
            )
            return
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        today_str = get_date()
        data_start_date = today_str
        data_end_date = today_str
        interval = self.interval_edit.text()
        for set_time in set_times.split("~"):
            # 设计一个定时器，支持间隔时间或者定时触发
            self.scheduled_jobs.append(
                schedule.every()
                .day.at(set_time)
                .do(self.run_command, data_start_date, data_end_date)
            )
        # schedule.every(int(interval * 1000)).minutes.do(self.run_command)
        print("Spider working now")
        while True:
            schedule.run_pending()
            app.processEvents()

    # 点击任务开始
    @Slot()
    def on_start_now_clicked(self):
        self.start_now.setEnabled(False)
        data_start_date = self.data_start_date.text()
        data_end_date = self.data_end_date.text()
        self.run_command(data_start_date, data_end_date)
        self.start_now.setEnabled(True)

    @Slot()
    def on_stop_clicked(self):
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        # Cancel the scheduled job
        for job in self.scheduled_jobs:
            schedule.cancel_job(job)
        self.scheduled_jobs.clear()

    def run_command(self, data_start_date, data_end_date):
        # 执行命令
        userID = self.userID.text()
        passwd = self.passwd.text()
        userID_oa = self.userID_oa.text()
        passwd_oa = self.passwd_oa.text()
        if len(userID) == 0 or len(passwd) == 0:
            QMessageBox.warning(self, "注意", "邮箱用户名或密码都不能为空")
        else:
            # 默认保存登录信息，快捷开始
            # 如果登录成功，保存“记住密码”选项和用户名到 QSettings 中
            self.config.setValue("remember_me", self.remember_check.isChecked())
            # 如果用户选择了“记住密码”选项，将用户名和密码保存到 Qt Keychain API 中
            if self.remember_check.isChecked():
                keyring.set_password("myapp", "userID", userID)
                keyring.set_password("myapp", userID, passwd)
                keyring.set_password("myapp", "userID_oa", userID_oa)
                keyring.set_password("myapp", userID_oa, passwd_oa)

            if self.rpa_client.isChecked():
                # 打开代理
                # start_ip_proxy()
                # 1、打包启动
                worK_server = Worker(
                    RPAClient,
                    classMethod="have_done",
                    classMethodArgs={},
                    scrapy_userID=userID_oa,
                    scrapy_passwd=passwd_oa,
                    mail_userID=userID,
                    mail_passwd=passwd,
                    data_start_date=data_start_date,
                    data_end_date=data_end_date,
                )
                QThreadPool.globalInstance().start(worK_server)

            elif self.rpa_server.isChecked():
                QThreadPool.globalInstance().start(
                    Worker(
                        RPAServer,
                        classMethod="start",
                        classMethodArgs={},
                        mail_userID=userID,
                        mail_passwd=passwd,
                    )
                )
            # 循环刷新界面，以显示最新日志内容
            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit)
            loop.exec()

    # 后期可以在界面添加编排任务，然后在此处解析循环执行
    def task_execute(self, userID, passwd, userID_oa, passwd_oa):
        # 默认保存登录信息，快捷开始
        # self.config.setValue("userID", userID)
        # self.config.setValue("passwd", enctry(passwd))
        # self.config.setValue("userID_oa", userID_oa)
        # self.config.setValue("passwd_oa", enctry(passwd_oa))
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
                mail_passwd=passwd,
            )
            QThreadPool.globalInstance().start(worker_server)
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
        row_select = self.taskTableWidget.selectedItems()
        if len(row_select) == 0:
            return
        row_2 = self.taskTableWidget.currentRow()
        self.taskTableWidget.removeRow(row_2)

    def closeEvent(self, event):
        sys.stdout = sys.__stdout__
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
