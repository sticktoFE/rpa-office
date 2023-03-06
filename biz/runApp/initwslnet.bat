@echo off
setlocal enabledelayedexpansion
::强制获取winow的管理员运行权限
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
wsl -u root service docker start | findstr "Starting Docker" > nul
if !errorlevel! equ 0 (
    echo docker start success
	:: set wsl2 ip
    wsl -u root ip addr | findstr "192.168.50.16" > nul
    if !errorlevel! equ 0 (
        echo wsl ip has set 192.168.50.16
    ) else (
        wsl -d Ubuntu-20.04 -u root ip addr add 192.168.50.16/24 broadcast 192.168.50.255 dev eth0 label eth0:1
        echo set wsl ip success: 192.168.50.16
    )
    :: set windows ip
    ipconfig | findstr "192.168.50.88" > nul
    if !errorlevel! equ 0 (
        echo windows ip has set 192.168.50.88
    ) else (
        netsh interface ip add address "vEthernet (WSL)" 192.168.50.88 255.255.255.0
        echo set windows ip success: 192.168.50.88
    )
)
wsl -u partner --cd ~
::pause