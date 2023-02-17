import os
import random
import re
import sys
import time
from urllib import request

import execjs

from scrapy import Request, Spider
from mytools.general_spider.general_spider.items import CSRCItem
from parsel import Selector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urlparse


class BankReportSpider(Spider):
    name = "bank_report"
    allowed_domains = ["http://vip.stock.finance.sina.com.cn"]
    # start_urls = ["http://vip.stock.finance.sina.com.cn"]
    total_pages = 0
    currentDir = os.path.dirname(__file__)

    def start_requests(self):
        with open(f"{self.currentDir}/BankReportStockNum.txt", encoding="utf-8") as f:
            for line in f.readlines():
                # print(line, end="")
                searchResult = re.search(r"(\d+)--(\w+)", line)
                if searchResult:
                    url = f"http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{searchResult.group(1)}/page_type/ndbg.phtml"
                    yield Request(
                        url,
                        # callback=self.parse,
                        meta={
                            "stock_id": searchResult.group(1),
                            "stock_name": searchResult.group(2),
                        },
                    )

    def parse(self, response):
        target = r"&id=[_0-9_]{6,}"
        target_list = re.findall(target, response.text)
        stock_id = response.meta["stock_id"]
        stock_name = response.meta["stock_name"]
        for rindex in target_list:
            target_url = f"http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid={stock_id}{rindex}"
            yield Request(
                target_url,
                callback=self.parse_detail,
                meta={"stock_id": stock_id, "stock_name": stock_name},
                encoding="utf-8",
                dont_filter=True,
            )

    # 解析详情页
    def parse_detail(self, response):
        stock_id = response.meta["stock_id"]
        stock_name = response.meta["stock_name"]
        file_url = re.search(
            "http://file.finance.sina.com.cn/211.154.219.97:9494/.*/(\d{4})/.*?PDF",
            response.text,
        )
        if file_url:
            target_url = file_url.group(0)
            yield Request(
                target_url,
                callback=self.parse_file,
                meta={
                    "stock_id": stock_id,
                    "stock_name": stock_name,
                    "year": file_url.group(1),
                    "file_name": file_url.group(0).split("/")[-1],
                },
                encoding="utf-8",
                dont_filter=True,
            )

    # 存储文件
    def parse_file(self, response):
        # print(file_url.group(0))
        stock_id = response.meta["stock_id"]
        stock_name = response.meta["stock_name"]
        year = response.meta["year"]
        file_name = response.meta["file_name"]
        local = f"{self.currentDir}/bank/{stock_name}({stock_id})--{int(year)-1}--{file_name}".replace(
            "PDF", "pdf"
        )
        with open(local, "wb") as Pypdf:
            Pypdf.write(response.body)
            # for chunk in response.iter_content(chunk_size=1024):
            #     if chunk:
            #         Pypdf.write(chunk)
        print("done!")
