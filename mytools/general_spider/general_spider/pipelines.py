import os
from sqlite3 import connect
from twisted.enterprise import adbapi
import json
from myutils.info_out_manager import dump_json_table


# 定义一个异步操作数据库的通用类
class TwistedPipeline(object):
    def __init__(self, db_path):
        self.dbpool = None
        self.db_path = db_path
        self.sqlite_table = None
        self.in_sql = None
        self.up_sql = None
        self.de_sql = None

    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get("SQLITE_DB_PATH")
        return cls(db_path)

    def open_spider(self, spider):
        # 定义数据库连接池
        self.dbpool = adbapi.ConnectionPool(
            "sqlite3", self.db_path, check_same_thread=False
        )

    def close_spider(self, spider):
        self.dbpool.close()

    def execute(self, item, spider, table_name, action="insert", primary=None):
        if action == "insert":
            defer = self.dbpool.runInteraction(self.insert_item, item, table_name)
        elif action == "update":
            defer = self.dbpool.runInteraction(
                self.update_item, item, table_name, primary=primary
            )
        elif action == "delete":
            defer = self.dbpool.runInteraction(
                self.delete_item, item, table_name, primary=primary
            )
        elif action == "deleteAinsert":
            defer = self.dbpool.runInteraction(
                self.deleteAinsert_item, item, table_name, primary=primary
            )
        defer.addErrback(self.handle_error, item, spider)

    def deleteAinsert_item(self, cursor, item, table_name, primary=None):
        cursor.execute("BEGIN")
        try:
            self.delete_item(cursor, item, table_name, primary)
            self.insert_item(cursor, item, table_name)
        except:
            cursor.execute("ROLLBACK")
            raise
        else:
            cursor.execute("COMMIT")

    def insert_item(self, cursor, item, table_name):
        if not self.in_sql:
            self.in_sql = f"insert into {table_name}({', '.join(item.keys())}) values ({', '.join(['?'] * len(item.keys()))})"

        values = tuple(
            "\\n".join(value) if isinstance(value, list) else value
            for value in item.values()
        )
        cursor.execute(self.in_sql, values)  # tuple(item.values()))

    def delete_item(self, cursor, item, table_name, primary=None):
        if not self.de_sql:
            self.de_sql = f"delete from {table_name} "
            if primary is not None:
                self.de_sql = f"{self.de_sql} where {primary} = ?"
        cursor.execute(self.de_sql, (item[primary],))  # tuple(item.values()))

    def update_item(self, cursor, item, table_name, primary=None):
        if not self.up_sql:
            self.up_sql = f"update {table_name} set ({', '.join(item.keys())}) = ({', '.join(['?'] * len(item.keys()))}) "
            if primary is not None:
                self.up_sql = f"{self.up_sql} where {primary} = '{item[primary]}'"
        values = tuple(
            "\\n".join(value) if isinstance(value, list) else value
            for value in item.values()
        )
        cursor.execute(self.up_sql, values)

    def handle_error(self, error, item, spider):
        print("=" * 15 + "error" + "=" * 15)
        print(error)
        print("=" * 15 + "error" + "=" * 15)


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


class CSRCMarketWeeklyPipeline(TwistedPipeline):
    def process_item(self, item, spider):
        # 1、存入数据库
        super().execute(
            item,
            spider,
            "csrc_market_weekly",
            action="deleteAinsert",
            primary="index_no",
        )
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
    def process_item(self, item, spider):
        # 1、存入数据库
        super().execute(
            item,
            spider,
            "pro_demand_admit_ledger",
            action="deleteAinsert",
            primary="demand_no",
        )
        # 2、接着导出为json
        dump_json_table(dict(item), spider.out_file)
        return item
