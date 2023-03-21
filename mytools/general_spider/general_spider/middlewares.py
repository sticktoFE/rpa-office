import random
from scrapy.http import HtmlResponse
import logging
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
from fake_useragent import UserAgent

# 为了解决使用nuitka导出exe后，报fake_useragent.data找不到的问题
# 搜索了两天，使用其他方式解决不了，这个方法还可以
from fake_useragent import data
from mytools.general_spider.general_spider.extension import IPProxy
from scrapy.http.response.html import HtmlResponse
from myutils.web_driver_manager import get_driver_ChromeDriver


# 随机IP
class RandomProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # self.proxy_url = proxy_url

    # 动态设置代理服务器的IP 地址
    def process_request(self, request, spider):
        useProxy = request.meta.get("useProxy", False)
        if useProxy:
            proxy = IPProxy.get_random_proxy5010()
            if proxy:
                self.logger.debug("======" + "使用代理 " + str(proxy) + "======")
                request.meta["proxy"] = "http://{proxy}".format(proxy=proxy)


# 更换请求标识头
class RandomUserAgentMiddleware(object):
    """
    随机更换user-agent
    模仿并替换site-package/scrapy/downloadermiddlewares源代码中的
    useragent.py中的UserAgentMiddleware类
    """

    # 更换用户代理逻辑在此方法中
    def process_request(self, request, spider):
        # location = "browsers.json"
        ua = UserAgent(verify_ssl=False)  # ,cache_path=data.brow)
        request.headers["User-Agent"] = ua.random


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
        usedSelenium = request.meta.get("useSelenium", False)
        questCurrentLink = request.meta.get("questCurrentLink", True)
        if usedSelenium:
            # 控制浏览器打开目标链接,针对需要模拟浏览器打开目标连接，就不要使用传进来的连接，如需要翻页的场景
            if questCurrentLink:
                spider.browser.get(request.url)
            # 在构造渲染后的HtmlResponse之前，做一些事情
            # 1.比如等待浏览器页面中的某个元素出现后，再返回渲染后的html；
            # 2.比如将页面切换进iframe中的页面；
            spider.selenium_func(request)
            # 获取浏览器渲染后的html
            body = spider.browser.page_source
            url = spider.browser.current_url
            # spider.browser.close()
            # spider.browser.switch_to.window(current_window)
            # url = request.respons
            # 构造Response
            # 这个Response将会被你的爬虫进一步处理
            return HtmlResponse(
                url=url,
                body=body,
                encoding="utf-8",
                status=200,
            )


# 参考代码
class TaobaoSeleniumMiddleware:
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
        if spider.name == "taobao":
            time.sleep(random.uniform(1, 6))
            """
            用PhantomJS抓取页面
            :param request: Request对象
            :param spider: Spider对象
            :return: HtmlResponse
            """
            self.logger.debug("PhantomJS is Starting")
            page = request.meta.get("page", 1)
            try:
                self.browser.get(request.url)
                if page > 1:
                    input = self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#mainsrp-pager div.form > input")
                        )
                    )
                    submit = self.wait.until(
                        EC.element_to_be_clickable(
                            (
                                By.CSS_SELECTOR,
                                "#mainsrp-pager div.form > span.btn.J_Submit",
                            )
                        )
                    )
                    input.clear()
                    input.send_keys(page)
                    submit.click()
                self.wait.until(
                    EC.text_to_be_present_in_element(
                        (By.CSS_SELECTOR, "#mainsrp-pager li.item.active > span"),
                        str(page),
                    )
                )
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".m-itemlist .items .item")
                    )
                )
                return HtmlResponse(
                    url=request.url,
                    body=self.browser.page_source,
                    request=request,
                    encoding="utf-8",
                    status=200,
                )
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            timeout=crawler.settings.get("SELENIUM_TIMEOUT"),
            service_args=crawler.settings.get("PHANTOMJS_SERVICE_ARGS"),
        )
