# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import scrapy


class JianshuItem(scrapy.Item):
    """
    定义所需字段
    """

    title = scrapy.Field()
    content = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    author = scrapy.Field()
    avatar = scrapy.Field()
    pub_time = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    word_count = scrapy.Field()
    subjects = scrapy.Field()
    comment_count = scrapy.Field()


class CSRCItem(scrapy.Item):
    """
    定义所需字段
    """

    index = scrapy.Field()
    con_type = scrapy.Field()
    pub_org = scrapy.Field()
    pub_date = scrapy.Field()
    title = scrapy.Field()
    text_num = scrapy.Field()
    content = scrapy.Field()
    detail_url = scrapy.Field()


class FuZhouEcoIndexItem(scrapy.Item):
    """
    定义所需字段
    """

    title = scrapy.Field()
    pub_date = scrapy.Field()
    detail_url = scrapy.Field()
    y_m = scrapy.Field()
    name = scrapy.Field()
    current_page = scrapy.Field()


class ProjectItem(scrapy.Item):
    """
    定义所需字段
    """
    title = scrapy.Field()
    org = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
