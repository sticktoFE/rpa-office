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
        self.horizontalLayout_14 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
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


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

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

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.userID_oa = QLineEdit(self.centralwidget)
        self.userID_oa.setObjectName(u"userID_oa")

        self.horizontalLayout_7.addWidget(self.userID_oa)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.passwd_oa = QLineEdit(self.centralwidget)
        self.passwd_oa.setObjectName(u"passwd_oa")
        self.passwd_oa.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_8.addWidget(self.passwd_oa)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.data_start_date = QLineEdit(self.centralwidget)
        self.data_start_date.setObjectName(u"data_start_date")

        self.horizontalLayout_11.addWidget(self.data_start_date)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.data_end_date = QLineEdit(self.centralwidget)
        self.data_end_date.setObjectName(u"data_end_date")

        self.horizontalLayout_12.addWidget(self.data_end_date)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)


        self.verticalLayout_5.addLayout(self.verticalLayout_6)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
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

        self.taskTableWidget = QTableWidget(self.centralwidget)
        if (self.taskTableWidget.columnCount() < 3):
            self.taskTableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.taskTableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.taskTableWidget.setObjectName(u"taskTableWidget")
        sizePolicy.setHeightForWidth(self.taskTableWidget.sizePolicy().hasHeightForWidth())
        self.taskTableWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.taskTableWidget)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 9)

        self.verticalLayout_7.addLayout(self.verticalLayout)

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

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName(u"start")
        sizePolicy1.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.start)

        self.start_now = QPushButton(self.centralwidget)
        self.start_now.setObjectName(u"start_now")
        sizePolicy1.setHeightForWidth(self.start_now.sizePolicy().hasHeightForWidth())
        self.start_now.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.start_now)

        self.stop = QPushButton(self.centralwidget)
        self.stop.setObjectName(u"stop")
        sizePolicy1.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy1)

        self.horizontalLayout_9.addWidget(self.stop)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)


        self.verticalLayout_7.addLayout(self.verticalLayout_4)


        self.horizontalLayout_14.addLayout(self.verticalLayout_7)

        self.out_log = QTextEdit(self.centralwidget)
        self.out_log.setObjectName(u"out_log")

        self.horizontalLayout_14.addWidget(self.out_log)

        Form.setCentralWidget(self.centralwidget)
#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.userID)
        self.label_2.setBuddy(self.passwd)
        self.label_5.setBuddy(self.userID_oa)
        self.label_6.setBuddy(self.passwd_oa)
        self.label_9.setBuddy(self.userID_oa)
        self.label_10.setBuddy(self.userID_oa)
        self.label_7.setBuddy(self.interval_edit)
        self.label_11.setBuddy(self.interval_edit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.userID, self.passwd)
        QWidget.setTabOrder(self.passwd, self.userID_oa)
        QWidget.setTabOrder(self.userID_oa, self.passwd_oa)
        QWidget.setTabOrder(self.passwd_oa, self.fileAdd)
        QWidget.setTabOrder(self.fileAdd, self.fileRemove)
        QWidget.setTabOrder(self.fileRemove, self.taskTableWidget)
        QWidget.setTabOrder(self.taskTableWidget, self.interval_edit)
        QWidget.setTabOrder(self.interval_edit, self.start_now)
        QWidget.setTabOrder(self.start_now, self.start)
        QWidget.setTabOrder(self.start, self.out_log)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"auto_mobile", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u8fd0\u884c\u7aef", None))
        self.rpa_client.setText(QCoreApplication.translate("Form", u"\u5ba2\u6237\u7aef", None))
        self.rpa_server.setText(QCoreApplication.translate("Form", u"\u670d\u52a1\u7aef", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u90ae\u7bb1", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u7528\u6237", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u5bc6\u7801", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"OA", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u7528\u6237", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u5bc6\u7801", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u5f00\u59cb\u65e5\u671f", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7ed3\u675f\u65e5\u671f", None))
        self.fileAdd.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.fileRemove.setText(QCoreApplication.translate("Form", u"\u79fb\u9664", None))
        ___qtablewidgetitem = self.taskTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u6a21\u5757", None));
        ___qtablewidgetitem1 = self.taskTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u5bf9\u8c61", None));
        ___qtablewidgetitem2 = self.taskTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u65b9\u6cd5", None));
        self.label_7.setText(QCoreApplication.translate("Form", u"\u6267\u884c\u95f4\u9694\uff08\u79d2\uff09\uff1a", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u6bcf\u65e5\u5b9a\u65f6\uff1a", None))
        self.start.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb", None))
        self.start_now.setText(QCoreApplication.translate("Form", u"\u7acb\u5373\u5f00\u59cb", None))
        self.stop.setText(QCoreApplication.translate("Form", u"\u505c\u6b62", None))
    # retranslateUi

