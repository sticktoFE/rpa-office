# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLayout,
    QMainWindow, QProgressBar, QSizePolicy, QVBoxLayout,
    QWidget)

from component.GifSplashScreen import GifSplashScreen
import pic_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(180, 203)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(150, 168))
        MainWindow.setWindowOpacity(0.800000000000000)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setTabletTracking(True)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet(u"border-image: url(:/icon/001.png);")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 18, 2, 15)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setStyleSheet(u"border-image: url();")
        self.groupBox_4.setFlat(True)

        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(18, 5, 16, 5)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet(u"border-image: url();")
        self.groupBox.setFlat(True)

        self.horizontalLayout_2.addWidget(self.groupBox)

        self.GSS = GifSplashScreen(self.centralwidget)
        self.GSS.setObjectName(u"GSS")
        self.GSS.setEnabled(True)
        sizePolicy.setHeightForWidth(self.GSS.sizePolicy().hasHeightForWidth())
        self.GSS.setSizePolicy(sizePolicy)
        self.GSS.setMinimumSize(QSize(106, 124))
        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        self.GSS.setFont(font)
        self.GSS.setMouseTracking(True)
        self.GSS.setAcceptDrops(True)
        self.GSS.setAutoFillBackground(False)
        self.GSS.setStyleSheet(u"border-image: url();")

        self.horizontalLayout_2.addWidget(self.GSS)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setStyleSheet(u"border-image: url();")
        self.groupBox_3.setFlat(True)

        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 8)
        self.horizontalLayout_2.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setStyleSheet(u"border-image: url();")
        self.groupBox_5.setFlat(True)
        self.progressBar = QProgressBar(self.groupBox_5)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(40, 0, 101, 8))
        font1 = QFont()
        font1.setPointSize(6)
        self.progressBar.setFont(font1)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QProgressBar.TopToBottom)

        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.verticalLayout_3.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_4.setTitle("")
        self.groupBox.setTitle("")
        self.groupBox_3.setTitle("")
        self.groupBox_5.setTitle("")
    # retranslateUi

