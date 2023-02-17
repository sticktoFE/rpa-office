import random
from twisted.internet import defer, threads
from scrapy.http import HtmlResponse
import hashlib
import json
import logging
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
from fake_useragent import UserAgent
from mytools.general_spider.general_spider.spiders.extendsion import IPProxy
# useful for handling different item types with a single interface
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver

from myutils.web_driver_manager import get_driver_ChromeDriver


class RandomProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.proxy_url = proxy_url

    # 动态设置代理服务器的IP 地址
    def process_request(self, request, spider):
        proxy = IPProxy.get_random_proxy5010()
        if proxy:
            self.logger.debug("======" + "使用代理 " + str(proxy) + "======")
            request.meta["proxy"] = "http://{proxy}".format(proxy=proxy)


class RandomUserAgentMiddlware(object):
    """
    随机更换user-agent
    模仿并替换site-package/scrapy/downloadermiddlewares源代码中的
    useragent.py中的UserAgentMiddleware类
    """

    def __init__(self, crawler):
        super(RandomUserAgentMiddlware, self).__init__()
        self.ua = UserAgent(verify_ssl=False)
        # 可读取在settings文件中的配置，来决定开源库ua执行的方法，
        # 默认是random，也可是ie、Firefox等等 ua.random
        # 在配置文件中 可以 RANDOM_UA_TYPE = "ie"
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 更换用户代理逻辑在此方法中
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        print(get_ua())
        request.headers.setdefault("User-Agent", get_ua())


class GeneralSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class GeneralSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


"""
负责返回浏览器渲染后的Response
"""


class SeleniumDownloaderMiddleware(object):
    """
    Selenium下载器中间件
    """

    def process_request(self, request, spider):
        # 如果spider为SeleniumSpider的实例，并且request为SeleniumRequest的实例
        # 那么该Request就认定为需要启用selenium来进行渲染html
        # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        usedSelenium = request.meta.get('usedSelenium', False)
        if usedSelenium:
            # 控制浏览器打开目标链接
            spider.browser.get(request.url)
            # 最大化窗口
            spider.browser.maximize_window()
            spider.browser.implicitly_wait(10)
            # 在构造渲染后的HtmlResponse之前，做一些事情
            # 1.比如等待浏览器页面中的某个元素出现后，再返回渲染后的html；
            # 2.比如将页面切换进iframe中的页面；
            spider.selenium_func(request)
            # 获取浏览器渲染后的html
            html = spider.browser.page_source
            # 构造Response
            # 这个Response将会被你的爬虫进一步处理
            return HtmlResponse(url=spider.browser.current_url, request=request, body=html.encode(), encoding="utf-8")

# 参考代码


class TaobaoSeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = get_driver_ChromeDriver()
        self.browser.set_window_size(1400, 700)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        if spider.name == 'taobao':
            time.sleep(random.uniform(1, 6))
            """
            用PhantomJS抓取页面
            :param request: Request对象
            :param spider: Spider对象
            :return: HtmlResponse
            """
            self.logger.debug('PhantomJS is Starting')
            page = request.meta.get('page', 1)
            try:
                self.browser.get(request.url)
                if page > 1:
                    input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                    submit = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                    input.clear()
                    input.send_keys(page)
                    submit.click()
                self.wait.until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
                self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.m-itemlist .items .item')))
                return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'), service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
