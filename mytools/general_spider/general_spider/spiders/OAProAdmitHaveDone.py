import random
import time
import scrapy
from scrapy.http import HtmlResponse
from mytools.general_spider.general_spider.items import OAProAdmitHaveDoneItem
from mytools.general_spider.general_spider.extension.SeleniumSpider import (
    SeleniumSpider,
)
from mytools.general_spider.general_spider.extension.tools import waitForXpath
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
)

from myutils.DateAndTime import get_weeks_current_date


class OAProAdmitHaveDoneSpider(SeleniumSpider):
    name = "OAProAdmitHaveDone"
    url_format = "http://oa.zybank.com.cn/#/sd-frame/sd-mytodolist"
    # 制定专属pipeline
    custom_settings = {
        "ITEM_PIPELINES": {
            "mytools.general_spider.general_spider.pipelines.OAProAdmitHaveDonePipeline": 300
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

    # 解析列表数据
    def parse(self, response):
        meta = response.meta
        if meta["page_num"] != -1:  # -1表示没有下一页了
            self.current_url = response.url
            # 获取当前页面中的文章列表
            articles = response.xpath(
                '//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]'
            )
            # articles = response.xpath('//*[@id="sd-body"]/section/section/main/section/main/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div/table/tbody')
            for article in articles:
                time.sleep(random.randint(3, 6))
                # 获取文章的标题和链接
                title = article.xpath("./td[1]/@title").get()
                # 仅针对科技需求任务进行获取
                if "信息科技项目建设需求申请" not in title:
                    continue
                # 2.实例化：
                item = OAProAdmitHaveDoneItem()
                # 3.赋值
                item["title"] = title
                # 打开详情
                current_window = self.browser.current_window_handle
                try:
                    title_ele = waitForXpath(
                        self.browser,
                        f'//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]/td[@title="{title}"]',
                        timeout=self.timeout,
                    )
                    title_ele.click()
                except TimeoutException as e:
                    print(e)
                time.sleep(random.randint(3, 6))
                # 也未涉及到跳转窗口，所以需要切换窗口
                all_windows = self.browser.window_handles
                for window in all_windows:
                    if window != current_window:
                        self.browser.switch_to.window(window)

                # 寻找流程节点中产创办审核时间点
                # 切换到“流程跟踪”
                submit = waitForXpath(
                    self.browser,
                    "//div[@class=' ant-tabs-tab' and @role='tab' and contains(text(),'流程跟踪')]",  # 2是已办理tab页
                    timeout=self.timeout,
                )
                submit.click()
                # 寻找审批时间
                admit_time_ele = waitForXpath(
                    self.browser,
                    '//div[@class="ant-table-body"]//tbody[@class="ant-table-tbody"]//td[contains(text(),"产品管理委员会办公室意见")]/following-sibling::td[2]/span',
                    timeout=self.timeout,
                )
                admit_time = admit_time_ele.text
                admit_date = admit_time[:10]
                item["admit_date"] = admit_date
                item["weeks"] = get_weeks_current_date(admit_date)
                # 寻找审批人
                admit_person_ele = waitForXpath(
                    self.browser,
                    '//div[@class="ant-table-body"]//tbody[@class="ant-table-tbody"]//td[contains(text(),"产品管理委员会办公室意见")]/preceding-sibling::td[2]/span',
                    timeout=self.timeout,
                )
                admit_person = admit_person_ele.text
                item["admit_person"] = admit_person
                # 使用产创办审批时间来判断时间范围
                if not (
                    admit_date <= self.settings.get("data_end_date")
                    and admit_date >= self.settings.get("data_start_date")
                ):
                    self.browser.close()
                    self.browser.switch_to.window(current_window)
                    continue
                # 如果满足时间范围，切换回需求表单获取相关内容
                # 切换到“基本信息”
                submit = waitForXpath(
                    self.browser,
                    "//div[@class=' ant-tabs-tab' and @role='tab']/span[contains(text(),'基本信息')]",
                    timeout=self.timeout,
                )
                submit.click()
                body = self.browser.page_source
                url = self.browser.current_url
                response = HtmlResponse(
                    url=url,
                    body=body,
                    encoding="utf-8",
                    status=200,
                )
                self.parse_article(item, response)
                time.sleep(random.randint(3, 6))
                self.browser.close()
                self.browser.switch_to.window(current_window)
                # 存在作废的需求 demand_no为空，不为空的才获取
                # 根据提交日期判断停止继续,大于等于设定日期的才获取----换成上面的委员会审批日期来判断
                # 注意item不设置值的情况下报keyerror错误
                if (
                    item["demand_no"] == "None"
                ):  # or not (item["submit_date"] <= self.settings.get("data_end_date") and item["submit_date"] >= self.settings.get("data_start_date")):
                    continue
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
                    url=self.current_url,
                    meta=meta,
                    callback=self.parse,
                    dont_filter=True,
                )

    def parse_article(self, item, response):
        # item = response.meta["data"]
        # 获取文章的正文内容
        content = response.xpath('//table[@class="sd-form-theme sd-default"]')
        demand_no = content.xpath("./tr[2]/td[2]/span/text()").get()
        if demand_no is None:
            item["demand_no"] = "None"
        else:
            item["demand_no"] = content.xpath("./tr[2]/td[2]/span/text()").get().strip()
            item["submit_date"] = (
                content.xpath("./tr[2]/td[4]/span/text()").get().strip()
            )
            item["submitter"] = content.xpath("./tr[3]/td[2]/span/text()").get().strip()
            item["submit_depart"] = (
                content.xpath("./tr[4]/td[2]/span/text()").get().strip()
            )
            # 需求背景
            item["background"] = []
            backgrounds = content.xpath("./tr[8]/td[2]//text()").getall()
            for background in backgrounds:
                item["background"].append(background.strip())
            # 需求概述
            item["summary"] = []
            summarys = content.xpath("./tr[9]/td[2]//text()").getall()
            for summary in summarys:
                item["summary"].append(summary.strip())
            # 产品登记预审结果 准入 备案 不涉及
            item["admit_result"] = content.xpath("./tr[39]/td[2]//text()").get()
            # 产品分类
            item["pro_type"] = content.xpath("./tr[39]/td[4]//text()").get()

    # 使用selenium请求时，请求后的动作
    # 这个方法会在我们的下载器中间件返回Response之前被调用
    # 等待content内容加载成功后，再继续
    # 这样的话，我们就能在parse_content方法里应用选择器扣出#content了
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
            userid_input.send_keys(self.settings.get("userID"))
            password_input.clear()
            password_input.send_keys(self.settings.get("passwd"))
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
                "//div[@class='ant-tabs ant-tabs-top ant-tabs-line ant-tabs-no-animation sd-has-table']//div[@role='tab'][2]",  # 2是已办理tab页
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
            # 1、通过点击下一页按钮执行翻页
            next_page = waitForXpath(
                self.browser,
                "//div[@role='tabpanel' and @aria-hidden='false' and @class='ant-tabs-tabpane ant-tabs-tabpane-active']//li[@title='下一页']",
                timeout=5,
            )
            np = next_page.get_attribute("class")
            if np == "ant-pagination-disabled ant-pagination-next":
                request.meta.update({"page_num": -1})
            else:
                next_page.click()
            # 2、 通过输入页数点击并点击确定翻页
            # try:
            #     input = waitForXpath(
            #         self.browser,
            #         "//div[@role='tabpanel' and @aria-hidden='false' and @class='ant-tabs-tabpane ant-tabs-tabpane-active']//div[@class='ant-pagination-options-quick-jumper' and contains(text(),'跳至')]/input[@type='text']",
            #         timeout=5,
            #     )
            # except (TimeoutException,NoSuchElementException):
            #     request.meta.update({'page_num':-1})
            # else:#没异常正常处理
            #     input.clear()
            #     input.send_keys(page)
            #     self.browser.switch_to.active_element.send_keys(Keys.ENTER)
            # 切换到已处理
            submit = waitForXpath(
                self.browser,
                "//div[@class='ant-tabs ant-tabs-top ant-tabs-line ant-tabs-no-animation sd-has-table']//div[@role='tab'][2]",
                timeout=self.timeout,
            )
            submit.click()
            # 等待页面加载完标识出现
            waitForXpath(
                self.browser,
                f"//ul[@class='ant-pagination ant-table-pagination']",
                timeout=self.timeout,
            )
        # elif meta["purpose"] == "download":
        #     a = waitForXpath(
        #         self.browser, '//div[@id="files"]/a[1]', timeout=self.timeout
        #     )
        #     a.click()

    def closed(self, reason):
        # # 判断文件是否存在
        out_file = Path(self.out_file)
        if out_file.exists():
            # 重命名
            out_file.rename(self.out_file + "_finished")
        return super().closed(reason)
