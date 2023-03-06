import random
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from myutils.sele_driver import web_driver_manager
from myutils import office_tools
from myutils.info_out_manager import load_json_table


class TXDocument:
    def __init__(self, userID, passwd, infile):
        self.userID = userID
        self.passwd = passwd
        self.driver = web_driver_manager.get_driver_ChromeDriver(SetHeadless=False)
        self.driver.implicitly_wait(15)
        # 最大化窗口
        self.driver.maximize_window()
        self.infile = infile

    def login(self):
        # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
        self.driver.get(
            "https://docs.qq.com/sheet/DVFNudFdYUFpQRnhJ?tab=s93vnj&u=621c3ece0c4042ab96d46a84bf74d1da"
        )  # 填写表的地址
        # self.driver.switch_to.frame("login_frame")
        try:
            # 如果找不到抛异常说明登陆过了
            self.driver.find_element(
                by=By.ID, value="header-login-btn"
            ).click()  # 点击登陆按钮
            self.driver.find_element(
                by=By.XPATH,
                value="//li[@class='dui-tabs-bar-item scene-tab-item active dui-tabs-bar-item-active' and @tabindex='0']",
            ).click()  # 点击微信登陆
        except:
            # self.driver.find_element(by=By.ID, value="switcher_plogin").click()
            # time.sleep(1)
            # #   会跳出输入手机令牌来，建议使用快捷登陆
            # self.driver.find_element(by=By.ID, value="u").send_keys(
            #     "2064662418"
            # )  # 改为使用用户名密码登陆的qq
            # self.driver.find_element(by=By.ID, value="p").send_keys(
            #     "mhw1724282931"
            # )  # 改为使用用户名密码登陆的密码
            # self.driver.find_element(by=By.ID, value="login_button").click()
            # print("账号登录成功")
            # time.sleep(5)
            # # 转换frame
            # self.driver.switch_to.parent_frame()
            print("登录成功过了")
        # 登入账号,用快速登入的功能,前提,已经电脑qq登入了
        # self.driver.switch_to.parent_frame()
        time.sleep(1)
        self.driver.maximize_window()
        # 转换frame
        self.driver.switch_to.parent_frame()
        return self.driver

    def switch_tab(self, tab_name):
        elmet = self.driver.find_element(
            by=By.XPATH,
            value=f"//div[@class='sheet-box sheet sheet-tab-focus' and @data-id='s93vnj' and @aria-label='{tab_name}']",
        ).click()

    # 重新回到第一行or第一列 or 第一行第一列（left_up）的格子
    def back_first_rowcol(self, move_dirc="left"):
        elmet = self.driver.find_element(by=By.ID, value="canvasContainer").click()
        # 获取登录过后格子所在位置
        elmet = self.driver.find_element(by=By.XPATH, value="//div[@class='bar-label']")
        pos = re.match(r"([A-Z]+)(\d+)", elmet.text)
        row = pos.group(2)
        col = pos.group(1)
        # 移动到关注要素所在列的首行
        # 右移动格子  # 移动到表格左上角
        if move_dirc == "left" or move_dirc == "left_up":
            col_n = office_tools.convert_to_number(col, 1)
            for _ in range(col_n - 1):
                ActionChains(self.driver).send_keys(Keys.LEFT).perform()
                time.sleep(random.uniform(0.1, 0.3))
        # 上移动格子
        if move_dirc == "up" or move_dirc == "left_up":
            for _ in range(int(row) - 1):
                ActionChains(self.driver).send_keys(Keys.UP).perform()
                time.sleep(random.uniform(0.2, 0.4))

    # 搜索关键列关键值是否存在
    def exists_key(self, key_title, key_value):
        self.back_first_rowcol("left_up")
        # 找到并移动到第一行标题栏中的关键字
        while True:
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            txt = elmet.text.strip()
            if txt == key_title:
                print("找到关键字所在列")
                break
            elif len(txt) == 0:
                raise Exception("关键字不存在")
            else:
                ActionChains(self.driver).send_keys(Keys.RIGHT).perform()
                time.sleep(random.uniform(0.1, 0.5))
        # 寻找关键字对应的值存不存在
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        while True:
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            txt = elmet.text.strip()
            # 这一行遇到主键列为空视为寻找的主键值
            if len(txt) == 0:
                print("要保存的值不存在")
                return False
            elif txt == key_value:
                print("要保存的值已存在")
                return True
            else:
                ActionChains(self.driver).send_keys(Keys.DOWN).perform()
                time.sleep(random.uniform(0.1, 0.5))

    def write_content(self, contents):
        edit_text = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
        time.sleep(random.uniform(0.1, 3))
        edit_text.clear()
        if isinstance(contents, list):
            for content in contents:
                edit_text.send_keys("" if content is None else content)
                edit_text.send_keys(Keys.ALT + Keys.ENTER)
                # ActionChains(self.driver).send_keys(Keys.ALT + Keys.ENTER).perform()
        else:
            edit_text.send_keys("" if contents is None else contents)
        # edit_text.click()  # 模拟鼠标点击
        edit_text.send_keys(Keys.TAB)  # 进入下一个单元格

    # 更新内容到腾讯文档
    def modify(self):
        self.login()
        list_generator = load_json_table(self.infile)
        # 使用列表的元素数来定义循环次数，7个为一组
        for line_record in list_generator:
            demand_no = line_record.get("demand_no")
            submitter = line_record.get("submitter")
            submit_depart = line_record.get("submit_depart")
            submit_date = line_record.get("submit_date")
            title = line_record.get("title")
            # 以下两个考虑到长文本，获取信息时是list
            background = line_record.get("background")
            summary = line_record.get("summary")
            # 把summary合并到background中
            background.extend(summary)
            pro_type = line_record.get("pro_type")
            admit_result = line_record.get("admit_result")
            # 不存在新增，存在避开主键去覆盖
            if not self.exists_key("需求编号", demand_no):
                # 先跳到第一列
                edit_text = self.driver.find_element(
                    by=By.ID, value="alloy-simple-text-editor"
                )
                edit_text.send_keys(Keys.HOME)
                # 编号--如果不需要，则注释掉
                # s = self.driver.find_element(
                #     by=By.XPATH,
                #     value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[1]/div/div/div[1]/div[1]",
                # ).text  # 获取此行的行数
                # a = int(s[1:])  # 将A**去除A，留下数字
                # a = str(a - 2)  # 如果你的排序为行的相差则减去几即可
                # edit_text.send_keys(a)  # 输出a以形成序号
                # 按照标题顺序写入
                self.write_content(demand_no)
                self.write_content(submitter)
                self.write_content(submit_depart)
                self.write_content(submit_date)
                self.write_content(title)
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.write_content(background)
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.write_content(admit_result)
                self.write_content(pro_type)
            else:
                # 先跳到第一列
                edit_text = self.driver.find_element(
                    by=By.ID, value="alloy-simple-text-editor"
                )
                edit_text.send_keys(Keys.HOME)
                time.sleep(random.uniform(0.1, 0.5))
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.write_content(submitter)
                self.write_content(submit_depart)
                self.write_content(submit_date)
                self.write_content(title)
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.write_content(background)
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                self.write_content(admit_result)
                self.write_content(pro_type)
        time.sleep(1)
        self.driver.close()
