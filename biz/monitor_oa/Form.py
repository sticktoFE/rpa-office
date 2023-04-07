# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Form.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(825, 772)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.label_8)

        self.rpa_client = QCheckBox(self.centralwidget)
        self.rpa_client.setObjectName(u"rpa_client")
        self.rpa_client.setChecked(True)

        self.horizontalLayout_10.addWidget(self.rpa_client)

        self.rpa_server = QCheckBox(self.centralwidget)
        self.rpa_server.setObjectName(u"rpa_server")

        self.horizontalLayout_10.addWidget(self.rpa_server)

        self.remember_check = QCheckBox(self.centralwidget)
        self.remember_check.setObjectName(u"remember_check")

        self.horizontalLayout_10.addWidget(self.remember_check)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.userID = QLineEdit(self.centralwidget)
        self.userID.setObjectName(u"userID")

        self.horizontalLayout_2.addWidget(self.userID)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.passwd = QLineEdit(self.centralwidget)
        self.passwd.setObjectName(u"passwd")
        self.passwd.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.passwd)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.taskTableWidget = QTableWidget(self.centralwidget)
        if (self.taskTableWidget.columnCount() < 5):
            self.taskTableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.taskTableWidget.setObjectName(u"taskTableWidget")
        sizePolicy.setHeightForWidth(self.taskTableWidget.sizePolicy().hasHeightForWidth())
        self.taskTableWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.taskTableWidget)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.fileAdd = QPushButton(self.centralwidget)
        self.fileAdd.setObjectName(u"fileAdd")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fileAdd.sizePolicy().hasHeightForWidth())
        self.fileAdd.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.fileAdd)

        self.fileRemove = QPushButton(self.centralwidget)
        self.fileRemove.setObjectName(u"fileRemove")
        sizePolicy1.setHeightForWidth(self.fileRemove.sizePolicy().hasHeightForWidth())
        self.fileRemove.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.fileRemove)

        self.horizontalLayout_5.setStretch(0, 5)
        self.horizontalLayout_5.setStretch(1, 5)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout.setStretch(0, 9)
        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_5.addLayout(self.verticalLayout)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_7)

        self.interval_edit = QLineEdit(self.centralwidget)
        self.interval_edit.setObjectName(u"interval_edit")

        self.horizontalLayout.addWidget(self.interval_edit)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_11)

        self.set_time = QLineEdit(self.centralwidget)
        self.set_time.setObjectName(u"set_time")

        self.horizontalLayout_13.addWidget(self.set_time)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.data_start_date = QLineEdit(self.centralwidget)
        self.data_start_date.setObjectName(u"data_start_date")

        self.horizontalLayout_11.addWidget(self.data_start_date)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.data_end_date = QLineEdit(self.centralwidget)
        self.data_end_date.setObjectName(u"data_end_date")

        self.horizontalLayout_12.addWidget(self.data_end_date)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_12)


        self.verticalLayout_4.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName(u"start")
        sizePolicy1.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.start)

        self.stop = QPushButton(self.centralwidget)
        self.stop.setObjectName(u"stop")
        sizePolicy1.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.stop)

        self.start_now = QPushButton(self.centralwidget)
        self.start_now.setObjectName(u"start_now")
        sizePolicy1.setHeightForWidth(self.start_now.sizePolicy().hasHeightForWidth())
        self.start_now.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.start_now)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.verticalLayout_5.setStretch(0, 1)
        self.verticalLayout_5.setStretch(1, 6)
        self.verticalLayout_5.setStretch(2, 2)

        self.horizontalLayout_15.addLayout(self.verticalLayout_5)

        self.out_log = QTextEdit(self.centralwidget)
        self.out_log.setObjectName(u"out_log")

        self.horizontalLayout_15.addWidget(self.out_log)

        self.horizontalLayout_15.setStretch(0, 6)
        self.horizontalLayout_15.setStretch(1, 4)

        self.verticalLayout_6.addLayout(self.horizontalLayout_15)

        Form.setCentralWidget(self.centralwidget)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.userID)
        self.label_2.setBuddy(self.passwd)
        self.label_7.setBuddy(self.interval_edit)
        self.label_11.setBuddy(self.interval_edit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.userID, self.passwd)
        QWidget.setTabOrder(self.passwd, self.fileAdd)
        QWidget.setTabOrder(self.fileAdd, self.fileRemove)
        QWidget.setTabOrder(self.fileRemove, self.taskTableWidget)
        QWidget.setTabOrder(self.taskTableWidget, self.interval_edit)
        QWidget.setTabOrder(self.interval_edit, self.start)
        QWidget.setTabOrder(self.start, self.out_log)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"auto_mobile", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u7aef", None))
        self.rpa_client.setText(QCoreApplication.translate("Form", u"\u5ba2\u6237\u7aef", None))
        self.rpa_server.setText(QCoreApplication.translate("Form", u"\u670d\u52a1\u7aef", None))
        self.remember_check.setText(QCoreApplication.translate("Form", u"\u8bb0\u4f4f\u5bc6\u7801", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u90ae\u7bb1", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u7528\u6237", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u5bc6\u7801", None))
        ___qtablewidgetitem = self.taskTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u7c7b\u578b", None));
        ___qtablewidgetitem1 = self.taskTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d", None));
        ___qtablewidgetitem2 = self.taskTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u7528\u6237\u5bc6\u7801", None));
        ___qtablewidgetitem3 = self.taskTableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u6267\u884c\u722c\u866b\u540d\u79f0", None));
        ___qtablewidgetitem4 = self.taskTableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u72b6\u6001", None));
        self.fileAdd.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.fileRemove.setText(QCoreApplication.translate("Form", u"\u79fb\u9664", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u6267\u884c\u95f4\u9694\uff08\u79d2\uff09\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u6bcf\u65e5\u5b9a\u65f6\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u8d77\u59cb\u65e5", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u622a\u81f3\u65e5", None))
        self.start.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
        self.stop.setText(QCoreApplication.translate("Form", u"\u505c\u6b62", None))
        self.start_now.setText(QCoreApplication.translate("Form", u"\u7acb\u5373\u5f00\u59cb", None))
    # retranslateUi

