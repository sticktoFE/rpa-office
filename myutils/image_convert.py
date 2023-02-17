# Pillow → OpenCV
import os
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QPixmap, Qt, QImage
import numpy as np
import cv2
from PIL import Image, ImageQt


def pil2cv(image):
    """PIL型 -> OpenCV型"""
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


""" 这个更原始些，直接操作第三维的顺序进行转化，道出了上面cv2.cvtColor逻辑 """


def pil2cv_2(image):
    """PIL型 -> OpenCV型"""
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    return new_image


# OpenCV → Pillow


def cv2pil(image):
    """OpenCV型 -> PIL型"""
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


""" 这个更原始些，直接操作第三维的顺序进行转化，道出了上面cv2.cvtColor逻辑 """


def cv2pil_2(image):
    """OpenCV型 -> PIL型"""
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = new_image[:, :, ::-1]
    elif new_image.shape[2] == 4:  # 透過
        new_image = new_image[:, :, [2, 1, 0, 3]]
    new_image = Image.fromarray(new_image)
    return new_image


def get_shot_bytes(qPixmap):
    shot_bytes = QByteArray()
    buffer = QBuffer(shot_bytes)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    #   qPixmap = qPixmap.toImage()
    qPixmap.save(buffer, "png")
    return shot_bytes.data()


def savePixmap(pixmap, dirName):
    shot_bytes = QByteArray()
    buffer = QBuffer(shot_bytes)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    shot_img = pixmap.toImage()
    img_path = os.path.join(dirName, "screenshot.png")
    shot_img.save(img_path, "png")
    return img_path


def pixmap2cv_2(pixmap):
    byte_str = get_shot_bytes(pixmap)
    return cv2.imdecode(np.frombuffer(byte_str, dtype=np.uint8), cv2.IMREAD_COLOR)


def pixmap2cv_1(pixmap):
    pil_img = ImageQt.fromqpixmap(pixmap)
    return pil2cv(pil_img)


# QPixmap 转为 CV2 此方法自由，可以裁剪
def pixmap2cv(qtpixmap: QPixmap):
    # print("-----QPixmap_to_Opencv-----")
    # print("qtpixmap type:", type(qtpixmap))
    qimg = qtpixmap.toImage()  # QPixmap-->QImage
    # print("qimg type:", type(qimg))
    temp_shape = (qimg.height(), qimg.bytesPerLine()
                  * 8 // qimg.depth())  # 高 宽
    temp_shape += (4,)  # 通道数
    # print(f"pixmap2cv 转化图片格式，图形形状为{temp_shape}")
    ptr = qimg.bits()
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]  # 去掉通道第4个 A 即透明度
    # cv2.imwrite('./result.jpg',result) # 保存的话会显示RGB格式
    return result


def cv2pixmap(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    # cv2image深度为8位
    convert_to_Qt_format = QImage(
        rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888
    )
    # cv2image深度为16位  还有32位 Format_RGB32
    # convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_Grayscale16)
    # convert_to_Qt_format = convert_to_Qt_format.scaled(disply_width, display_height, Qt.KeepAspectRatio)
    return QPixmap.fromImage(convert_to_Qt_format)


def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    # Bild in RGBA konvertieren, falls nicht bereits passiert
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QImage(
        data, im.size[0], im.size[1], QImage.Format.Format_ARGB32)
    pixmap = QPixmap.fromImage(qim)
    return pixmap
