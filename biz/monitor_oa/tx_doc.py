from pathlib import Path
import random
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from general_spider.utils.tools import waitNotForXpath

from general_spider.utils.web_driver_manager import WebDriverManager
from myutils import office_tools
from myutils.info_out_manager import load_json_table
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TXDocument:
    def __init__(self, userID, passwd):
        self.userID = userID
        self.passwd = passwd
        self.wd = WebDriverManager()
        self.driver = self.wd.get_driver()
        self.col_title = {
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
        self.login()
        # 根据主键生成主键相关数据
        self.init_metadata(key_title="需求编号")

    # 构建腾讯文档的元数据，思路为：
    # 形成标题和列的字典
    # 形成{主键：行数}的字典，用于判断要插入的记录是不是存在，如果不存在把当前主键值和行更新进去
    # 要有一个表示空行开始行数的变量，用于插入记录
    def init_metadata(self, key_title=None):
        # 数据最后一列的下一个空行，用于插入新记录
        self.first_blank_rn = 1
        # 主键值及所在行
        self.exist_primary_rn = {}
        # 标题及所在列数
        self.title_col_num = {}
        self.move_to(1, 1)
        # 1、找到并移动到第一行标题栏中的{关键字:列数}
        while True:
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            txt = elmet.text.strip()
            if len(txt) == 0:
                print("到最后的空列了")
                break
            else:
                # 把表格标题列号存起来，为了移动使用
                curr_rn, curr_cn = self.get_current_cell_pos()
                self.move_to(curr_rn, curr_cn + 1)
                self.title_col_num[txt] = curr_cn
                # time.sleep(random.uniform(0.1, 0.5))
        # 2、下移一行并进入主键列，生成{主键值:行数}，用以判断记录是否已存在
        curr_rn, curr_cn = self.get_current_cell_pos()
        self.move_to(curr_rn, self.title_col_num[key_title])
        while True:
            curr_rn, curr_cn = self.get_current_cell_pos()
            self.move_to(curr_rn + 1, curr_cn)
            elmet = self.driver.find_element(by=By.ID, value="alloy-simple-text-editor")
            primary_txt = elmet.text.strip()
            # 这一行遇到主键列为空，意味着主键值寻找完毕
            if len(primary_txt) == 0:
                print("到最后的空行了")
                self.first_blank_rn = curr_rn + 1
                break
            else:
                self.exist_primary_rn[primary_txt] = curr_rn + 1

    def login(self):
        # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
        self.driver.get(
            # "https://docs.qq.com/sheet/DVFNudFdYUFpQRnhJ?tab=ognojy&_t=1680773031705" 调试用
            "https://docs.qq.com/sheet/DVFNudFdYUFpQRnhJ?tab=s93vnj&_t=1680773031705&u=8924b60228f34d339d4c91fa99605a65"
        )  # 填写表的地址
        # self.driver.switch_to.frame("login_frame")
        try:
            # 首先判断当前要素是否存在
            login_eles = self.driver.find_elements(
                by=By.XPATH,
                value='//div[@class="dui-button-container" and @data-dui-0-138-1="dui-button-container" and text()="登录腾讯文档"]',
            )
            # 1）更新下拉框
            if len(login_eles) > 0:
                # 如果找不到抛异常说明登陆过了
                self.driver.find_element(
                    by=By.ID, value="header-login-btn"
                ).click()  # 点击登陆按钮
                self.driver.find_element(
                    by=By.XPATH,
                    value='//li[@class="dui-tabs-bar-item dui-tabs-bar-item-medium scene-tab-item active dui-tabs-bar-item-active" and @tabindex="0"]',
                ).click()  # 点击微信登陆
                # 等着登录框消失
                waitNotForXpath(
                    self.driver,
                    '//div[@class="wechat-login"]',
                    timeout=60,
                )
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
        # 选中内容部分
        self.driver.find_element(by=By.ID, value="canvasContainer").click()
        return self.driver

    # 获取选中的当前单元格所在的行和列，都是从1开始
    def get_current_cell_pos(self):
        elmet = self.driver.find_element(by=By.XPATH, value="//div[@class='bar-label']")
        pos = re.match(r"([A-Z]+)(\d+)", elmet.text)
        row_n = int(pos.group(2))
        col = pos.group(1)
        col_n = office_tools.convert_to_number(col, 1)
        return row_n, col_n

    # DOWN UP LEFT RIGHT不如 ENTER,SHIFT+ENTER,SHIFT+TAB,TAB好使
    # 但是编码时ENTER等并不能用 唉！！！
    def move_to(self, to_row, to_col):
        curr_rn, curr_cn = self.get_current_cell_pos()
        acs = ActionChains(self.driver)
        jump_row = to_row - curr_rn
        if jump_row >= 0:
            for _ in range(jump_row):
                acs.send_keys(Keys.DOWN).perform()
        else:
            for _ in range(-jump_row):
                acs.send_keys(Keys.UP).perform()
        jump_col = to_col - curr_cn
        if jump_col >= 0:
            for _ in range(jump_col):
                acs.send_keys(Keys.RIGHT).perform()
        else:
            for _ in range(-jump_col):
                acs.send_keys(Keys.LEFT).perform()
        curr_rn, curr_cn = self.get_current_cell_pos()
        # 移动后，当前所在行和所在列应该和移动时的目标行和目标列一样，这样才算达到目的，
        # 否则很可能行或者列没有空行了，这时需要点击+增加行或者列，然后再移动
        is_move_again = False
        if curr_rn != to_row:
            row_button = self.driver.find_element(
                by=By.XPATH,
                value='//div[@class="expand-one-row-button" and @title="向下增加一行"]/div[@class="expand-one-row-button-icon"]',
            )
            # 使用 JavaScript 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView(true);", row_button)
            # 等待元素可见
            WebDriverWait(self.driver, 10).until(EC.visibility_of(row_button))
            row_button.click()
            is_move_again = True
        if curr_cn != to_col:
            col_button = self.driver.find_element(
                by=By.XPATH,
                value='//div[@class="expand-one-col-button" and @title="向右增加一列"]',
            )
            col_button.click()
            is_move_again = True
        if is_move_again:
            self.move_to(to_row, to_col)

    # 移动到目标单元格并填值
    def write_content_up(self, rn, col_str, contents):
        # 1、先移动到目标单元格
        target_col = self.title_col_num[self.col_title[col_str]]
        self.move_to(rn, target_col)
        # 2、写值-----------这一部分有可能报clear问题，所以此文件备份copy 2.py暂时保留，它试图做一些改变
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
        else:
            if contents is None:
                contents = ""
            else:
                contents = re.sub(r"\t+", " ", contents).strip()
            edit_text.send_keys(contents)
        # 上面输入完内容，按esc手动操作是可以继续挪动单元格的，但程序中传入却会删除值，所以只能tab一下，并把列指引加1
        # edit_text.send_keys(Keys.TAB)
        # 点击下防止单元格处于编辑状态而无法移动格子
        self.driver.find_element(by=By.XPATH, value="//div[@class='bar-label']").click()

    # 更新内容到腾讯文档，升级一下，加快速度
    def modify_up(self, infolder):
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
                curr_rn, curr_cn = self.get_current_cell_pos()
                target_data_row = self.exist_primary_rn.get(demand_no, 0)
                if target_data_row == 0:
                    purpose_rn = self.first_blank_rn
                    self.first_blank_rn = self.first_blank_rn + 1
                    # 把新主键放入缓存表
                    self.exist_primary_rn[demand_no] = purpose_rn
                    # 编号--如果不需要，则注释掉
                    # s = self.driver.find_element(
                    #     by=By.XPATH,
                    #     value="/html/body/div[3]/div/div[4]/div[2]/div/div/div[1]/div/div/div[1]/div[1]",
                    # ).text  # 获取此行的行数
                    # a = int(s[1:])  # 将A**去除A，留下数字
                    # a = str(a - 2)  # 如果你的排序为行的相差则减去几即可
                    # edit_text.send_keys(a)  # 输出a以形成序号
                    self.write_content_up(purpose_rn, "demand_no", demand_no)
                    self.write_content_up(purpose_rn, "submitter", submitter)
                    self.write_content_up(purpose_rn, "submit_depart", submit_depart)
                    self.write_content_up(purpose_rn, "submit_date", submit_date)
                    self.write_content_up(purpose_rn, "title", title)
                    self.write_content_up(purpose_rn, "background", background)
                    self.write_content_up(purpose_rn, "admit_date", admit_date)
                    self.write_content_up(purpose_rn, "admit_person", admit_person)
                    self.write_content_up(purpose_rn, "weeks", weeks)
                    self.write_content_up(purpose_rn, "admit_result", admit_result)
                    self.write_content_up(purpose_rn, "pro_type", pro_type)
                else:
                    # 回当前行第一列
                    self.write_content_up(target_data_row, "submitter", submitter)
                    self.write_content_up(
                        target_data_row, "submit_depart", submit_depart
                    )
                    self.write_content_up(target_data_row, "submit_date", submit_date)
                    self.write_content_up(target_data_row, "title", title)
                    self.write_content_up(target_data_row, "background", background)
                    self.write_content_up(target_data_row, "admit_date", admit_date)
                    self.write_content_up(target_data_row, "admit_person", admit_person)
                    self.write_content_up(target_data_row, "weeks", weeks)
                    self.write_content_up(target_data_row, "admit_result", admit_result)
                    self.write_content_up(target_data_row, "pro_type", pro_type)
        # 使用 ActionChains 执行 Ctrl + S 快捷键
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("s").key_up(
            Keys.CONTROL
        ).perform()
        time.sleep(5)
        self.wd.quit_driver(self.driver)
