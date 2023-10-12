from pathlib import Path
import random
from airtest.core.api import *
from airtest.core.android.android import *
from airtest.core.error import TargetNotFoundError
import logging

logger = logging.getLogger("airtest")
# 控制日志输出水平，免得打印太多
logger.setLevel(logging.ERROR)


# 1、打开应用
def open_app():
    android = Android()
    android.get_default_device()
    # 手机：XPL0220327004608  平板： R52TC00LB3K
    auto_setup(
        __file__,
        logdir=None,
        devices=[
            "android://127.0.0.1:5037/XPL0220327004608?cap_method=MINICAP&touch_method=MAXTOUCH&",
        ],
        project_root="D:/leichui/workspace/rpa-ocr_dev/auto_app",
    )
    # 获取应用的包名
    # print([app for app in android.list_app(third_only=True) if "zy" in app])
    # script content
    # 1、打开目标应用
    keyevent("HOME")
    android.stop_app("com.csii.zybk.ui")
    android.start_app("com.csii.zybk.ui")
    print("start...")
    sleep(5)


# 2、关掉一些弹窗信息，也可以关掉广告之类的干扰信息
def handle_disturb():
    ignore = exists(
        Template(
            r"tpl1686555850065.png", record_pos=(-0.054, 0.241), resolution=(2960, 1848)
        )
    )
    if ignore:
        touch(ignore)
    shutdown = exists(
        Template(
            r"tpl1686616946994.png", record_pos=(0.384, -0.584), resolution=(1080, 2340)
        )
    )
    if shutdown:
        touch(shutdown)


# 3、进入目标栏目
def to_purpose():
    try:
        licai = wait(
            Template(
                r"tpl1686554972586.png",
                record_pos=(-0.195, -0.374),
                resolution=(1080, 2340),
            )
        )
    except TargetNotFoundError as e:
        licai = wait(
            Template(
                r"tpl1686556335825.png",
                record_pos=(-0.065, -0.082),
                resolution=(2960, 1848),
            )
        )
    if licai:
        touch(licai)
    all_licai = wait(
        Template(
            r"tpl1686046347976.png", record_pos=(0.125, -0.025), resolution=(2960, 1848)
        )
    )
    if all_licai:
        touch(all_licai)


# 寻找列表中每个项目的关键特征点,获得其坐标，作为进入详情的点击点
# 处理逻辑是，使用find_all寻找到所有特征点位置，通过每个位置y坐标正排序来保证点击点是从上而下的
def get_list_drag_start_pos():
    zyordx_poses = []
    pics = [Template(r"tpl1686566547210.png"), Template(r"tpl1686566581111.png")]
    for pic in pics:
        pic_pos = find_all(pic)
        if pic_pos is not None:
            zyordx_poses.extend(pic_pos)
    zyordx_poses = sorted(zyordx_poses, key=lambda x: x["result"][1])
    return zyordx_poses


# 处理信息列表
def handle_list(worker):
    # 4、通过滚动产品列表，并进去产品信息页面获取产品信息
    syjj_drag_end_pos = exists(Template(r"tpl1686564142980.png"))
    # 开始迭代产品列表，获取产品信息
    while True:
        #         等待加载完毕
        sleep(random.uniform(0.2, 1))
        zyordx_poses = get_list_drag_start_pos()
        # 遍历每个产品项
        for zyordx_pos in zyordx_poses:
            # 打开产品详情
            touch(zyordx_pos["result"])
            get_detail(worker)
        #     滑动到下一个产品
        if not exists(Template(r"tpl1686219652816.png")) and len(zyordx_poses) > 0:
            # 这个会触发加载，导致页面并没有网上拖动多少，为了尽量减少重复内容，就再网上拖一次，但无法避免没有加载情况下多拖动的情况,待研究
            swipe(zyordx_poses[-1]["result"], syjj_drag_end_pos)

        else:
            break


# 寻找详情页关键特征点，,获得其坐标，作为滑动的起始点，
# 处理逻辑是以此判断罗列的特征点能不能找到，找到了就算命中，尽量寻找所有详情页的关键特征点，以减少整体的特征点数
def get_detail_drag_start_pos():
    # 截图的图片对象列表
    picList = [
        Template(
            r"tpl1686062879117.png",
            record_pos=(-0.369, -0.307),
            resolution=(1080, 2340),
        ),
        Template(
            r"tpl1686064382793.png",
            record_pos=(-0.346, 0.164),
            resolution=(1080, 2340),
        ),
    ]
    for pic in picList:
        pos = exists(pic)
        if pos:
            return pos
            break  # 只要找到图片列表中的任何一张图片，就可以
    # 实在找不到特征，自定义一个位置也可
    return (-0.346, 0.164)


# 4、获取详细信息
def get_detail(worker):
    pos_back = exists(
        Template(
            r"tpl1686061335759.png",
            record_pos=(-0.444, -0.949),
            resolution=(1080, 2340),
        )
    )
    drag_pos = get_detail_drag_start_pos()
    while True:
        worker.add_img(G.DEVICE.snapshot())
        if not exists(Template(r"tpl1686062712098.png")):
            swipe(drag_pos, vector=[0.0, -0.6])
            sleep(random.uniform(0.2, 1))
        else:
            worker.stop_thread()
            break
    #    返回产品列表页
    touch(pos_back)
    sleep(random.uniform(0.2, 1))


def get_app_info(worker):
    # 启动多线程把图片拼接成长图并ocr识别
    open_app()
    handle_disturb()
    to_purpose()
    handle_list(worker)


# get_app_info(None)
