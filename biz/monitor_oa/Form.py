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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QMainWindow, QPushButton, QSizePolicy, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from ImageLabel import ImageLabel

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(418, 412)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(Form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.actionStartPushButton = QPushButton(self.centralwidget)
        self.actionStartPushButton.setObjectName(u"actionStartPushButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.actionStartPushButton.sizePolicy().hasHeightForWidth())
        self.actionStartPushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.actionStartPushButton, 2, 0, 1, 1)

        self.getScreenShotPushButton = QPushButton(self.centralwidget)
        self.getScreenShotPushButton.setObjectName(u"getScreenShotPushButton")
        sizePolicy1.setHeightForWidth(self.getScreenShotPushButton.sizePolicy().hasHeightForWidth())
        self.getScreenShotPushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.getScreenShotPushButton, 0, 0, 1, 1)

        self.taskStopPushButton = QPushButton(self.centralwidget)
        self.taskStopPushButton.setObjectName(u"taskStopPushButton")
        sizePolicy1.setHeightForWidth(self.taskStopPushButton.sizePolicy().hasHeightForWidth())
        self.taskStopPushButton.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.taskStopPushButton, 2, 1, 1, 1)

        self.autoClickScreenShot = QPushButton(self.centralwidget)
        self.autoClickScreenShot.setObjectName(u"autoClickScreenShot")
        sizePolicy1.setHeightForWidth(self.autoClickScreenShot.sizePolicy().hasHeightForWidth())
        self.autoClickScreenShot.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.autoClickScreenShot, 0, 1, 1, 1)

        self.recordActionPushButton = QPushButton(self.centralwidget)
        self.recordActionPushButton.setObjectName(u"recordActionPushButton")
        sizePolicy1.setHeightForWidth(self.recordActionPushButton.sizePolicy().hasHeightForWidth())
        self.recordActionPushButton.setSizePolicy(sizePolicy1)
        self.recordActionPushButton.setCheckable(True)
        self.recordActionPushButton.setChecked(True)

        self.gridLayout.addWidget(self.recordActionPushButton, 1, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.actionLoadWidget = QWidget(self.centralwidget)
        self.actionLoadWidget.setObjectName(u"actionLoadWidget")
        self.verticalLayout = QVBoxLayout(self.actionLoadWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileAddPushButton = QPushButton(self.actionLoadWidget)
        self.fileAddPushButton.setObjectName(u"fileAddPushButton")
        sizePolicy1.setHeightForWidth(self.fileAddPushButton.sizePolicy().hasHeightForWidth())
        self.fileAddPushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.fileAddPushButton)

        self.fileRemovePushButton = QPushButton(self.actionLoadWidget)
        self.fileRemovePushButton.setObjectName(u"fileRemovePushButton")
        sizePolicy1.setHeightForWidth(self.fileRemovePushButton.sizePolicy().hasHeightForWidth())
        self.fileRemovePushButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.fileRemovePushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.taskTreeWidget = QTreeWidget(self.actionLoadWidget)
        self.taskTreeWidget.headerItem().setText(1, "")
        self.taskTreeWidget.setObjectName(u"taskTreeWidget")
        sizePolicy.setHeightForWidth(self.taskTreeWidget.sizePolicy().hasHeightForWidth())
        self.taskTreeWidget.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.taskTreeWidget)


        self.verticalLayout_2.addWidget(self.actionLoadWidget)

        self.verticalLayout_2.setStretch(0, 3)
        self.verticalLayout_2.setStretch(1, 7)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.screenLabel = ImageLabel(self.centralwidget)
        self.screenLabel.setObjectName(u"screenLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(204)
        sizePolicy2.setVerticalStretch(115)
        sizePolicy2.setHeightForWidth(self.screenLabel.sizePolicy().hasHeightForWidth())
        self.screenLabel.setSizePolicy(sizePolicy2)
        self.screenLabel.setMouseTracking(True)
        self.screenLabel.setTabletTracking(True)
        self.screenLabel.setAcceptDrops(False)
        self.screenLabel.setAutoFillBackground(False)
        self.screenLabel.setStyleSheet(u"")
        self.screenLabel.setScaledContents(True)
        self.screenLabel.setAlignment(Qt.AlignCenter)
        self.screenLabel.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.screenLabel)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 8)
        Form.setCentralWidget(self.centralwidget)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"auto_mobile", None))
        self.actionStartPushButton.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u6267\u884c", None))
        self.getScreenShotPushButton.setText(QCoreApplication.translate("Form", u"\u83b7\u53d6\u5c4f\u5e55", None))
        self.taskStopPushButton.setText(QCoreApplication.translate("Form", u"\u4efb\u52a1\u7ec8\u6b62", None))
        self.autoClickScreenShot.setText(QCoreApplication.translate("Form", u"\u542f\u52a8\u4efb\u52a1", None))
        self.recordActionPushButton.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u5f55\u5236\u52a8\u4f5c", None))
        self.fileAddPushButton.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.fileRemovePushButton.setText(QCoreApplication.translate("Form", u"\u79fb\u9664", None))
        ___qtreewidgetitem = self.taskTreeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u4efb\u52a1\u5217\u8868", None));
        self.screenLabel.setText(QCoreApplication.translate("Form", u"\u56fe\u7247\u663e\u793a\u533a\u57df", None))
    # retranslateUi

