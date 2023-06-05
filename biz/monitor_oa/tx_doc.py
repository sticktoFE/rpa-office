from pathlib import Path
import random
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from general_spider.utils import web_driver_manager
from myutils import office_tools
from myutils.info_out_manager import load_json_table


class TXDocument:
    def __init__(self, userID, passwd):
        self.userID = userID
        self.passwd = passwd
        self.driver = web_driver_manager.get_driver_ChromeDriver()
        self.driver.implicitly_wait(15)
        # 最大化窗口
        self.driver.maximize_window()
        self.metadata = {
            "demand_no": "需求编号",
            "submitter": "报送人",
            "submit_depart": "报送单位",
            "submit_date": "报送时间",
            "title": "需求名称",
            "background": "需求内容简述",
            "admit_result": "产品登记结果",
            "pro_type": "产品分类结果",
            "admit_date": "需求审核日期",
            "admit_person": "需求审核人",
            "weeks": "周标签",
        }

    def login(self):
        # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
        self.driver.get(
            "https://docs.qq.com/sheet/DVFNudFdYUFpQRnhJ?tab=s93vnj&_t=1680773031705&u=8924b60228f34d339d4c91fa99605a65"
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
            print("登录成功过！")
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
        # 左移动格子  # 移动到表格左上角
        if move_dirc == "left" or move_dirc == "left_up":
            col_n = office_tools.convert_to_number(col, 1)
            for _ in range(col_n - 1):
                ActionChains(self.driver).send_keys(Keys.LEFT).perform()
        # 上移动格子
        if move_dirc == "up" or move_dirc == "left_up":
            for _ in range(int(row) - 1):
                ActionChains(self.driver).send_keys(Keys.UP).perform()

    # tab nums次
    def key_tabs_nums(self, nums):
        for _ in range(nums):
            ActionChains(self.driver).send_keys(Keys.TAB).perform()

    # 获取选中的当前单元格所在的行和列，都是从1开始
    def get_current_cell_pos(self):
        elmet = self.driver.find_element(by=By.XPATH, value="//div[@class='bar-label']")
        pos = re.match(r"([A-Z]+)(\d+)", elmet.text)
        row_n = int(pos.group(2))
        col = pos.group(1)
        col_n = office_tools.convert_to_number(col, 1)
        return row_n, col_n

    # 构建腾讯文档的元数据，思路为：
    # 形成标题和列的字典
    # 形成主键的所有值和行的字典，用于判断要插入的记录是不是存在，如果不存在把当前主键值和行更新进去
    # 要有一个表示空行开始行数的变量，用于插入记录
    def produce_doc_metadat(self, key_title=None):
        caction = ActionChains(self.driver)
        # 主键及所在列数
        self.primary = {}
        # 数据最后一列的下一个空行，用于插入新记录
        self.last_empty_point = 1
        # 行和列当前指针
        self.curent_point_row = 1
        self.curent_point_col = 1
        # 主键值及所在行
        self.exist_primary_values = {}
        # 标题及所在列数
        self.title = {}
        self.back_first_rowcol("left_up")
        # 找到并移动到第一行标题栏中的关键字
        while True:
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            txt = elmet.text.strip()
            if len(txt) == 0:
                print("到最后的空列了")
                row_, col_ = self.get_current_cell_pos()
                self.curent_point_col = col_
                break
            else:
                # 把表格标题列号存起来，为了移动使用
                row_, col_ = self.get_current_cell_pos()
                self.title[txt] = col_
                if txt == key_title:
                    print("找到关键字所在列")
                    self.primary = {key_title: col_}
                caction.send_keys(Keys.RIGHT).perform()
                # time.sleep(random.uniform(0.1, 0.5))
        # 下移一行并进入主键列，获取主键值列表
        self.move_from_to(self.curent_point_col, self.primary[key_title], type="col")
        caction.send_keys(Keys.DOWN).perform()
        while True:
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            txt = elmet.text.strip()
            # 这一行遇到主键列为空，意味着主键值寻找完毕
            if len(txt) == 0:
                print("到最后的空行了")
                row_, col_ = self.get_current_cell_pos()
                self.last_empty_point = row_
                self.curent_point_row = row_
                break
            else:
                row_, col_ = self.get_current_cell_pos()
                self.exist_primary_values[txt] = row_
                caction.send_keys(Keys.DOWN).perform()

    # DOWN UP LEFT RIGHT不如 ENTER,SHIFT+ENTER,SHIFT+TAB,TAB好使
    # 但是编码时ENTER等并不能用 唉！！！
    def move_from_to(self, from_roc, to__roc, type="row"):
        caction = ActionChains(self.driver)
        jump_roc = to__roc - from_roc
        if jump_roc >= 0:
            for _ in range(jump_roc):
                if type == "row":
                    caction.send_keys(Keys.DOWN).perform()
                elif type == "col":
                    caction.send_keys(Keys.RIGHT).perform()
        else:
            for _ in range(-jump_roc):
                if type == "row":
                    caction.send_keys(Keys.UP).perform()
                elif type == "col":
                    caction.send_keys(Keys.LEFT).perform()
        if type == "row":
            self.curent_point_row = to__roc
        elif type == "col":
            self.curent_point_col = to__roc

    def write_content_up(self, title, contents):
        # 1、先移动到目标单元格
        target_col = self.title[self.metadata[title]]
        self.move_from_to(
            self.curent_point_col,
            target_col,
            type="col",
        )
        # 2、写值
        edit_text = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
        time.sleep(random.uniform(0.1, 1))
        edit_text.clear()
        if isinstance(contents, list):
            for count, content in enumerate(contents):
                if count > 0:
                    edit_text.send_keys(Keys.ALT + Keys.ENTER)
                # 字符里存在 \t 所以要替换掉，否则会导致文档输入错位
                content = re.sub(r"\t+", " ", content).strip()
                edit_text.send_keys("" if content is None else content)
                # ActionChains(self.driver).send_keys(Keys.ALT + Keys.ENTER).perform()
        else:
            if contents is None:
                contents = ""
            else:
                contents = re.sub(r"\t+", " ", contents).strip()
            edit_text.send_keys(contents)
        # 上面输入完内容，按esc手动操作是可以继续挪动单元格的，但程序中传入却会删除值，所以只能tab一下，并把列指引加1
        edit_text.send_keys(Keys.TAB)
        self.curent_point_col = self.curent_point_col + 1

    # 更新内容到腾讯文档，升级一下，加快速度
    def modify_up(self, infolder):
        self.login()
        # 根据主键生成主键相关数据
        self.produce_doc_metadat(key_title="需求编号")
        # 循环文件夹下的特定文件，解析到线上文档
        for infile in Path(infolder).glob("*_finished"):
            list_generator = load_json_table(infile)
            # 循环字典形成的列表
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
                admit_person = line_record.get("admit_person")
                admit_date = line_record.get("admit_date")
                admit_result = line_record.get("admit_result")
                weeks = line_record.get("weeks")
                # 不存在就新增记录，存在则避开主键去覆盖其他值
                curent_data_row = self.exist_primary_values.get(demand_no, 0)
                if curent_data_row == 0:
                    self.move_from_to(self.curent_point_row, self.last_empty_point)
                    # 把新主键放入缓存表
                    self.exist_primary_values[demand_no] = self.curent_point_row
                    self.last_empty_point = self.last_empty_point + 1
                    # 编号--如果不需要，则注释掉
                    # s = self.driver.find_element(
                    #     by=By.XPATH,
                    #     value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[1]/div/div/div[1]/div[1]",
                    # ).text  # 获取此行的行数
                    # a = int(s[1:])  # 将A**去除A，留下数字
                    # a = str(a - 2)  # 如果你的排序为行的相差则减去几即可
                    # edit_text.send_keys(a)  # 输出a以形成序号
                    self.write_content_up("demand_no", demand_no)
                    self.write_content_up("submitter", submitter)
                    self.write_content_up("submit_depart", submit_depart)
                    self.write_content_up("submit_date", submit_date)
                    self.write_content_up("title", title)
                    self.write_content_up("background", background)
                    self.write_content_up("admit_result", admit_result)
                    self.write_content_up("pro_type", pro_type)
                    self.write_content_up("admit_date", admit_date)
                    self.write_content_up("admit_person", admit_person)
                    self.write_content_up("weeks", weeks)
                else:
                    # 回当前行第一列
                    # ActionChains(self.driver).send_keys(Keys.HOME).perform()
                    self.move_from_to(self.curent_point_row, curent_data_row)
                    self.write_content_up("submitter", submitter)
                    self.write_content_up("submit_depart", submit_depart)
                    self.write_content_up("submit_date", submit_date)
                    self.write_content_up("title", title)
                    self.write_content_up("background", background)
                    self.write_content_up("admit_result", admit_result)
                    self.write_content_up("pro_type", pro_type)
                    self.write_content_up("admit_date", admit_date)
                    self.write_content_up("admit_person", admit_person)
                    self.write_content_up("weeks", weeks)
        time.sleep(1)
        self.driver.close()

    # 留档，有move_by_offset的一些用法
    def test(self, infile):
        self.login()
        list_generator = load_json_table(infile)
        # 循环字典形成的列表
        # for line_record in list_generator:
        #     demand_no = line_record.get("demand_no")
        #     submitter = line_record.get("submitter")
        elmet = self.driver.find_element(by=By.ID, value="canvasContainer")
        elmet.click()
        # 当前鼠标所在单元格的坐标
        # 获取登录过后格子所在位置
        current_elmet_pos = self.driver.find_element(
            by=By.XPATH,
            value="//div[@class='table-input-board']/div[@class='table-input-stage my-vip-cursor-style']",
        )
        ce_attr = current_elmet_pos.get_attribute("style")
        pos = re.match(r".*left: (\d+)px.*top: (\d+)px.*", ce_attr)
        pos_x = int(pos.group(1))
        pos_y = int(pos.group(2))
        # 假设左上第一个单元格坐标为 48,22
        # 获取登录过后格子所在位置

        action = ActionChains(self.driver)
        action.reset_actions()
        # action.move_by_offset(60, 70).click().perform()
        elmet = self.driver.find_element(
            by=By.XPATH, value="//div[@class='line-board']"
        )
        toMail_search = self.driver.switch_to.active_element
        action.move_to_element_with_offset(elmet, 500, 100).click().perform()
