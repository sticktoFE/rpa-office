# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_PDFdir(object):
    def setupUi(self, PDFdir):
        if not PDFdir.objectName():
            PDFdir.setObjectName(u"PDFdir")
        PDFdir.resize(669, 450)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PDFdir.sizePolicy().hasHeightForWidth())
        PDFdir.setSizePolicy(sizePolicy)
        PDFdir.setMinimumSize(QSize(330, 450))
        PDFdir.setMaximumSize(QSize(1000000, 450))
        PDFdir.setAcceptDrops(True)
        self.home_page_action = QAction(PDFdir)
        self.home_page_action.setObjectName(u"home_page_action")
        self.help_action = QAction(PDFdir)
        self.help_action.setObjectName(u"help_action")
        self.update_action = QAction(PDFdir)
        self.update_action.setObjectName(u"update_action")
        self.english_action = QAction(PDFdir)
        self.english_action.setObjectName(u"english_action")
        self.chinese_action = QAction(PDFdir)
        self.chinese_action.setObjectName(u"chinese_action")
        self.main_widget = QWidget(PDFdir)
        self.main_widget.setObjectName(u"main_widget")
        self.pdf_path_edit = QLineEdit(self.main_widget)
        self.pdf_path_edit.setObjectName(u"pdf_path_edit")
        self.pdf_path_edit.setGeometry(QRect(9, 30, 157, 20))
        self.open_button = QPushButton(self.main_widget)
        self.open_button.setObjectName(u"open_button")
        self.open_button.setGeometry(QRect(166, 26, 63, 27))
        self.dir_text_edit = QTextEdit(self.main_widget)
        self.dir_text_edit.setObjectName(u"dir_text_edit")
        self.dir_text_edit.setGeometry(QRect(9, 87, 217, 311))
        font = QFont()
        font.setPointSize(8)
        self.dir_text_edit.setFont(font)
        self.dir_text_edit.setAcceptRichText(False)
        self.export_button = QPushButton(self.main_widget)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setGeometry(QRect(608, 368, 61, 29))
        self.pdf_path_label = QLabel(self.main_widget)
        self.pdf_path_label.setObjectName(u"pdf_path_label")
        self.pdf_path_label.setGeometry(QRect(9, 6, 214, 19))
        self.dir_text_label = QLabel(self.main_widget)
        self.dir_text_label.setObjectName(u"dir_text_label")
        self.dir_text_label.setGeometry(QRect(9, 63, 217, 19))
        self.dir_tree_widget = QTreeWidget(self.main_widget)
        font1 = QFont()
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(1, font1);
        __qtreewidgetitem.setFont(0, font1);
        self.dir_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.dir_tree_widget.setObjectName(u"dir_tree_widget")
        self.dir_tree_widget.setEnabled(True)
        self.dir_tree_widget.setGeometry(QRect(336, 30, 271, 367))
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        self.dir_tree_widget.setFont(font2)
        self.dir_tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dir_tree_widget.setAcceptDrops(True)
        self.dir_tree_widget.setAutoScroll(False)
        self.dir_tree_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.dir_tree_widget.setDragDropMode(QAbstractItemView.DragDrop)
        self.dir_tree_widget.setDefaultDropAction(Qt.MoveAction)
        self.dir_tree_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.dir_tree_widget.setAutoExpandDelay(1)
        self.dir_tree_widget.header().setVisible(True)
        self.dir_tree_widget.header().setCascadingSectionResizes(False)
        self.preview_label = QLabel(self.main_widget)
        self.preview_label.setObjectName(u"preview_label")
        self.preview_label.setGeometry(QRect(336, 10, 54, 12))
        self.offset_edit = QLineEdit(self.main_widget)
        self.offset_edit.setObjectName(u"offset_edit")
        self.offset_edit.setGeometry(QRect(236, 130, 87, 20))
        self.offset_edit.setInputMethodHints(Qt.ImhDigitsOnly)
        self.offset_edit.setMaxLength(32767)
        self.offset_label = QLabel(self.main_widget)
        self.offset_label.setObjectName(u"offset_label")
        self.offset_label.setGeometry(QRect(236, 108, 54, 13))
        self.sub_dir_group = QGroupBox(self.main_widget)
        self.sub_dir_group.setObjectName(u"sub_dir_group")
        self.sub_dir_group.setGeometry(QRect(236, 166, 89, 229))
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        font3.setItalic(False)
        font3.setUnderline(False)
        font3.setKerning(True)
        self.sub_dir_group.setFont(font3)
        self.sub_dir_group.setAutoFillBackground(True)
        self.sub_dir_group.setAlignment(Qt.AlignCenter)
        self.sub_dir_group.setFlat(False)
        self.sub_dir_group.setCheckable(False)
        self.level0_button = QPushButton(self.sub_dir_group)
        self.level0_button.setObjectName(u"level0_button")
        self.level0_button.setGeometry(QRect(66, 24, 19, 17))
        font4 = QFont()
        font4.setPointSize(13)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setUnderline(True)
        font4.setKerning(True)
        self.level0_button.setFont(font4)
        self.level0_button.setStyleSheet(u"color: rgb(0, 0, 255)")
        self.level0_button.setFlat(True)
        self.level1_button = QPushButton(self.sub_dir_group)
        self.level1_button.setObjectName(u"level1_button")
        self.level1_button.setGeometry(QRect(66, 76, 19, 17))
        self.level1_button.setFont(font4)
        self.level1_button.setStyleSheet(u"color: rgb(0, 0, 255)")
        self.level1_button.setFlat(True)
        self.level2_button = QPushButton(self.sub_dir_group)
        self.level2_button.setObjectName(u"level2_button")
        self.level2_button.setGeometry(QRect(66, 126, 19, 17))
        self.level2_button.setFont(font4)
        self.level2_button.setStyleSheet(u"color: rgb(0, 0, 255)")
        self.level2_button.setFlat(True)
        self.level0_edit = QLineEdit(self.sub_dir_group)
        self.level0_edit.setObjectName(u"level0_edit")
        self.level0_edit.setGeometry(QRect(6, 44, 79, 20))
        self.level0_edit.setEchoMode(QLineEdit.Normal)
        self.level0_box = QCheckBox(self.sub_dir_group)
        self.level0_box.setObjectName(u"level0_box")
        self.level0_box.setGeometry(QRect(4, 24, 49, 16))
        self.level2_box = QCheckBox(self.sub_dir_group)
        self.level2_box.setObjectName(u"level2_box")
        self.level2_box.setGeometry(QRect(4, 124, 49, 16))
        self.level1_edit = QLineEdit(self.sub_dir_group)
        self.level1_edit.setObjectName(u"level1_edit")
        self.level1_edit.setGeometry(QRect(4, 94, 79, 20))
        self.unknown_level_label = QLabel(self.sub_dir_group)
        self.unknown_level_label.setObjectName(u"unknown_level_label")
        self.unknown_level_label.setGeometry(QRect(4, 174, 54, 12))
        self.level2_edit = QLineEdit(self.sub_dir_group)
        self.level2_edit.setObjectName(u"level2_edit")
        self.level2_edit.setGeometry(QRect(4, 144, 79, 20))
        self.unknown_level_box = QComboBox(self.sub_dir_group)
        self.unknown_level_box.addItem("")
        self.unknown_level_box.addItem("")
        self.unknown_level_box.addItem("")
        self.unknown_level_box.setObjectName(u"unknown_level_box")
        self.unknown_level_box.setGeometry(QRect(0, 194, 83, 22))
        self.level1_box = QCheckBox(self.sub_dir_group)
        self.level1_box.setObjectName(u"level1_box")
        self.level1_box.setGeometry(QRect(4, 74, 49, 16))
        PDFdir.setCentralWidget(self.main_widget)
        self.statusbar = QStatusBar(PDFdir)
        self.statusbar.setObjectName(u"statusbar")
        font5 = QFont()
        font5.setPointSize(7)
        self.statusbar.setFont(font5)
        PDFdir.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(PDFdir)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 669, 22))
        self.help_menu = QMenu(self.menuBar)
        self.help_menu.setObjectName(u"help_menu")
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName(u"menu")
        PDFdir.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.help_menu.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.help_menu.addAction(self.home_page_action)
        self.help_menu.addAction(self.help_action)
        self.help_menu.addAction(self.update_action)
        self.menu.addAction(self.english_action)
        self.menu.addAction(self.chinese_action)

        self.retranslateUi(PDFdir)

        QMetaObject.connectSlotsByName(PDFdir)
    # setupUi

    def retranslateUi(self, PDFdir):
        PDFdir.setWindowTitle(QCoreApplication.translate("PDFdir", u"PDFdir", None))
        self.home_page_action.setText(QCoreApplication.translate("PDFdir", u"\u4e3b\u9875", None))
        self.help_action.setText(QCoreApplication.translate("PDFdir", u"\u5e2e\u52a9\u624b\u518c", None))
        self.update_action.setText(QCoreApplication.translate("PDFdir", u"\u68c0\u67e5\u66f4\u65b0", None))
        self.english_action.setText(QCoreApplication.translate("PDFdir", u"English", None))
        self.chinese_action.setText(QCoreApplication.translate("PDFdir", u"\u4e2d\u6587", None))
        self.open_button.setText(QCoreApplication.translate("PDFdir", u"\u6253\u5f00", None))
        self.dir_text_edit.setHtml(QCoreApplication.translate("PDFdir", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'SimSun';\"><br /></p></body></html>", None))
        self.export_button.setText(QCoreApplication.translate("PDFdir", u"\u5199\u5165", None))
        self.pdf_path_label.setText(QCoreApplication.translate("PDFdir", u"PDF\u6587\u4ef6\u8def\u5f84", None))
        self.dir_text_label.setText(QCoreApplication.translate("PDFdir", u"\u76ee\u5f55\u6587\u672c", None))
        ___qtreewidgetitem = self.dir_tree_widget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("PDFdir", u"\u5b9e\u9645\u9875\u6570", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("PDFdir", u"\u6807\u6ce8\u9875\u7801", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("PDFdir", u"\u76ee\u5f55", None));
        self.preview_label.setText(QCoreApplication.translate("PDFdir", u"\u9884\u89c8", None))
        self.offset_edit.setInputMask("")
        self.offset_edit.setText(QCoreApplication.translate("PDFdir", u"0", None))
        self.offset_label.setText(QCoreApplication.translate("PDFdir", u"\u9875\u5dee", None))
        self.sub_dir_group.setTitle(QCoreApplication.translate("PDFdir", u"\u76ee\u5f55\u5206\u5c42", None))
        self.level0_button.setText(QCoreApplication.translate("PDFdir", u"...", None))
        self.level1_button.setText(QCoreApplication.translate("PDFdir", u"...", None))
        self.level2_button.setText(QCoreApplication.translate("PDFdir", u"...", None))
        self.level0_edit.setText("")
        self.level0_box.setText(QCoreApplication.translate("PDFdir", u"\u9996\u5c42", None))
        self.level2_box.setText(QCoreApplication.translate("PDFdir", u"\u4e09\u5c42", None))
        self.level1_edit.setText("")
        self.unknown_level_label.setText(QCoreApplication.translate("PDFdir", u"\u672a\u8bc6\u522b", None))
        self.level2_edit.setText("")
        self.unknown_level_box.setItemText(0, QCoreApplication.translate("PDFdir", u"\u9996\u5c42", None))
        self.unknown_level_box.setItemText(1, QCoreApplication.translate("PDFdir", u"\u4e8c\u5c42", None))
        self.unknown_level_box.setItemText(2, QCoreApplication.translate("PDFdir", u"\u4e09\u5c42", None))

        self.unknown_level_box.setCurrentText(QCoreApplication.translate("PDFdir", u"\u9996\u5c42", None))
        self.level1_box.setText(QCoreApplication.translate("PDFdir", u"\u4e8c\u5c42", None))
        self.help_menu.setTitle(QCoreApplication.translate("PDFdir", u"\u5e2e\u52a9", None))
        self.menu.setTitle(QCoreApplication.translate("PDFdir", u"\u8bed\u8a00", None))
    # retranslateUi

