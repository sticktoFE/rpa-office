from mytools.general_spider.general_spider.spiders.PingDingGov import PingDingGovSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
from PySide6.QtCore import QThreadPool
from myutils.GeneralThread import Worker


class Scraper:
    def __init__(self):
        # The path seen from root, ie. from main.py
        settings_file_path = 'mytools.general_spider.general_spider.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        settings = get_project_settings()
        self.process = CrawlerProcess(settings)
        self.spider = PingDingGovSpider  # The spider you want to crawl

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()  # the script will block here until the crawling is finished

    def start_ip_proxy(self):
        worker_server = Worker(
            'server', module='mytools.proxy_pool.proxyPool')
        QThreadPool.globalInstance().start(worker_server)
        worker_schedule = Worker(
            'schedule', module='mytools.proxy_pool.proxyPool')
        QThreadPool.globalInstance().start(worker_schedule)
