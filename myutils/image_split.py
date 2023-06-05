import cv2
import numpy as np


# 求 index_list中最接近l2的值
def get_idx(l2, index_list):
    min_dis = 1000
    idx = 0
    for i in index_list:
        dis = abs(l2 - i)
        if dis < min_dis:
            min_dis = dis
            idx = i
    return idx


# 把图片 img 分成 split_num 块axis 1是横向切块 0 纵向切块
def split(img, split_num=0, split_length=0, axis=1):
    height, width, _ = img.shape
    if split_num == 0 and split_length > 0:
        split_num = (
            width // split_length + 1 if axis == 0 else height // split_length + 1
        )
    if split_num > 0 and split_length == 0:
        split_length = width // split_num if axis == 0 else height // split_num
    """
    将图片二值化后，在纵轴或横轴方向求和
    """
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(f"D:\\leichui\\workspace\\rpa-ocr_dev\\myutils\\img_gray.jpg", GrayImage)
    ret, plate_binary_img = cv2.threshold(
        GrayImage, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    # cv2.imwrite(f"D:\\leichui\\workspace\\rpa-ocr_dev\\myutils\\img_gray_binary.jpg", plate_binary_img)
    row_histogram = np.sum(plate_binary_img, axis=axis)
    # 1、空白区域index,有效index为前后都是空白的index，这个范围可以调整,原先是检测反转后的空白页，但发现相反的图片，
    # 即原来是黑底白字，空白处二值化后变成了255的倍数是空白的，就没办法处理了
    # index_list = [index for index in range(1,row_histogram.shape[0]-1) if row_histogram[index] == 0 and row_histogram[index - 1] == 0 and row_histogram[index + 1] == 0]
    index_list = [
        index
        for index in range(1, row_histogram.shape[0] - 1)
        if row_histogram[index] == row_histogram[index - 1]
        and row_histogram[index] == row_histogram[index + 1]
    ]
    # 2、根据需要分的块数 基于上面的列表寻找最终的切分 index
    idx_list = []
    for i in range(split_num - 1):
        l2 = split_length * (i + 1)
        idx = get_idx(l2, index_list)
        idx_list.append(idx)
    idx_list.append(width - 1) if axis == 0 else idx_list.append(height - 1)
    # 3、根据2的index对图片进行切分
    img_list = []
    for i, idx in enumerate(idx_list):
        if i == 0:
            img_list.append(img[:, :idx, :]) if axis == 0 else img_list.append(
                img[:idx, :, :]
            )
        else:
            img_list.append(
                img[:, idx_list[i - 1] : idx, :]
            ) if axis == 0 else img_list.append(img[idx_list[i - 1] : idx, :, :])

    return img_list


if __name__ == "__main__":
    img = cv2.imread(r"D:\leichui\workspace\rpa-ocr_dev\myutils\jam_outputfile.png")
    img_list = split(img, 0, 640)
    for idx, im in enumerate(img_list):
        cv2.imwrite(f"D:\\leichui\\workspace\\rpa-ocr_dev\\myutils\\{idx}.jpg", im)
