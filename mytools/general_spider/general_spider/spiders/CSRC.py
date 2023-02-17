import random
import re
import sys
import time

import execjs
import scrapy
from mytools.general_spider.general_spider.items import CSRCItem
from parsel import Selector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urlparse

"""
对证监会（CHINA_SECURITIES_REGULATORY_COMMISSION）处罚信息进行抽取

"""


class CSRCSpider(scrapy.Spider):
    name = "csrc"
    allowed_domains = ["csrc.gov.cn"]
    start_urls = ["http://www.csrc.gov.cn/csrc/c101971/zfxxgk_zdgk.shtml"]
    total_pages = 0
    # 0、获取列表页的页数

    def parse(self, response):
        self.total_pages = response.xpath('//div[@class="row"]')
        self.parse_list(response)
        # 下一页
        start_download_url = (
            "http://www.csrc.gov.cn/pub/zjhpublic/3300/3313/index_7401_"
        )
        for i in range(1, int(self.total_pages) + 1):
            url = start_download_url + f"{i}.htm"
            # 3.封装请求  自己写一个parse的函数
            yield scrapy.Request(
                url=url, callback=self.parse_list, encoding="utf-8", dont_filter=True
            )  # 看到yield 要挂起

    # 列表页的解析函数
    def parse_list(self, response):
        # 1.获取整个处罚信息
        penalty_info_list = response.xpath('//div[@class="row"]')
        for penalty in penalty_info_list:
            title = penalty.xpath('./li[@class="mc"]//a/text()').get()
            soure_url = penalty.xpath('./li[@class="mc"]//a/@href').get()
            detail_url = response.urljoin(soure_url)
            pub_date = penalty.xpath('./li[@class="fbrq"]/text()').get()
            text_num = penalty.xpath('./li[@class="wh"]/text()').get()
            # 处理相对路径里 ../../的情况
            # if re.search(r"../../",detail_url):
            #     base_url = get_base_url(response)
            #     detail_url = urlparse.urljoin(base_url, detail_url)
            # else:
            #     detail_url = "/".join(response.url.split("/")[:-3])+"/"+detail_url
            # 2.实例化：
            item = CSRCItem()
            # 3.赋值
            # item['index'] = index
            # item['con_type'] = con_type
            # item['pub_org'] = pub_org
            item["pub_date"] = pub_date
            item["title"] = title
            item["text_num"] = text_num
            item["detail_url"] = detail_url
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={"data": item},
                encoding="utf-8",
                dont_filter=True,
            )
            # 把请求的重复的url过滤掉 dont_filter=True

    # 解析详情页
    def parse_detail(self, response):
        # print(response.url)
        # 获取报告内容# -------------：：和页面内容相关点：：
        penalty_texts_sellist = response.xpath(
            '//*[@id="ContentRegion"]/div//p//text()'
        )
        penalty_texts = penalty_texts_sellist.getall()
        penalty_texts = list(
            map(lambda x: re.sub(r'[/:*?"<>\s\xa0]+', "", x), penalty_texts)
        )
        content = "".join(x.strip() for x in penalty_texts)
        # 变速箱
        item = response.meta["data"]
        item["content"] = content
        print(item)
        yield item

    def get_value(self, value):
        if value:
            value = value[0]
        else:
            value = 1
        return value
