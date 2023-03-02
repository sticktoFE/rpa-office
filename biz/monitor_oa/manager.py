# 添加环境变量
# sys.path.append(dirpath)
# 一、待办任务处理
from pathlib import Path
import time, os
from mytools.general_spider.start_spider import Scraper
from mytools.general_spider.general_spider.spiders.OAProAdmitToDo import (
    OAProAdmitToDoSpider,
)
from mytools.general_spider.general_spider.spiders.OAProAdmitHaveDone import (
    OAProAdmitHaveDoneSpider,
)
from myutils.info_out_manager import get_temp_folder
from biz.monitor_oa.mail import SeleMail
from biz.monitor_oa.txdoc import TXDocument
from biz.monitor_oa.sendinfo import send_webchat


# 获取数据形成文件
class RPAClient:
    # 1、启动信息获取，获取列表信息和详情信息
    def __init__(self, mail_userID, mail_passwd):
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=True
        )
        self.out_file = f"{self.out_folder}/csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"

    # 待办
    def to_do(self):
        # 1）生成结构化的json文件，并下载表单中附件到相应目录
        self.scraper = Scraper(
            OAProAdmitToDoSpider,
            self.mail_userID,
            self.mail_passwd,
            out_file=self.out_file,
            down_path=self.out_folder,
        )
        self.scraper.run_spiders(start_proxy=False)
        # 2、把发送需求文档邮件给相关人，同时上传台账更新文件
        # 上传附件到草稿箱
        while not Path(self.out_finished).exists():
            time.sleep(1)
        # 把json文件上传到邮件
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.upload_through_draft(get_file=self.out_finished)
        # 把需求说明书发给相关人
        # self.sm = SeleMail(self.out_folder)
        # item_generator = load_json_table(self.out_finished)
        # self.sm.send_mails(item_generator)

    # 二、已办任务处理
    def have_done(self):
        # 1、启动信息获取，获取详情信息，生成台账更新文件
        self.scraper = Scraper(
            OAProAdmitHaveDoneSpider,
            self.mail_userID,
            self.mail_passwd,
            out_file=self.out_file,
            down_path=self.out_folder,
        )
        self.scraper.run_spiders(start_proxy=False)
        while not Path(self.out_finished).exists():
            time.sleep(1)
        # 2、获取台账更新文件并上传到邮件
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.upload_through_draft(get_file=self.out_finished)


# 服务端接收数据并进行相应处理，如更新文档，统计分析等
class RPAServer:
    def __init__(self, mail_userID, mail_passwd):
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=True
        )
        self.out_file = f"{self.out_folder}\\csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"
        self.mail_userID = mail_userID
        self.mail_passwd = mail_passwd

    # 一、待办任务处理
    def to_do(self):
        # 1、下载文件获取列表信息和详情信息结束后并新增到腾讯文档台账
        # # 判断文件是否存在,存在，则删除文件
        if os.path.exists(self.out_finished):
            os.remove(self.out_finished)
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.download_through_draft()
        self.td = TXDocument(self.mail_userID, self.mail_passwd, self.out_finished)
        self.td.write_content()
        # 2、发信息通知相关人登陆邮件查看需求说明书并更新腾讯文档
        send_webchat()

    # 二、已办任务处理
    # server端
    # 1、登陆邮件并下载台账更新文件，然后更新到腾讯文档台账
    def have_done(self):
        # 下载json结构化信息
        if os.path.exists(self.out_finished):
            os.remove(self.out_finished)
        self.sm = SeleMail(self.mail_userID, self.mail_passwd, self.out_folder)
        self.sm.download_through_draft()
        # 更新腾讯文档给台账
        txd = TXDocument(self.mail_userID, self.mail_passwd, self.out_finished)
        txd.modify()
        # 发信息通知管理人员今天的任务处理完毕
        # send_webchat()


if __name__ == "__main__":
    # client = RPAClient()
    # client.have_done()

    client = RPAServer()
    client.have_done()
