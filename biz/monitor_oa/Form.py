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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(587, 574)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_7 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
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

        self.password = QLineEdit(self.centralwidget)
        self.password.setObjectName(u"password")
        self.password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.password)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.taskStart = QPushButton(self.centralwidget)
        self.taskStart.setObjectName(u"taskStart")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.taskStart.sizePolicy().hasHeightForWidth())
        self.taskStart.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.taskStart)

        self.taskStop = QPushButton(self.centralwidget)
        self.taskStop.setObjectName(u"taskStop")
        sizePolicy1.setHeightForWidth(self.taskStop.sizePolicy().hasHeightForWidth())
        self.taskStop.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.taskStop)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.fileAdd = QPushButton(self.centralwidget)
        self.fileAdd.setObjectName(u"fileAdd")
        sizePolicy1.setHeightForWidth(self.fileAdd.sizePolicy().hasHeightForWidth())
        self.fileAdd.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.fileAdd)

        self.fileRemove = QPushButton(self.centralwidget)
        self.fileRemove.setObjectName(u"fileRemove")
        sizePolicy1.setHeightForWidth(self.fileRemove.sizePolicy().hasHeightForWidth())
        self.fileRemove.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.fileRemove)


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


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.out_log = QTextEdit(self.centralwidget)
        self.out_log.setObjectName(u"out_log")

        self.horizontalLayout_6.addWidget(self.out_log)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)

        Form.setCentralWidget(self.centralwidget)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"auto_mobile", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u90ae\u7bb1", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u7528\u6237", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u767b\u5f55\u5bc6\u7801", None))
        self.taskStart.setText(QCoreApplication.translate("Form", u"\u542f\u52a8\u4efb\u52a1", None))
        self.taskStop.setText(QCoreApplication.translate("Form", u"\u4efb\u52a1\u7ec8\u6b62", None))
        self.fileAdd.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.fileRemove.setText(QCoreApplication.translate("Form", u"\u79fb\u9664", None))
        ___qtablewidgetitem = self.taskTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u8def\u5f84", None));
        ___qtablewidgetitem1 = self.taskTableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u5305", None));
        ___qtablewidgetitem2 = self.taskTableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u65b9\u6cd5", None));
    # retranslateUi

