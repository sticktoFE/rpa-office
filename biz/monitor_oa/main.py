from PySide6.QtCore import (
    QThreadPool,
    QSettings,
)
from myutils.GeneralThread import Worker
import argparse

# 创建参数解析器
parser = argparse.ArgumentParser(description="命令行参数程序")

# 添加命令行参数
parser.add_argument(
    "-p", "--package", type=str, help="类名:RPAServer RPAClient", required=True
)
parser.add_argument(
    "-m", "--method", type=str, help="类方法名:to_do have_done", required=True
)
# 解析命令行参数
args = parser.parse_args()

path_ = "biz.monitor_oa.manager"
package_ = args.package
method_ = args.method
# 默认保存登录信息，快捷开始
settings = QSettings("./config.ini", QSettings.Format.IniFormat)
userID = settings.value("userID")
password = settings.value("password")
worker_server = Worker(
    package_,
    classMethod=method_,
    module=path_,
    mail_userID=userID,
    mail_passwd=password,
)
QThreadPool.globalInstance().start(worker_server)
