from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from mytools.general_spider.general_spider.items import JianshuItem


class JianshuSpider(CrawlSpider):
    name = "jianshu"
    allowed_domains = ["jianshu.com"]
    start_urls = ["https://www.jianshu.com/"]

    # 分析简书文章链接发现其链接地址结构为：域名 + /p/ + 12为数字字母组合字符串
    rules = (
        Rule(
            LinkExtractor(allow=r".*/p/[0-9a-z]{12}.*"),
            callback="parse_detail",
            follow=True,
        ),
    )

    def parse_detail(self, response):
        """
        进行爬取结果分析
        :param response:
        :return:
        """
        title = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/h1/text()'
        ).get()
        avatar = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/a/img/@src'
        ).get()
        author = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[1]/span/a/text()'
        ).get()
        pub_time = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/time/text()'
        ).get()
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split("/")[-1]
        content = response.xpath('//div[@class="show-content"]').get()

        word_count = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[2]/text()'
        ).get()
        comment_count = response.xpath(
            '//*[@id="note-page-comment"]/section/h3[last()]/div[1]/span[2]/text()'
        ).get()
        like_count = response.xpath(
            '//*[@id="__next"]/div[1]/div/div[1]/section[1]/div[3]/div[1]/div[1]/span/text()'
        ).get()
        read_count = response.xpath(
            '//*[@id="__next"]/div[1]/div/div/section[1]/div[1]/div/div/div[2]/span[3]/text()'
        ).get()
        subjects = ",".join(
            response.xpath(
                '//*[@id="__next"]/div[1]/div/div[1]/section[3]/div[1]/a//text()'
            ).getall()
        )

        item = JianshuItem(
            title=title,
            avatar=avatar,
            author=author,
            pub_time=pub_time,
            origin_url=url1,
            article_id=article_id,
            content=content,
            word_count=word_count,
            comment_count=comment_count,
            like_count=like_count,
            read_count=read_count,
            subjects=subjects,
        )
        yield item
