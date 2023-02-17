import glob
import os
import re
import shutil
import sys
from pathlib import Path
import time
from PySide6.QtCore import QStandardPaths, QSettings

"""
    目前还没找到用处
"""
# 将print输出内容重定位到txt文件中
# sys.stdout = open('test.txt','w')
# print("text")
# 将print输出内容重定位到ist变量中


def print_var(content):
    class RedirectStdout:  # 建立对象，添加输出流需要的write写方法，和清空缓存的于Lush方
        def __init__(self):
            self.content = ""
            self.savedStdout = sys.stdout

        def write(self, outStr):
            # print(args)
            self.content += outStr  # 此时的args为元组类型 [('你好',), ('\n',)]

        # def flush(self):
        #     self.content = ''
        def restore(self):
            # self.content = ''
            # if self.memObj.closed != True:
            #     self.memObj.close()
            # if self.fileObj.closed != True:
            #     self.fileObj.close()
            # if self.nulObj.closed != True:
            #     self.nulObj.close()
            sys.stdout = self.savedStdout  # sys.__stdout__

    redirObj = RedirectStdout()
    sys.stdout = redirObj  # 本句重定向
    print(content)  # 此时语句输出到buffer列表中
    redirObj.restore()  # 输出恢复为控制台，即默认的输出位置
    return redirObj.content


# class RedirectStdout:  #import os, sys, cStringIO
#     def __init__(self):
#         self.content = ''
#         self.savedStdout = sys.stdout
#         self.memObj, self.fileObj, self.nulObj = None, None, None

#     #外部的print语句将执行本write()方法，并由当前sys.stdout输出
#     def write(self, outStr):
#         #self.content.append(outStr)
#         self.content += outStr

#     def toCons(self):  #标准输出重定向至控制台
#         sys.stdout = self.savedStdout #sys.__stdout__

#     def toMemo(self):  #标准输出重定向至内存
#         self.memObj = StringIO()
#         sys.stdout = self.memObj

#     def toFile(self, file='out.txt'):  #标准输出重定向至文件
#         self.fileObj = open(file, 'a+', 1) #改为行缓冲
#         sys.stdout = self.fileObj

#     def toMute(self):  #抑制输出
#         self.nulObj = open(os.devnull, 'w')
#         sys.stdout = self.nulObj

#     def restore(self):
#         self.content = ''
#         if self.memObj.closed != True:
#             self.memObj.close()
#         if self.fileObj.closed != True:
#             self.fileObj.close()
#         if self.nulObj.closed != True:
#             self.nulObj.close()
#         sys.stdout = self.savedStdout #sys.__stdout__
# 获取输出临时文件夹
def get_temp_folder(execute_file_path=None, des_folder_name=None, is_clear_folder=False):
    # 使用配置文件中的默认设置
    settings = QSettings("./config.ini", QSettings.Format.IniFormat)
    des_folder = settings.value("tmp_path")
    if execute_file_path is not None:
        path_list = re.split(r"[/\\]", execute_file_path)
        last_two = (f"{path_list[-2]}_{path_list[-1]}")
        des_folder = f"{des_folder}/{last_two}"
    # files_path = f'{QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)}/rpa-office/{Path(current_file_path).parent.stem}--{Path(current_file_path).stem}'
    # 临时文件统一放到系统文档文件夹里
    if not os.path.exists(des_folder):
        os.makedirs(des_folder)
    if des_folder_name is not None:
        des_folder = f"{des_folder}/{des_folder_name}"
        if not os.path.exists(des_folder):
            os.makedirs(des_folder)
    if is_clear_folder:  # 清理文件夹内容
        filelist = glob.glob(f"{des_folder}/*")
        for f in filelist:
            if Path(f).is_dir():
                # os.removedirs(f) 只能删除空目录
                shutil.rmtree(f)
            else:
                os.remove(f)
    return des_folder

# 获取临时文件，名字按时间取，用于一些日志信息


def get_temp_file(des_folder=None, save_file_name=None, save_file_type="xlsx"):
    save_file_name = str(time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    return f"{des_folder}/{save_file_name}.{save_file_type}"


if __name__ == "__main__":
    result = print_var("你好")
    print(result)
    # redirObj = RedirectStdout()
    # sys.stdout = redirObj #本句会抑制"Let's begin!"输出
    # print("Let's begin!")
