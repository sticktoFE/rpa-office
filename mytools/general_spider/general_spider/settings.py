# Scrapy settings for ter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
import time


BOT_NAME = "general_spider"

SPIDER_MODULES = ["mytools.general_spider.general_spider.spiders"]
NEWSPIDER_MODULE = "mytools.general_spider.general_spider.spiders"

FEED_EXPORT_ENCODING = "utf-8"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ter (+http://www.yourdomain.com)'
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36 Edg/91.0.864.48"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs#设置下裁之后的自动延迟
DOWNLOAD_DELAY = random.randint(5, 9)
# 启用后，当从相同的网站获取数据时，Scrapy将会等待一个随机的值，延迟时间为0.5到1.5之间的一个随机值乘以DOWNLOAD_DELAY
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'general_spider.middlewares.TerSpiderMiddleware': 543,
# }
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# 开启中间件
DOWNLOADER_MIDDLEWARES = {
    # 'general_spider.middlewares.SeleniumDownloadMiddleware': 543,
    # 'general_spider.middlewares.RandomUserAgentMiddlware': 400,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
    "mytools.general_spider.general_spider.middlewares.RandomProxyMiddleware": 350,
    # 'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
    "mytools.general_spider.general_spider.middlewares.SeleniumDownloaderMiddleware": 550,
    # "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    # 这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}


FAKEUSERAGENT_PROVIDERS = [
    # this is the first provider we'll try
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",
    # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FakerProvider",
    # fall back to USER_AGENT value
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",
]
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'general_spider.pipelines.TerPipeline': 300,
# }
# 开启item pipelines
ITEM_PIPELINES = {
    # 'general_spider.pipelines.JianshuTwistedPipeline': 300,
    "mytools.general_spider.general_spider.pipelines.OAProAdmitToDoPipeline": 300,
    "mytools.general_spider.general_spider.pipelines.OAProAdmitHaveDonePipeline": 301,
    # 'general_spider.pipelines.JianshuSpiderPipeline': 300,
    # "general_spider.pipelines.FuZhouEcoIndexPipeline": 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# 开启访问频率限制
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay #设置访问开始的延迟
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# 设置访问之间的最大延迟
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# 设置Scrapy 并行发给每台远程服务器的请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY = 10
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# 设置日志信息 INFO
""" LOG_FILE = 'CSRC.log'
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'DEBUG' """
# 经常因为页面报404导致spider停止，此处
HTTPERROR_ALLOWED_CODES = [404]

KEYWORDS = ["iPhone"]
MAX_PAGE = 5
SELENIUM_TIMEOUT = 20
