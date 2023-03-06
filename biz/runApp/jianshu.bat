::@echo off
%隐藏cmd窗口%
::if "%1"=="h" goto begin
::start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
color 0a
set Activate=%~dp0..\Miniconda3\condabin\activate.bat

%Activate% nlp&&start /d D:\leichui\workspace\ter\ter\spiders scrapy crawl jianshu
