# 添加环境变量
# sys.path.append(dirpath)
import os
from biz.monitor_oa.zy_mail import SeleMail
from biz.monitor_oa.zy_txdoc import TXDocument, write_qqdoc
from biz.monitor_oa.zy_sendinfo import send_webchat
from myutils.info_out_manager import get_temp_folder


class RPAServer:
    def __init__(self):
        self.out_folder = get_temp_folder(
            des_folder_name="spiders_out", is_clear_folder=True
        )
        self.out_file = f"{self.out_folder}\\csrc_market_weekly.txt"
        self.out_finished = self.out_file + "_finished"

    # 一、待办任务处理
    def to_do(self):
        # 1、下载文件获取列表信息和详情信息结束后并新增到腾讯文档台账
        # # 判断文件是否存在,存在，则删除文件
        if os.path.exists(self.out_finished):
            os.remove(self.out_finished)
        self.sm = SeleMail(self.out_folder)
        self.sm.download_through_draft()
        write_qqdoc(self.out_finished)
        # 2、发信息通知相关人登陆邮件查看需求说明书并更新腾讯文档
        send_webchat()

    # 二、已办任务处理
    # server端
    # 1、登陆邮件并下载台账更新文件，然后更新到腾讯文档台账
    def have_done(self):
        # 下载json结构化信息
        if os.path.exists(self.out_finished):
            os.remove(self.out_finished)
        self.sm = SeleMail(self.out_folder)
        self.sm.download_through_draft()
        # 更新腾讯文档给台账
        txd = TXDocument()
        txd.modify(self.out_finished)
        # 发信息通知管理人员今天的任务处理完毕
        send_webchat()


if __name__ == "__main__":
    client = RPAServer()
    client.to_do()
