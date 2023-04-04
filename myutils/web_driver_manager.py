from pathlib import Path
import random
import subprocess
from selenium import webdriver

from myutils.info_out_manager import ReadWriteConfFile, get_temp_folder

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
        return webdriver.Chrome(executable_path="chromedriver110.exe", options=options)
        # return webdriver.Chrome(
        #     service=Service(ChromeDriverManager().install()), options=options
        # )

    else:
        print(f"子进程结束：{completedProcess.stderr}")


# 2、获取driver，通过驱动程序
def get_driver_ChromeDriver(
    browser_parameter_name=None,
    down_file_save_path="D:\\downloads",
):
    options = webdriver.ChromeOptions()
    # 切换成便携版chrome，避免跨平台时，所在平台没有安装chrome或chrome和chromedriver版本不一致
    chrome_portable_path = (
        f"{Path(__file__).parent}\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
    )
    options.binary_location = chrome_portable_path
    # 设置浏览器运行参数
    # 浏览器地址栏访问chrome://version/查看个人资料路径,去掉最后的/Default
    chrome_parameter_path = get_temp_folder(
        des_folder_name="spiders_out/selenum_zy",
        is_clear_folder=False,
    ).replace("/", "\\")
    options.add_argument(
        f"user-data-dir={chrome_parameter_path}\\AutomationProfile_{'default' if browser_parameter_name is None else browser_parameter_name}"
    )
    # 配置下载文件的保存目录
    prefs = {
        "profile": {"exit_type": "Normal"},  # 避免有头打开浏览器时出现恢复页面的弹窗提醒
        "download.default_directory": down_file_save_path.replace(
            "/", "\\"
        ),  # 必须采取 \\xx\\格式，/xx/格式会报错误，下载失败
        "download.prompt_for_download": False,  # 为True则弹框，选择保存文件路径，False则用down_file_save_path为保存目录
    }
    options.add_experimental_option("prefs", prefs)
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
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-application-cache")
    # options.add_argument("--disable-popup-blocking")

    options.add_argument(
        "log-level=3"
    )  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    options.add_argument("--window-size=1920,1080")  # 使用有头模式，需设置初始窗口大小
    options.add_argument("--no-first-run")  # 不打开首页
    options.add_argument("--no-default-browser-check")  # 不检查默认浏览器
    # 默认是无头模式，意思是浏览器将会在后台运行，也是为了加速scrapy
    # 我们可不想跑着爬虫时，旁边还显示着浏览器访问的页面
    # 调试的时候可以把SetHeadless设为False，看一下跑着爬虫时候，浏览器在干什么
    SetHeadless = ReadWriteConfFile.getSectionValue(
        "General", "SetHeadless", type="boolean"
    )
    if SetHeadless:
        # 无头模式，无UI
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug
    # 针对UA请求头的操作，防止因为没有添加请求头导致的访问被栏截了
    options.add_argument(
        "User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) >AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57"
    )
    # 这两行会清理cookie,影响登录默认设置失效，导致每次登录都是全新的，比如短信验证码要重复登录
    # 不要轻易打开
    # options.add_argument("--incognito")  # 无痕隐身模式
    # options.add_argument("--no-sandbox")
    # options.add_argument("--no-startup-window")
    # 不加载图片, 提升速度 不知为什么，打开后导致checkbox显示不出来
    # options.add_argument("blink-settings=imagesEnabled=false")
    # 添加启用的去去广告插件,以拦截广告
    options.add_extension(
        f"{Path(__file__).parent}\\GoogleChromePortable\\adblock_v5.4.1.crx"
    )
    # options.add_argument(f"--remote-debugging-port={random.randint(9000, 9999)}")
    driver = webdriver.Chrome(
        executable_path=f"{Path(__file__).parent}\\GoogleChromePortable\\chromedriver.exe",
        chrome_options=options,
        port=random.randint(9000, 9999),
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
    # driver.implicitly_wait(15)
    return driver


# 2、获取driver，通过驱动程序

# 浏览器是否设置无头模式，仅测试时可以为False
# SetHeadless = True
# 是否允许浏览器使用cookies
# EnableBrowserCookies = True


def get_driver_FireFoxDriver(SetHeadless=True, EnableBrowserCookies=True):
    """
    使用selenium操作火狐浏览器
    """
    profile = webdriver.FirefoxProfile()
    options = webdriver.FirefoxOptions()
    # 下面一系列禁用操作是为了减少selenium的资源耗用，加速scrapy
    # 禁用图片
    profile.set_preference("permissions.default.image", 2)
    profile.set_preference("browser.migration.version", 9001)
    # 禁用css
    profile.set_preference("permissions.default.stylesheet", 2)
    # 禁用flash
    profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")
    # 如果EnableBrowserCookies的值设为False，那么禁用cookies
    if EnableBrowserCookies:
        # •值1 - 阻止所有第三方cookie。
        # •值2 - 阻止所有cookie。
        # •值3 - 阻止来自未访问网站的cookie。
        # •值4 - 新的Cookie Jar策略（阻止对跟踪器的存储访问）
        profile.set_preference("network.cookie.cookieBehavior", 2)
    # 默认是无头模式，意思是浏览器将会在后台运行，也是为了加速scrapy
    # 我们可不想跑着爬虫时，旁边还显示着浏览器访问的页面
    # 调试的时候可以把SetHeadless设为False，看一下跑着爬虫时候，浏览器在干什么
    if SetHeadless:
        # 无头模式，无UI
        options.add_argument("-headless")
    # 禁用gpu加速
    options.add_argument("--disable-gpu")
    return webdriver.Firefox(firefox_profile=profile, options=options)
