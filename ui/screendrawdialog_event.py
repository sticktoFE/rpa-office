from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog

from ui.screendrawdialog import Ui_Dialog

# import requests


class ShotDialog(QDialog, Ui_Dialog):
    def __init__(self, pixmap):
        super().__init__()
        self.setupUi(self)
        self.adjustSize()
        self.setWindowFlag(Qt.FramelessWindowHint)  # 没有窗口栏
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置背景透明
        self.pushButton_copy.clicked.connect(self.save_to_clipboard)
        self.pushButton_ocr.clicked.connect(self.ocr)
        self.pushButton_save.clicked.connect(self.save_local)
        self.pushButton_cancel.clicked.connect(self.close)
        self.label_shot.setPixmap(pixmap)
        self.setWindowFlag(Qt.Tool)  # 不然exec_执行退出后整个程序退出

    def get_shot_img(self):
        return self.label_shot.pixmap().toImage()

    def get_shot_bytes(self):
        shot_bytes = Qt.QByteArray()
        buffer = Qt.QBuffer(shot_bytes)
        buffer.open(Qt.QIODevice.WriteOnly)
        shot_img = self.get_shot_img()
        shot_img.save(buffer, "png")
        return shot_bytes.data()

    def save_local(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "保存到" "./", "screenshot.jpg", "Image files(*.jpg *.gif *.png)"
        )
        if file:
            shot_img = self.get_shot_img()
            shot_img.save(file)
        self.close()

    def save_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.label_shot.pixmap())
        self.close()

    def ocr(self):
        shot_img = self.get_shot_img()

    # def upload_to_picbed(self):
    #     shot_bytes = self.get_shot_bytes()
    #     filename = "shot" + str(time.time()).split('.')[0] + '.jpg'
    #     files = {
    #         "file": (filename, shot_bytes, "image/jpeg")
    #     }
    #     cfg = ConfigParser()
    #     cfg.read('config.ini')
    #     headers = {
    #         "Cookie": cfg.get("picbed", 'cookie')
    #     }
    #     try:
    #         res = requests.post(cfg.get("picbed", 'api'), data={'compress': 960},files=files, headers=headers)
    #         status_code = res.json()['code']
    #         if status_code == 200:
    #             out_info = res.json()['data']['raw_out']
    #             message = "\n".join(info_list[1] for info_list in out_info )
    #             QMessageBox.information(self, '正常返回',message , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #         else:
    #             QMessageBox.information(self, '服务非正常返回',"not 200, code: {}".format(res.status_code) , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     except Exception as e:
    #         print(e.args)
    #     self.close()
