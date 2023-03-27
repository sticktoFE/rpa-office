import cv2
import numpy as np
from myutils.DateAndTime import clock
from PySide6.QtCore import QThread, Signal
from myutils import globalvar

# 使用文字转语音功能，发出问候音：xx,你好！
from win32com.client import Dispatch


def welcome(id):
    msg = "退出"
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(msg)
    del speaker


# 对图片进行脸部一系列识别 并标注在图片上
def face_ocr(frame_img):
    img = frame_img
    face_cascade = cv2.CascadeClassifier(
        f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(frame_img, scaleFactor=1.3, minNeighbors=2)
    eye_cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_eye.xml")
    smile_cascade = cv2.CascadeClassifier(
        f"{cv2.data.haarcascades}haarcascade_smile.xml"
    )
    for x, y, w, h in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_area = img[y : y + h, x : x + w]
        eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
        for ex, ey, ew, eh in eyes:
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
        smiles = smile_cascade.detectMultiScale(
            face_area,
            scaleFactor=1.16,
            minNeighbors=65,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        for ex, ey, ew, eh in smiles:
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
            cv2.putText(img, "Smile", (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
    return img


"""
    对图片进行ocr识别，作为识别工具直接展示识别内容
    
        # 数据获取来源有以下几种：
    # 1、爬取网页
    # 2、解析pdf
    # 3、摄像头拍照
    # 4、桌面截图
  # 以下实现3   
"""


class OCRVideo(QThread):
    signal = Signal(tuple)
    signal_img = Signal(np.ndarray)

    def __init__(self, **kwargs):
        super().__init__()
        self.runCon = True
        self._isPause = False  # 线程暂停
        self.cap = None

    def pause(self):
        self._isPause = True

    # 线程恢复
    def resume(self):
        self._isPause = False

    def stop(self):
        if self.isRunning():
            self.runCon = False
            self.quit()
            self.wait()

    @clock
    def run(self):
        print("OCRVideo进程开始")
        ocr_request = globalvar.get_var("ocrserver")
        while not ocr_request:
            self.sleep(1)
            ocr_request = globalvar.get_var("ocrserver")
        if self.cap is None or not self.cap.isOpened():
            # 1、调用笔记本摄像头摄像头
            self.cap = cv2.VideoCapture(1)
            # 2、调用手机摄像头
            # http://admin:lbllei@192.168.1.7:8099/video 这个连接速度快
            # http://admin:lbllei@a2322ogcplzqf.local:8099/video
            # self.cap = cv2.VideoCapture(
            #     # "http://admin:admin@172.15.39.33:4747/mjpegfeed?640x480"
            #     "http://admin:admin@172.15.39.33:4747/video"
            # )  # @前为账号密码，@后为ip地址
        # print("CAM0 分辨率 %d x %d" % (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        # self.cap.set(10,100) #亮度设为100
        # self.cap.set(11,128) #对比度设为128
        # self.cap.set(12,128) #饱和度设为128
        # kk = 0
        while self.runCon and self.cap.isOpened():
            # kk += 1
            # 获取摄像头拍摄到的画面 ret true表示拍摄成功  frame拍摄的照片
            ret, show = self.cap.read()
            # show = cv2.resize(show,(260,480)) # width, height
            # show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            # 旋转90度
            # show = cv2.rotate(show, cv2.ROTATE_90_CLOCKWISE)
            # cv2.imwrite("tmp/example.png", frame) # 将拍摄内容保存为png图片
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # img = cv2.imdecode(np.fromfile(frame, dtype=np.uint8), -1)
            # img = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), -1)
            # 调用模型进行识别 并把相应信息保存到临时目录下
            # html_content = []
            # img_show, result = ocr_request.ocr(show)
            # img_show,result = self.ocr_request.upload_ocr_info_thread(show,keep_format="2")
            # 人脸识别
            # img_show = face_ocr(frame)
            # img_show = cv2.flip(img_show,1)
            # 实时展示效果画面
            # cv2.imshow('识别器',img_show)
            self.signal_img.emit(show)
            # img_show.show()
            # 识别出来后，存入数据库
            # self.save()
            while self._isPause:
                # 展示识别的内容
                (
                    img_show,
                    result,
                    html_content,
                ) = ocr_request.ocr_structure(show)
                self.signal.emit((show, img_show, result, html_content))
                self.sleep(1)
            # 每5毫秒监听一次键盘动作,按q退出
            if cv2.waitKey(25) & 0xFF == ord("q"):
                # self.mutex.unlock()  # 解锁
                break
        self.cap.release()
        welcome("阳光")
        # 最后，关闭所有窗口
        cv2.destroyAllWindows()

    # # 把获取的信息保存到数据库
    # def save(self):
    #   temp_list = []
    #   line_list = []
    #   temp_y = 0

    #   for line in out_info:
    #       # print(line)
    #       if abs(line[0][0][1]-temp_y) < 6:  # 认为两个文字块儿的左上角坐标y值相差不超过6，认为是一行的
    #           line_list.append([line[0][0][0], line[1][0]]
    #                             )  # 把坐标x也存进，方便排序以确定一行的顺序
    #           temp_y = line[0][0][1]  # 识别的一个文字块儿的左上角的坐标的y值
    #       else:
    #           line_list.sort(key=lambda x: x[0])
    #           line_info_list = [istr[1] for istr in line_list]
    #           temp_list.append(line_info_list)
    #           line_list.clear()
    #           line_list.append([line[0][0][0], line[1][0]])
    #           temp_y = line[0][0][1]  # 识别的一个文字块儿的左上角的坐标的y值

    #   self.signal.emit(temp_list)
