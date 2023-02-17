# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     configHandler
   Description :
   Author :        JHao
   date：          2020/6/22
-------------------------------------------------
   Change Activity:
                   2020/6/22:
-------------------------------------------------
"""
__author__ = 'JHao'

import os
from mytools.proxy_pool import setting
from mytools.proxy_pool.util.singleton import Singleton
from mytools.proxy_pool.util.lazyProperty import LazyProperty
from mytools.proxy_pool.util.six import reload_six, withMetaclass


class ConfigHandler(withMetaclass(Singleton)):

    def __init__(self):
        pass

    @LazyProperty
    def serverHost(self):
        return os.environ.get("HOST", setting.HOST)

    @LazyProperty
    def serverPort(self):
        return os.environ.get("PORT", setting.PORT)

    @LazyProperty
    def dbConn(self):
        return os.getenv("DB_CONN", setting.DB_CONN)

    @LazyProperty
    def tableName(self):
        return os.getenv("TABLE_NAME", setting.TABLE_NAME)

    @property
    def fetchers(self):
        reload_six(setting)
        return setting.PROXY_FETCHER

    @LazyProperty
    def httpUrl(self):
        return os.getenv("HTTP_URL", setting.HTTP_URL)

    @LazyProperty
    def httpsUrl(self):
        return os.getenv("HTTPS_URL", setting.HTTPS_URL)

    @LazyProperty
    def verifyTimeout(self):
        return os.getenv("VERIFY_TIMEOUT", setting.VERIFY_TIMEOUT)

    # @LazyProperty
    # def proxyCheckCount(self):
    #     return os.getenv("PROXY_CHECK_COUNT", setting.PROXY_CHECK_COUNT)

    @LazyProperty
    def maxFailCount(self):
        return os.getenv("MAX_FAIL_COUNT", setting.MAX_FAIL_COUNT)

    # @LazyProperty
    # def maxFailRate(self):
    #     return os.getenv("MAX_FAIL_RATE", setting.MAX_FAIL_RATE)

    @LazyProperty
    def poolSizeMin(self):
        return os.getenv("POOL_SIZE_MIN", setting.POOL_SIZE_MIN)

    @LazyProperty
    def timezone(self):
        return os.getenv("TIMEZONE", setting.TIMEZONE)
