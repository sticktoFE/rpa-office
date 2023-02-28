import os
import random
import re
import time
import scrapy
from scrapy.http import HtmlResponse
from mytools.general_spider.general_spider.items import OAProAdmitHaveDoneItem
from mytools.general_spider.general_spider.extendsion.SeleniumSpider import (
    SeleniumSpider,
)
from mytools.general_spider.general_spider.extendsion.tools import waitForXpath
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException,TimeoutException
class OAProAdmitHaveDoneSpider(SeleniumSpider):
    name = "OAProAdmitHaveDone"
    url_format = "http://oa.zybank.com.cn/#/sd-frame/sd-mytodolist"
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
        yield scrapy.Request(start_url, meta=meta, callback=self.parse,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        if meta["page_num"] != -1: # -1表示没有下一页了
            self.current_url = response.url
            # 获取当前页面中的文章列表
            articles = response.xpath('//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]')
            # articles = response.xpath('//*[@id="sd-body"]/section/section/main/section/main/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
            for article in articles:
                time.sleep(random.randint(3, 6))
                # 获取文章的标题和链接
                title = article.xpath("./td[1]/@title").get()
                # 仅针对科技需求任务进行获取
                if '信息科技项目建设需求申请' not in title:
                    continue
                # 2.实例化：
                item = OAProAdmitHaveDoneItem()
                # 3.赋值
                item["title"] = title
                # 打开详情
                current_window = self.browser.current_window_handle
                title_ele = waitForXpath(self.browser,f'//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]/td[@title="{title}"]',timeout=self.timeout)
                title_ele.click()
                time.sleep(random.randint(2, 8))
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
                body = self.browser.page_source
                url = self.browser.current_url
                response = HtmlResponse(
                    url=url,
                    body=body,
                    encoding="utf-8",
                    status=200,
                )
                self.parse_article(item,response)
                # 根据日期判断停止继续,目前只获取当天提取的需求进行获取
                current_date = str(time.strftime("%Y-%m-%d", time.localtime()))
                if item["submit_date"] != current_date:
                    break
                time.sleep(random.randint(3, 6))
                self.browser.close()
                self.browser.switch_to.window(current_window)
                yield item
            #翻页
            meta["page_num"] += 1
            if meta["page_num"] < self.settings.get('MAX_PAGE'):  # 不超过3页
                meta.update(
                    {
                        "useSelenium": True,
                        "questCurrentLink": False,
                        "dont_redirect": True,
                        "purpose": "next",
                    }
                )
                yield scrapy.Request(url=self.current_url, meta=meta, callback=self.parse, dont_filter=True)

    def parse_article(self, item,response):
        # item = response.meta["data"]
        # 获取文章的正文内容
        content = response.xpath('//table[@class="sd-form-theme sd-default"]')
        item["demand_no"]  = content.xpath("./tr[2]/td[2]/span/text()").get().strip()
        item["submit_date"]  = content.xpath("./tr[2]/td[4]/span/text()").get().strip()
        item["submitter"]  = content.xpath("./tr[3]/td[2]/span/text()").get().strip()
        item["submit_depart"]  = content.xpath("./tr[4]/td[2]/span/text()").get().strip()
        # 需求背景
        item["background"] = '\r\n'.join(content.xpath("./tr[8]/td[2]//text()").getall()).strip()
        # 需求概述
        item["summary"] = '\r\n'.join(content.xpath("./tr[9]/td[2]//text()").getall()).strip()
        # 产品登记预审结果 准入 备案 不涉及
        item["admit_result"] = '\r\n'.join(content.xpath("./tr[39]/td[2]//text()").getall()).strip()
        # 产品分类
        item["pro_type"] = '\r\n'.join(content.xpath("./tr[39]/td[4]//text()").getall()).strip()
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
            userid_input.send_keys('loubenlei')
            password_input.clear()
            password_input.send_keys('abcd@1234')
            submit = waitForXpath(
                self.browser,
                "//form[@class='ant-form ant-form-horizontal form_sd-login_login']//span[text()='登 录']",
                timeout=self.timeout,
            )
            # submit.click()
            login = self.browser.switch_to.active_element
            login.send_keys(Keys.ENTER)
            
            waitForXpath(
                self.browser,"//div[@class='ant-tabs-tab-active ant-tabs-tab' and @role='tab' and contains(text(),'待处理')]",
                timeout=self.timeout,
            )
            # 切换到已处理
            submit = waitForXpath(
                self.browser,
                "//div[@class='ant-tabs ant-tabs-top ant-tabs-line ant-tabs-no-animation sd-has-table']//div[@role='tab'][2]",#2是已办理tab页
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
            except (TimeoutException,NoSuchElementException):
                request.meta.update({'page_num':-1})
            else:#没异常正常处理
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
