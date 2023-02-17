# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manage_config.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListWidget, QListWidgetItem,
    QSizePolicy, QStackedWidget, QWidget)

from biz.monitor_work_flow.ui.flowremindtype import FlowRemindType
from biz.monitor_work_flow.ui.pagefingerprint_event import PageFingerprint
from biz.monitor_work_flow.ui.pagetoflow import PageToFlow
from biz.monitor_work_flow.ui.remindtype import RemindType
from biz.monitor_work_flow.ui.workflow import WorkFlow
import pic_rc

class Ui_ManagerConfig(object):
    def setupUi(self, ManagerConfig):
        if not ManagerConfig.objectName():
            ManagerConfig.setObjectName(u"ManagerConfig")
        ManagerConfig.resize(1023, 498)
        self.horizontalLayout = QHBoxLayout(ManagerConfig)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(ManagerConfig)
        icon = QIcon()
        icon.addFile(u":/01/icon/01.ico", QSize(), QIcon.Normal, QIcon.Off)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setIcon(icon);
        icon1 = QIcon()
        icon1.addFile(u":/02/icon/02.ico", QSize(), QIcon.Normal, QIcon.Off)
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setIcon(icon1);
        icon2 = QIcon()
        icon2.addFile(u":/07/icon/07.ico", QSize(), QIcon.Normal, QIcon.Off)
        font = QFont()
        font.setUnderline(True)
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem2.setFont(font);
        __qlistwidgetitem2.setIcon(icon2);
        icon3 = QIcon()
        icon3.addFile(u":/06/icon/06.ico", QSize(), QIcon.Normal, QIcon.Off)
        __qlistwidgetitem3 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem3.setIcon(icon3);
        __qlistwidgetitem4 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem4.setIcon(icon2);
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.listWidget)

        self.stackedWidget = QStackedWidget(ManagerConfig)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.stackedWidget.setLineWidth(0)
        self.PF = PageFingerprint()
        self.PF.setObjectName(u"PF")
        self.stackedWidget.addWidget(self.PF)
        self.PFL = PageToFlow()
        self.PFL.setObjectName(u"PFL")
        self.stackedWidget.addWidget(self.PFL)
        self.FR = FlowRemindType()
        self.FR.setObjectName(u"FR")
        self.stackedWidget.addWidget(self.FR)
        self.WF = WorkFlow()
        self.WF.setObjectName(u"WF")
        self.stackedWidget.addWidget(self.WF)
        self.RT = RemindType()
        self.RT.setObjectName(u"RT")
        self.stackedWidget.addWidget(self.RT)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 9)

        self.retranslateUi(ManagerConfig)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(ManagerConfig)
    # setupUi

    def retranslateUi(self, ManagerConfig):
        ManagerConfig.setWindowTitle(QCoreApplication.translate("ManagerConfig", u"Form", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("ManagerConfig", u"\u9875\u9762\u6307\u7eb9", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("ManagerConfig", u"\u9875\u9762\u5bf9\u5e94\u6d41\u7a0b", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("ManagerConfig", u"\u6d41\u7a0b\u914d\u7f6e\u63d0\u9192", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("ManagerConfig", u"\u6d41\u7a0b\u6e05\u5355", None));
        ___qlistwidgetitem4 = self.listWidget.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("ManagerConfig", u"\u63d0\u9192\u5206\u7c7b", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

