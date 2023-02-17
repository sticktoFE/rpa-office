import re
import shutil
from pathlib import Path
import subprocess
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 1、获取driver，用本地浏览器，据说可以有效反反爬


def get_driver_Chromeexe():
    # 此处 Chrome 的路径需要修改为你本机的 Chrome 安装位置
    # --remote-debugging-port 指定任何打开的端口
    # --user-data-dir,形式C:\xxxxx\AutomationProfile中xxxxx建议设置为selenium_text  selenium_taobao  selenium_kanzhun这样的格式
    # 不同的就是可以开启不同的账号，如果都用这个位置，可能会发现哪怕用不同的端口，但是程序只会第一个调用的成功。
    # 所以：不同的端口做不同的事情，用不同的文件夹位置放账户配置信息。哪怕这次窗口关闭了，
    # 你下次调用这个窗口打开一样的页面，只要不到cookie失效时间，你登录的信息都还是存在的。
    chrome_path = r'"C:\Program Files\Google\Chrome\Application\chrome.exe " --remote-debugging-port=19222 --user-data-dir="d:\temp\selenum_zy\AutomationProfile"'
    completedProcess = subprocess.Popen(  # run是同步
        chrome_path,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if completedProcess.poll() is None:  # 表示子进程还在运行
        # options = Options()
        options = webdriver.ChromeOptions()
        # 千万别用这个，否则，很多信息无法保存，每次重新登陆网站都是全新
        # 无法做到比如 下次登录不用再验证短信验证码之类 ，费了老大劲试出来的
        # options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # 这里的信息是附加信息，可以不设置，但是推荐设置
        # 此处端口需要与上一步中使用的端口保持一致
        # 其它大多博客此处使用 127.0.0.1:9222, 经测试无法连接, 建议采用 localhost:9222
        # 具体原因参见: https://www.codenong.com/6827310/
        options.add_experimental_option("debuggerAddress", "localhost:19222")
        # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
        return webdriver.Chrome(
            executable_path="chromedriver110.exe", options=options
        )
        # return webdriver.Chrome(
        #     service=Service(ChromeDriverManager().install()), options=options
        # )

    else:
        print(f"子进程结束：{completedProcess.stderr}")


# 2、获取driver，通过驱动程序
def get_driver_ChromeDriver():
    options = webdriver.ChromeOptions()
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium#禁止打印日志
    # 访问https的网站，Selenium可能会报错，使用ignore-certificate-errors可以忽略报错
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "ignore-certificate-errors"]
    )
    options.add_experimental_option("useAutomationExtension", False)
    # 上面的针对chrome79后续版本无效，所以用下面两行来规避反爬
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")  # 禁用“chrome正受到自动测试软件的控制”提示
    options.add_argument(
        "log-level=3"
    )  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_argument("--window-size=1920,1080")  # 使用无头模式，需设置初始窗口大小
    options.add_argument("--no-first-run")  # 不打开首页
    options.add_argument("--no-default-browser-check")  # 不检查默认浏览器
    options.add_argument("--start-maximized")  # 最大化
    # options.add_argument("--headless")  # 无头模式--静默运行 不提供可视化页面
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    # 针对UA请求头的操作，防止因为没有添加请求头导致的访问被栏截了
    options.add_argument(
        "User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) >AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57"
    )
    # 这两行会清理cookie,影响登录默认设置失效，导致每次登录都是全新的，比如短信验证码要重复登录
    # 不要轻易打开
    # options.add_argument("--incognito")  # 无痕隐身模式
    # options.add_argument("--no-sandbox")
    # 浏览器地址栏访问chrome://version/查看个人资料路径,去掉最后的/Default
    # cookie等浏览器默认参数保存路径
    options.add_argument(
        "user-data-dir=d:\\temp\\selenum_zy\\AutomationProfile")
    # 不加载图片, 提升速度 不知为什么，打开后导致checkbox显示不出来
    # options.add_argument("blink-settings=imagesEnabled=false")
    # 配置下载文件的保存目录
    prefs = {"download.default_directory": "D:\\转型\\downloads"}
    options.add_experimental_option("prefs", prefs)
    # 初始化web驱动
    driver = webdriver.Chrome(
        executable_path="chromedriver110.exe", chrome_options=options
    )
    # driver = webdriver.Chrome(
    #     service=Service(ChromeDriverManager().install()), options=options
    # )
    # 修改 webdriver 值，为了反反爬
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        },
    )
    # 隐私等待，整体等待元素出现最长时间暂时设置为10s,selenium.dev上说 显示等待和隐式等待不要同时使用
    driver.implicitly_wait(15)
    return driver
