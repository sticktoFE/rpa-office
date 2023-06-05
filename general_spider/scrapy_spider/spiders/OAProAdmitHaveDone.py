import random
import time
import scrapy
from scrapy.http import HtmlResponse
from general_spider.scrapy_spider.items import OAProAdmitHaveDoneItem
from general_spider.utils.SeleniumSpider import (
    SeleniumSpider,
)
from general_spider.utils.tools import (
    waitForXpath,
    waitNotForXpath,
)
from pathlib import Path
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException,
)

from myutils.DateAndTime import get_weeks_current_date
from myutils.info_out_manager import ReadWriteConfFile


class OAProAdmitHaveDoneSpider(SeleniumSpider):
    name = "OAProAdmitHaveDone"
    start_url = "http://oa.zybank.com.cn/#/sd-frame/sd-mytodolist"
    # 制定专属pipeline
    custom_settings = {
        "ITEM_PIPELINES": {
            "general_spider.scrapy_spider.pipelines.OAProAdmitHaveDonePipeline": 300
        }
    }
    """
        start_requests parse parse_detail三个标配方法
        如果整体需要selenuim，那么就需要重写start_requests方法
        在parse中，翻页questCurrentLink设为False，始终基于当前页的情况下翻页
        在打开详情页时，视列表中能否获取详情链接来区别对待，存在的无需selenium
        不存在则需要调动selenium，并存在切换窗口的情况，类似本模块的实现
    """

    def start_requests(self):
        meta = {
            "useSelenium": True,
            "loadRequestUrl": True,
            "dont_redirect": False,
            "purpose": "login",
            "page_num": 1,
        }
        # 列表页是动态的，所以需要启用selenium
        yield scrapy.Request(
            self.start_url, meta=meta, callback=self.parse, dont_filter=True
        )

    # 解析列表数据
    def parse(self, response):
        meta = response.meta
        # -1表示没有下一页了
        if meta["page_num"] != -1:
            self.current_url = response.url
            # 获取当前页面中的文章列表
            articles = response.xpath(
                '//div[@role="tabpanel" and @aria-hidden="false" and @class="ant-tabs-tabpane ant-tabs-tabpane-active"]//tbody[@class="ant-table-tbody"]/tr[@class="ant-table-row ant-table-row-level-0"]'
            )
            for article in articles:
                time.sleep(random.uniform(2.6, 5.5))
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
                time.sleep(random.uniform(1.6, 3.8))
                # 0、切换到打开浏览器新tab窗口
                all_windows = self.browser.window_handles
                for window in all_windows:
                    if window != current_window:
                        self.browser.switch_to.window(window)

                # 1、切换到“流程跟踪” 寻找流程节点中产创办审核时间点
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
                item["weeks"] = get_weeks_current_date(admit_date)[2]
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
                # 2、切换到“基本信息”，如果满足时间范围，切换回需求表单获取相关内容
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
            # 翻页(所有爬虫标配)
            meta["page_num"] += 1
            max_page = ReadWriteConfFile.getSectionValue(
                "General", "max_page", type="int"
            )
            if meta["page_num"] <= max_page:
                meta.update(
                    {
                        "useSelenium": True,
                        "loadRequestUrl": False,
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

    # 解析详情页
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
            backgrounds = content.xpath(
                ".//label[@title='需求背景及必要性分析']/../following-sibling::td[1]//text()"
            ).getall()
            for background in backgrounds:
                item["background"].append(background.strip())
            # 需求概述
            item["summary"] = []
            summarys = content.xpath(
                ".//label[@title='需求概述']/../following-sibling::td[1]//text()"
            ).getall()
            for summary in summarys:
                item["summary"].append(summary.strip())
            # 产品登记预审结果 准入 备案 不涉及
            item["admit_result"] = content.xpath(
                ".//label[@title='产品登记预审']/../following-sibling::td[1]//text()"
            ).get()
            # 产品分类
            item["pro_type"] = content.xpath(
                ".//label[@title='产品分类']/../following-sibling::td[1]//text()"
            ).get()

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
            # 等待待处理出现
            waitForXpath(
                self.browser,
                "//div[@class='ant-tabs-tab-active ant-tabs-tab' and @role='tab' and contains(text(),'待处理')]",
                timeout=self.timeout,
            )
            # 切换到已处理或已办结
            # which_tab = ReadWriteConfFile.getSectionValue("Client", "which_tab")
            which_tab = self.settings.get("which_tab")
            submit = waitForXpath(
                self.browser,
                f"//div[@class=' ant-tabs-tab' and @role='tab' and contains(text(),'{which_tab}')]",  # 已处理或已办结tab页
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
            # 等待页面加载完标识出现，即等待覆盖上面的元素消失
            waitNotForXpath(
                self.browser,
                "//div[@class='ant-spin ant-spin-spinning']",
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
