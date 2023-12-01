from pathlib import Path
import shutil
import subprocess
import threading
from selenium import webdriver
from myutils.DateAndTime import get_date
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent

from myutils.info_out_manager import ReadWriteConfFile

chrome_path = Path(__file__).parent.joinpath("GoogleChromePortable")


class WebDriverManager:
    _instance = None
    _available_drivers = {}
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                    cls.folder_index = 0
                    cls.ua = UserAgent()
        return cls._instance

    def get_folder(self):
        # 寻找浏览器参数目录中，是否存在没有使用的参数文件夹，
        # 如存在就征用，并标记为激活状态，如不存在就复制正在使用的参数目录形成一个临时的参数目录来使用
        # 在当前爬虫结束后要清理掉
        parent_profile = Path(chrome_path) / "Data"
        source_profile = parent_profile / "profile"
        temp_profile = parent_profile / get_date(format="%Y_%m_%d_%H_%M_%S_%f")
        with self._lock:
            self.folder_index += 1
        # 保留5个常备的参数文件夹，开的浏览器超过三个，增加临时的参数文件夹，用完删除
        if self.folder_index < 6 and (
            notused_profile := list(parent_profile.glob(f"{self.folder_index}"))
        ):
            one_notused_profile = notused_profile[0]
            used_profile = one_notused_profile.rename(
                str(one_notused_profile) + "_used"
            )
            brower_profile = str(used_profile)
        else:
            shutil.copytree(source_profile, temp_profile, dirs_exist_ok=True)
            brower_profile = str(temp_profile)
        return brower_profile

    def quit_driver(self, driver_obj=None):
        def restore_folder(browser_profile):
            browser_profile_path = Path(browser_profile)
            if browser_profile_path.stem.endswith("_used"):
                browser_profile_path.rename(
                    str(browser_profile_path).replace("_used", "")
                )
            else:
                shutil.rmtree(browser_profile_path)

        if driver_obj is not None:
            folder, driver = self._available_drivers[id(driver_obj)]
            driver.quit()
            restore_folder(folder)
        else:
            for folder, driver in self._available_drivers.values():
                driver.quit()
                restore_folder(folder)

    # 2、获取driver，通过驱动程序
    # 发现不写 driver.quit(),只要代码执行完，浏览器也会退出
    def get_driver(self, down_file_save_path="D:\\downloads", timeout=30):
        options = webdriver.ChromeOptions()
        # 切换成便携版chrome，避免跨平台时，所在平台没有安装chrome或chrome和chromedriver版本不一致
        options.binary_location = f"{chrome_path}\\App\\Chrome-bin\\chrome.exe"
        # 设置浏览器运行参数
        # 浏览器地址栏访问chrome://version/查看个人资料路径,去掉最后的/Default
        current_folder = self.get_folder()
        options.add_argument(f"user-data-dir={current_folder}")
        # 配置下载文件的保存目录
        prefs = {
            "profile": {"exit_type": "Normal"},  # 避免有头打开浏览器时出现恢复页面的弹窗提醒
            "download.default_directory": down_file_save_path.replace(
                "/", "\\"
            ),  # 必须采取 \\xx\\格式，/xx/格式会报错误，下载失败
            # 为True则弹框，选择保存文件路径，False则用down_file_save_path为保存目录
            "download.prompt_for_download": False,  # 是否显示下载提示框
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
        options.add_argument(f"User-Agent={self.ua.random}")
        # 这两行会清理cookie,影响登录默认设置失效，导致每次登录都是全新的，比如短信验证码要重复登录
        # 不要轻易打开
        # options.add_argument("--incognito")  # 无痕隐身模式
        # options.add_argument("--no-sandbox")
        # options.add_argument("--no-startup-window")
        # 不加载图片, 提升速度 不知为什么，打开后导致checkbox显示不出来
        # options.add_argument("blink-settings=imagesEnabled=false")
        # 添加启用的去去广告插件,以拦截广告
        # options.add_extension(f"{chrome_path}\\adblock_v5.4.1.crx")
        # options.add_argument(f"--remote-debugging-port={random.randint(9000, 9999)}")
        chrome_driver_path = f"{chrome_path}\\chromedriver.exe"
        # driver = webdriver.Chrome(
        #     executable_path=chrome_driver_path,
        #     chrome_options=options,
        #     # port=random.randint(9000, 9999),
        # )
        # selenium新版使用下面的
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        # 修改 webdriver 值，为了反反爬
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            },
        )
        # 隐私等待，整体等待元素出现最长时间暂时设置为10s,selenium.dev上说 显示等待和隐式等待不要同时使用
        driver.implicitly_wait(timeout)
        # 最大化窗口
        driver.maximize_window()
        # driver.set_window_size(1400, 700)
        driver.set_page_load_timeout(timeout)
        self._available_drivers[id(driver)] = (current_folder, driver)
        return driver

    # 1、获取driver，用本地浏览器，据说可以有效反反爬
    # 直接使用本地浏览器
    def get_driver_Chromeexe(self, timeout=30):
        # 此处 Chrome 的路径需要修改为你本机的 Chrome 安装位置
        # --remote-debugging-port 指定任何打开的端口
        # --user-data-dir,形式C:\xxxxx\AutomationProfile中xxxxx建议设置为selenium_text  selenium_taobao  selenium_kanzhun这样的格式
        # 不同的就是可以开启不同的账号，如果都用这个位置，可能会发现哪怕用不同的端口，但是程序只会第一个调用的成功。
        # 所以：不同的端口做不同的事情，用不同的文件夹位置放账户配置信息。哪怕这次窗口关闭了，
        # 你下次调用这个窗口打开一样的页面，只要不到cookie失效时间，你登录的信息都还是存在的。
        # chrome_path_exe = f'"{chrome_path}\\App\\Chrome-bin\\chrome.exe " --remote-debugging-port=19222 --user-data-dir="{chrome_path.joinpath("Data")}"'
        chrome_path_exe = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=19222'

        completedProcess = subprocess.Popen(  # run是同步
            chrome_path_exe,
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
            chrome_driver_path = "E:\\360Downloads\\chromedriver.exe"
            # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
            driver = webdriver.Chrome(
                service=Service(chrome_driver_path), options=options
            )
            driver.implicitly_wait(timeout)
            # 最大化窗口
            driver.maximize_window()
            # driver.set_window_size(1400, 700)
            driver.set_page_load_timeout(timeout)
            return driver
            # return webdriver.Chrome(
            #     service=Service(ChromeDriverManager().install()), options=options
            # )

        else:
            print(f"子进程结束：{completedProcess.stderr}")
