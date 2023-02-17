import re
import sys
import scrapy
from mytools.general_spider.general_spider.items import FuZhouEcoIndexItem


class FuZhouEcoIndexSpider(scrapy.Spider):
    name = "fuzhou"
    allowed_domains = ["tjj.fuzhou.gov.cn"]
    start_urls = ["http://tjj.fuzhou.gov.cn/zz/zwgk/tjzl/jdsj/index.htm"]
    total_pages = 0

    def parse(self, response):
        # 第一次请求用的是start_urls的地址，可以获取总页数，同时也是分页第一页，所以在这里一并处理，后面的从第二页循环处理
        # 以后处理分页的都可以从第一页找总页数，并处理第一页，后面的页数找规律循环去download
        if self.total_pages == 0:
            self.get_total_pages(response)
            self.parse_list(response)
        # 处理从第二页开始的所有页面
        common_url = "http://tjj.fuzhou.gov.cn/zz/zwgk/tjzl/jdsj/"
        for i in range(1, int(self.total_pages)):
            url = f"{common_url}index_{i}.htm"
            # 3.封装请求  自己写一个parse的函数
            yield scrapy.Request(
                url=url,
                callback=self.parse_list,
                meta={"current_page": int(i + 1)},
                encoding="utf-8",
                dont_filter=True,
            )
    # 0、获取列表页的页数

    def get_total_pages(self, response):
        # 解析得到所有的 script 脚本内容
        path_html = response.xpath("//script/text()").getall()
        print(path_html)
        if len(path_html) == 0:
            print("无分页信息！")
            sys.exit(0)
        # 遍历找到含有分页信息的脚本片段
        for script in path_html:
            scrtipt = str(script)
            if "createPageHTML" in scrtipt:
                if resultMa := re.search(r"[(](\d+),.*", script):
                    self.total_pages = int(resultMa[1])
                    break
    # 单页的解析

    def parse_list(self, response):
        current_page = response.meta["current_page"]
        # 1.获取此页的列表信息
        penalty_info_list = response.xpath('//table[@class="tab_libox"]//tr')
        for penalty in penalty_info_list:
            # title = penalty.xpath('./td[@class="listy1e"]//a/text()').get()
            # detail_url = penalty.xpath('.//td[@class="listy1e"]//a/@href').get()
            # detail_url = response.urljoin(detail_url)
            # pub_date = penalty.xpath('.//td[@class="listy1e"]/../td[2]/a/text()').get()
            title = penalty.xpath("./td//a/text()").get()
            detail_url = penalty.xpath("./td//a/@href").get()
            detail_url = response.urljoin(detail_url)
            pub_date = penalty.xpath("./td/../td[2]/a/text()").get()
            # 2.实例化：
            item = FuZhouEcoIndexItem()
            # 3.赋值
            item["title"] = title
            item["pub_date"] = pub_date
            item["detail_url"] = detail_url
            item["current_page"] = current_page
            yield scrapy.Request(
                url=detail_url,
                callback=self.parse_detail,
                meta={"data": item},
                encoding="utf-8",
                dont_filter=True,
            )
    # 解析详情页

    def parse_detail(self, response):
        item = response.meta["data"]
        # print(response.url)
        ## 获取报告内容#
        # 获取table下面所有文本 返回值  ["table1_content","table2_content"]
        infos = response.xpath('//div[@id="docontcent"]//table')
        name = ""
        for info in infos:
            # info = re.sub(r"\xa0|\u3000|\s+|<span>.*</span>", "", str(info))
            tmp = info.xpath(".//text()").getall()
            if len(tmp) > 0:
                name = [re.sub(r"\xa0|\u3000|\s+", "", onetmp).strip()
                        for onetmp in tmp]
                name = "  ".join(name)
            if len(name) > 0:
                item["name"] = name
                print(item)
                yield item
