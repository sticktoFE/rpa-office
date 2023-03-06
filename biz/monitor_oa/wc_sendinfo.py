import sys
from PySide6.QtWidgets import (
    QApplication,
)

from biz.monitor_oa.AppActionExecThread import AppExec


def send_webchat():
    for_pics = [
        "biz/monitor_oa/image/search.png",
        "biz/monitor_oa/image/selectfile.png",
        "biz/monitor_oa/image/send.png",
    ]
    ae = AppExec(class_name="WeChatMainWndForPC", window_name="微信", for_pics=for_pics)
    # self.ae.setFileNames(name_list)
    # self.ae.signal.connect(self.ocrResult)
    ae.start()


if __name__ == "__main__":
    send_webchat()
