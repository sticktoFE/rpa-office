import cv2
from pathlib import Path
from numpy import vstack
from PySide6.QtCore import (
    QThread,
    QThreadPool,
    Signal,
)

# 使用文字转语音功能，发出问候音：xx,你好！
from myutils.DateAndTime import clock
from myutils.GeneralQThread import Worker
from myutils.image_merge import ImageMergeWithDetect
from myutils.info_out_manager import get_temp_folder
from myutils.ScreenShot import ScreenShot
from myutils import globalvar, image_split
import numpy as np
from PIL import Image

from route.OCRRequest import get_ocr_result, ocr

"""
    第一版 实现的划区域截图 独立线程
    获取截图区域，然后截图图片并进行ocr识别
    """


class OCRGeneral(QThread):
    signal = Signal(tuple)

    def __init__(self, **kwargs):
        super().__init__()
        self.box = kwargs.get("box")
        self.shotscreen = ScreenShot()

    @clock
    def run(self):
        print("OCRGeneral进程开始")
        ocr_request = globalvar.get_var("ocrserver")
        while not ocr_request:
            self.sleep(1)
            ocr_request = globalvar.get_var("ocrserver")
        cv2_img = self.shotscreen.shot_screen(box=self.box)
        # cv2.imwrite("xxxxexample.png", cv2_img)
        html_content = []
        cv2_img_draw, out_info, html_content = ocr_request.ocr_structure(cv2_img)
        self.signal.emit((cv2_img, cv2_img_draw, out_info, html_content))

        # cv2_img,out_info= self.ocr_request.upload_ocr_info_thread(cv2_img, keep_format="2")
        # self.signal.emit((cv2_img,out_info,html_content))


class OCRThread(QThread):
    """
    第二版 实现的划区域截图 独立线程
    先截图形成长图，再统一分割图片去识别，速度较慢
    对图片进行ocr识别，作为识别工具直接展示识别内容
    """

    signal = Signal(tuple)

    def __init__(self, **kwargs):
        super().__init__()
        # self.ocr_request = kwargs.pop('ocr_request')
        # self.ocr_request = ocr_request_process
        # self.ocr_request.set_output_filepath(f'{Path(__file__).parent}/tmp')

    def set_img(self, img_cv2):
        self.img_cv2 = img_cv2

    @clock
    def run(self):
        print("OCRThread")
        ocr_request = globalvar.get_var("ocrserver")
        while not ocr_request:
            self.sleep(1)
            ocr_request = globalvar.get_var("ocrserver")
        final_cv2 = None
        final_info = []
        final_html_content = []
        h, w, d = self.img_cv2.shape
        # 1、据说长度超过2000，适当缩放能增加识别的准确率，这是一种解决方式
        # if h >=2000:
        #     self.img_cv2 = cv2.resize(self.img_cv2,(int(w*0.9),int(h*0.5)), interpolation=cv2.INTER_AREA)
        # final_cv2,final_info,final_html_content = self.ocr_request.ocr_structure(self.img_cv2)
        # cv2_img,out_info= self.ocr_request.upload_ocr_info_thread(cv2_img, keep_format="2")

        # 2、更好方式是 把长图片拆成小图片
        # h = 0
        if h >= 960:
            # 以640为单位 把长图片分成小图片
            imgs_list = image_split.split(self.img_cv2, split_length=960, axis=1)
            for i, img_cv2_seg in enumerate(imgs_list):
                # 一小段一小段识别
                resize_img_cv2, out_info, html_content = ocr_request.ocr_structure(
                    img_cv2_seg
                )
                cv2.imwrite(f"{Path(__file__).parent}/tmp/seg{i}.png", resize_img_cv2)
                # 画识别的区域的图片再拼接起来
                if final_cv2 is None:
                    final_cv2 = resize_img_cv2
                else:
                    final_cv2 = vstack((final_cv2, resize_img_cv2))
                # 识别内容存起来
                final_info.extend(out_info)
                final_html_content.extend(html_content)
        else:
            final_cv2, final_info, final_html_content = ocr_request.ocr_structure(
                self.img_cv2
            )
        self.signal.emit((None, final_cv2, final_info, final_html_content))
        cv2.imwrite(f"{Path(__file__).parent}/tmp/ocr_draw_result.png", final_cv2)


"""
    第三版 实现连续接受图片 独立线程
    可以实现边截图或迭代图片，边OCR
    尽量使用这个，不满足就升级来兼容
    """


class ScreenShotTasks(QThread):
    """
    # 定義任務，在這裏主要創建線程
    """

    result = Signal(object)

    def __init__(self, max_thread_number=3, single_img_module_size=10):
        super().__init__()
        # self.pool = QThreadPool.globalInstance() 用这个会导致界面卡死，找不到原因
        self.pool = QThreadPool()
        # 設置最大線程數
        self.pool.setMaxThreadCount(max_thread_number)
        self.running = True
        self.img_package = []
        self.img_module = []
        self.img_chunk = []
        self.img_chunk_size = single_img_module_size

        self.final_file_path = get_temp_folder(
            des_folder_path=__file__, is_clear_folder=True
        )
        self.ImageMergeWithDetect = ImageMergeWithDetect(
            drop_head_tail=False,
            draw_match_output_path=self.final_file_path,
        )

    def add_img(self, img: np.ndarray | Image.Image):
        if isinstance(img, Image.Image):
            # 把图片转化为numpy的格式
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            # img = cv2.imdecode(
            #     np.asarray(bytearray(img), dtype=np.uint8), cv2.IMREAD_COLOR
            # )
        self.img_chunk.append(img)
        if len(self.img_chunk) == self.img_chunk_size:
            self.img_module.append(self.img_chunk.copy())
            self.img_chunk.clear()

    def stop_thread(self):
        # 最后图片模块结束时，收收尾
        if len(self.img_chunk) > 0:
            self.img_module.append(self.img_chunk.copy())
            self.img_chunk.clear()
        if len(self.img_module) > 0:
            self.img_package.append(self.img_module.copy())
            self.img_module.clear()
        self.running = False

    def run(self):
        while self.running or len(self.img_package):
            if len(self.img_package):
                img_modules = self.img_package.pop(0)
                # 需要给模块中的每一捆图片加序号，因为开多个线程，不确定每个线程处理结束时间，导致
                # 每捆合成后存到列表的的最终图片整个顺序是不确定的
                i = 0
                while len(img_modules):
                    i = i + 1
                    img_chunk = img_modules.pop(0)
                    worker = Worker(self.ImageMergeWithDetect.chunk_merge, img_chunk, i)
                    worker.setAutoDelete(True)  # 是否自動刪除
                    # worker.signals.progress.connect(self.update_progress)
                    # worker.signals.finished.connect(partial(self.readyOcr,1))
                    # worker.signals.result.connect(after_merge_and_ocr)
                    self.pool.start(worker)
                    # self.pool.start(Worker(merge_and_ocr_package,img_chunk.copy()))
                    print("submit handle a img package")
                self.pool.waitForDone()  # 等待任務執行完畢
                finalimg = self.ImageMergeWithDetect.module_merge()
                if finalimg is not None:
                    self.result.emit(ocr(finalimg, ocr_method="ocr"))
            else:
                QThread.msleep(1)
