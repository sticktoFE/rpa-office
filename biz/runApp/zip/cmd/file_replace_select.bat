@echo off
set filename=plugin.properties
set f=.\%filename%
set version_class=%1
set tmp1=.\%f%.tmp1
set tmp2=.\%f%.tmp2
set version_code_value=""
::for /?>%f%
::基本逻辑是，先针对原始文件识别出内容，然后修改相应的的值，
::对于依赖修改的值再修改其他值的再重新读文件再循环修改
if exist %tmp1% del %tmp1%
if exist %tmp2% del %tmp2%
setlocal enabledelayedexpansion
::循环文件每一行，并用=和;分割，取前两块  形如 name=value;  获取 name value
for /f "tokens=1,2 delims==;" %%i in (%f%) do (
    set name=%%i
    set value=%%j
	::识别出要修改的内容，即对类似 x.y.z中 识别一个自动+1
    if !name!==version_name (
        for /f "tokens=1,2,3 delims=." %%x in ("%%j") do (
            if %version_class%==1 (
                set /a trdvalue=%%x+1
                set value=!trdvalue!.%%y.%%z
            ) else if %version_class%==2 (
                set /a trdvalue=%%y+1
                set value=%%x.!trdvalue!.%%z
            ) else if %version_class%==3 (
                set /a trdvalue=%%z+1
                set value=%%x.%%y.!trdvalue!
            )  
			::字符串替换，把value中.替换成空
            set version_code_value=!value:.=!
        )
    )
    set line=!name!=!value!;
	::全部生成到临时文件里tmp1中
    echo !line!>>%tmp1%
 )	
 ::循环文件每一行，并用=和;分割行，取前两块  形如 name=value;  获取 name value
 ::对类似 x.y.z中 识别一个自动+1
for /f "tokens=1,2 delims==;" %%i in (%tmp1%) do (
    set name=%%i
    set value=%%j
    if !name!==version_code (
        set value=%version_code_value%
    )
	::全部生成到临时文件里tmp2中
    set line=!name!=!value!;
    echo !line!>>%tmp2%
 )
 ::定义函数
:handleKV


move /y "%f%" .\cmd\logs\"%filename%_%Date:~3,4%%Date:~8,2%%Date:~11,2%%Time:~0,2%%Time:~3,2%%Time:~6,2%"
if exist %tmp1% del %tmp1%
if exist %tmp2% move /y %tmp2% "%f%"