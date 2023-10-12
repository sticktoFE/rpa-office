import random
from PIL import Image, ImageEnhance
import cv2
import numpy as np


def generate_random(adjust_num):
    min_range = 1
    max_range = 15.0
    random_range = min_range + (max_range - min_range) * adjust_num / 100
    # 生成随机数并保留两位小数
    random_number = round(random.uniform(min_range, random_range), 3)
    return random_number


# 2. 图像预处理以提高识别度
def scale_image(image: Image.Image | np.ndarray, adjust_num):
    scale_factor = generate_random(adjust_num)
    # 2. 图像缩放
    # 计算新的宽度和高度
    if isinstance(image, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # 转回RGB颜色空间
    new_width = int(image.width * scale_factor)
    new_height = int(image.height * scale_factor)
    # 进行插值，生成扩大尺寸后的图像
    image = image.resize((new_width, new_height), Image.LANCZOS)

    # 调整对比度和亮度（效果明显）
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(scale_factor)  # 适当调整对比度增强 2.0
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(scale_factor)  # 适当提高亮度 1.5

    # 3. 图像去噪
    # image_cv = np.array(image)  # 将Pillow图像转换为OpenCV图像
    # image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)  # 转换为BGR颜色空间
    # image_cv = cv2.fastNlMeansDenoisingColored(image_cv, None, 10, 10, 7, 21)
    # image = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))  # 转回RGB颜色空间

    # 4. 数据增强（轻微旋转）
    # 旋转图像
    rotation_angle = 0.1  # 旋转角度
    image = image.rotate(rotation_angle)

    # 5.添加噪声
    # noise = np.random.normal(0, 30, image.size)  # 生成均值为0，标准差为30的高斯噪声
    # image = Image.fromarray(np.array(image) + noise.astype(np.uint8))  # 添加噪声

    return image
