# 添加环境变量
# sys.path.append(dirpath)

# 1、启动信息获取
from biz.monitor_oa.zy_mail import uploadOrDownload_through_draft
from mytools.general_spider.run_spider import Scraper
scraper = Scraper()
scraper.start_ip_proxy()
scraper.run_spiders()
# 2、获取信息结束后，上传邮件
uploadOrDownload_through_draft(type=0)

# 2、获取信息结束后，下载邮件
uploadOrDownload_through_draft(type=1)
