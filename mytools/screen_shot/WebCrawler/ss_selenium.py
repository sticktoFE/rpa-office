import time
import traceback


from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import myutils.sele_driver.web_driver_manager as web_driver_manager
from WebShotScreen import ShotScreenManager


class SeleniumManager(
    ShotScreenManager,
):
    shot_selenium_driver_Chromeexe = 1
    shot_selenium_driver_Chromedriver = 2

    # 利用谷歌浏览器截图
    def shotScreen12(self, search_text):
        print("Selenium->shotScreen")
        if self.shot_driver == SeleniumManager.shot_selenium_driver_Chromeexe:
            # 利用本地谷歌浏览器程序截图
            driver = web_driver_manager.get_driver_Chromeexe()
        elif self.shot_driver == SeleniumManager.shot_selenium_driver_Chromedriver:
            # 利用谷歌浏览器驱动截图
            driver = web_driver_manager.get_driver_ChromeDriver()
        if self.win_width and self.win_height:
            driver.set_window_size(width=self.win_width, height=self.win_height)
        else:
            driver.maximize_window()
        driver.get(self.win_url)
        # 打开页面后，操作html元素
        # input = driver.find_element_by_id('kw')
        # input.clear()
        # input.send_keys(search_text)
        # button = driver.find_element_by_id('su')
        # button.click()
        # 执行js代码，滚动页面
        script = """
            var scroll = function(dHeight){
                # 滚动条顶部位置距内容最顶部的位置
                var t = document.documentElement.scrollTop;
                # 内容最顶部到最底部的长度,即展示完整页面内容的高度，包括显示和隐藏两部分
                var h = document.documentElement.scrollHeight;
                # 等于 dHeight，页面内容显示部分的高度
                var ch = document.documentElement.clientHeight;
                dHeight = dHeight || ch;
                var current = t + dHeight;
                if(current > h){
                    window.scrollTo(0, ch)
                }else{
                    window.scrollTo(0, current)
                }
            }
        """
        script += f"\n scroll()"
        script = script + "\n document.getElementById('head').style.display='none'"
        driver.execute_script(script)
        picName = f"{self.getSavePath()}/{self.image_name}"
        driver.get_screenshot_as_file(picName)
        time.sleep(50)
        driver.quit()
        self.checkShotCallback(file=None, error=traceback.format_exc())

    def shotScreen(self, search_text):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("window-size=1920x1080")
        try:
            driver = webdriver.Chrome(
                executable_path="spider/WebCrawler/chromedriver.exe", options=options
            )
            # driver.get("file:///C:/map.html")
            driver.get(self.win_url)
            # 打开页面后，操作html元素
            # input = driver.find_element_by_id('kw')
            # input.clear()
            # input.send_keys(search_text)
            # button = driver.find_element_by_id('su')
            # button.click()
            # 执行js代码，滚动页面
            driver.execute_script(
                "window.scrollTo(0,100)"
            )  # 执行自定义JS滚动屏幕，可以动态测出整个body的宽度和高度
            driver.set_window_size(
                2000, 2000
            )  # 写死一个屏幕宽度和高度，高度可以超出显示器的物理高度，可以用动态测量的值，参考https://blog.csdn.net/BobYuan888/article/details/108769274
            time.sleep(8)
            driver.get_screenshot_as_file(f"{self.getSavePath()}/{self.image_name}")
            driver.quit()
        except WebDriverException as err:
            print("截图失败")
            print(err)
