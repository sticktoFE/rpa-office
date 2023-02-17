from functools import reduce
from pathlib import Path
import cv2
from numpy import vstack
from .image_compare import PicMatcher
from PIL import Image
# 针对图像列表寻找拼接点，后面的图片去掉与前面图片重复区域
def drop_repeat(src_img_list,draw_match_output=None,drop_head_tail = True):
    picMatcher = PicMatcher(nfeatures=500,draw=True,draw_match_output=draw_match_output)
    # 只有迭代器才有 next方法 ，生成器是一个迭代器
    img_gen = iter(src_img_list)
    if drop_head_tail:
        img_gen = picMatcher.drop_head_tail(src_img_list)
    rgbimg1 = next(img_gen)
    drop_result_list = []
    # 如果正在滚动状态或self.img_list还有图片没有处理完就一直处理
    for rgbimg2 in img_gen: 
        # 调用picMatcher的match方法获取拼接匹配信息
        y_distance, m1, m2 = picMatcher.match(rgbimg1, rgbimg2)
        if y_distance == 0:
            continue
        elif y_distance == -1:
            drop_result_list.append(rgbimg1)
        else:
            # 逻辑是，每次循环用前一个compare_img1和后一个compare_img2作比较，
            # compare_img1重复区域最下面的边界点对应的compare_img2的的点就是compare_img2的切割点，要下面的即可
            rgbimg1 = rgbimg1[:int(m1),:,:]
            drop_result_list.append(rgbimg1)
            rgbimg2 = rgbimg2[int(m2):, :, :]
        rgbimg1 = rgbimg2
    return drop_result_list
# 图像寻找拼接点并拼接的主函数,运行于后台线程,从self.img_list中取数据进行拼接
def merge_1(src_img_list,draw_match_output=None,drop_head_tail = True):
    drop_repeat_list = drop_repeat(src_img_list,draw_match_output,drop_head_tail)
    print("image_merge.match_and_merge-sucess merge a img")
    return reduce(lambda x, y:vstack((x,y)),drop_repeat_list)

# 图像寻找拼接点并拼接的主函数,运行于后台线程,从self.img_list中取数据进行拼接
def merge(src_img_list,draw_match_output=None,drop_head_tail = True):
    picMatcher = PicMatcher(nfeatures=500,draw=True,draw_match_output=draw_match_output)
    # 只有迭代器才有 next方法 ，生成器是一个迭代器
    img_gen = iter(src_img_list)
    if drop_head_tail:
        img_gen = picMatcher.drop_head_tail(src_img_list)
    finalimg = next(img_gen)
    rgbimg1 = finalimg 
    # 如果正在滚动状态或self.img_list还有图片没有处理完就一直处理
    for rgbimg2 in img_gen:
        # 调用picMatcher的match方法获取拼接匹配信息
        y_distance, m1, m2 = picMatcher.match(rgbimg1, rgbimg2)
        if y_distance == 0:
            continue
        # 裁剪拼接图片
        #两个图片没有相似特征
        elif y_distance == -1:
            i1 = finalimg
            i2 = rgbimg2
        else:
            # 已拼接的图片finalimg必然包括compare_img1内容，每次循环 用compare_img1和compare_img2作比较
            # 然后把finalimg中已拼接compare_img1的内容和compare_img2进行融合
            #当前已拼接图片的裁剪
            finalheightforcutting = finalimg.shape[0] - rgbimg1.shape[0] + int(m1)  
            i1 = finalimg[:finalheightforcutting, :, :]
            #新图片的裁剪
            i2 = rgbimg2[int(m2):, :, :]
        # 当前已拼接图片和新图片拼接
        finalimg = vstack((i1, i2))
        rgbimg1 = rgbimg2
    return finalimg

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
    