import time
import cv2
from pathlib import Path
from numpy import vstack
import hashlib
import http.client
import random
import sys
from PySide6.QtCore import (
    QObject, QThread, QThreadPool, Signal, QThread, Signal, QSettings)
from urllib.parse import quote
# 使用文字转语音功能，发出问候音：xx,你好！
from myutils.DateAndTime import clock
from myutils.GeneralThread import Worker, WorkerSignals
from myutils.image_merge import merge
from myutils.info_out_manager import get_temp_folder
from myutils.window_handle.ScreenShot import ScreenShot
from myutils import globalvar, image_split
import numpy as np
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
        cv2_img_draw, out_info, html_content = ocr_request.ocr_structure(
            cv2_img)
        self.signal.emit((cv2_img, cv2_img_draw, out_info, html_content))

        # cv2_img,out_info= self.ocr_request.upload_ocr_info_thread(cv2_img, keep_format="2")
        # self.signal.emit((cv2_img,out_info,html_content))
"""
    第二版 实现的划区域截图 独立线程
    先截图形成长图，再统一分割图片去识别，速度减慢
    """


class OCRScrollOut(QThread):
    """
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
        print("OCRScrollOut")
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
        # final_cv2,final_info,final_html_content = self.ocr_request.upload_ocr_structure_thread(self.img_cv2)
        # cv2_img,out_info= self.ocr_request.upload_ocr_info_thread(cv2_img, keep_format="2")

        # 2、更好方式是 把长图片拆成小图片
        # h = 0
        if h >= 960:
            # 以640为单位 把长图片分成小图片
            imgs_list = image_split.split(
                self.img_cv2, split_length=960, axis=1)
            for i, img_cv2_seg in enumerate(imgs_list):
                # 一小段一小段识别
                resize_img_cv2, out_info, html_content = ocr_request.ocr_structure(
                    img_cv2_seg)
                cv2.imwrite(
                    f'{Path(__file__).parent}/tmp/seg{i}.png', resize_img_cv2)
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
                self.img_cv2)
        self.signal.emit((None, final_cv2, final_info, final_html_content))
        cv2.imwrite(
            f'{Path(__file__).parent}/tmp/ocr_draw_result.png', final_cv2)


class TrThread(QThread):
    resultsignal = Signal(str)
    showm_singal = Signal(str)
    change_item_signal = Signal(str)

    def __init__(self, text, from_lan, to_lan):
        super(QThread, self).__init__()
        self.text = text
        self.toLang = to_lan
        self.appid = QSettings('Fandes', 'jamtools').value(
            'tran_appid', '20190928000337891', str)
        self.secretKey = QSettings('Fandes', 'jamtools').value(
            'tran_secretKey', 'SiNITAufl_JCVpk7fAUS', str)
        salt = str(random.randint(32768, 65536))
        sign = self.appid + self.text + salt + self.secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        q = quote(self.text)
        self.re_url = f'/api/trans/vip/translate?appid={self.appid}&q={q}&from={from_lan}' + \
            '&to={0}&salt=' + salt + '&sign=' + sign
        self.geturl = self.re_url.format(self.toLang)
        # self.args={"sign": sign,"salt":salt, "appid": self.appid,"to": to_lan,"from":from_lan ,"q":q}

    def run(self):
        if not str(self.text).replace(" ", "").replace("\n", ""):
            print("空翻译")
            self.resultsignal.emit("没有文本!")
            return
        try:
            # res = requests.get("https://api.fanyi.baidu.com",headers=self.args)
            # print(res.text)
            httpClient0 = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient0.request('GET', self.geturl)
            response = httpClient0.getresponse()
            print("strat t")
        except Exception:
            print(sys.exc_info())
            self.showm_singal.emit(f"翻译出错！请确保网络畅通！{sys.exc_info()[0]}")
        else:
            s = response.read().decode('utf-8')
            print(s)
            s = eval(s)
            text = ''
            # print(s)
            f_l = s['from']
            t_l = s['to']
            if f_l == t_l:
                if t_l == 'zh':
                    self.geturl = self.re_url.format('en')
                    try:
                        # jamtools.tra_to.setCurrentText('英语')
                        self.change_item_signal.emit("英语")
                    except Exception:
                        print(sys.exc_info())
                else:
                    self.geturl = self.re_url.format('zh')
                    try:
                        self.change_item_signal.emit("中文")
                    except Exception:
                        print(sys.exc_info())
                self.run()
                return
            for line in s['trans_result']:
                temp = line['dst'] + '\n'
                text += temp
            self.resultsignal.emit(text)


def ocr_split_long_pic(img_cv2):
    assert isinstance(img_cv2, (np.ndarray))
    print("ocr_split_long_pic")
    ocr_request = globalvar.get_var("ocrserver")
    while not ocr_request:
        time.sleep(1)
        ocr_request = globalvar.get_var("ocrserver")
    final_cv2_draw = None
    final_info = []
    final_html_content = []
    h, w, d = img_cv2.shape
    # 把长图片拆成小图片，设置成图片高度超过960就拆图片再识别，然后再合并图片和识别内容
    # h = 0
    if h >= 960:
        # 以640为单位 把长图片分成小图片
        imgs_list = image_split.split(img_cv2, split_length=960, axis=1)
        for img_cv2_seg in imgs_list:
            # 一小段一小段识别
            img_cv2_seg_draw, out_info, html_content = ocr_request.ocr_structure(
                img_cv2_seg)
            # cv2.imwrite(f'{Path(__file__).parent}/tmp/seg{i}.png',img_cv2_seg_draw)
            # 画识别的区域的图片再拼接起来
            final_cv2_draw = img_cv2_seg_draw if final_cv2_draw is None else vstack(
                (final_cv2_draw, img_cv2_seg_draw))
            # 识别内容存起来
            final_info.extend(out_info)
            final_html_content.extend(html_content)
    else:
        final_cv2_draw, final_info, final_html_content = ocr_request.ocr_structure(
            img_cv2)
    # cv2.imwrite(f'{Path(__file__).parent}/tmp/ocr_draw_result.png', final_cv2_draw)
    return (final_cv2_draw, final_info, final_html_content)
# 支持子线程再开孙子线程


class TasksThread(QThread):
    communication = None

    def __init__(self, img_package_list, max_thread_number=3):
        super().__init__()
        self.communication = WorkerSignals()
        self.tasks = Tasks(communication=self.communication,
                           img_package_list=img_package_list, max_thread_number=max_thread_number)

    def run(self):
        self.tasks.start()
# 定義任務，在這裏主要創建線程


class Tasks(QObject):
    def __init__(self, communication, img_package_list, max_thread_number):
        super().__init__()
        # self.pool = QThreadPool.globalInstance() 用这个会导致界面卡死，找不到原因
        self.pool = QThreadPool()
        # 設置最大線程數
        self.pool.setMaxThreadCount(max_thread_number)
        self.communication = communication
        self.communication.thread_stop.connect(self.thread_stop)
        self.in_rolling = True
        self.img_package_list = img_package_list
        self.final_file_path = get_temp_folder(
            execute_file_path=__file__,
            is_clear_folder=True
        )
        self.final_merge_file_path = get_temp_folder(execute_file_path=__file__,
                                                     des_folder_name="final_merge_pic",
                                                     is_clear_folder=True)

    def thread_stop(self):
        self.in_rolling = False

    def start(self):
        package_result = []
        print('merge_and_ocr thread name: ', QThread.currentThread())
        # 拼接一个包内的图片为长图片，并对长图片进行OCR识别

        def merge_and_ocr_package(img_list):
            print('merge_and_ocr_package thread name: ', QThread.currentThread())
            merge_result_img = merge(img_list[1], self.final_file_path)
            # final_cv2,final_info,final_html_content = ocr_request.ocr_structure(merge_result_img)
            package_result.append((img_list[0], merge_result_img))
            # progress_signal.emit(100*img_list[0]/500) 试图搞一个进度条，但因为 总的处理数未知，同时在一个进程中循环开多个进程不知道怎么获取每个进程的参数，所以暂时未实现
        # 对多个线程处理的长图片再合并成最终的长图片

        def merge_result():
            print('对多个线程处理的长图片再合并成最终的长图片')
            finalimg = None
            final_cv2_draw = None
            final_info = []
            final_html_content = []
            # 按照先后顺序排序，然后再拼接
            package_result_sorted = sorted(
                package_result, key=lambda item: item[0])
            finalimg = merge([item[1] for item in package_result_sorted],
                             self.final_merge_file_path, drop_head_tail=False)
            final_cv2_draw, final_info, final_html_content = ocr_split_long_pic(
                finalimg)
            self.communication.finished.emit(1)
            self.communication.result.emit(
                (finalimg, final_cv2_draw, final_info, final_html_content))
        while self.in_rolling or len(self.img_package_list):
            if len(self.img_package_list):  # 如果有图片
                img_list = self.img_package_list.pop(0)
                worker = Worker(merge_and_ocr_package, img_list)
                worker.setAutoDelete(True)  # 是否自動刪除
                # worker.signals.progress.connect(self.update_progress)
                # worker.signals.finished.connect(partial(self.readyOcr,1))
                # worker.signals.result.connect(after_merge_and_ocr)
                self.pool.start(worker)
                # self.pool.start(Worker(merge_and_ocr_package,img_list.copy()))
                print("submit handle a img package")
            else:
                # 等待图片到来 后台线程没有收到图片时,睡眠一下避免占用过高
                QThread.msleep(1)
                # print("等待图片包到来")
        self.pool.waitForDone()  # 等待任務執行完畢
        merge_result()
