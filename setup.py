import re
import subprocess

# print(__loader__)
# --windows-disable-console 打的包可以输出日志
cmd = """
nuitka 
--windows-disable-console 
--standalone  --mingw64 --show-memory --show-progress  
--nofollow-imports  
--plugin-enable=pyside6  
--include-qt-plugins=sensible,styles  
--include-package=mytools.general_spider
--remove-output 
--output-dir=output 
--windows-icon-from-ico=rpa.ico 
biz/monitor_oa/main.py
"""
cmd_list = cmd.split()
print(cmd_list)
completedProcess = subprocess.Popen(
    cmd_list,
    shell=True,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    # encoding="utf8",
    # cwd=ip_pool,
)
# 程序执行中
while completedProcess.poll() is None:
    print(1)
    line = completedProcess.stdout.readline().strip()
    if line:
        #   pout = "".join(line)
        #   output = pout.decode("cp936").encode("utf-8")
        print(f"-------------------------Subprogram output: [{line}]")
# 程序执行完毕，0为正常退出
if completedProcess.returncode == 0:
    result = re.search(r"(\w+): (\d+)", completedProcess.stdout.readline())
    if result:
        print(f"源系统显示密度：{result.group(2)}")
    print("-------------------------Subprogram success")
else:
    print(
        f"-------------------------Subprogram failed:{completedProcess.stderr.readlines()}"
    )
