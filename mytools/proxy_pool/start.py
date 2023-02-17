import re
import sys
import os
from scrapy import cmdline

# from proxy_pool import proxyPool
import subprocess
# 获取当前脚本路径
dirpath = os.path.dirname(__file__)
# 添加环境变量
# sys.path.append(dirpath)
# 启动爬虫,第三个参数为爬虫name

os.chdir(dirpath)  # 切换到当前目录
# cmdline.execute("scrapy crawl csrc".split())
cmdline.execute("python proxyPool.py server".split())
cmdline.execute("python proxyPool.py schedule".split())
# cmdline.execute("scrapy crawl bank_report".split())

# proxyPool.schedule()
# proxyPool.server()


# # cmdline.execute(["scrapy", "crawl", "csrc"])
# completedProcess = subprocess.Popen(
#     f"python proxyPool.py server & \
# python proxyPool.py schedule",
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     universal_newlines=True,
#     cwd=dirpath,
# )
# # if completedProcess.returncode == 0:
# #     result = re.search(r"(\w+): (\d+)", completedProcess.stdout)
# #     if result:
# #         print(f"源系统显示密度：{result.group(2)}")
# # else:
# #     print(f"{completedProcess.stderr}")
# while completedProcess.poll() is None:
#     line = completedProcess.stdout.readline().strip()
#     if line:
#         print(f"Subprogram output: [{line}]")
# if completedProcess.returncode == 0:
#     print("Subprogram success")
# else:
#     print(f"Subprogram failed:{completedProcess.stderr}")
# ip_pool = os.path.join(dirpath, "proxy_pool")
# completedProcess = subprocess.Popen(
#     f"python proxyPool.py server&&python proxyPool.py schedule",
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     universal_newlines=True,
#     encoding="utf8",
#     cwd=ip_pool,
# )

# while completedProcess.poll() is None:
#     line = completedProcess.stdout.readline().strip()
#     if line:
#         #   pout = "".join(line)
#         #   output = pout.decode("cp936").encode("utf-8")
#         print(f"Subprogram output: [{line}]")
# if completedProcess.returncode == 0:
#     print("Subprogram success")

# else:
#     print(f"Subprogram failed:{completedProcess.stdout}")
