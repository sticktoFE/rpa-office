import subprocess
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from general_spider.utils.web_driver_manager import BaseDriver
from pathlib import Path

"""
    自动打开 pdf文件，并进行文字抽取，存储，语义分析
    待完成
"""


class SeleniumManager(BaseDriver):
    shot_selenium_driver_Chromeexe = 1
    shot_selenium_driver_Chromedriver = 2

    # 1、获取driver，用本地浏览器，据说可以有效反反爬
    def get_driver_Chromeexe(self):
        # 此处 Chrome 的路径需要修改为你本机的 Chrome 安装位置
        # --remote-debugging-port 指定任何打开的端口
        chrome_path = f"{Path(__file__).parent}/统计学习方法.pdf"
        completedProcess = subprocess.Popen(  # run是同步
            chrome_path,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        if completedProcess.poll() is None:  # 表示子进程还在运行
            print("####")
            print(completedProcess.stdout)
        else:
            print(f"子进程结束：{completedProcess.stderr}")

    # 利用谷歌浏览器截图
    def shotScreen(self, search_text):
        print("Selenium->shotScreen")

        # 利用本地谷歌浏览器程序截图
        driver = self.get_driver_Chromeexe()

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
                //滚动条顶部位置距内容最顶部的位置
                var t = document.documentElement.scrollTop;
                //内容最顶部到最底部的长度,即展示完整页面内容的高度，包括显示和隐藏两部分
                var h = document.documentElement.scrollHeight;
                //等于 dHeight，页面内容显示部分的高度
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
