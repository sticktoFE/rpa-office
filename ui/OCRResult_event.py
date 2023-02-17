import os
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QTableView,
    QHeaderView,
)
from PySide6.QtGui import QImage
from mytools.AIVideo.model.inference.OCRVideo import OCRVideo
from myutils.image_convert import cv2pixmap
from myutils.info_out_manager import get_temp_file, get_temp_folder
from ui.component.TipsShower import TipsShower
from .OCRResult import Ui_OCRResult
import pandas as pd
import numpy as np
import cv2
from myutils.office_tools import to_excel_auto_column_weight
from ui.component.pandas_model import PandasModel
from docx import Document


class TotalMessage(QDialog, Ui_OCRResult):
    def __init__(self, content):
        super().__init__()
        self.setupUi(self)
        self.adjustSize()
        self.setWindowFlags(
            Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint
        )  # Qt.WindowStaysOnTopHint|
        # self.setWindowFlag(Qt.FramelessWindowHint)  # 没有窗口栏
        # self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        self.select_btn_pic.clicked.connect(self.ocr_pdf)
        self.select_btn_pdf.clicked.connect(self.ocr_pdf)
        self.start_btn_scan.clicked.connect(self.ocr_pdf)
        self.start_btn_video.clicked.connect(self.start_ocr_video)
        self.start_btn_video_screenshot.clicked.connect(
            self.ocr_video_screenshot)
        self.start_btn_video_monitor.clicked.connect(self.ocr_video_monitor)
        self.start_btn_video_stop.clicked.connect(self.ocr_video_close)
        self.table_btn.clicked.connect(self.display_data_table)
        self.export_data_excel.clicked.connect(self.save_data_excel)
        self.export_data_word.clicked.connect(self.save_data_word)
        self.gridEdit.setAlignment(Qt.AlignCenter)
        self.init_info(content)
        # self.scrollArea.installEventFilter(self)
        self.graphicsView.installEventFilter(self)
        self.graphicsView.setMouseTracking(True)  # 2
        self.last_time_move = 0

        self.Tipsshower = TipsShower(
            "  ", targetarea=(100, 70, 0, 0), parent=self)
        # tipsfont = QFont("Microsoft YaHei")
        # tipsfont.setBold(True)
        # tipsfont.setPointSize(60)
        # self.Tipsshower.setFont(tipsfont)
        # palette = QPalette()
        # palette.setColor(QPalette.WindowText,Qt.red)
        # self.Tipsshower.setPalette(palette)

    def init_info(self, content):
        if type(content) is np.ndarray:
            show = cv2.resize(content, (320, 260))
            self.graphicsView.setPixmap(cv2pixmap(show))
            # 以下是使用QTextEdit方式插入图片，这个会不断往下追加，先用QLabel吧
            # document = self.videoEdit.document()
            # cursor = QTextCursor(document)
            # p1 = cursor.position() # returns int
            # cursor.insertImage(showImage)
        elif type(content) is tuple:
            # 识别的图，上面带识别的区域划线
            self.src_long_pic = cv2pixmap(content[0])
            pic_draw = content[1]
            ocr_result = content[2]
            ocr_result_html = content[3]
            self.graphicsView.setPixmap(cv2pixmap(pic_draw))
            # 识别的内容列表
            self.content_list = ocr_result  # pd.DataFrame(ocr_result) 已经变成list
            # reduce是为了把list拼成一个字符串
            # df_series = self.content_list.apply(lambda row: reduce(lambda x, y: f"{str(x) if x is not None else ''} {str(y) if y is not None else ''}", row.values.tolist()), axis=1)
            # to_s = '\n'.join(df_series.values) #if ocr_result_html else ''.join(df_series.values)
            # to_s.replace(r'\s+','')
            # self.gridEdit.setText(str(self.content_list))
            self.gridEdit.clear()
            for content_sec in ocr_result:
                self.gridEdit.append(
                    content_sec.to_string(header=False, index=False)
                    if type(content_sec) is pd.DataFrame
                    else content_sec
                )
            # self.gridEdit.setAlignment(Qt.AlignLeft)
            # 如果原生带格式识别，就展示出来
            self.htmlEdit.clear()
            for html_script in ocr_result_html:
                self.htmlEdit.append(html_script)
        elif type(content) is str:
            self.gridEdit.setText(content)
        # self.cameraLabel.resize(480,260)

    def display_data_table(self):
        self.view = QTableView()
        self.view.resize(1200, 800)
        self.view.resizeColumnsToContents()
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        # self.view.resizeRowsToContents()
        # QTableWidget.resizeRowsToContents(self.view)
        model = PandasModel(self.content_list)
        self.view.setModel(model)
        self.view.show()
        # self.hide()

    def save_data_excel(self):
        temp_path = get_temp_folder(execute_file_path=__file__)
        file_path = get_temp_file(des_folder=temp_path)
        i = 0
        for content_sec in self.content_list:
            if type(content_sec) is pd.DataFrame:
                to_excel_auto_column_weight(
                    {f"sheet{str(i)}": content_sec}, file_name=file_path
                )
                i += 1
        # 打开文件
        if i != 0:
            os.startfile(file_path)
        # 选择文件进行pdf内容识别

    def save_data_word(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "保存到", "example.docx", "word files(*.docx *doc)"
        )
        if file:
            # 创建 Document 对象，等价于在电脑上打开一个 Word 文档
            document = Document()
            # 在 Word 文档中添加一个标题
            document.add_heading("这是一个标题", level=0)
            # 文档添加段落
            p = document.add_paragraph("这是白给的段落")
            # 添加带样式的文字
            # 添加段落，文本可以包含制表符（\t）、换行符（\n）或回车符（\r）等
            # add_run() 在段落后面追加文本
            p.add_run("\n我倾斜了").italic = True  # 添加一个倾斜文字
            # 添加一个加粗文字
            p.add_run(f"\n{self.gridEdit.toPlainText()}").bold = True
            # 保存文档
            document.save(file)
        # self.close()
        # 选择文件进行pdf内容识别

    def ocr_pdf(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "screenshot.jpg", "pdf files(*.pdf)"
        )
        if file:
            shot_img = self.graphicsView.pixmap.toImage()
            shot_img.save(file)
        self.close()

    # 视频扫描
    def start_ocr_video(self):
        if not hasattr(self, "video_ocr"):
            self.video_ocr = OCRVideo()
            self.video_ocr.signal.connect(self.ocr_video_result)
            self.video_ocr.signal_img.connect(self.ocr_video_result)
            # # 准备就绪，启动线程开始扫描 此时 run中
            self.video_ocr.start()
        if not self.video_ocr.isRunning():
            self.video_ocr.start()

    def ocr_video_screenshot(self):
        self.video_ocr.pause()

    def ocr_video_monitor(self):
        self.video_ocr.resume()

    def ocr_video_close(self):
        self.video_ocr.stop()

    def ocr_video_result(self, result):
        # print(result)
        self.init_info(result)

    def save_local(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "保存到", "screenshot.jpg", "Image files(*.jpg *.gif *.png)"
        )
        if file:
            shot_img = self.graphicsView.pixmap.toImage()
            shot_img.save(file)
        self.close()

    def save_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.graphicsView.pixmap)
        self.close()

    def closeEvent(self, event):
        if hasattr(self, "video_ocr") and self.video_ocr:
            self.video_ocr.stop()

    def open_image(self):
        """
        select image file and open it
        :return:
        """
        img_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "*.jpg;;*.png;;*.jpeg"
        )
        self.box.set_image(img_name)

    # 成员函数copyPic
    # 作用：复制图片
    def copyPic(self):
        with open(self.graphicsView.pixmap, "rb") as f_src:
            # 读取图片内容并存储到content变量
            content = f_src.read()
            with open("./1.jpg", "wb") as f_copy:
                # 源图片的内容以二进制形式写入新图片
                f_copy.write(content)

    def eventFilter(self, source, event):
        # 双击拷贝图片
        # print(event.type() )
        if (
            event.type() == QEvent.MouseButtonDblClick
            and event.button() == Qt.LeftButton
        ):
            QApplication.clipboard().setPixmap(self.graphicsView.pixmap)
        elif (
            event.type() == QEvent.MouseButtonDblClick
            and event.button() == Qt.RightButton
        ):
            QApplication.clipboard().setPixmap(self.src_long_pic)
            # QApplication.clipboard().setImage(QImage(f"{Path(__file__).parent.parent}/dw/DataFactory/AIScreenshot/tmp/long_screenshot.png"))
        elif event.type() == QEvent.Enter:
            """
            鼠标悬停，提示信息
            """
            self.Tipsshower.setText("双击保存")

        # elif event.type() == QEvent.MouseMove and event.button() == Qt.LeftButton:
        #     """
        #     mouse move events for the widget
        #     :param event: QMouseEvent
        #     :return:
        #     """
        #     self.move_dis = event.pos()- self.start_pos
        #     self.point_x = self.point_x + self.move_dis
        #     self.start_pos = event.pos()
        #     self.repaint()
        # elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
        #     """
        #     mouse release events for the widget
        #     :param e: QMouseEvent
        #     :return:
        #     """
        #     self.left_click = False
        # return super().eventFilter(source, event)

    # def paintEvent(self, e):
    #     """
    #     receive paint events
    #     :param e: QPaintEvent
    #     :return:
    #     """
    #     scaled_img = self.cameraLabel.pixmap()

    #     self.cameraLabel.rect()
    #     if scaled_img:
    #         painter = QPainter()
    #         painter.begin(self)
    #         painter.drawPixmap(QRect(self.point[0],self.point[1],self.cameraLabel.size().width(),self.cameraLabel.size().height()), scaled_img)
    #         painter.end()
