from distutils.log import error
from subprocess import PIPE, Popen, STDOUT, CREATE_NEW_CONSOLE
from pathlib import Path
from time import sleep
import os, sys, stat
import ctypes
import shutil


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def release(obj: Path):

    if obj.is_file():
        return
    #   Cacls C:\ruery /t /e /c /g ruery:F
    # "/t"表示修改文件夹及子文件夹中所有文件的ACL.
    # "/e"表示仅做编辑工作而不替换.
    # "/c"表示在出现拒绝访问错误时继续.
    # "/g ruery:F"表示给予本地用户ruery以完全控制的权限.
    # "f"代表完全控制，如果只是希望给予读取权限，那么应当是"r"
    for file in obj.glob("hw_*"):
        # shell为True表示第一个入参是字符串，False表示列表
        process = Popen(
            ["cmd"],
            # creationflags=CREATE_NEW_CONSOLE,
            shell=False,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
        )
        commands = (
            f'takeown /F "{file}" /A\n'  # 这个\n表示回车，别忘了 先换成administrator管理员用户
            f'takeown /F "{file}"\n'  # 再换成当前用户
            f'icacls "{file}" /grant loube:(OI)(CI)(F)\n'  # 授予所有权限
            f'rd /s /q "{file}" \n'  # 删除
            # f'del /f "{file}" y \n'
            # f'icacls "{file}" /setowner everyone'
            # r"y\n"
            "pause"
        )
        print(commands)
        sleep(1)
        # 使用gbk格式代替utf-8,避免在解码过程中遇到中文文件名而报错
        outs, errs = process.communicate(commands.encode("utf-8"))
        content = [z.strip() for z in outs.decode("gbk").split("\n") if z]
        print(*content, sep="\n")
        # os.chmod(file, stat.S_IRWXO)
        # shutil.rmtree(file)
# 显示文件信息，此处备份
# import win32api
# import win32con
# import win32security
 
# FILENAME = "temp.txt"
# open(FILENAME, "w").close()
 
# print "I am", win32api.GetUserNameEx(win32con.NameSamCompatible)
 
# sd = win32security.GetFileSecurity(FILENAME, win32security.OWNER_SECURITY_INFORMATION)
# owner_sid = sd.GetSecurityDescriptorOwner()
# name, domain, type = win32security.LookupAccountSid(None, owner_sid)
 
# print "File owned by %s\\%s" % (domain, name)

if __name__ == "__main__":
    if not is_admin() and sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
    redir = Path("C:\\Program Files")
    release(redir)
    # rmcmd = 'rmdir ' + redir + ' /s /q'
    # print(rmcmd)
    # os.system(rmcmd)
