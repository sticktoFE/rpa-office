# %%
import random

# 导入By类
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
import re
from pathlib import Path

# import sys
# sys.path.insert(0, str(Path.cwd().parent.parent))
import importlib

# 解决修改自定义包，无法生效的问题
from myutils import web_driver_manager
from myutils import office_tools

# %%
# 去除txt文档中的空格行
def txt_os():
    file1 = open(
        "biz/monitor_oa/wiki.txt", "r", encoding="utf-8"
    )  # 打开要去掉空行的文件,这里的文件改成语雀脚本生成的文件
    file2 = open("biz/monitor_oa/wiki2.txt", "w", encoding="utf-8")  # 生成没有空行的文件
    for line in file1.readlines():  # 去除空行
        if line == "\n":
            line = line.strip("\n")
        file2.write(line)  # 输出到新文件中
    print("输出成功....")
    file1.close()
    file2.close()
    # 将txt文件读入列表去除行中的回车


def txt_to_list():
    txt_os()
    file = open(
        "biz/monitor_oa/wiki2.txt", "r", encoding="utf-8"
    )  # 这里的文件对应txt_os中生产的文件
    list = file.readlines()
    list = [x.strip() for x in list if x.strip() != ""]  # 去除行中的回车
    print(list)
    return list  # 返回列表


# %%
importlib.reload(web_driver_manager)


def login():
    driver = web_driver_manager.get_driver_Chromeexe()
    # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
    driver.get("https://docs.qq.com/sheet/DSk9uUnJhS1daVmFs?tab=hzgxzt")  # 填写表的地址
    driver.implicitly_wait(10)
    # driver.switch_to.frame("login_frame")
    try:
        # 如果找不到抛异常说明登陆过了
        driver.find_element(by=By.ID, value="header-login-btn").click()  # 点击登陆按钮
        driver.find_element(
            by=By.XPATH,
            value="//li[@class='dui-tabs-bar-item scene-tab-item active dui-tabs-bar-item-active' and @tabindex='0']",
        ).click()  # 点击微信登陆
    except:
        # driver.find_element(by=By.ID, value="switcher_plogin").click()
        # time.sleep(1)
        # #   会跳出输入手机令牌来，建议使用快捷登陆
        # driver.find_element(by=By.ID, value="u").send_keys(
        #     "2064662418"
        # )  # 改为使用用户名密码登陆的qq
        # driver.find_element(by=By.ID, value="p").send_keys(
        #     "mhw1724282931"
        # )  # 改为使用用户名密码登陆的密码
        # driver.find_element(by=By.ID, value="login_button").click()
        # print("账号登录成功")
        # time.sleep(5)
        # # 转换frame
        # driver.switch_to.parent_frame()
        print("登录成功过了")
    # 登入账号,用快速登入的功能,前提,已经电脑qq登入了
    # driver.switch_to.parent_frame()
    time.sleep(1)
    driver.maximize_window()
    # 转换frame
    driver.switch_to.parent_frame()
    return driver


# %%
# 重新回到第一行or第一列 or 第一行第一列（left_up）的格子
def back_first_rowcol(driver, move_dirc="left"):
    elmet = driver.find_element(by=By.ID, value="canvasContainer").click()
    # 获取登录过后格子所在位置
    elmet = driver.find_element(by=By.XPATH, value="//div[@class='bar-label']")
    pos = re.match(r"([A-Z]+)(\d+)", elmet.text)
    row = pos.group(2)
    col = pos.group(1)
    # 移动到关注要素所在列的首行
    # 右移动格子  # 移动到表格左上角
    if move_dirc == "left" or move_dirc == "left_up":
        col_n = office_tools.convert_to_number(col, 1)
        for _ in range(col_n - 1):
            ActionChains(driver).send_keys(Keys.LEFT).perform()
            time.sleep(random.uniform(0.1, 0.3))
    # 上移动格子
    if move_dirc == "up" or move_dirc == "left_up":
        for _ in range(int(row) - 1):
            ActionChains(driver).send_keys(Keys.UP).perform()
            time.sleep(random.uniform(0.2, 0.4))


# 搜索关键列关键值是否存在
def exists_key(driver, key_title, key_value):
    back_first_rowcol(driver, "left_up")
    # 找到并移动到第一行标题栏中的关键字
    while True:
        elmet = driver.find_element(by=By.ID, value="alloy-simple-text-editor")
        txt = elmet.text.strip()
        if txt == key_title:
            print("找到关键字所在列")
            break
        elif len(txt) == 0:
            raise Exception("关键字不存在")
        else:
            ActionChains(driver).send_keys(Keys.RIGHT).perform()
            time.sleep(random.uniform(0.1, 0.5))
    # 寻找关键字对应的值存不存在
    ActionChains(driver).send_keys(Keys.DOWN).perform()
    while True:
        elmet = driver.find_element(by=By.ID, value="alloy-simple-text-editor")
        txt = elmet.text.strip()
        if len(txt) == 0:
            print("要保存的值不存在")
            return False
        elif txt == key_value:
            print("要保存的值已存在")
            return True
        else:
            ActionChains(driver).send_keys(Keys.DOWN).perform()
            time.sleep(random.uniform(0.1, 0.5))


# %%
def tx_write():
    driver = login()
    ####################################################################################
    j = 0  # 使用变量来定位列表
    list = txt_to_list()
    # 使用列表的元素数来定义循环次数，7个为一组
    for line_record in list:
        if len(line_record.strip()) == 0:
            break
        # 默认分隔符是空格，并且多个空格视为一个
        line_elements = line_record.split()
        if not exists_key(driver, "姓名", line_elements[0]):
            # 先跳到第一列
            edit_text = driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            edit_text.send_keys(Keys.HOME)
            # 编号--如果不需要，则注释掉
            # s = driver.find_element(
            #     by=By.XPATH,
            #     value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[1]/div/div/div[1]/div[1]",
            # ).text  # 获取此行的行数
            # a = int(s[1:])  # 将A**去除A，留下数字
            # a = str(a - 2)  # 如果你的排序为行的相差则减去几即可
            # edit_text.send_keys(a)  # 输出a以形成序号
            for ele in line_elements:
                edit_text = driver.find_element(
                    by=By.ID, value="alloy-simple-text-editor"
                )
                time.sleep(random.uniform(0.1, 3))
                edit_text.send_keys(ele)
                # edit_text.click()  # 模拟鼠标点击
                edit_text.send_keys(Keys.TAB)  # 进入下一个单元格
    time.sleep(1)
    print("输入成功")
    driver.close()


# %%
if __name__ == "__main__":
    tx_write()
