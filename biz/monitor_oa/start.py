# 添加环境变量
# sys.path.append(dirpath)
# 一、待办任务处理
from biz.monitor_oa.client import RPAClient
from biz.monitor_oa.server import RPAServer


client = RPAClient()
client.to_do()

# server = RPAServer()
# server.to_do()
