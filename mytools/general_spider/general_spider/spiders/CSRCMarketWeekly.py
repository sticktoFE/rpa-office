import os
import re
import scrapy
from mytools.general_spider.general_spider.items import CSRCMarketWeeklyItem
from mytools.general_spider.general_spider.extension.SeleniumSpider import (
    SeleniumSpider,
)
from mytools.general_spider.general_spider.extension.tools import waitForXpath
from pathlib import Path
from selenium.webdriver.common.by import By

from myutils.info_out_manager import ReadWriteConfFile


class CSRCMarketWeeklySpider(SeleniumSpider):
    name = "csrc_market_weekly"
    # start_urls = ["http://www.csrc.gov.cn/csrc/c101971/zfxxgk_zdgk.shtml"]
    url_format = "http://www.csrc.gov.cn/csrc/c100119/common_list.shtml"
    # 制定专属pipeline
    custom_settings = {
        "ITEM_PIPELINES": {
            "mytools.general_spider.general_spider.pipelines.CSRCMarketWeeklyPipeline": 300
        }
    }

    def start_requests(self):
        # self.out_file = self.settings.get('out_file')
        """
        开始发起请求，记录页码
        """
        start_url = f"{self.url_format}"
        meta = {
            "useSelenium": True,
            "questCurrentLink": True,
            "dont_redirect": True,
            "purpose": "list",
            "page_num": 1,
        }
        # 列表页是动态的，所以需要启用selenium
        yield scrapy.Request(start_url, meta=meta, callback=self.parse)

    def parse(self, response):
        meta = response.meta
        if meta["page_num"] != -1:  # -1表示没有下一页了
            self.current_url = response.url
            # 获取当前页面中的文章列表
            articles = response.xpath('//ul[@class="list mt10" and @id="list"]/li')
            i = 0
            for article in articles:
                i = i + 1
                if i == 3:  # 为了测试 取两个记录即退出
                    break
                # 获取文章的标题和链接
                title = article.xpath("./a/text()").get()
                link = article.xpath("./a/@href").get()
                date = article.xpath("./span/text()").get()
                # 2.实例化：
                item = CSRCMarketWeeklyItem()
                # 3.赋值
                item["title"] = title
                item["detail_url"] = response.urljoin(link)
                item["pub_date"] = date
                # 构造请求，访问文章详情页并传递title参数
                meta.update(
                    {
                        "useSelenium": True,
                        "questCurrentLink": True,
                        "dont_redirect": True,
                        "purpose": "download",
                        "data": item,
                    }
                )
                yield scrapy.Request(
                    url=response.urljoin(link), callback=self.parse_article, meta=meta
                )

            # 获取下一页的链接
            meta["page_num"] += 1
            MAX_PAGE = ReadWriteConfFile.getSectionValue(
                "General", "MAX_PAGE", type="int"
            )
            if meta["page_num"] <= MAX_PAGE:
                meta.update(
                    {
                        "useSelenium": True,
                        "questCurrentLink": True,
                        "dont_redirect": True,
                        "purpose": "next",
                    }
                )
                yield scrapy.Request(
                    url=self.current_url,
                    meta=meta,
                    callback=self.parse,
                    dont_filter=True,
                )

    def parse_article(self, response):
        item = response.meta["data"]
        # 获取文章的正文内容
        content = response.xpath('//div[@class="xxgk-table"]//tbody')
        # 获取文章的标题和链接
        item["index_no"] = content.xpath("./tr[1]/td[1]/text()").get()
        item["con_type"] = content.xpath("./tr[1]/td[1]/text()").get()
        item["pub_org"] = content.xpath("./tr[2]/td[1]/text()").get()
        content_attach = response.xpath('//div[@id="files"]')
        attach_name = content_attach.xpath("./a[1]/text()").get()
        item["attach_name"] = re.sub(r"\s+", "", attach_name)
        item["attach_link"] = content_attach.xpath("./a[1]/@href").get()
        item["attach_save_path"] = f'{self.down_path}/{item["attach_name"]}'
        yield item

    def selenium_func(self, request):
        meta = request.meta
        if meta["purpose"] == "next":
            page = meta["page_num"]
            # 这个方法会在我们的下载器中间件返回Response之前被调用
            # 等待content内容加载成功后，再继续
            # 这样的话，我们就能在parse_content方法里应用选择器扣出#content了
            # 通过“下一页”按钮翻页
            # a = waitForXpath(
            #     self.browser, "//a[@class='nextbtn' and text()='下一页']")
            # a.click()
            # 通过输入页数点击并点击确定翻页
            input = waitForXpath(
                self.browser,
                "//div[@class='page_num']//input[@id='page_input' and @type='text']",
                timeout=self.timeout,
            )
            submit = waitForXpath(
                self.browser,
                "//div[@class='page_num']//a[text()='确定']",
                timeout=self.timeout,
            )
            input.clear()
            input.send_keys(page)
            submit.click()
            waitForXpath(
                self.browser,
                f"//div[@class='page_num']//a[@class='current' and text()={str(page)}]",
                timeout=self.timeout,
            )
        elif meta["purpose"] == "download":
            a = waitForXpath(
                self.browser, '//div[@id="files"]/a[1]', timeout=self.timeout
            )
            # a.click()

    def closed(self, reason):
        # # 判断文件是否存在
        out_file = Path(self.out_file)
        if out_file.exists():
            # 重命名
            out_file.rename(self.out_file + "_finished")
        return super().closed(reason)
