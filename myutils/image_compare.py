# 利用python实现多种方法来实现图像识别
import datetime
from functools import reduce
import itertools
import math
import operator
import cv2
import numpy as np
from numpy import zeros, uint8


# 计算汉明距离
def hammingDist(hash1, hash2):
    assert len(hash1) == len(hash2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2))


# # 1. 平均哈希算法（aHash）：
# aHash的计算步骤：
# 先将图片压缩成8*8的小图
# 将图片转化为灰度图
# 计算图片的Hash值，这里的hash值是64位，或者是32位01字符串
# 将上面的hash值转换为16位的
# 通过hash值来计算汉明距离
def aHash_1(image):
    # 缩放为8*8
    image = cv2.resize(image, (8, 8))
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 求平均灰度
    avreage = np.mean(gray)
    hash = []
    for i, j in itertools.product(range(gray.shape[0]), range(gray.shape[1])):
        if gray[i, j] > avreage:
            hash.append(1)
        else:
            hash.append(0)
    return hash


#   2.感知哈希算法（pHash）：
# pHash的计算步骤：
# 缩小图片：32 * 32是一个较好的大小，这样方便DCT计算转化为灰度图
# 转化为灰度图
# 计算DCT：利用Opencv中提供的dct()方法，注意输入的图像必须是32位浮点型，所以先利用numpy中的float32进行转换
# 缩小DCT：DCT计算后的矩阵是32 * 32，保留左上角的8 * 8，这些代表的图片的最低频率
# 计算平均值：计算缩小DCT后的所有像素点的平均值。
# 进一步减小DCT：大于平均值记录为1，反之记录为0.
# 得到信息指纹：组合64个信息位，顺序随意保持一致性。
# 最后比对两张图片的指纹，获得汉明距离即可。
# 输入灰度图，返回dhash
def pHash_1(image):
    # 缩放32*32
    image = cv2.resize(image, (32, 32))  # , interpolation=cv2.INTER_CUBIC
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 将灰度图转为浮点型，再进行dct变换
    dct = cv2.dct(np.float32(gray))
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct_roi = dct[0:8, 0:8]
    # 再使用平均哈希算法
    avreage = np.mean(dct_roi)
    hash = []
    for i, j in itertools.product(range(dct_roi.shape[0]), range(dct_roi.shape[1])):
        if dct_roi[i, j] > avreage:
            hash.append(1)
        else:
            hash.append(0)
    return hash


#  3. 差异值哈希算法（dHash）：
# 相比pHash，dHash的速度要快的多，相比aHash，dHash在效率几乎相同的情况下的效果要更好，它是基于渐变实现的。
# dHash的hanming距离步骤：
# 先将图片压缩成9*8的小图，有72个像素点
# 将图片转化为灰度图
# 计算差异值：dHash算法工作在相邻像素之间，这样每行9个像素之间产生了8个不同的差异，一共8行，则产生了64个差异值，或者是32位01字符串。
# 获得指纹：如果左边的像素比右边的更亮，则记录为1，否则为0.
# 最后比对两张图片的dHash指纹，获得汉明距离即可
# 差异值哈希算法
# 差值感知算法
def dHash_1(img):
    # 缩放9*8
    # cv2.resize(img,(width, height))，所以(9,8)是9列8行 而 numpy.shape[0]表示行  numpy.shape[1]表示列 注意区别
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash = []
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j + 1]:
                hash.append(1)
            else:
                hash.append(0)
    return hash


#################针对上面的利用矩阵计算，加快速度
# 均值哈希算法
def aHash(img):
    img = cv2.resize(img, (8, 8))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    np_mean = np.mean(gray)  # 求numpy.ndarray平均值
    ahash_01 = (
        gray > np_mean
    ) + 0  # 大于平均值=1，否则=0  numpy.array比较结果值是True False +0 可以转化成 1 0
    return ahash_01.reshape(1, -1)[0].tolist()  # 展平->转成列表


