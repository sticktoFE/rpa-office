Dim WshShell 
Set WshShell=WScript.CreateObject("WScript.Shell") 
WshShell.Run "cmd.exe"
WScript.Sleep 1500 
' WshShell.SendKeys "ssh -fNg -L 9999:192.168.31.63:22 zl@192.168.31.63" 把本地端口 9999 转发到 远程服务192.168.31.63:22
WshShell.SendKeys "ssh zl@192.168.31.63"
WshShell.SendKeys "{ENTER}"
WScript.Sleep 1500 
WshShell.SendKeys "8579"
WshShell.SendKeys "{ENTER}"