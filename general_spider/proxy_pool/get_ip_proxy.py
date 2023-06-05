import random
import time
import requests
import json

# 解决 Max retries exceeded with url: http://www.baidu.com/问题
requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
req = requests.session()
req.keep_alive = False  # 关闭多余连接


# 随机ip代理获取
def get_random_proxy5010():
    proxy = None
    # 尝试100次，如果获取不到ip代理就用主机IP
    retry_time = 100
    try:
        while retry_time > 0:
            response = requests.get("http://localhost:5010/get/")
            if response.status_code == 200:
                proxy_body = json.loads(response.text).get("proxy")
                if proxy_body is None:
                    retry_time = retry_time - 1
                    continue
                # 格式化ip:port
                proxy = "{}".format(proxy_body)
                print("get proxy ...".join(proxy))
                # 用百度做个验证
                verifyBD = False
                if verifyBD:
                    r = requests.get(
                        "http://www.baidu.com",
                        proxies={
                            "http": "http://" + proxy,
                            "https": "https://" + proxy,
                        },
                        timeout=5,
                    )
                    if r.status_code == 200:
                        return proxy
                else:
                    print("-----------------")
                    print(retry_time)
                    return proxy
        return proxy
    except requests.exceptions.ConnectionError as e:
        # 视为不使用代理
        print("server not started：", e.args)
        return None
    except requests.exceptions.RequestException as e:
        print("Exception，get proxy again：", e.args)
        return get_random_proxy5010()


if __name__ == "__main__":
    print(get_random_proxy5010())
