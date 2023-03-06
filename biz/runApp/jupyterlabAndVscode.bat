@echo off
start /min jupyterlab --no-browser 
::--ip localhost
set Activate=%~dp0..\Miniconda3\condabin\activate.bat
%Activate% ml && start /min %~dp0..\VSCode\VSCode-win32-x64\Code.exe --extensions-dir "D:\leichui\VSCode\.vscode\extensions"