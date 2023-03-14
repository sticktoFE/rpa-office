# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter

# import pymysql
# from pymysql import cursors
from sqlite3 import connect
from twisted.enterprise import adbapi
import json

from myutils.info_out_manager import dump_json_table, get_temp_folder

# 进行数据处理


class JianShuPipeline(object):
    """
    这种方法只能同步进行保存到数据库
    """

    def __init__(self):
        # db_parames = {
        #     "host": "wslip",
        #     "port": 3306,
        #     "user": "root",
        #     "password": "root",
        #     "database": "ter",
        #     "charset": "utf8",
        # }
        # 连接数据库(原来是mysql,此处用sqlite3代替)
        # self.conn = pymysql.connect(**db_parames)
        # self.cursor = self.conn.cursor()

        self.conn = connect("dw/risk.db")
        # 获取游标、数据
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        print("this is CSRCPipeline")
        self.cursor.execute(
            self.sql,
            (
                item["title"],
                item["content"],
                item["author"],
                item["avatar"],
                item["pub_time"],
                item["article_id"],
                item["origin_url"],
            ),
        )
        # self.cursor.commit()
        print(item)
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            INSERT INTO article(id,title,content,author,avatar,pub_time,article_id,origin_url)
            VALUE(null,?,?,?,?,?,?,?)
            """
            return self._sql
        return self._sql


class JianShuTwistedPipeline(object):
    """
    使用Twisted进行异步保存到数据库
    """

    def __init__(self):
        self.conn = connect("dw/risk.db")
        # 获取游标、数据
        self.cursor = self.conn.cursor()
        self._sql = None
        # 定义数据库连接池
        self.dbpool = adbapi.ConnectionPool("pymysql", **db_parames)

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                INSERT INTO article(id,title,content,author,avatar,pub_time,article_id,origin_url,word_count)
                VALUE(null,?,?,?,?,?,?,?,?)
                """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        print("this is CSRCPipeline")
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)
        print(item)
        return item

    def insert_item(self, cursor, item):
        cursor.execute(
            self.sql,
            (
                item["title"],
                item["content"],
                item["author"],
                item["avatar"],
                item["pub_time"],
                item["article_id"],
                item["origin_url"],
                item["word_count"],
            ),
        )

    def handle_error(self, error, item, spider):
        print("=" * 15 + "error" + "=" * 15)
        print(error)
        print("=" * 15 + "error" + "=" * 15)


class FuZhouEcoIndexPipeline(object):
    def process_item(self, item, spider):
        print("this is CSRCPipeline")
        if item["name"] == "" or len(item["name"].replace("【】", "").strip()) == 0:
            return item
        cufolder = os.path.join(os.path.dirname(__file__), "FuZhou", "fuzhou.txt")
        # # 判断文件是否存在
        # if os.path.exists(cufolder):
        #     # 存在，则删除文件
        #     os.remove(cufolder)
        with open(cufolder, "a", encoding="utf-8") as fp:
            json.dump(
                dict(item),
                fp,
                ensure_ascii=False,
                # sort_keys=True,
                indent=2,
                separators=(",", ": "),
            )
            # 输出完换行
            fp.write("\n")
        return item


# 参考代码


class TaobaoPipeline(object):
    def process_item(self, item, spider):
        print("this is MongoPipeline")
        cufolder = os.path.join(os.path.dirname(__file__), "spiders", "ipad.txt")
        with open(cufolder, "a", encoding="utf-8") as fp:
            json.dump(
                dict(item),
                fp,
                ensure_ascii=False,
                # sort_keys=True,
                indent=2,
                separators=(",", ": "),
            )
            # 输出完换行
            fp.write("\n")
        return item


class CSRCPenaltyPipeline(object):
    def process_item(self, item, spider):
        with open(spider.out_file, "a", encoding="utf-8") as fp:
            json.dump(dict(item), fp, ensure_ascii=False)
            # 输出完换行
            fp.write("\n")
        return item


class TwistedPipeline(object):
    def __init__(self, table_name):
        # 定义数据库连接池
        self.dbpool = adbapi.ConnectionPool(
            "sqlite3", database="dw/risk.db", check_same_thread=False
        )
        self.sqlite_table = table_name
        self._sql = None

    def exeute(self, item, spider, action="insert"):
        if action == "insert":
            defer = self.dbpool.runInteraction(self.insert_item, item)
            defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item):
        self.insert_sql(item)
        values = tuple(
            "\\n".join(value) if isinstance(value, list) else value
            for value in item.values()
        )
        cursor.execute(self._sql, values)  # tuple(item.values()))

    def insert_sql(self, item):
        if not self._sql:
            self._sql = f"insert into {self.sqlite_table}({', '.join(item.keys())}) values ({', '.join(['?'] * len(item.keys()))})"
            return self._sql
        return self._sql

    def handle_error(self, error, item, spider):
        print("=" * 15 + "error" + "=" * 15)
        print(error)
        print("=" * 15 + "error" + "=" * 15)


class CSRCMarketWeeklyPipeline(TwistedPipeline):
    def __init__(self):
        super().__init__("csrc_market_weekly")

    def process_item(self, item, spider):
        # 1、存入数据库
        super().exeute(item, spider, action="insert")
        # 2、接着导出为json
        dump_json_table(dict(item), spider.out_file)
        return item


# 任务待办内容处理
class OAProAdmitToDoPipeline(object):
    def process_item(self, item, spider):
        dump_json_table(dict(item), spider.out_file)
        return item


# 任务已办内容处理
class OAProAdmitHaveDonePipeline(TwistedPipeline):
    def __init__(self):
        super().__init__("pro_demand_admit_ledger")

    def process_item(self, item, spider):
        # 1、存入数据库
        super().exeute(item, spider, action="insert")
        # 2、接着导出为json
        dump_json_table(dict(item), spider.out_file)
        return item
