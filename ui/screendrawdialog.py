# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'screendrawdialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(396, 241)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_shot = QLabel(Dialog)
        self.label_shot.setObjectName(u"label_shot")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_shot.sizePolicy().hasHeightForWidth())
        self.label_shot.setSizePolicy(sizePolicy)
        self.label_shot.setScaledContents(False)

        self.verticalLayout.addWidget(self.label_shot)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_ocr = QPushButton(self.groupBox)
        self.pushButton_ocr.setObjectName(u"pushButton_ocr")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_ocr.sizePolicy().hasHeightForWidth())
        self.pushButton_ocr.setSizePolicy(sizePolicy2)
        icon = QIcon()
        icon.addFile(u"icon/upload.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_ocr.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton_ocr)

        self.pushButton_copy = QPushButton(self.groupBox)
        self.pushButton_copy.setObjectName(u"pushButton_copy")
        sizePolicy2.setHeightForWidth(self.pushButton_copy.sizePolicy().hasHeightForWidth())
        self.pushButton_copy.setSizePolicy(sizePolicy2)
        icon1 = QIcon()
        icon1.addFile(u"icon/clipboard.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_copy.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButton_copy)

        self.pushButton_save = QPushButton(self.groupBox)
        self.pushButton_save.setObjectName(u"pushButton_save")
        sizePolicy2.setHeightForWidth(self.pushButton_save.sizePolicy().hasHeightForWidth())
        self.pushButton_save.setSizePolicy(sizePolicy2)
        icon2 = QIcon()
        icon2.addFile(u"icon/save.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_save.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.pushButton_cancel = QPushButton(self.groupBox)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        sizePolicy2.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy2)
        icon3 = QIcon()
        icon3.addFile(u"icon/cancel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_cancel.setIcon(icon3)

        self.horizontalLayout.addWidget(self.pushButton_cancel)


        self.horizontalLayout_2.addWidget(self.groupBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_shot.setText("")
        self.groupBox.setTitle("")
        self.pushButton_ocr.setText(QCoreApplication.translate("Dialog", u"ocr\u8bc6\u522b", None))
        self.pushButton_copy.setText(QCoreApplication.translate("Dialog", u"\u590d\u5236", None))
        self.pushButton_save.setText(QCoreApplication.translate("Dialog", u"\u4fdd\u5b58", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

