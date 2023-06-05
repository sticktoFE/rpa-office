import glob
import os
import shutil
import sys
from pathlib import Path
import time
import json
import configparser
from types import GeneratorType

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


# 获取输出临时文件夹
def get_temp_folder(
    execute_file_path=None, des_folder_name=None, is_clear_folder=False
):
    # 使用配置文件中的默认设置
    des_folder = ReadWriteConfFile.getSectionValue("General", "tmp_path")
    des_folder = Path(des_folder)
    if execute_file_path is not None:
        # path_list = re.split(r"[/\\]", execute_file_path)
        # last_two = f"{path_list[-2]}_{path_list[-1]}"
        # des_folder = f"{des_folder}/{last_two}"
        efp = Path(execute_file_path)
        des_folder = des_folder / efp.parent.stem / efp.stem
    # files_path = f'{QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)}/rpa-office/{Path(current_file_path).parent.stem}--{Path(current_file_path).stem}'
    # 临时文件统一放到系统文档文件夹里
    if des_folder_name is not None:
        des_folder = des_folder.joinpath(des_folder_name)
    des_folder.mkdir(parents=True, exist_ok=True)
    if is_clear_folder:  # 清理文件夹内容
        filelist = glob.glob(f"{des_folder.as_posix()}/*")
        for f in filelist:
            if Path(f).is_dir():
                # os.removedirs(f) 只能删除空目录
                shutil.rmtree(f)
            else:
                os.remove(f)
    return des_folder.as_posix()


# 获取临时文件，名字按时间取，用于一些日志信息
def get_temp_file(des_folder=None, save_file_name=None, save_file_type="xlsx"):
    save_file_name = str(time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
    return f"{des_folder}/{save_file_name}.{save_file_type}"


# 多次输出到文件，以列表中多个字典的形式，类似数据库表数据
def dump_json_table(content: dict | list, purpose_file):
    # 把字典装到列表中，再转换成json格式
    now_json = None
    with open(purpose_file, "a+", encoding="utf-8") as write_file:
        # 挪动文件中的指针位置，读取都是从指针后面开始，要注意
        write_file.seek(0)
        if len(write_file.readlines()) != 0:
            write_file.seek(0)
            now_json = json.load(write_file)
        else:
            now_json = []
        if isinstance(content, dict):
            now_json.append(content)
        elif isinstance(content, list):
            now_json.extend(content)
        elif isinstance(content, GeneratorType):
            now_json.extend(list(content))
    with open(purpose_file, "w", encoding="utf-8") as write_file:
        # 使用json.dump时需解决中文乱码问题
        json.dump(
            now_json,
            write_file,
            indent=4,
            separators=(",", ": "),
            sort_keys=True,
            ensure_ascii=False,
        )
        # write_file.write('\n')


# 读取json文件并返回一条记录
def load_json_table(purpose_file):
    with open(purpose_file, "r", encoding="utf-8") as write_file:
        now_json = json.load(write_file)
        for onedict in now_json:
            yield onedict


# 将txt文件读入列表去除行中的回车---暂时没用
def strip_txt(file_path):
    # 打开要去掉空行的文件
    line = None
    with open(file_path, "r", encoding="utf-8") as file1:
        for line in file1.readlines():  # 去除空行
            if line == "\n":
                line = line.strip("\n")
    with open(file_path, "w", encoding="utf-8") as file2:  # 生成没有空行的文件
        file2.write(line)  # 输出到新文件中


def txt_to_list(file_path):
    with open(file_path, "r", encoding="utf-8") as file:  # 这里的文件对应txt_os中生产的文件
        list = file.readlines()
        list = [x.strip() for x in list if x.strip() != ""]  # 去除行中的回车
        return list  # 返回列表


# 读写配置文件 xxx.ini
class ReadWriteConfFile:
    configDir = Path(__file__).parent.parent
    filepath = configDir / "config.ini"

    @staticmethod
    def getConfigParser():
        cf = configparser.ConfigParser()
        cf.read(ReadWriteConfFile.filepath, encoding="utf-8")  # 加encoding以支持配置文件中有中文
        return cf

    @staticmethod
    def writeConfigParser(cf):
        with open(ReadWriteConfFile.filepath, "w") as f:
            cf.write(f)

    @staticmethod
    def getSectionValue(section, key, type="str"):
        cf = ReadWriteConfFile.getConfigParser()
        if type == "str":
            return cf.get(section, key)
        elif type == "boolean":
            return cf.getboolean(section, key)
        else:
            return cf.getint(section, key)

    @staticmethod
    def addSection(section):
        cf = ReadWriteConfFile.getConfigParser()
        allSections = cf.sections()
        if section in allSections:
            return
        else:
            cf.add_section(section)
        ReadWriteConfFile.writeConfigParser(cf)

    @staticmethod
    def setSectionValue(section, key, value):
        cf = ReadWriteConfFile.getConfigParser()
        cf.set(section, key, value)
        ReadWriteConfFile.writeConfigParser(cf)


if __name__ == "__main__":
    # result = print_var("你好")
    # print(result)
    # redirObj = RedirectStdout()
    # sys.stdout = redirObj #本句会抑制"Let's begin!"输出
    # print("Let's begin!")
    ReadWriteConfFile.addSection("messages")
    ReadWriteConfFile.setSectionValue("messages", "name", "sophia")
    x = ReadWriteConfFile.getSectionValue("General", "chrome_version")
    print(x)
