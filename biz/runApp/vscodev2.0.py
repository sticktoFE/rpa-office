#!/usr/bin/env python
# coding: utf-8

# In[11]:
import os, glob

# In[12]:

"""把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12"""
import time


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    # return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
    return time.strftime("%Y-%m-%d", timeStruct)


# In[13]:
##1、解压缩zipb
import zipfile
from pathlib import Path
import shutil
import sys, os

BASE_DIR = "D:\\leichui"
# os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # __file__获取执行文件相对路径&#xff0c;整行为取上一级的上一级目录
CodeDirPath = os.path.join(BASE_DIR, "VSCode", "VSCode-win32-x64")
downPath = glob.glob("D:\\转型\\downloads\\VSCode*")  # glob支持通配符
downPath.sort(key=os.path.getmtime)
for i, item in enumerate(downPath):
    if i != len(downPath) - 1:
        os.remove(item)
    else:
        # 删除目标目录
        if os.path.exists(CodeDirPath):
            shutil.rmtree(CodeDirPath, ignore_errors=True)
        if not os.path.exists(CodeDirPath):
            os.mkdir(CodeDirPath)
        with zipfile.ZipFile(item, "r") as zFile:
            zFile.extractall(CodeDirPath)
        os.remove(item)

# In[14]:


##3、执行程序
import subprocess


def cmd1(command):
    ret = subprocess.run(
        command,
        universal_newlines=True,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="gbk",
        timeout=None,
    )
    if ret.returncode == 0:
        return "success:", ret
        print("success:", ret)
    else:
        return "error:", ret
        print("error:", ret)


# 此方法是异步的,官方推荐使用subprocess.run，除非满足不了，再使用Popen
def cmd2(command):
    st = subprocess.STARTUPINFO()
    st.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
    st.wShowWindow = subprocess.SW_HIDE
    subp = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="gbk",
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    subp.wait(20)
    if subp.poll() == 0:
        print(subp.communicate()[1])
    else:
        print("失败")


# In[15]:
CodePath = os.path.join(CodeDirPath, "Code.exe")
CodeExt = os.path.join(BASE_DIR, "VSCode", ".vscode", "extensions")
###start /b 加上后面的 taskkill /F /IM python.exe可以去掉一个dos窗口
##cmd1('set Activate=..\\condabin\\activate.bat&&cmd /K %Activate% nlp&&'+' start /b '+vsCodeDir+'VSCode-win32-x64\\Code.exe --extensions-dir "'+vsCodeDir+'.vscode\\extensions"')
###cmd1('start /b '+vsCodeDir+'VSCode-win32-x64\\Code.exe --extensions-dir "'+vsCodeDir+'.vscode\\extensions"'+' &&taskkill /F /IM python.exe')
currentFileName = os.path.basename(__file__)
cmd1(f'{CodePath} --extensions-dir "{CodeExt}"')
# cmd1('taskkill /IM python.exe /F ')
