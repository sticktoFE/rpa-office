@echo off
set f=.\plugin.properties
set key=version_code
set tmp=.\%f%.tmp
::for /?>%f%
if exist %tmp% del %tmp%
setlocal enabledelayedexpansion
::循环文件每一行，并用=和;分割行，取前两块  形如 name=value;  获取 name value
for /f "tokens=1,2 delims==;" %%i in (%f%) do (
    set name=%%i
    set value=%%j
    if !name!==version_code (
        set /a value=%%j+1
    ) else if !name!==version_name (
        echo !name!
        for /f "tokens=1,2,3 delims=." %%x in ("%%j") do (
            set /a trdvalue=%%z+1
            set value=%%x.%%y.!trdvalue!
        )
    )
    set line=!name!=!value!;
    echo !line!>>%tmp%
 )