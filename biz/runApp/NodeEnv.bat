@echo off
color 0a
set NODE_HOME=%~dp0..\node-v14.16.1-win-x64
set NODE_PATH=%NODE_HOME%\node_modules
set path=%NODE_HOME%;%path%
::echo %path%
cmd "/K" npm config set prefix %NODE_HOME%\node-global&&npm config set cache %NODE_HOME%\node-cache&&npm config set tmp %NODE_HOME%\node-tmp&&npm config set registry https://registry.npm.taobao.org


