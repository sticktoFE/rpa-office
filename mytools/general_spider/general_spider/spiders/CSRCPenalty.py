import scrapy
from mytools.general_spider.general_spider.items import CSRCPenaltyItem
from mytools.general_spider.general_spider.extension.SeleniumSpider import (
    SeleniumSpider,
)
from mytools.general_spider.general_spider.extension.tools import waitForXpath
from pathlib import Path
from myutils import web_driver_manager

from myutils.info_out_manager import ReadWriteConfFile


class CSRCPenaltySpider(SeleniumSpider):
    name = "csrc_penalty"
    # start_urls = ["http://www.csrc.gov.cn/csrc/c101971/zfxxgk_zdgk.shtml"]
    url_format = "http://www.csrc.gov.cn/csrc/c101971/zfxxgk_zdgk.shtml"
    # 制定专属pipeline
    custom_settings = {
        "ITEM_PIPELINES": {
            "mytools.general_spider.general_spider.pipelines.CSRCPenaltyPipeline": 300
        }
    }

    def start_requests(self):
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
            articles = response.xpath('//ul[@class="list_ul"]//tr[position()>1]')
            i = 0
            for article in articles:
                i = i + 1
                if i == 3:  # 为了测试 取两个记录即退出
                    break
                # 获取文章的标题和链接
                title = article.xpath("./td[2]/a/text()").get()
                link = article.xpath("./td[2]/a/@href").get()
                text_num = article.xpath("./td[3]/text()").get()
                date = article.xpath("./td[4]//text()").get()
                # 2.实例化：
                item = CSRCPenaltyItem()
                # 3.赋值
                item["pub_date"] = date
                item["title"] = title
                item["text_num"] = text_num
                item["detail_url"] = link
                # 构造请求，访问文章详情页并传递title参数
                yield scrapy.Request(
                    url=link,
                    callback=self.parse_article,
                    meta={"data": item},
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
        # 获取文章的正文内容
        content = response.xpath('//div[@class="detail-news"]/p/text()').getall()
        content = "".join(content).strip()
        # 获取传递过来的标题参数
        item = response.meta["data"]
        item["content"] = content
        yield item

    def selenium_func(self, request):
        meta = request.meta
        page = meta["page_num"]
        if meta["purpose"] == "next":
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
                "//div[@class='page_num']//input[@class='zxfinput' and @type='number']",
                timeout=self.timeout,
            )
            submit = waitForXpath(
                self.browser,
                "//div[@class='page_num']//span[@class='zxfokbtn' and text()='确定']",
                timeout=self.timeout,
            )
            input.clear()
            input.send_keys(page)
            submit.click()
            waitForXpath(
                self.browser,
                f"//div[@class='page_num']//span[@class='current' and text()={str(page)}]",
                timeout=self.timeout,
            )
            waitForXpath(
                self.browser,
                f"//div[@class='rightList']//ul[@class='list_ul']",
                timeout=self.timeout,
            )

    def closed(self, reason):
        # # 判断文件是否存在
        out_file = Path(self.out_file)
        if out_file.exists():
            # 重命名
            out_file.rename(self.out_file + "_finished")
        return super().closed(reason)
