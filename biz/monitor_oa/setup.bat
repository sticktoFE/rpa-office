@echo off
::使用nuitka打包python 
set python_path=D:\leichui\Miniconda3\envs\rpa\python.exe 
%python_path% -m nuitka --standalone --mingw64 --show-progress ^
--include-qt-plugins=sensible,styles --plugin-enable=pyside6 ^
--follow-import-to=biz.monitor_oa,myutils ^
--include-package=mytools.general_spider.general_spider,^
mytools.general_spider.general_spider.spiders,scrapy,fake_useragent ^
--nofollow-import-to=tkinter,pil,numpy,scipy,matplotlib,pandas,xlwings,^
openpyxl,pyautogui,email,requests,docx,openssl,paddle,paddleocr,schedule,^
fitz,pyput,unittest,Ipython,jedi,win32gui,win32con,pygments,pip,mss,asyncio,^
blib2to3,lib2to3,idna,cryptography,hyperlink,attr,wrapt,selenium,click,jinja2,^
configparser ^
--output-dir=output --windows-icon-from-ico=.\rpa.ico --jobs=10 .\biz\monitor_oa\mainw.py
::把没有编译的库，复制到打包文件中
set source=.\output\packages
set destination=.\output\mainw.dist
echo A | xcopy /E /I "%source%" "%destination%"
echo 复制完成！
pause