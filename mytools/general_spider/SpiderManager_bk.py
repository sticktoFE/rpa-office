import random
import time
from scrapy.utils.project import get_project_settings
import os
from PySide6.QtCore import QThreadPool
from myutils.GeneralThread import Worker
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from PySide6.QtCore import QObject, Signal
from crochet import setup, wait_for, get_reactor


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

    def start(self):
        # 创建一个Twisted Reactor
        setup()
        reactor = get_reactor()

    # 使用Crochet库来运行Scrapy
    @wait_for(timeout=60.0)
    def run_spiders(self, spider_name):
        # 启动爬虫另一种方式
        # spider_cls = self.spider_loader.load(spider_name)
        d = self.runner.crawl(spider_name)
        # d.addBoth(lambda _: reactor.stop())
        d.addBoth(lambda _: self.stop_reactor())
        # reactor.run()
        return d

    def stop_reactor(self):
        self.spider_finished.emit()

    def start_ip_proxy(self):
        worker_schedule = Worker("schedule", module="mytools.proxy_pool.proxyPool")
        QThreadPool.globalInstance().start(worker_schedule)
        # 等一下再启动服务
        time.sleep(random.randint(1, 3))
        worker_server = Worker("server", module="mytools.proxy_pool.proxyPool")
        QThreadPool.globalInstance().start(worker_server)
        time.sleep(random.randint(1, 3))


# if __name__ == "__main__":
#     from mytools.general_spider.general_spider.spiders.CSRCPenalty import CSRCSpider

#     scraper = Scraper(CSRCSpider)
#     scraper.run_spiders(start_proxy=False)
