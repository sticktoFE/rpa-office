@echo off
echo please input 1¡¢first version num  2¡¢second version num  3¡¢hird version num:
set /p name=
call .\cmd\file_replace_select %name%
::¿ªÊ¼Ñ¹Ëõ
if exist www.zip del www.zip
start  /wait "" .\cmd\WinRaR a -as  -ruf -zplugin.properties -x@.\cmd\exclude_list.txt www.zip  .\
pause
