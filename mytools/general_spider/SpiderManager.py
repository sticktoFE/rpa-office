from scrapy.utils.project import get_project_settings
import os
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from PySide6.QtCore import QObject, Signal
from twisted.internet import task, reactor
from scrapy import cmdline


def run_spiders(
    q,
    spider_name,
    userID,
    passwd,
    data_start_date,
    data_end_date,
    out_file=None,
    down_path=None,
):
    settings_file_path = "mytools.general_spider.general_spider.settings"
    settings_file_path = "mytools.general_spider.general_spider.settings"
    os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
    settings = get_project_settings()
    settings.set("userID", userID)
    settings.set("passwd", passwd)
    settings.set("out_file", out_file)
    settings.set("down_path", down_path)
    settings.set("data_start_date", data_start_date)
    settings.set("data_end_date", data_end_date)
    try:
        # runner = CrawlerRunner(settings)
        # deferred = runner.crawl(spider_name)
        # deferred.addBoth(lambda _: reactor.stop())
        # reactor.run() #放到进程中，runner此处无效导致无法启动爬虫
        process = CrawlerProcess(settings)
        process.crawl(spider_name)
        # process.crawl(Spider2)
        process.start(stop_after_crawl=True)  # 这能支持scrapy重复启动？
        q.put(None)
    except Exception as e:
        q.put(e)


class SpiderManager(QObject):
    # 定义爬虫结束信号
    spider_finished = Signal()

    def __init__(
        self, userID, passwd, out_file=None, down_path=None, start_proxy=False
    ):
        super().__init__()
        if start_proxy:
            self.start_ip_proxy()
        configure_logging()
        settings_file_path = "mytools.general_spider.general_spider.settings"
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
        self.settings = get_project_settings()
        self.settings.set("userID", userID)
        self.settings.set("passwd", passwd)
        self.settings.set("out_file", out_file)
        self.settings.set("down_path", down_path)
        self.runner = CrawlerRunner(self.settings)

    def schedule_spider(self, spider_name):
        # run the spider every hour
        l = task.LoopingCall(self.run_spider, spider_name)
        l.start(3600)
        reactor.run()

    def run_spiders(self, spider_name):
        # 启动爬虫另一种方式
        # spider_cls = self.spider_loader.load(spider_name)
        d = self.runner.crawl(spider_name)
        d.addBoth(lambda _: self.spider_finished.emit(100))
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

    def run_spiders1(self, spider_name):
        process = CrawlerProcess(self.settings)
        defer = process.crawl(spider_name)
        defer.addBoth(lambda _: self.spider_finished.emit())
        # process.crawl(Spider2)
        process.start(stop_after_crawl=False)  # 这能支持scrapy重复启动？

    # 这个是
    def run_spiders3(self, spider_name):
        dirpath = os.path.dirname(__file__)
        os.chdir(dirpath)  # 切换到当前目录
        cmdline.execute(
            [
                "scrapy",
                "crawl",
                spider_name,
                # "-s",
                # f"SETTINGS_MODULE={self.settings}",
            ],
            settings=self.settings,
        )
        # scrapy_process2 = subprocess.Popen(['scrapy', 'crawl', 'spider2'])
        # 获取cmdline.execute的返回值


# if __name__ == "__main__":
#     from mytools.general_spider.general_spider.spiders.CSRCPenalty import CSRCSpider

#     scraper = Scraper(CSRCSpider)
#     scraper.run_spiders(start_proxy=False)
