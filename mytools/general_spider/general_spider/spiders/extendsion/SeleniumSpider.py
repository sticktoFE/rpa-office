"""
一个spider开一个浏览器
"""
import logging
import scrapy
from selenium import webdriver
from myutils import web_driver_manager


class SeleniumSpider(scrapy.Spider):
    """
    Selenium专用spider

    一个spider开一个浏览器

    浏览器驱动下载地址:http://www.cnblogs.com/qiezizi/p/8632058.html
    """
    # 浏览器是否设置无头模式，仅测试时可以为False
    SetHeadless = True
    # 是否允许浏览器使用cookies
    EnableBrowserCookies = True

    def __init__(self, *args, **kwargs):
        super(SeleniumSpider, self).__init__(*args, **kwargs)
        # 获取浏览器操控权
        self.browser = self._get_browser()

    def _get_browser(self):
        """
        返回浏览器实例
        """
        # 设置selenium与urllib3的logger的日志等级为ERROR
        # 如果不加这一步，运行爬虫过程中将会产生一大堆无用输出
        logging.getLogger('selenium').setLevel('ERROR')
        logging.getLogger('urllib3').setLevel('ERROR')

        # selenium已经放弃了PhantomJS，开始支持firefox与chrome的无头模式
        return self._use_chrome()

    def _use_chrome(self):
        browser = web_driver_manager.get_driver_ChromeDriver()
        browser.set_window_size(1400, 700)
        browser.set_page_load_timeout(3)
        return browser

    def _use_firefox(self):
        """
        使用selenium操作火狐浏览器
        """
        profile = webdriver.FirefoxProfile()
        options = webdriver.FirefoxOptions()
        # 下面一系列禁用操作是为了减少selenium的资源耗用，加速scrapy
        # 禁用图片
        profile.set_preference('permissions.default.image', 2)
        profile.set_preference('browser.migration.version', 9001)
        # 禁用css
        profile.set_preference('permissions.default.stylesheet', 2)
        # 禁用flash
        profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        # 如果EnableBrowserCookies的值设为False，那么禁用cookies
        if hasattr(self, "EnableBrowserCookies") and self.EnableBrowserCookies:
            # •值1 - 阻止所有第三方cookie。
            # •值2 - 阻止所有cookie。
            # •值3 - 阻止来自未访问网站的cookie。
            # •值4 - 新的Cookie Jar策略（阻止对跟踪器的存储访问）
            profile.set_preference("network.cookie.cookieBehavior", 2)

        # 默认是无头模式，意思是浏览器将会在后台运行，也是为了加速scrapy
        # 我们可不想跑着爬虫时，旁边还显示着浏览器访问的页面
        # 调试的时候可以把SetHeadless设为False，看一下跑着爬虫时候，浏览器在干什么
        if self.SetHeadless:
            # 无头模式，无UI
            options.add_argument('-headless')
        # 禁用gpu加速
        options.add_argument('--disable-gpu')
        return webdriver.Firefox(firefox_profile=profile, options=options)

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