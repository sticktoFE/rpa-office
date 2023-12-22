from multiprocessing import Process, Queue
import time
import scrapy
from scrapy.utils.project import get_project_settings
import os
from scrapy.crawler import CrawlerProcess


# import pysnooper
# @pysnooper.snoop(depth=1)
def go_scrapy(spiderargs_controlkwargs):
    processes = []
    result_queue = Queue()
    # args_kwargs:
    # [((scrapy_userID, scrapy_passwd, which_tab,data_start_date,data_end_date),{"spider_name":"x000","result_queue":result_queue,"out_file":"yyyyy"}),()]
    for kwargs_ in spiderargs_controlkwargs:
        kwargs_["result_queue"] = result_queue
        process = Process(
            target=spider_worker,
            args=(kwargs_,),
            daemon=True,
        )
        processes.append(process)
        process.start()
        # 由于多次启动爬虫时开多进程打开多个浏览器
        # 而每个浏览器都需要参数文件夹，两次启动间隔过短会导致同时识别一个文件夹，会导致出错，所以做一下停顿
        time.sleep(5)
    # Wait for all processes to complete
    for p in processes:
        p.join()
    # Get the results from the queue and check if they are all True
    results = []
    while not result_queue.empty():
        spider_name, reason = result_queue.get()
        print(f"Spider {spider_name} finished with reason: {reason}")
        if reason == "finished":
            results.append(True)
        else:
            results.append(False)
    if len(results) == len(spiderargs_controlkwargs) and all(results):
        print("所有爬虫全部执行完毕")
        return True
    else:
        print("At least one process failed.")
        return False


# 通过程序启动爬虫
def spider_worker(kwargs_):
    spider_name = kwargs_.get("spider_name")
    result_queue = kwargs_.get("result_queue")
    apply_new_spider_modules = kwargs_.get("apply_new_spider_modules")
    out_file = kwargs_.get("out_file")
    settings_file_path = "general_spider.scrapy_spider.settings"
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
    settings = get_project_settings()

    if apply_new_spider_modules:
        settings.set("SPIDER_MODULES", [apply_new_spider_modules])
    if out_file is not None:
        settings.set("OUT_FILE", out_file)
    try:
        process = CrawlerProcess(settings)
        spider = process.create_crawler(spider_name)

        def callback_func(spider, reason):
            result_queue.put((spider.name, reason))

        spider.signals.connect(callback_func, signal=scrapy.signals.spider_closed)
        process.crawl(spider, **kwargs_)  # spider_args中的值爬虫可以直接取 如 self.start_date
        process.start()
        # result_queue.put(True)
    except Exception as e:
        # result_queue.put(False)
        print(e)


# # 以下代码被上面代码替代，暂时没用处，但是可以参考
# class SpiderManager(QObject):
#     # 定义爬虫结束信号
#     spider_finished = Signal()

#     def __init__(
#         self, userID, passwd, out_file=None, down_path=None, start_proxy=False
#     ):
#         super().__init__()
#         if start_proxy:
#             self.start_ip_proxy()
#         configure_logging()
#         settings_file_path = "general_spider.scrapy_spider.settings"
#         os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
#         self.settings = get_project_settings()
#         self.settings.set("userID", userID)
#         self.settings.set("passwd", passwd)
#         self.settings.set("out_file", out_file)
#         self.settings.set("down_path", down_path)
#         self.runner = CrawlerRunner(self.settings)

#     def schedule_spider(self, spider_name):
#         # run the spider every hour
#         l = task.LoopingCall(self.run_spider, spider_name)
#         l.start(3600)
#         reactor.run()

#     def run_spiders(self, spider_name):
#         # 启动爬虫另一种方式
#         # spider_cls = self.spider_loader.load(spider_name)
#         d = self.runner.crawl(spider_name)
#         d.addBoth(lambda _: self.spider_finished.emit(100))
#         d.addBoth(lambda _: reactor.stop())
#         reactor.run()

#     def run_spiders1(self, spider_name):
#         process = CrawlerProcess(self.settings)
#         defer = process.crawl(spider_name)
#         defer.addBoth(lambda _: self.spider_finished.emit())
#         # process.crawl(Spider2)
#         process.start(stop_after_crawl=False)  # 这能支持scrapy重复启动？

