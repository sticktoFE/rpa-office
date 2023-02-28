"""
整合selenium的爬虫示例
"""
import os
import random
import time
from mytools.general_spider.general_spider.extendsion.SeleniumSpider import SeleniumSpider
from mytools.general_spider.general_spider.extendsion.tools import waitForXpath
import scrapy
from mytools.general_spider.general_spider.items import ProjectItem
from pathlib import Path

from myutils.info_out_manager import get_temp_folder
# 这个爬虫类继承了SeleniumSpider
# 在爬虫跑起来的时候，将启动一个浏览器


class PingDingGovSpider(SeleniumSpider):
    """
    这一网站，他的列表页是静态的，但是内容页是动态的
    所以，用selenium试一下，目标是扣出内容页的#content
    """
    name = 'ping_ding_gov_tender'
    allowed_domains = ['pingdingshan.hngp.gov.cn']
    url_format = 'http://pingdingshan.hngp.gov.cn/pingdingshan/ggcx?soCode=af4f57d4bc2a4dd2a7ce7f2361275d9a'
    out_folder = get_temp_folder(
        des_folder_name='spiders_out', is_clear_folder=True)
    out_file = f"{out_folder}/PingDingGov.txt"
    out_finished = f"{out_folder}/PingDingGov_finished.txt"

    def start_requests(self):
        """
        开始发起请求，记录页码
        """
        page_num = 1
        start_url = f'{self.url_format}'  # {page_num}
        meta = dict(page_num=1)
        # 列表页是静态的，所以不需要启用selenium，用普通的scrapy.Request就可以了
        yield scrapy.Request(start_url, meta=meta, callback=self.parse)

    def parse(self, response):
        self.current_url = response.url
        """
        从列表页解析出正文的url
        """
        meta = response.meta
        all_li = response.css("div.List2>ul>li")
        # 列表
        for li in all_li:
            content_href = li.xpath('./a/@href').extract()[0]
            content_url = response.urljoin(content_href)
            # 内容页是动态的，#content是ajax动态加载的，所以启用一波selenium
            meta.update(
                {'usedSelenium': True, 'dont_redirect': True, 'purpose': 'content'})
            # 增加随机请求，防止频繁
            time.sleep(random.uniform(0.1, 2))
            yield scrapy.Request(url=content_url, meta=meta, callback=self.parse_content, encoding='utf-8')
        # 翻页
        # if meta['page_num'] < 2:
        #     meta['page_num'] += 1
        #     meta.update(
        #         {'usedSelenium': False, 'dont_redirect': True})
        #     next_url = f'{self.url_format}{meta["page_num"]}'
        #     # 列表页是静态的，所以不需要启用selenium，用普通的scrapy.Request就可以了
        #     yield scrapy.Request(url=next_url, meta=meta, callback=self.parse)
        # 翻页直接点击next
        if meta['page_num'] < 2:
            meta['page_num'] += 1
            meta.update(
                {'usedSelenium': True, 'dont_redirect': True, 'purpose': 'next'})
            yield scrapy.Request(url=self.current_url, meta=meta, callback=self.parse, dont_filter=True)

    def parse_content(self, response):
        """
        解析正文内容
        """
        item = ProjectItem()
        main_content = response.xpath('//*[@id="print-content"]')
        item['title'] = ''.join(main_content.xpath(
            './h1/text()').get()).strip()
        item['org'] = ''.join(main_content.xpath(
            './div[1]/span[1]/text()').get()).strip()
        item['time'] = ''.join(main_content.xpath(
            './div[1]/span[2]/text()').get()).strip()
        # 输出txt换行需要用 \r\n
        item['content'] = '\r\n'.join(main_content.xpath(
            './div[@class="Content"]//tr//text()').getall()).strip()
        yield item
        # for item in items:
        #     item['price'] = '\n'.join(item.xpath('.//text()').getall()).strip()
        #     yield item

    def selenium_func(self, request):
        meta = request.meta
        if meta['purpose'] == 'content':
            # 这个方法会在我们的下载器中间件返回Response之前被调用
            # 等待content内容加载成功后，再继续
            # 这样的话，我们就能在parse_content方法里应用选择器扣出#content了
            waitForXpath(self.browser, "//*[@id='content']/*[1]")
        elif meta['purpose'] == 'next':
            # 这个方法会在我们的下载器中间件返回Response之前被调用
            # 等待content内容加载成功后，再继续
            # 这样的话，我们就能在parse_content方法里应用选择器扣出#content了

            # if page > 1:
            a = waitForXpath(self.browser, "//li[@class='nextPage']/*[1]")
            # submit = self.wait.until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, '#mainsrp-pager div.form> span.btn.J_Submit')))
            # input.clear()
            # input.send_keys(page)
            a.click()
        elif meta['purpose'] == 'search':
            a = waitForXpath(self.browser, "//li[@class='nextPage']/*[1]")
            # submit = self.wait.until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, '#mainsrp-pager div.form> span.btn.J_Submit')))
            # input.clear()
            # input.send_keys(page)
            a.click()

    def closed(self, reason):
        # # 判断文件是否存在
        out_file = Path(self.out_file)
        if out_file.exists():
            # 重命名
            out_file.rename(self.out_finished)
        return super().closed(reason)
