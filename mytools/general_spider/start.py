from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from general_spider.spiders.Covid19 import Covid19Spider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import scrapy
import re
import sys
import os
from scrapy import cmdline
from mytools.general_spider.general_spider.spiders.PingDingGov import SeleniumExampleSpider
from myutils.GeneralThread import Worker
from PySide6.QtCore import QThreadPool
from proxy_pool.proxyPool import startProxy
import subprocess

# 添加环境变量
# sys.path.append(dirpath)

# 1、启动ip池
# Any other args, kwargs are passed to the run function
worker_ocr_server = Worker(
    'startProxy', module='mytools.general_spider.proxy_pool.proxyPool')
QThreadPool.globalInstance().start(worker_ocr_server)

# &   顺序执行多条命令，而不管命令是否执行成功
# 例：copy nul 5.txt   & echo 666 >>5.txt &   more 5.txt
# 创建5.txt文档，向5.txt文档中写入内容“666”，输出5.txt的内容。
# &&   顺序执行多条命令，当碰到执行出错的命令后将不执行后面的命令
# ||   顺序执行多条命令，当碰到执行正确的命令后将不执行后面的命令
# |   管道命令   前一个命令的执行结果输出到后一个命令
# >   清除文件中原有的内容后再写入
# >> 追加内容到文件末尾，而不会清除原有的内容主要将本来显示在屏幕上的内容输出 到指定文件中指定文件如果不存在，则自动生成该文件
# ip_pool = os.path.join(dirpath, "proxy_pool")
# completedProcess = subprocess.Popen(
#     f"python proxyPool.py server && python proxyPool.py schedule",
#     shell=True,
#     text=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     universal_newlines=True,
#     encoding="utf8",
#     cwd=ip_pool,
# )
# print(completedProcess.communicate())
# while completedProcess.poll() is None:
#     print(1)
#     line = completedProcess.stdout.readline().strip()
#     if line:
#         #   pout = "".join(line)
#         #   output = pout.decode("cp936").encode("utf-8")
#         print(f"-------------------------Subprogram output: [{line}]")
# if completedProcess.returncode == 0:  # 正常退出
#     print('-------------------------')
#     result = re.search(r"(\w+): (\d+)", completedProcess.stdout)
#     if result:
#         print(f"源系统显示密度：{result.group(2)}")
#     print("-------------------------Subprogram success")
# else:
#     print(
#         f"-------------------------Subprogram failed:{completedProcess.stderr}")

# 2、启动爬虫,第三个参数为爬虫name
# 获取当前脚本路径
# dirpath = os.path.dirname(__file__)
# os.chdir(dirpath)  # 切换到当前目录
# # cmdline.execute("scrapy crawl covid19nchcTW -o covid19nchcTW.csv".split())
# cmdline.execute("scrapy crawl selenium_example".split())
# cmdline.execute("scrapy crawl bank_report".split())
# cmdline.execute(["scrapy", "crawl", "csrc"])

# 可以利用scrapy提供的核心API通过编程方式启动scrapy，代替传统的scrapy crawl启动方式。
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
# The path seen from root, ie. from main.py
settings_file_path = 'general_spider.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
settings = get_project_settings()
print('-------------')
print(settings.get('MAX_PAGE'))
runner = CrawlerRunner(settings)
d = runner.crawl(SeleniumExampleSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()  # the script will block here until the crawling is finished
