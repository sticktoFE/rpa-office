import random
import time
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from PySide6.QtCore import QThreadPool
from myutils.GeneralThread import Worker
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class Scraper:
    def __init__(self, spider, out_file=None, down_path=None):
        configure_logging()
        # The path seen from root, ie. from main.py
        settings_file_path = "mytools.general_spider.general_spider.settings"
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", settings_file_path)
        settings = get_project_settings()
        settings.set("out_file", out_file)
        settings.set("down_path", down_path)
        self.process = CrawlerProcess(settings)
        # self.process = CrawlerRunner(settings)
        self.spider = spider  # The spider you want to crawl

    def run_spiders(self, start_proxy=False):
        if start_proxy:
            self.start_ip_proxy()
        # 启动爬虫另一种方式
        # d = self.process.crawl(self.spider)
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()  # the script will block here until the crawling is finished
        # 启动爬虫另一种方式
        self.process.crawl(self.spider)
        self.process.start()  # the script will block here until the crawling is finished

    def start_ip_proxy(self):
        worker_schedule = Worker("schedule", module="mytools.proxy_pool.proxyPool")
        QThreadPool.globalInstance().start(worker_schedule)
        # 等一下再启动服务
        time.sleep(random.randint(1, 3))
        worker_server = Worker("server", module="mytools.proxy_pool.proxyPool")
        QThreadPool.globalInstance().start(worker_server)
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    from mytools.general_spider.general_spider.spiders.CSRCPenalty import CSRCSpider
    scraper = Scraper(CSRCSpider)
    scraper.run_spiders(start_proxy=False)
