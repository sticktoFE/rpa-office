# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'OCRResult.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
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
    QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSlider, QSplitter,
    QTextEdit, QVBoxLayout, QWidget)

from ui.component.ImageViewer import ImageViewer

class Ui_OCRResult(object):
    def setupUi(self, OCRResult):
        if not OCRResult.objectName():
            OCRResult.setObjectName(u"OCRResult")
        OCRResult.resize(1025, 411)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OCRResult.sizePolicy().hasHeightForWidth())
        OCRResult.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setStyleStrategy(QFont.PreferAntialias)
        OCRResult.setFont(font)
        OCRResult.setMouseTracking(True)
        OCRResult.setAcceptDrops(True)
        self.verticalLayout_3 = QVBoxLayout(OCRResult)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(OCRResult)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setHandleWidth(1)
        self.file_list_widget = QListWidget(self.splitter_2)
        self.file_list_widget.setObjectName(u"file_list_widget")
        self.splitter_2.addWidget(self.file_list_widget)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_file_btn = QPushButton(self.layoutWidget)
        self.select_file_btn.setObjectName(u"select_file_btn")
        sizePolicy.setHeightForWidth(self.select_file_btn.sizePolicy().hasHeightForWidth())
        self.select_file_btn.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.select_file_btn)

        self.start_btn_video = QPushButton(self.layoutWidget)
        self.start_btn_video.setObjectName(u"start_btn_video")
        sizePolicy.setHeightForWidth(self.start_btn_video.sizePolicy().hasHeightForWidth())
        self.start_btn_video.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.start_btn_video)

        self.start_btn_video_screenshot = QPushButton(self.layoutWidget)
        self.start_btn_video_screenshot.setObjectName(u"start_btn_video_screenshot")
        sizePolicy.setHeightForWidth(self.start_btn_video_screenshot.sizePolicy().hasHeightForWidth())
        self.start_btn_video_screenshot.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.start_btn_video_screenshot)

        self.start_btn_video_monitor = QPushButton(self.layoutWidget)
        self.start_btn_video_monitor.setObjectName(u"start_btn_video_monitor")
        sizePolicy.setHeightForWidth(self.start_btn_video_monitor.sizePolicy().hasHeightForWidth())
        self.start_btn_video_monitor.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.start_btn_video_monitor)

        self.start_btn_video_stop = QPushButton(self.layoutWidget)
        self.start_btn_video_stop.setObjectName(u"start_btn_video_stop")
        sizePolicy.setHeightForWidth(self.start_btn_video_stop.sizePolicy().hasHeightForWidth())
        self.start_btn_video_stop.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.start_btn_video_stop)

        self.start_screenshot_btn = QPushButton(self.layoutWidget)
        self.start_screenshot_btn.setObjectName(u"start_screenshot_btn")
        sizePolicy.setHeightForWidth(self.start_screenshot_btn.sizePolicy().hasHeightForWidth())
        self.start_screenshot_btn.setSizePolicy(sizePolicy)
        self.start_screenshot_btn.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout.addWidget(self.start_screenshot_btn)

        self.slider = QSlider(self.layoutWidget)
        self.slider.setObjectName(u"slider")
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider)

        self.re_screen_shot = QPushButton(self.layoutWidget)
        self.re_screen_shot.setObjectName(u"re_screen_shot")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.re_screen_shot.sizePolicy().hasHeightForWidth())
        self.re_screen_shot.setSizePolicy(sizePolicy1)
        self.re_screen_shot.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout.addWidget(self.re_screen_shot)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter = QSplitter(self.layoutWidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShadow(QFrame.Plain)
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.setHandleWidth(1)
        self.graphicsView = ImageViewer(self.splitter)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setAcceptDrops(True)
        self.splitter.addWidget(self.graphicsView)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.ocrTextEdit = QTextEdit(self.layoutWidget1)
        self.ocrTextEdit.setObjectName(u"ocrTextEdit")
        font1 = QFont()
        font1.setPointSize(18)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.ocrTextEdit.setFont(font1)
        self.ocrTextEdit.setStyleSheet(u"font: 18pt; line-height: 6em;")
        self.ocrTextEdit.setFrameShadow(QFrame.Plain)

        self.horizontalLayout_4.addWidget(self.ocrTextEdit)

        self.htmlEdit = QTextEdit(self.layoutWidget1)
        self.htmlEdit.setObjectName(u"htmlEdit")
        sizePolicy.setHeightForWidth(self.htmlEdit.sizePolicy().hasHeightForWidth())
        self.htmlEdit.setSizePolicy(sizePolicy)
        self.htmlEdit.setAutoFillBackground(True)
        self.htmlEdit.setFrameShadow(QFrame.Plain)
        self.htmlEdit.setLineWidth(3)

        self.horizontalLayout_4.addWidget(self.htmlEdit)

        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout.addWidget(self.splitter)

        self.splitter_2.addWidget(self.layoutWidget)
        self.layoutWidget2 = QWidget(self.splitter_2)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridEdit = QTextEdit(self.layoutWidget2)
        self.gridEdit.setObjectName(u"gridEdit")
        sizePolicy.setHeightForWidth(self.gridEdit.sizePolicy().hasHeightForWidth())
        self.gridEdit.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setFamilies([u"Cascadia Mono Light"])
        font2.setPointSize(18)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStyleStrategy(QFont.PreferAntialias)
        self.gridEdit.setFont(font2)
        self.gridEdit.setLayoutDirection(Qt.LeftToRight)
        self.gridEdit.setStyleSheet(u"font: 18pt; line-height: 6em;")
        self.gridEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.gridEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.gridEdit.setAutoFormatting(QTextEdit.AutoAll)
        self.gridEdit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.gridEdit.setOverwriteMode(True)
        self.gridEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextEditable|Qt.TextEditorInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_2.addWidget(self.gridEdit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.find_input = QLineEdit(self.layoutWidget2)
        self.find_input.setObjectName(u"find_input")

        self.horizontalLayout_3.addWidget(self.find_input)

        self.find_button = QPushButton(self.layoutWidget2)
        self.find_button.setObjectName(u"find_button")
        sizePolicy.setHeightForWidth(self.find_button.sizePolicy().hasHeightForWidth())
        self.find_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.find_button)

        self.horizontalLayout_3.setStretch(0, 8)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.replace_input = QLineEdit(self.layoutWidget2)
        self.replace_input.setObjectName(u"replace_input")

        self.horizontalLayout_5.addWidget(self.replace_input)

        self.replace_button = QPushButton(self.layoutWidget2)
        self.replace_button.setObjectName(u"replace_button")
        sizePolicy.setHeightForWidth(self.replace_button.sizePolicy().hasHeightForWidth())
        self.replace_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.replace_button)

        self.horizontalLayout_5.setStretch(0, 8)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.format_table = QPushButton(self.layoutWidget2)
        self.format_table.setObjectName(u"format_table")
        sizePolicy.setHeightForWidth(self.format_table.sizePolicy().hasHeightForWidth())
        self.format_table.setSizePolicy(sizePolicy)
        self.format_table.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.format_table)

        self.export_data_word = QPushButton(self.layoutWidget2)
        self.export_data_word.setObjectName(u"export_data_word")
        sizePolicy.setHeightForWidth(self.export_data_word.sizePolicy().hasHeightForWidth())
        self.export_data_word.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.export_data_word)

        self.export_data_excel = QPushButton(self.layoutWidget2)
        self.export_data_excel.setObjectName(u"export_data_excel")
        sizePolicy.setHeightForWidth(self.export_data_excel.sizePolicy().hasHeightForWidth())
        self.export_data_excel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.export_data_excel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2.setStretch(0, 9)
        self.splitter_2.addWidget(self.layoutWidget2)

        self.verticalLayout_3.addWidget(self.splitter_2)


        self.retranslateUi(OCRResult)

        QMetaObject.connectSlotsByName(OCRResult)
    # setupUi

    def retranslateUi(self, OCRResult):
        OCRResult.setWindowTitle(QCoreApplication.translate("OCRResult", u"\u4fe1\u606f\u6846", None))
        self.select_file_btn.setText(QCoreApplication.translate("OCRResult", u"\u9009\u62e9\u6587\u4ef6", None))
        self.start_btn_video.setText(QCoreApplication.translate("OCRResult", u"\u542f\u52a8\u76d1\u63a7", None))
        self.start_btn_video_screenshot.setText(QCoreApplication.translate("OCRResult", u"\u62cd\u7167", None))
        self.start_btn_video_monitor.setText(QCoreApplication.translate("OCRResult", u"\u7ee7\u7eed\u76d1\u63a7", None))
        self.start_btn_video_stop.setText(QCoreApplication.translate("OCRResult", u"\u505c\u6b62\u76d1\u63a7", None))
        self.start_screenshot_btn.setText(QCoreApplication.translate("OCRResult", u"\u622a\u5c4f", None))
        self.re_screen_shot.setText(QCoreApplication.translate("OCRResult", u"\u91cd\u65b0\u622a\u5c4f", None))
        self.find_button.setText(QCoreApplication.translate("OCRResult", u"\u67e5\u627e", None))
        self.replace_button.setText(QCoreApplication.translate("OCRResult", u"\u66ff\u6362", None))
#if QT_CONFIG(tooltip)
        self.format_table.setToolTip(QCoreApplication.translate("OCRResult", u"<html><head/><body><p align=\"justify\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.format_table.setText(QCoreApplication.translate("OCRResult", u"\u8868\u683c\u5f62\u5f0f", None))
        self.export_data_word.setText(QCoreApplication.translate("OCRResult", u"\u5bfc\u51faword", None))
        self.export_data_excel.setText(QCoreApplication.translate("OCRResult", u"\u5bfc\u51faexcel", None))
    # retranslateUi

