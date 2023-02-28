# 添加环境变量
# sys.path.append(dirpath)
# 一、待办任务处理
from pathlib import Path
import time
from biz.monitor_oa.zy_mail import SeleMail
from mytools.general_spider.start_spider import Scraper
from mytools.general_spider.general_spider.spiders.OAProAdmitToDo import OAProAdmitToDoSpider
from mytools.general_spider.general_spider.spiders.OAProAdmitHaveDone import OAProAdmitHaveDoneSpider
from myutils.info_out_manager import get_temp_folder


class RPAClient:
    # 1、启动信息获取，获取列表信息和详情信息
    def __init__(self):
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=True
        )
        self.out_file = f"{self.out_folder}/csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"

    # 待办
    def to_do(self):
        # 1）生成结构化的json文件，并下载表单中附件到相应目录
        self.scraper = Scraper(
            OAProAdmitToDoSpider, out_file=self.out_file, down_path=self.out_folder
        )
        self.scraper.run_spiders(start_proxy=False)
        # 2、把发送需求文档邮件给相关人，同时上传台账更新文件
        # 上传附件到草稿箱
        while not Path(self.out_finished).exists():
            time.sleep(1)
        # 把json文件上传到邮件
        self.sm = SeleMail(self.out_folder)
        self.sm.upload_through_draft(get_file=self.out_finished)
        # 把需求说明书发给相关人
        # self.sm = SeleMail(self.out_folder)
        # item_generator = load_json_table(self.out_finished)
        # self.sm.send_mails(item_generator)
    # 二、已办任务处理
    def have_done(self):
        # 1、启动信息获取，获取详情信息，生成台账更新文件
        self.scraper = Scraper(
            OAProAdmitHaveDoneSpider, out_file=self.out_file, down_path=self.out_folder
        )
        self.scraper.run_spiders(start_proxy=False)
        while not Path(self.out_finished).exists():
            time.sleep(1)
        # 2、获取台账更新文件并上传到邮件
        self.sm = SeleMail(self.out_folder)
        self.sm.upload_through_draft(get_file=self.out_finished)


if __name__ == "__main__":
    client = RPAClient()
    client.have_done()
