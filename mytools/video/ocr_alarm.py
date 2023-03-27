import cv2

# 使用文字转语音功能，发出问候音：xx,你好！
from win32com.client import Dispatch


def welcome(id):
    msg = "你好，" + str(id)
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(msg)
    del speaker


# 对图片进行脸部一系列识别 并标注在图片上
def face_ocr(frame_img):
    img = frame_img
    # 1、人脸识别
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    # 人脸检测，1.3和2分别为图片缩放比例和需要检测的有效点数
    faces = face_cascade.detectMultiScale(frame_img, scaleFactor=1.3, minNeighbors=2)
    # 2、眼睛、微笑识别
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    smile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_smile.xml"
    )
    for x, y, w, h in faces:
        # 画出人脸框，蓝色，画笔宽度微
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
        face_area = img[y : y + h, x : x + w]
        # 1）、人眼检测
        # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        eyes = eye_cascade.detectMultiScale(face_area, 1.3, 10)
        for ex, ey, ew, eh in eyes:
            # 画出人眼框，绿色，画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
        # 2）、微笑检测
        # 用微笑级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
        smiles = smile_cascade.detectMultiScale(
            face_area,
            scaleFactor=1.16,
            minNeighbors=65,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        for ex, ey, ew, eh in smiles:
            # 画出微笑框，红色（BGR色彩体系），画笔宽度为1
            cv2.rectangle(face_area, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 1)
            cv2.putText(img, "Smile", (x, y - 7), 3, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
    return img


# 调用摄像头摄像头
cap = cv2.VideoCapture(0)
while True:
    # 获取摄像头拍摄到的画面 ret true表示拍摄成功  frame拍摄的照片
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = face_ocr(gray)
    # 实时展示效果画面
    cv2.imshow("frame2", img)
    # 每5毫秒监听一次键盘动作,按q退出
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break
cap.release()
welcome("阳光")
# 最后，关闭所有窗口
cv2.destroyAllWindows()
