import os
import random
import re
import time
import scrapy
from scrapy.http import HtmlResponse
from mytools.general_spider.general_spider.items import OAProAdmitToDoItem
from mytools.general_spider.general_spider.extendsion.SeleniumSpider import (
    SeleniumSpider,
)
from mytools.general_spider.general_spider.extendsion.tools import waitForXpath
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
)


class OAProAdmitToDoSpider(SeleniumSpider):
    name = "OAProAdmitToDo"
    url_format = "http://oa.zybank.com.cn/#/sd-frame/sd-mytodolist"
    custom_settings = {
        "ITEM_PIPELINES": {
            "mytools.general_spider.general_spider.pipelines.OAProAdmitToDoPipeline": 300
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
            "dont_redirect": False,
            "purpose": "login",
            "page_num": 1,
        }
        # 列表页是动态的，所以需要启用selenium
        yield scrapy.Request(
            start_url, meta=meta, callback=self.parse, dont_filter=True
        )

    def parse(self, response):
        meta = response.meta
        if meta["page_num"] != -1:  # -1表示没有下一页了
            current_url = response.url
            # 获取当前页面中的文章列表
            articles = response.xpath(
                '//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]'
            )
            # articles = response.xpath('//*[@id="sd-body"]/section/section/main/section/main/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
            for article in articles:
                time.sleep(random.randint(3, 6))
                # 获取文章的标题和链接
                title = article.xpath("./td[2]/@title").get()
                submitter = article.xpath("./td[3]/@title").get()
                submit_depart = article.xpath("./td[4]/@title").get()
                submit_date = article.xpath("./td[5]/@title").get()
                # 根据日期判断停止继续
                item_date = submit_date[:10]
                if not (
                    item_date < self.settings.get("DATA_END_DATE")
                    and item_date >= self.settings.get("DATA_START_DATE")
                ):
                    continue
                # 2.实例化：
                item = OAProAdmitToDoItem()
                # 3.赋值
                item["title"] = title
                item["submitter"] = submitter
                item["submit_depart"] = submit_depart
                item["submit_date"] = submit_date
                # 打开详情
                current_window = self.browser.current_window_handle
                title_ele = waitForXpath(
                    self.browser,
                    f'//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]/td[@title="{title}"]',
                    timeout=self.timeout,
                )
                title_ele.click()
                time.sleep(random.randint(3, 6))
                # 也未涉及到跳转窗口，所以需要切换窗口
                all_windows = self.browser.window_handles
                for window in all_windows:
                    if window != current_window:
                        self.browser.switch_to.window(window)
                waitForXpath(
                    self.browser,
                    '//div[@class="ant-tabs-content ant-tabs-content-no-animated ant-tabs-top-content"]/div[@class="ant-tabs-tabpane ant-tabs-tabpane-active"]',
                    timeout=self.timeout,
                )
                detail_body = self.browser.page_source
                detail_url = self.browser.current_url
                response = HtmlResponse(
                    url=detail_url,
                    body=detail_body,
                    encoding="utf-8",
                    status=200,
                )
                self.parse_article(item, response)
                time.sleep(random.randint(3, 6))
                self.browser.close()
                self.browser.switch_to.window(current_window)
                yield item
            # 翻页
            meta["page_num"] += 1
            if meta["page_num"] <= self.settings.get("MAX_PAGE"):  # 不超过3页
                meta.update(
                    {
                        "useSelenium": True,
                        "questCurrentLink": False,
                        "dont_redirect": True,
                        "purpose": "next",
                    }
                )
                yield scrapy.Request(
                    url=current_url, meta=meta, callback=self.parse, dont_filter=True
                )

    def parse_article(self, item, response):
        # item = response.meta["data"]
        # 获取文章的正文内容
        content = response.xpath('//table[@class="sd-form-theme sd-default"]')
        # 需求背景
        item["background"] = content.xpath("./tr[8]/td[2]/span/text()").get()
        # 背景后面的附件名称
        content_attachs = content.xpath(
            "./tr[8]/td[3]//ul[@class='ant-list-items wapper_sd-draggable_common']/li[@class='ant-list-item actionlist_sd-attachment_common list_sd-attachment_common item_sd-draggable_common']"
        )
        item["attach_save_path"] = []
        for one_attach in content_attachs:
            one_attach_name = one_attach.xpath("./span//span/text()").get()
            item["attach_save_path"].append(re.sub(r"\s+", "", one_attach_name))
        # 点击下载按钮下载
        if len(content_attachs) > 0:
            content_attachs_downloads = waitForXpath(
                self.browser,
                "//table[@class='sd-form-theme sd-default']/tr[8]/td[3]//ul[@class='ant-list-items wapper_sd-draggable_common']/li[@class='ant-list-item actionlist_sd-attachment_common list_sd-attachment_common item_sd-draggable_common']//button[@class='ant-btn ant-btn-link ant-btn-icon-only']",
                timeout=self.timeout,
                is_elements=True,
            )
            for submit_download in content_attachs_downloads:
                submit_download.click()
                time.sleep(2)
        # 相关文件下载
        relate_content_attachs = content.xpath(
            "./tr[13]/td[2]//ul[@class='ant-list-items wapper_sd-draggable_common']/li[@class='ant-list-item actionlist_sd-attachment_common list_sd-attachment_common item_sd-draggable_common']"
        )
        item["relate_attach_save_path"] = []
        for one_attach in relate_content_attachs:
            one_attach_name = one_attach.xpath("./span//span/text()").get()
            item["relate_attach_save_path"].append(re.sub(r"\s+", "", one_attach_name))
        # 点击下载按钮下载
        if len(relate_content_attachs) > 0:
            relate_content_attachs_downloads = waitForXpath(
                self.browser,
                "//table[@class='sd-form-theme sd-default']/tr[13]/td[2]//ul[@class='ant-list-items wapper_sd-draggable_common']/li[@class='ant-list-item actionlist_sd-attachment_common list_sd-attachment_common item_sd-draggable_common']//button[@class='ant-btn ant-btn-link ant-btn-icon-only']",
                timeout=self.timeout,
                is_elements=True,
            )
            for submit_download in relate_content_attachs_downloads:
                submit_download.click()
                time.sleep(2)
        # 需求概述
        item["summary"] = content.xpath("./tr[9]/td[2]//text()").get()
        # yield item

    # 使用selenium请求时，请求后的动作
    def selenium_func(self, request):
        meta = request.meta
        if meta["purpose"] == "login":
            userid_input = waitForXpath(
                self.browser,
                "//form[@class='ant-form ant-form-horizontal form_sd-login_login']//input[@id='horizontal_login_userName' and @type='text']",
                timeout=self.timeout,
            )
            password_input = waitForXpath(
                self.browser,
                "//form[@class='ant-form ant-form-horizontal form_sd-login_login']//input[@id='horizontal_login_password' and @type='password']",
                timeout=self.timeout,
            )
            userid_input.clear()
            userid_input.send_keys("loubenlei")
            password_input.clear()
            password_input.send_keys("abcd@1234")
            submit = waitForXpath(
                self.browser,
                "//form[@class='ant-form ant-form-horizontal form_sd-login_login']//span[text()='登 录']",
                timeout=self.timeout,
            )
            # submit.click()
            login = self.browser.switch_to.active_element
            login.send_keys(Keys.ENTER)

            waitForXpath(
                self.browser,
                "//div[@class='ant-tabs-tab-active ant-tabs-tab' and @role='tab' and contains(text(),'待处理')]",
                timeout=self.timeout,
            )
            # 切换到已处理
            submit = waitForXpath(
                self.browser,
                "//div[@class='ant-tabs ant-tabs-top ant-tabs-line ant-tabs-no-animation sd-has-table']//div[@role='tab'][1]",  # 1是待处理tab页
                timeout=self.timeout,
            )
            submit.click()
            # self.browser.switch_to.frame('frame_name')
            # login = self.browser.switch_to.active_element
            waitForXpath(
                self.browser,
                f"//ul[@class='ant-pagination ant-table-pagination']",
                timeout=self.timeout,
            )
            # 等待数据完全展示出来
            time.sleep(3)
            # pass
        elif meta["purpose"] == "next":
            page = meta["page_num"]
            # 这个方法会在我们的下载器中间件返回Response之前被调用
            # 等待content内容加载成功后，再继续
            # 这样的话，我们就能在parse_content方法里应用选择器扣出#content了
            # 通过“下一页”按钮翻页
            # a = waitForXpath(
            #     self.browser, "//a[@class='nextbtn' and text()='下一页']")
            # a.click()
            # 通过输入页数点击并点击确定翻页
            try:
                input = waitForXpath(
                    self.browser,
                    "//div[@class='ant-pagination-options-quick-jumper' and contains(text(),'跳至')]/input[@type='text']",
                    timeout=5,
                )
            except (TimeoutException, NoSuchElementException):
                request.meta.update({"page_num": -1})
            else:  # 没异常正常处理
                input.clear()
                input.send_keys(page)
                self.browser.switch_to.active_element.send_keys(Keys.ENTER)
                # 切换到已处理
                submit = waitForXpath(
                    self.browser,
                    "//div[@class='ant-tabs ant-tabs-top ant-tabs-line ant-tabs-no-animation sd-has-table']//div[@role='tab'][2]",
                    timeout=self.timeout,
                )
                submit.click()
                waitForXpath(
                    self.browser,
                    f"//ul[@class='ant-pagination ant-table-pagination']",
                    timeout=self.timeout,
                )
        elif meta["purpose"] == "download":
            a = waitForXpath(
                self.browser, '//div[@id="files"]/a[1]', timeout=self.timeout
            )
            a.click()

    def closed(self, reason):
        # # 判断文件是否存在
        out_file = Path(self.out_file)
        if out_file.exists():
            # 重命名
            out_file.rename(self.out_file + "_finished")
        return super().closed(reason)
