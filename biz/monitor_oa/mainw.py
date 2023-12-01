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
    QStyledItemDelegate,
    QLineEdit,
    QStyle,
)
from biz.monitor_oa.manager import RPAClient, RPAServer
from myutils.DateAndTime import get_date, get_weeks_current_date
from myutils.GeneralQThread import Worker
from Form import Ui_Form
import schedule

# import win32timezone
from keyring.backends import Windows
import keyring

from myutils.info_out_manager import get_temp_folder

keyring.set_keyring(Windows.WinVaultKeyring())


# 为QTableWidget设置密码输入框
class PasswordDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setEchoMode(QLineEdit.EchoMode.Password)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        style = option.widget.style() or QApplication.style()
        hint = style.styleHint(QStyle.StyleHint.SH_LineEdit_PasswordCharacter)
        option.text = chr(hint) * len(option.text)


# 把print输出到重定向窗口中
class Stream(QObject):
    newText = Signal(str)

    def write(self, text):
        self.newText.emit(str(text))


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Set the delegate for the password column
        delegate = PasswordDelegate()
        self.taskTableWidget.setItemDelegateForColumn(2, delegate)
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
                config_parameter_row_count = keyring.get_password(
                    "myapp", "config_parameter_row_count"
                )
                for one_para in range(
                    int(
                        0
                        if config_parameter_row_count is None
                        else config_parameter_row_count
                    )
                ):
                    userID_oa_ = keyring.get_password("myapp", f"userID_oa_{one_para}")
                    passwd_oa_ = keyring.get_password("myapp", f"passwd_oa_{one_para}")
                    which_tab_ = keyring.get_password(
                        "myapp", f"which_tab_oa_{one_para}"
                    )
                    scrapy_oa_ = keyring.get_password("myapp", f"scrapy_oa_{one_para}")
                    self.insert_row_inTable(
                        "OA", userID_oa_, passwd_oa_, which_tab_, scrapy_oa_, "有效"
                    )
            except keyring.errors.NoKeyringError:
                # 如果没有安装任何密钥环后端，使用默认密码
                userID = ""
                passwd = ""
            self.userID.setText(userID)
            self.passwd.setText(passwd)

        yesterday_str = get_weeks_current_date()[0]
        today_str = get_weeks_current_date()[1]
        self.data_start_date.setText(yesterday_str)
        self.data_end_date.setText(today_str)
        self.scheduled_jobs = []
        self.srapy_running = False
        self.set_time.setText("11:30~19:00~22:00")
        self.out_folder = get_temp_folder(
            des_folder_path=__file__, is_clear_folder=True
        )

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

    # 执行相关任务的总方法
    def run_command(self, data_start_date, data_end_date):
        # 执行命令
        userID = self.userID.text()
        passwd = self.passwd.text()
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
            # 可以增加多个oa登录账号和密码，放到userID_Passwd
            scrapy_info = []
            config_parameter_row_count = self.taskTableWidget.rowCount()
            # 记录行数，为了启动初始化时，知道增加多少记录
            if self.remember_check.isChecked():
                keyring.set_password(
                    "myapp", "config_parameter_row_count", config_parameter_row_count
                )
            for row in range(config_parameter_row_count):
                item_type = self.taskTableWidget.cellWidget(row, 0).currentText()
                item_status = self.taskTableWidget.cellWidget(row, 5).currentText()
                if item_type is not None and item_type == "OA" and item_status == "有效":
                    # 获取单元格文本
                    item_user = self.taskTableWidget.item(row, 1).text()
                    item_passwd = self.taskTableWidget.item(row, 2).text()
                    item_which_tab = self.taskTableWidget.cellWidget(
                        row, 3
                    ).currentText()
                    item_scrapy = self.taskTableWidget.cellWidget(row, 4).currentText()
                    if self.remember_check.isChecked():
                        keyring.set_password("myapp", f"userID_oa_{row}", item_user)
                        keyring.set_password("myapp", f"passwd_oa_{row}", item_passwd)
                        keyring.set_password(
                            "myapp", f"which_tab_oa_{row}", item_which_tab
                        )
                        keyring.set_password("myapp", f"scrapy_oa_{row}", item_scrapy)
                    scrapy_info.append(
                        {
                            "user_id": item_user,
                            "user_passwd": item_passwd,
                            "which_tab": item_which_tab,
                            "start_date": data_start_date,
                            "end_date": data_end_date,
                            "spider_name": item_scrapy,
                            "out_file": f"{self.out_folder}/{item_user}_{item_which_tab}.txt",
                        }
                    )
            if self.rpa_client.isChecked():
                # 打开代理
                # start_ip_proxy()
                # 1、打包启动
                worK_server = Worker(
                    RPAClient,
                    classMethod="have_done",
                    classMethodArgs={},
                    scrapy_info=scrapy_info,
                    mail_userID=userID,
                    mail_passwd=passwd,
                    out_folder=self.out_folder,
                )
                QThreadPool.globalInstance().start(worK_server)
                # 调试用，开子线程无法调试
                # RPAClient(scrapy_info, userID, passwd, self.out_folder).have_done()
            elif self.rpa_server.isChecked():
                QThreadPool.globalInstance().start(
                    Worker(
                        RPAServer,
                        classMethod="start",
                        classMethodArgs={},
                        mail_userID=userID,
                        mail_passwd=passwd,
                        out_folder=self.out_folder,
                    )
                )
                # 调试用，开子线程无法调试
                # RPAServer(userID, passwd).start()
            # 循环刷新界面，以显示最新日志内容
            loop = QEventLoop()
            QTimer.singleShot(2000, loop.quit)
            loop.exec()

    # 展示任务进程
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.out_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.out_log.setTextCursor(cursor)
        self.out_log.ensureCursorVisible()

    def insert_row_inTable(self, account_type, user, passwd, which_tab, scrapy, status):
        row = self.taskTableWidget.rowCount()
        # 在末尾插入一空行
        self.taskTableWidget.insertRow(row)
        comBox_class_method = QComboBox()
        comBox_class_method.addItems(["OA", "EMAIL"])
        comBox_class_method.setCurrentText(account_type)
        self.taskTableWidget.setCellWidget(row, 0, comBox_class_method)
        # 用户名
        item_user = QTableWidgetItem(user)
        item_user.setFlags(item_user.flags() | Qt.ItemFlag.ItemIsEditable)
        self.taskTableWidget.setItem(row, 1, item_user)
        # 密码
        item_passwd = QTableWidgetItem(passwd)
        item_passwd.setFlags(item_passwd.flags() | Qt.ItemFlag.ItemIsEditable)
        self.taskTableWidget.setItem(row, 2, item_passwd)
        # 执行哪一个栏目
        comBox_which_tab = QComboBox()
        # addItem 参数为text 和 data值，如果两者一样，可以用addItems即可
        comBox_which_tab.addItems(["已处理", "已办结"])
        comBox_which_tab.setCurrentText(which_tab)  # 选择哪个值
        self.taskTableWidget.setCellWidget(row, 3, comBox_which_tab)
        # 执行的爬虫对象
        comBox_scrapy_name = QComboBox()
        # addItem 参数为text 和 data值，如果两者一样，可以用addItems即可
        comBox_scrapy_name.addItems(
            ["csrc_penalty", "OAProAdmitHaveDone", "csrc_market_weekly"]
        )
        comBox_scrapy_name.setCurrentText(scrapy)  # 选择哪个值
        self.taskTableWidget.setCellWidget(row, 4, comBox_scrapy_name)
        # 状态
        comBox_class_method = QComboBox()
        comBox_class_method.addItems(["有效", "无效"])
        comBox_class_method.setCurrentText(status)  # 选择哪个值
        self.taskTableWidget.setCellWidget(row, 5, comBox_class_method)

    # 点击添加文件
    @Slot()
    def on_fileAdd_clicked(self):
        self.insert_row_inTable("OA", "", "", "已处理", "OAProAdmitHaveDone", "有效")

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
