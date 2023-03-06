@echo off
color 0a
set CONDA=%~dp0..\Miniconda3\condabin\conda.bat

call %CONDA% config --remove-key channels
rem call %CONDA% config --add channels anaconda
rem call %CONDA% config --add channels conda-forge
rem call %CONDA% config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
rem call %CONDA% config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
rem call %CONDA% config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
rem call %CONDA% config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/

call %CONDA% config --add channels https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
call %CONDA% config --set show_channel_urls yes 
rem cls
call %CONDA% info
cmd "/K"

