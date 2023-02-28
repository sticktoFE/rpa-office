# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infoframe.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLayout, QScrollArea,
    QSizePolicy, QVBoxLayout, QWidget)

from ui.component.mscrolllabel import ScrollLabel
import pic_rc

class Ui_InfoWidget(object):
    def setupUi(self, InfoWidget):
        if not InfoWidget.objectName():
            InfoWidget.setObjectName(u"InfoWidget")
        InfoWidget.resize(437, 376)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InfoWidget.sizePolicy().hasHeightForWidth())
        InfoWidget.setSizePolicy(sizePolicy)
        InfoWidget.setMouseTracking(True)
        InfoWidget.setAcceptDrops(True)
        InfoWidget.setWindowOpacity(0.700000000000000)
        InfoWidget.setAutoFillBackground(True)
        self.verticalLayout = QVBoxLayout(InfoWidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.head = QHBoxLayout()
        self.head.setSpacing(5)
        self.head.setObjectName(u"head")
        self.head.setContentsMargins(10, -1, 10, -1)
        self.label_2 = QLabel(InfoWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(35, 35))
        self.label_2.setMaximumSize(QSize(35, 35))
        self.label_2.setMouseTracking(True)
        self.label_2.setAcceptDrops(True)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet(u"border-image: url(:/006/icon/006.png);")
        self.label_2.setFrameShape(QFrame.WinPanel)
        self.label_2.setFrameShadow(QFrame.Raised)
        self.label_2.setLineWidth(0)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setMargin(0)
        self.label_2.setTextInteractionFlags(Qt.NoTextInteraction)

        self.head.addWidget(self.label_2)

        self.label = QLabel(InfoWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAcceptDrops(True)
        self.label.setAutoFillBackground(True)
        self.label.setStyleSheet(u"border-image: url();")
        self.label.setFrameShape(QFrame.WinPanel)
        self.label.setFrameShadow(QFrame.Raised)
        self.label.setLineWidth(0)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.head.addWidget(self.label)

        self.head.setStretch(0, 6)
        self.head.setStretch(1, 4)

        self.verticalLayout.addLayout(self.head)

        self.scrollArea = QScrollArea(InfoWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setAcceptDrops(True)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setFrameShape(QFrame.Box)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 433, 294))
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        self.formLayout.setHorizontalSpacing(5)
        self.formLayout.setVerticalSpacing(5)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_3 = ScrollLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAcceptDrops(True)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAutoFillBackground(True)
        self.label_3.setStyleSheet(u"")
        self.label_3.setFrameShape(QFrame.Box)
        self.label_3.setFrameShadow(QFrame.Plain)
        self.label_3.setLineWidth(0)
        self.label_3.setMidLineWidth(0)
        self.label_3.setTextFormat(Qt.AutoText)
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_3.setWordWrap(True)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 8)

        self.retranslateUi(InfoWidget)

        QMetaObject.connectSlotsByName(InfoWidget)
    # setupUi

    def retranslateUi(self, InfoWidget):
        InfoWidget.setWindowTitle(QCoreApplication.translate("InfoWidget", u"Form", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("InfoWidget", u"\u8bc6\u522b\u6210\u529f", None))
        self.label_3.setText("")
    # retranslateUi

