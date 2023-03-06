@echo off
set WORKSPACE_HOME=%~dp0..\workspace
set APP_HOME=%WORKSPACE_HOME%\Cloud-Platform-UI-V2
set NODE_HOME=%~dp0..\node-v14.16.1-win-x64
set NODE_PATH=%NODE_HOME%\node_modules
set NODE_GLOBAL=%NODE_HOME%\node-global
set NODE_CACHE=%NODE_HOME%\node-cache
set NODE_TMP=%NODE_HOME%\node-tmp
set path=%NODE_HOME%;%path%

npm config set prefix %NODE_GLOBAL%&&npm config set cache %NODE_CACHE%&&npm config set tmp %NODE_TMP%&&npm config set registry "https://registry.npm.taobao.org"&&start /d %APP_HOME% npm run dev


