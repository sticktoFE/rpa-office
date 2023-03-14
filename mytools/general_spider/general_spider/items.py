# Define here the models for your scraped items
#
# See documentation in:
# https://docs.org/en/latest/topics/items.html

from scrapy import Item, Field


class JianshuItem(Item):
    """
    定义所需字段
    """

    title = Field()
    content = Field()
    article_id = Field()
    origin_url = Field()
    author = Field()
    avatar = Field()
    pub_time = Field()
    read_count = Field()
    like_count = Field()
    word_count = Field()
    subjects = Field()
    comment_count = Field()


class CSRCPenaltyItem(Item):
    """
    定义所需字段
    """

    index = Field()
    con_type = Field()
    pub_org = Field()
    pub_date = Field()
    title = Field()
    text_num = Field()
    content = Field()
    detail_url = Field()


class CSRCMarketWeeklyItem(Item):
    """
    定义所需字段
    """

    index_no = Field()
    title = Field()
    detail_url = Field()
    pub_date = Field()

    con_type = Field()
    pub_org = Field()
    text_num = Field()
    content = Field()
    attach_name = Field()
    attach_link = Field()
    attach_save_path = Field()


class OAProAdmitToDoItem(Item):
    """
    定义所需字段
    """

    demand_no = Field()
    title = Field()
    submitter = Field()
    submit_depart = Field()
    submit_date = Field()
    background = Field()
    summary = Field()
    admit_result = Field()
    pro_type = Field()
    attach_save_path = Field()
    relate_attach_save_path = Field()


class OAProAdmitHaveDoneItem(Item):
    """
    定义所需字段
    """

    demand_no = Field()
    title = Field()
    submitter = Field()
    submit_depart = Field()
    submit_date = Field()
    background = Field()
    summary = Field()
    pro_type = Field()
    admit_person = Field()
    admit_date = Field()
    admit_result = Field()
    weeks = Field()
    attach_save_path = Field()
    relate_attach_save_path = Field()
    handling_date = Field()


class FuZhouEcoIndexItem(Item):
    """
    定义所需字段
    """

    title = Field()
    pub_date = Field()
    detail_url = Field()
    y_m = Field()
    name = Field()
    current_page = Field()


class ProjectItem(Item):
    """
    定义所需字段
    """

    title = Field()
    org = Field()
    time = Field()
    content = Field()