#     # 这个是
#     def run_spiders3(self, spider_name):
#         dirpath = os.path.dirname(__file__)
#         os.chdir(dirpath)  # 切换到当前目录
#         cmdline.execute(
#             [
#                 "scrapy",
#                 "crawl",
#                 spider_name,
#                 # "-s",
#                 # f"SETTINGS_MODULE={self.settings}",
#             ],
#             settings=self.settings,
#         )
#         # scrapy_process2 = subprocess.Popen(['scrapy', 'crawl', 'spider2'])
#         # 获取cmdline.execute的返回值


# if __name__ == "__main__":
#     from general_spider.scrapy_spider.spiders.CSRCPenalty import CSRCPenaltySpider

#     scraper = Scraper(CSRCPenaltySpider)
#     scraper.run_spiders(start_proxy=False)

# 添加环境变量
# sys.path.append(dirpath)

# # 1、启动ip池
# # Any other args, kwargs are passed to the run function
# worker_ocr_server = Worker("startProxy", module="general_spider.proxy_pool.proxyPool")
# QThreadPool.globalInstance().start(worker_ocr_server)

# # &   顺序执行多条命令，而不管命令是否执行成功
# # 例：copy nul 5.txt   & echo 666 >>5.txt &   more 5.txt
# # 创建5.txt文档，向5.txt文档中写入内容“666”，输出5.txt的内容。
# # &&   顺序执行多条命令，当碰到执行出错的命令后将不执行后面的命令
# # ||   顺序执行多条命令，当碰到执行正确的命令后将不执行后面的命令
# # |   管道命令   前一个命令的执行结果输出到后一个命令
# # >   清除文件中原有的内容后再写入
# # >> 追加内容到文件末尾，而不会清除原有的内容主要将本来显示在屏幕上的内容输出 到指定文件中指定文件如果不存在，则自动生成该文件
# # ip_pool = os.path.join(dirpath, "proxy_pool")
# # completedProcess = subprocess.Popen(
# #     f"python proxyPool.py server && python proxyPool.py schedule",
# #     shell=True,
# #     text=True,
# #     stdout=subprocess.PIPE,
# #     stderr=subprocess.PIPE,
# #     universal_newlines=True,
# #     encoding="utf8",
# #     cwd=ip_pool,
# # )
# # print(completedProcess.communicate())
# # while completedProcess.poll() is None:
# #     print(1)
# #     line = completedProcess.stdout.readline().strip()
# #     if line:
# #         #   pout = "".join(line)
# #         #   output = pout.decode("cp936").encode("utf-8")
# #         print(f"-------------------------Subprogram output: [{line}]")
# # if completedProcess.returncode == 0:  # 正常退出
# #     print('-------------------------')
# #     result = re.search(r"(\w+): (\d+)", completedProcess.stdout)
# #     if result:
# #         print(f"源系统显示密度：{result.group(2)}")
# #     print("-------------------------Subprogram success")
# # else:
# #     print(
# #         f"-------------------------Subprogram failed:{completedProcess.stderr}")

# # 2、启动爬虫,第三个参数为爬虫name
# # 获取当前脚本路径
# # dirpath = os.path.dirname(__file__)
# # os.chdir(dirpath)  # 切换到当前目录
# # # cmdline.execute("scrapy crawl covid19nchcTW -o covid19nchcTW.csv".split())
# # cmdline.execute("scrapy crawl selenium_example".split())
# # cmdline.execute("scrapy crawl bank_report".split())
# # cmdline.execute(["scrapy", "crawl", "csrc"])

# # 可以利用scrapy提供的核心API通过编程方式启动scrapy，代替传统的scrapy crawl启动方式。
# configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
# # The path seen from root, ie. from main.py
# settings_file_path = "general_spider.scrapy_spider.settings"
# os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
# settings = get_project_settings()
# print("-------------")
# print(settings.get("MAX_PAGE"))
# runner = CrawlerRunner(settings)
# d = runner.crawl(CSRCPenaltySpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run()  # the script will block here until the crawling is finished
