# 添加环境变量
# sys.path.append(dirpath)
# 一、待办任务处理
from pathlib import Path
import random
import time
from general_spider.scrapy_start import go_scrapy
from myutils.GeneralQThread import Worker
from myutils.info_out_manager import get_temp_folder
from biz.monitor_oa.zy_email import SeleMail
from biz.monitor_oa.tx_doc import TXDocument
from PySide6.QtCore import QThreadPool
from biz.monitor_oa.wc_sendinfo import send_webchat


# 获取数据形成文件
class RPAClient:
    # 1、启动信息获取，获取列表信息和详情信息
    def __init__(
        self, scrapy_info=None, mail_userID=None, mail_passwd=None, out_folder=None
    ):
        self.scrapy_info = scrapy_info
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd
        self.out_folder = out_folder

    # 上传附件
    def upload_file_to_mail(self):
        # 2、获取台账更新文件并上传到邮件（开启子线程）
        # 改成判断文件夹下是否有 后缀为'_finished'的文件
        while not list(Path(self.out_folder).glob("*_finished")):
            time.sleep(0.5)
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.upload_through_draft()

    # 把需求说明书发给相关人
    def notify_attache(self):
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.send_mails()

    def have_done(self):
        re = go_scrapy(self.scrapy_info)
        if re:
            self.upload_file_to_mail()


# 服务端接收数据并进行相应处理，如更新文档，统计分析等
class RPAServer:
    def __init__(self, mail_userID, mail_passwd, out_folder=None):
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd
        self.out_folder = out_folder

    # 已办任务处理
    # server端
    # 1、登陆邮件并下载台账更新文件，然后更新到腾讯文档台账
    def start(self):
        # 下载json结构化信息
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.download_through_draft()
        # 更新腾讯文档给台账
        txd = TXDocument(self.mail_userID, self.mail_passwd)
        txd.modify_up(self.out_folder)
        # 发信息通知管理人员今天的任务处理完毕
        # send_webchat()


def start_ip_proxy():
    worker_schedule = Worker("schedule", module="general_spider.proxy_pool.proxyPool")
    QThreadPool.globalInstance().start(worker_schedule)
    # 等一下再启动服务
    time.sleep(random.randint(1, 3))
    worker_server = Worker("server", module="general_spider.proxy_pool.proxyPool")
    QThreadPool.globalInstance().start(worker_server)
    time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    # client = RPAClient(mail_userID="", mail_passwd="")
    # client.have_done()
    client = RPAServer("", "")
    client.start()