def pHash(img):
    img = cv2.resize(img, (32, 32))  # 默认interpolation=cv2.INTER_CUBIC
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dct = cv2.dct(np.float32(gray))
    dct_roi = dct[0:8, 0:8]  # opencv实现的掩码操作
    avreage = np.mean(dct_roi)
    phash_01 = (dct_roi > avreage) + 0
    return phash_01.reshape(1, -1)[0].tolist()


def dHash(img):
    img = cv2.resize(img, (9, 8))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    hash_str0 = []
    # for i in range(8):
    #       hash_str0.append(gray[:, i] > gray[:, i + 1])
    # hash_str1 = np.array(hash_str0)+0
    # phash_01 = hash_str1.T
    phash_01 = (gray[:, :-1] > gray[:, 1:]) + 0
    return phash_01.reshape(1, -1)[0].tolist()


def dDistance(img1, img2):
    dhash_str1 = dHash(img1)
    dhash_str2 = dHash(img2)
    return hammingDist(dhash_str1, dhash_str2)


# 通过得到RGB每个通道的直方图来计算相似度
def classify_hist_with_split(image1, image2, size=(256, 256)):
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = sum(calculate(im1, im2) for im1, im2 in zip(sub_image1, sub_image2))
    return sub_data / 3


# 计算单通道的直方图的相似值
def calculate(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 可以比较下直方图
    # plt.plot(range(256),hist1,'r')
    # plt.plot(range(256),hist2,'b')
    # plt.show()
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    return degree / len(hist1)


# 图像匹配类
# from PySide6.QtCore import QThread
class PicMatcher:
    def __init__(self, nfeatures=500, draw=False, draw_match_output_path=None):
        self.SIFT = cv2.SIFT_create(nfeatures=nfeatures)  # 生成sift算子(抽取图片特征)
        self.bf = cv2.BFMatcher(crossCheck=False)  # 生成图像匹配器（根据计算相似性）
        self.draw = draw
        self.draw_match_output_path = draw_match_output_path

    # 图像匹配函数,获得图像匹配的点以及匹配程度
    def match(self, im1, im2):
        im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        # 保存各自图片（保存合体划线图即可，所以注释了）
        file_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        cv2.imencode(".jpg", im1)[1].tofile(
            f"{self.draw_match_output_path}/{file_time}_01.png"
        )
        cv2.imencode(".jpg", im2)[1].tofile(
            f"{self.draw_match_output_path}/{file_time}_02.png"
        )
        kps1, des1 = self.SIFT.detectAndCompute(im1, None)
        kps2, des2 = self.SIFT.detectAndCompute(im2, None)
        matches = self.bf.knnMatch(des1, des2, k=2)
        good = []
        tempgoods = []
        y_gaps = {}
        for m, n in matches:
            # m.distance == 0:  这个特征判断是完全相似，太苛刻，采用第一个相似度小于次相似度的50%就行
            if m.distance < n.distance * 0.75:
                pos0 = kps1[m.queryIdx].pt
                pos1 = kps2[m.trainIdx].pt
                # 滑动截图的图片，前后两张重叠部分，相似的特征必然在x方向上一样，y方向上不一样，
                # 即数组坐标 x1,y1和x2,y2
                # 要求x1和x2相同，只是y1和y2在不同位置，如果也相同，两张截图可以认为是一样的
                if pos0[0] == pos1[0] and pos0[1] > pos1[1]:  # 筛选拼接点
                    d = int(pos0[1] - pos1[1])
                    if d in y_gaps:
                        y_gaps[d] += 1
                    else:
                        y_gaps[d] = 0
                    tempgoods.append(m)
        # 为空说明两张没有相似特征
        # 4为特征点数,当大于4时才认为特征明显
        if not y_gaps:
            print("rt -1 0 0：两张图找不到相似特征1")
            return -1, 0, 0
        best_y_gaps = max(y_gaps, key=lambda key: y_gaps[key])
        if y_gaps[best_y_gaps] < 2:
            print("rt -1 0 0：两张图找不到相似特征2")
            return -1, 0, 0
        max1y = max2y = 0
        for match in tempgoods:
            pos0 = kps1[match.queryIdx].pt
            pos1 = kps2[match.trainIdx].pt
            if int(pos0[1] - pos1[1]) == best_y_gaps:
                if pos0[1] > max1y:
                    max1y = pos0[1]
                    max2y = pos1[1]
                good.append(match)
        if self.draw:
            self.draw_join_line(im1, im2, kps1, kps2, good)
        return best_y_gaps, max1y, max2y

    def draw_join_line(self, im1, im2, kps1, kps2, good):
        img3 = cv2.drawMatches(im1, kps1, im2, kps2, good, None, flags=2)
        # 新建一个空图像用于绘制特征点
        img_sift1 = zeros(im1.shape, uint8)
        img_sift2 = zeros(im2.shape, uint8)
        # 绘制特征点
        cv2.drawKeypoints(im1, kps1, img_sift1)
        cv2.drawKeypoints(im2, kps2, img_sift2)
        # imwrite对路径要求只能是数字和英文，很苛刻--这里保留遗迹，尽量用cv2.imencode
        file_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

        cv2.imencode(".jpg", img3)[1].tofile(
            f"{self.draw_match_output_path}/{file_time}_match.png"
        )
        # cv2.imwrite(f"{self.draw_match_output_path}/{file_time}_match.png", img3)


def is_same(img1, img2):  # 判断两张图片的相似度,用于判断结束条件
    h1 = img1.histogram()
    h2 = img2.histogram()
    # 求所有像素点的协方差，似乎也是一种测量图片差异度的方式
    result = math.sqrt(
        reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1)
    )
    return result <= 5


