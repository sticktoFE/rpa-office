"""
一个spider开一个浏览器
"""
import logging
import scrapy
from general_spider.utils import web_driver_manager


class SeleniumSpider(scrapy.Spider):
    """
    Selenium专用spider
    一个spider开一个浏览器
    浏览器驱动下载地址:http://www.cnblogs.com/qiezizi/p/8632058.html
    """

    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 获取浏览器操控权
        self.timeout = settings.get("SELENIUM_TIMEOUT")
        self.out_file = settings.get("out_file")
        self.down_path = settings.get("down_path")
        self.browser_parameter_file_name = settings.get("browser_parameter_file_name")
        """
        返回浏览器实例
        """
        # 设置selenium与urllib3的logger的日志等级为ERROR
        # 如果不加这一步，运行爬虫过程中将会产生一大堆无用输出
        logging.getLogger("selenium").setLevel("ERROR")
        logging.getLogger("urllib3").setLevel("ERROR")
        # web_driver_manager.get_driver_FireFoxDriver()
        self.browser = web_driver_manager.get_driver_ChromeDriver(
            browser_parameter_file_name=self.browser_parameter_file_name,
            down_file_save_path=self.down_path,
            timeout=self.timeout,
        )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(crawler.settings, *args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def selenium_func(self, request):
        """
            在返回浏览器渲染的html前做一些事情,在需要使用的子类中要重写该方法，并利用self.browser操作浏览器
            1.比如等待浏览器页面中的某个元素出现后，再返回渲染后的html；
            2.比如将页面切换进iframe中的页面；
            假如内容页的目标信息处于iframe中，我们可以将窗口切换进目标iframe里面，然后返回iframe的html
        要实现这样的操作，只需要重写一下SeleniumSpider子类中的selenium_func方法
        要注意到SeleniumSpider中的selenium_func其实是啥也没做的，一个pass，所有的功能都在子类中重写
            def selenium_func(self, request):
                # 找到id为myPanel的iframe
                target = self.browser.find_element_by_xpath("//iframe[@id='myPanel']")
                # 将浏览器的窗口切换进该iframe中
                # 那么切换后的self.browser的page_source将会是iframe的html
                self.browser.switch_to.frame(target)
        """
        pass

    def closed(self, reason):
        # 在爬虫关闭后，关闭浏览器的所有tab页，并关闭浏览器
        self.browser.quit()
        # 日志记录一下
        self.logger.info("selenium已关闭浏览器...")


# 以下是为了解决 使用nuitka工具打包成exe时，报 could not get source code错误的问题
# 为了一个打包，真是坎坷
# def warn_on_generator_with_return_value_stub(spider, callable):
#     pass

# scrapy.utils.misc.warn_on_generator_with_return_value = (
#     warn_on_generator_with_return_value_stub
# )
# scrapy.core.scraper.warn_on_generator_with_return_value = (
#     warn_on_generator_with_return_value_stub
# )

# 以上是直接忽略相应警告，而通过在rpa/lib/inspedt.py中加入print,
# 发现是当前爬虫文件在打包文件夹中不存在，如 CSRCMarketWeekly.py，通过
# 手动添加，可以在执行exe时如爬虫有问题，还可以修改此文件，即支持修改，所以
# 就采取这种方式解决问题
