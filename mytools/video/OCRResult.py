# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OCRResult.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_OCRResult(object):
    def setupUi(self, OCRResult):
        if not OCRResult.objectName():
            OCRResult.setObjectName(u"OCRResult")
        OCRResult.resize(860, 874)
        self.verticalLayout_4 = QVBoxLayout(OCRResult)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.select_btn_pic = QPushButton(OCRResult)
        self.select_btn_pic.setObjectName(u"select_btn_pic")

        self.verticalLayout.addWidget(self.select_btn_pic)

        self.lineEdit = QLineEdit(OCRResult)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.lineEdit)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.select_btn_pdf = QPushButton(OCRResult)
        self.select_btn_pdf.setObjectName(u"select_btn_pdf")

        self.verticalLayout_2.addWidget(self.select_btn_pdf)

        self.lineEdit_2 = QLineEdit(OCRResult)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.lineEdit_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.start_btn_video = QPushButton(OCRResult)
        self.start_btn_video.setObjectName(u"start_btn_video")

        self.horizontalLayout_4.addWidget(self.start_btn_video)

        self.start_btn_video_screenshot = QPushButton(OCRResult)
        self.start_btn_video_screenshot.setObjectName(u"start_btn_video_screenshot")

        self.horizontalLayout_4.addWidget(self.start_btn_video_screenshot)

        self.start_btn_video_monitor = QPushButton(OCRResult)
        self.start_btn_video_monitor.setObjectName(u"start_btn_video_monitor")

        self.horizontalLayout_4.addWidget(self.start_btn_video_monitor)

        self.start_btn_video_stop = QPushButton(OCRResult)
        self.start_btn_video_stop.setObjectName(u"start_btn_video_stop")

        self.horizontalLayout_4.addWidget(self.start_btn_video_stop)

        self.start_btn_scan = QPushButton(OCRResult)
        self.start_btn_scan.setObjectName(u"start_btn_scan")

        self.horizontalLayout_4.addWidget(self.start_btn_scan)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scrollArea = QScrollArea(OCRResult)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMouseTracking(True)
        self.scrollArea.setAcceptDrops(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 426, 304))
        self.scrollAreaWidgetContents.setMouseTracking(True)
        self.scrollAreaWidgetContents.setAcceptDrops(True)
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.cameraLabel = QLabel(self.scrollAreaWidgetContents)
        self.cameraLabel.setObjectName(u"cameraLabel")
        self.cameraLabel.setMouseTracking(True)
        self.cameraLabel.setAcceptDrops(True)
        self.cameraLabel.setScaledContents(True)
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.cameraLabel.setWordWrap(True)

        self.gridLayout.addWidget(self.cameraLabel, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)

        self.htmlEdit = QTextEdit(OCRResult)
        self.htmlEdit.setObjectName(u"htmlEdit")
        self.htmlEdit.setAutoFillBackground(True)
        self.htmlEdit.setFrameShadow(QFrame.Raised)
        self.htmlEdit.setLineWidth(3)

        self.horizontalLayout.addWidget(self.htmlEdit)

        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 5)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.gridEdit = QTextEdit(OCRResult)
        self.gridEdit.setObjectName(u"gridEdit")
        font = QFont()
        font.setFamilies([u"Cascadia Mono SemiBold"])
        font.setPointSize(12)
        font.setBold(True)
        self.gridEdit.setFont(font)
        self.gridEdit.setLayoutDirection(Qt.LeftToRight)
        self.gridEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalLayout_3.addWidget(self.gridEdit)

        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(1, 6)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.export_data_word = QPushButton(OCRResult)
        self.export_data_word.setObjectName(u"export_data_word")

        self.horizontalLayout_2.addWidget(self.export_data_word)

        self.table_btn = QPushButton(OCRResult)
        self.table_btn.setObjectName(u"table_btn")
        sizePolicy.setHeightForWidth(self.table_btn.sizePolicy().hasHeightForWidth())
        self.table_btn.setSizePolicy(sizePolicy)
        self.table_btn.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.table_btn)

        self.export_data_excel = QPushButton(OCRResult)
        self.export_data_excel.setObjectName(u"export_data_excel")

        self.horizontalLayout_2.addWidget(self.export_data_excel)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.verticalLayout_4.setStretch(2, 9)

        self.retranslateUi(OCRResult)

        QMetaObject.connectSlotsByName(OCRResult)
    # setupUi

    def retranslateUi(self, OCRResult):
        OCRResult.setWindowTitle(QCoreApplication.translate("OCRResult", u"Dialog", None))
        self.select_btn_pic.setText(QCoreApplication.translate("OCRResult", u"\u9009\u62e9\u56fe\u7247", None))
        self.select_btn_pdf.setText(QCoreApplication.translate("OCRResult", u"\u9009\u62e9pdf", None))
        self.start_btn_video.setText(QCoreApplication.translate("OCRResult", u"\u542f\u52a8\u76d1\u63a7", None))
        self.start_btn_video_screenshot.setText(QCoreApplication.translate("OCRResult", u"\u62cd\u7167", None))
        self.start_btn_video_monitor.setText(QCoreApplication.translate("OCRResult", u"\u7ee7\u7eed\u76d1\u63a7", None))
        self.start_btn_video_stop.setText(QCoreApplication.translate("OCRResult", u"\u505c\u6b62\u76d1\u63a7", None))
        self.start_btn_scan.setText(QCoreApplication.translate("OCRResult", u"\u6301\u7eed\u626b\u63cf\u5c4f\u5e55", None))
        self.cameraLabel.setText("")
        self.export_data_word.setText(QCoreApplication.translate("OCRResult", u"\u5bfc\u51faword", None))
#if QT_CONFIG(tooltip)
        self.table_btn.setToolTip(QCoreApplication.translate("OCRResult", u"<html><head/><body><p align=\"justify\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.table_btn.setText(QCoreApplication.translate("OCRResult", u"\u8868\u683c\u5f62\u5f0f", None))
        self.export_data_excel.setText(QCoreApplication.translate("OCRResult", u"\u5bfc\u51faexcel", None))
    # retranslateUi

