# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'option.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGroupBox, QLabel, QLineEdit, QSizePolicy,
    QWidget)

class Ui_Dialog_Option(object):
    def setupUi(self, Dialog_Option):
        if not Dialog_Option.objectName():
            Dialog_Option.setObjectName(u"Dialog_Option")
        Dialog_Option.setWindowModality(Qt.ApplicationModal)
        Dialog_Option.resize(512, 440)
        icon = QIcon()
        icon.addFile(u"../icon/setting.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog_Option.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(Dialog_Option)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(190, 170, 201, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.groupBox = QGroupBox(Dialog_Option)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 30, 541, 101))
        self.lineEdit_api = QLineEdit(self.groupBox)
        self.lineEdit_api.setObjectName(u"lineEdit_api")
        self.lineEdit_api.setGeometry(QRect(80, 20, 451, 21))
        self.lineEdit_api.setMinimumSize(QSize(200, 0))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 55, 48, 16))
        self.requestURL = QLabel(self.groupBox)
        self.requestURL.setObjectName(u"requestURL")
        self.requestURL.setGeometry(QRect(20, 20, 54, 16))
        self.lineEdit_cookie = QLineEdit(self.groupBox)
        self.lineEdit_cookie.setObjectName(u"lineEdit_cookie")
        self.lineEdit_cookie.setGeometry(QRect(80, 55, 451, 21))
        self.lineEdit_cookie.setMinimumSize(QSize(200, 0))

        self.retranslateUi(Dialog_Option)
        self.buttonBox.accepted.connect(Dialog_Option.accept)
        self.buttonBox.rejected.connect(Dialog_Option.reject)

        QMetaObject.connectSlotsByName(Dialog_Option)
    # setupUi

    def retranslateUi(self, Dialog_Option):
        Dialog_Option.setWindowTitle(QCoreApplication.translate("Dialog_Option", u"\u53c2\u6570\u914d\u7f6e", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Dialog_Option", u"cookie", None))
        self.requestURL.setText(QCoreApplication.translate("Dialog_Option", u"URL", None))
    # retranslateUi

