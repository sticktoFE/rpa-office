# 添加环境变量
# sys.path.append(dirpath)
# 一、待办任务处理
from pathlib import Path
import random
import time
from mytools.general_spider.SpiderManager import run_spiders
from myutils.GeneralThread import Worker
from myutils.info_out_manager import ReadWriteConfFile, get_temp_folder, load_json_table
from biz.monitor_oa.zy_email import SeleMail
from biz.monitor_oa.tx_doc import TXDocument
from biz.monitor_oa.wc_sendinfo import send_webchat
from PySide6.QtCore import QThreadPool
from myutils.GeneralThread import Worker
from multiprocessing import Process, Queue


# 获取数据形成文件
class RPAClient:
    # 1、启动信息获取，获取列表信息和详情信息
    def __init__(
        self,
        scrapy_userID=None,
        scrapy_passwd=None,
        mail_userID=None,
        mail_passwd=None,
        data_start_date=None,
        data_end_date=None,
    ):
        self.scrapy_userID = scrapy_userID
        self.scrapy_passwd = scrapy_passwd
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd
        self.data_start_date = data_start_date
        self.data_end_date = data_end_date
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=True
        )
        self.out_file = f"{self.out_folder}/csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"

    def start_spider(self, spider_name):
        q = Queue()
        p = Process(
            target=run_spiders,
            args=(
                q,
                spider_name,
                self.scrapy_userID,
                self.scrapy_passwd,
                self.data_start_date,
                self.data_end_date,
            ),
            kwargs={
                "out_file": self.out_file,
                "down_path": self.out_folder,
            },
        )
        p.start()
        result = q.get()
        p.join()
        if result is not None:
            raise result
        else:
            return True

    # 客户端待办、已办任务处理
    # 爬取信息
    def scrapy_info(self):
        # 1、启动信息获取，获取详情信息，生成台账更新文件（已经是子线程模式了）
        # self.scraper = SpiderManager(
        #     self.scrapy_userID,
        #     self.scrapy_passwd,
        #     out_file=self.out_file,
        #     down_path=self.out_folder,
        # )
        # self.scraper.run_spiders(
        #     "csrc_market_weekly"
        # )  # csrc_market_weekly OAProAdmitHaveDone
        # # self.scraper.spider_finished.connect()
        # 2、由上面的直接调用改成下面的启动进程方式
        # 从配置文本中获取要执行的爬虫
        spider_name = ReadWriteConfFile.getSectionValue("General", "spider_name")
        return self.start_spider(spider_name)

    # 上传附件
    def upload_file_to_mail(self):
        # 2、获取台账更新文件并上传到邮件（开启子线程）
        while not Path(self.out_finished).exists():
            time.sleep(0.5)
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.upload_through_draft(get_file=self.out_finished)

    # 把需求说明书发给相关人
    def notify_attache(self):
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        item_generator = load_json_table(self.out_finished)
        self.sm.send_mails(item_generator)

    def have_done(self):
        re = self.scrapy_info()
        if re:
            # self.rpacli = RPAClient(userID_oa, password_oa, userID, password)
            # self.rpacli.scrapy_info()
            # # 启动上传功能
            # self.rpacli.scraper.spider_finished.connect(self.after_scrapy)
            # worK_server = Worker(self.rpacli.scrapy_info)
            self.upload_file_to_mail()


# 服务端接收数据并进行相应处理，如更新文档，统计分析等
class RPAServer:
    def __init__(self, mail_userID, mail_passwd):
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=False
        )
        self.out_file = f"{self.out_folder}\\csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"

    # 已办任务处理
    # server端
    # 1、登陆邮件并下载台账更新文件，然后更新到腾讯文档台账
    def start(self):
        # 下载json结构化信息
        # self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        # self.sm.download_through_draft()
        # 更新腾讯文档给台账
        txd = TXDocument(self.mail_userID, self.mail_passwd, self.out_finished)
        txd.modify_up()
        # 发信息通知管理人员今天的任务处理完毕
        # send_webchat()


def start_ip_proxy():
    worker_schedule = Worker("schedule", module="mytools.proxy_pool.proxyPool")
    QThreadPool.globalInstance().start(worker_schedule)
    # 等一下再启动服务
    time.sleep(random.randint(1, 3))
    worker_server = Worker("server", module="mytools.proxy_pool.proxyPool")
    QThreadPool.globalInstance().start(worker_server)
    time.sleep(random.randint(1, 3))


# if __name__ == "__main__":
# client = RPAClient(mail_userID="", mail_passwd="")
# client.have_done()

client = RPAServer("", "")
client.start()