# 计算同样高度的图片，相同的头部和尾部部分
# 计算每个图片横向像素均值，然后计算图片间横向的方差
# 方差小的，比如小于等于所有方差均值的认为两者差异很小，视为两区域相似
def real_content_imgs(img_list):
    data = []
    for img in img_list:
        h, w, n = img.shape
        # 计算图片每行的均值,形成一个一维数组，1表示横向计算均值
        data.append(img.reshape((h, -1)).mean(1))
    # 转置以下始终行代表图片的一行
    data = np.array(data).transpose()
    # 然后继续横向计算方差，看下图片横向的差异度
    var = data.var(1)
    # where返回的是满足条件的的形式为 ([index1,index2..],dtype=int64)
    where = np.where(var > var.mean())[0]
    img_sart_pos = where.min()
    img_end_pos = where.max() + 1
    return (
        [img[img_sart_pos:img_end_pos] for img in img_list],
        img_sart_pos,
        img_end_pos,
    )


if __name__ == "__main__":
    raw_img1 = r"C:\Users\loube\Pictures\C-B1.png"
    raw_img2 = r"C:\Users\loube\Pictures\C-B2.png"
    img1 = cv2.imread(raw_img1)
    img2 = cv2.imread(raw_img2)

    # gen_pic = drop_head_tail([img1, img2])
    # cv2.imwrite("drop_head_tail_match1.png", next(gen_pic))
    # cv2.imwrite("drop_head_tail_match2.png", next(gen_pic))
    # ahash_str1 = aHash(img1)
    # ahash_str2 = aHash(img2)

    # phash_str1 = pHash(img1)
    # phash_str2 = pHash(img2)

    # dhash_str1 = dHash(img1)
    # dhash_str2 = dHash(img2)
    # a_score = hammingDist(ahash_str1, ahash_str2)
    # p_score = hammingDist(phash_str1, phash_str2)
    # d_score = hammingDist(dhash_str1, dhash_str2)

    # n = classify_hist_with_split(img1, img2)
    # print("三直方图算法相似度：", n)
    # print(f"a_score:{a_score},p_score:{p_score},d_score{d_score}")
