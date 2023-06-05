from functools import reduce
import cv2
from numpy import vstack
from .image_compare import PicMatcher, real_content_imgs
from PIL import Image


# 使用对图像的侦测算法来合并图片
class ImageMergeWithDetect:
    def __init__(self, draw_match_output_path=None, drop_head_tail=False):
        self.draw_match_output_path = draw_match_output_path
        self.picMatcher = PicMatcher(
            nfeatures=500, draw=True, draw_match_output_path=draw_match_output_path
        )
        self.drop_head_tail = drop_head_tail
        self.package_result = []
        self.one_src_img = None

    # 针对图像列表寻找拼接点，后面的图片去掉与前面图片重复区域
    def merg_two(self, sum_img, img1, img2):
        # 调用picMatcher的match方法获取拼接匹配信息
        y_distance, m1, m2 = self.picMatcher.match(img1, img2)
        if y_distance == 0:
            return sum_img, img1
        # 裁剪拼接图片
        # 两个图片没有相似特征
        elif y_distance == -1:
            i1 = sum_img
            i2 = img2
        else:
            # 已拼接的图片finalimg必然包括compare_img1内容，每次循环 用compare_img1和compare_img2作比较
            # 然后把finalimg中已拼接compare_img1的内容和compare_img2进行融合
            # 当前已拼接图片的裁剪
            finalheightforcutting = sum_img.shape[0] - img1.shape[0] + int(m1)
            i1 = sum_img[:finalheightforcutting, :, :]
            # 新图片的裁剪
            i2 = img2[int(m2) :, :, :]
        # 当前已拼接图片和新图片拼接
        return vstack((i1, i2)), img2

    # 很纯粹，把列表中的图片去重后合并成长图
    def merge_list(self, img_list):
        merg_result = None
        for i, img in enumerate(img_list):
            if i == 0:
                merg_result = img
                recent_img = img
            else:
                merg_result, recent_img = self.merg_two(merg_result, recent_img, img)
        return merg_result

    # 合并图片列表时，考虑每张图片头尾都一样的情况
    def merge(self, src_img_list):
        if len(src_img_list) == 1:
            return src_img_list[0]
        drop_list_gen, self.content_pos_start, self.content_pos_end = real_content_imgs(
            src_img_list
        )
        if self.one_src_img is None:
            self.one_src_img = src_img_list[0]
        merg_result = self.merge_list(drop_list_gen)
        self.package_result.append(merg_result)
        cv2.imencode(".jpg", merg_result)[1].tofile(
            f"{self.draw_match_output_path}/{len(self.package_result)}_match.png"
        )

    # 对多个线程处理的长图片再合并成最终的长图片
    def merge_result(self):
        print("对多个线程处理的长图片再合并成最终的长图片")
        # 按照先后顺序排序，然后再拼接
        # package_result_sorted = sorted(self.package_result, key=lambda item: item[0])
        finalimg = self.merge_list(self.package_result)
        if not self.drop_head_tail:
            if self.content_pos_start > 0:
                head_seg = self.one_src_img[: self.content_pos_start]
                finalimg = vstack((head_seg, finalimg))
            if self.content_pos_end > 0 and self.content_pos_end < len(
                self.one_src_img
            ):
                tail_seg = self.one_src_img[self.content_pos_end :]
                finalimg = vstack((finalimg, tail_seg))
        return finalimg


# 此方法用于网页拼接，因为网页可以计算滚动条高度
class ImageMerge:
    root_path = None
    save_path = None
    im_list = []

    def __init__(self, save_path=None):
        print("ImageMerge->__init__")
        self.save_path = save_path
        self.im_list = []

    def add_im(self, path):
        print("ImageMerge.add_im", path)
        # im = Image.open(path)
        self.im_list.append(path)  # 直接传入Image
        return self

    def get_new_size(self):
        print("ImageMerge->get_new_size")
        max_width = 0
        total_height = 0
        # 计算合成后图片的宽高（以最宽的为准）和高度
        for img in self.im_list:
            width, height = img.size
            if width > max_width:
                max_width = width
            total_height += height
        return max_width, total_height

    def image_merge(self, filename):
        file_path = f"{self.save_path}/{filename}"
        if len(self.im_list) > 1:
            max_width, total_height = self.get_new_size()
            # 产生一张空白图
            new_img = Image.new("RGB", (max_width - 15, total_height), 255)
            x = y = 0
            for img in self.im_list:
                width, height = img.size
                new_img.paste(img, (x, y))
                y += height
        else:
            obj = self.im_list[0]
            width, height = obj.size
            left, top, right, bottom = 0, 0, width, height
            box = (left, top, right, bottom)
            region = obj.crop(box)
            new_img = Image.new("RGB", (width, height), 255)
            new_img.paste(region, box)
        new_img.save(file_path)
        return file_path, new_img
