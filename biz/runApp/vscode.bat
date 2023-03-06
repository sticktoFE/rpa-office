@echo off
set Activate=%~dp0..\Miniconda3\Scripts\activate.bat
%Activate% train&&python vscodev2.0.py 