import random
import re
import time

from general_spider.utils.web_driver_manager import WebDriverManager
from myutils.info_out_manager import load_json_table
from general_spider.utils.tools import waitForXpath
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class ProductChildModify:
    def __init__(self, userID, passwd):
        self.userID = userID
        self.passwd = passwd
        self.wd = WebDriverManager()
        self.browser = self.wd.get_driver()
        self.timeout = 20
        # self.browser.implicitly_wait(15)

    # 登录
    def login(self):
        # 启动chrome的地址，需要下载chromedriver文件，下载地址https://registry.npmmirror.com/binary.html?path=chromedriver
        self.browser.get("http://plm.zybank.com.cn/#/system-tool/factor")  # 填写表的地址
        userid_input = waitForXpath(
            self.browser,
            "//form[@class='el-form login-form el-form--label-top']//input[@name='userId' and @type='text' and @class='el-input__inner']",
            timeout=self.timeout,
        )
        password_input = waitForXpath(
            self.browser,
            "//form[@class='el-form login-form el-form--label-top']//input[@name='password' and @type='password' and @class='el-input__inner']",
            timeout=self.timeout,
        )
        userid_input.clear()
        userid_input.send_keys(self.userID)
        password_input.clear()
        password_input.send_keys(self.passwd)
        submit = waitForXpath(
            self.browser,
            "//form[@class='el-form login-form el-form--label-top']//span[text()='登录']",
            timeout=self.timeout,
        )
        submit.click()
        # login = self.browser.switch_to.active_element
        # login.send_keys(Keys.ENTER)
        # 等待系统工具项出现，并点击
        system_tool = waitForXpath(
            self.browser,
            "//div[@class='menu_ware' and @indexpath='/system-tool']//span[text()='系统工具']",
            timeout=self.timeout,
        )
        system_tool.click()
        # 切换具体操作页，即子产品产品编辑页
        time.sleep(1)
        submit = waitForXpath(
            system_tool,
            "//div[@class='menu_ware nest-menu' and @indexpath='/system-tool/factor/factor']",
            timeout=self.timeout,
        )
        submit.click()

    def get_products_single_page(self):
        # 等完全加载了完了再获取内容，否则会导致获取上一页的内容
        time.sleep(1.2)
        title_eles = self.browser.find_elements(
            by=By.XPATH,
            value='//li[@class="listV2_row pointer"]/span[@class="listV2_cell ellipsis" and @name="productName"]',
        )
        return [title_ele.get_attribute("title") for title_ele in title_eles]

    def search_products(self, product_info: dict):
        product_names = []
        # 1、产品名称搜索
        product_name = product_info["子产品名称"]
        if len(product_name) > 0:
            search_content = waitForXpath(
                self.browser,
                '//div[@class="el-input el-input--mini"]/input[@type="text" and @autocomplete="off" and @placeholder="产品名称" and @class="el-input__inner"]',
                timeout=self.timeout,
            )
            search_content.clear()
            search_content.send_keys(product_name)
        # 1、产品分类搜索
        # 点击下拉菜单
        main_product_classes = product_info["产品分类"]
        if len(main_product_classes) > 0:
            product_departer_ele = waitForXpath(
                self.browser,
                f'//div[@class="nowrap font12 mr8" and @style="white-space: nowrap;" and contains(text(),"产品分类")]/following-sibling::div[1]//input[@type="text" and @readonly="readonly" and @autocomplete="off" and @placeholder="请选择" and @class="el-input__inner"]',
                timeout=self.timeout,
            )
            product_departer_ele.click()
            # 选择下拉菜单里的内容
            parent_drop_select = waitForXpath(
                self.browser,
                f'//div[@class="el-popper el-cascader__dropdown" and @x-placement="bottom-start"]',
                timeout=self.timeout,
            )
            for product_class in main_product_classes.split("/"):
                drop_select_radio = waitForXpath(
                    parent_drop_select,
                    f'//div[@class="el-scrollbar el-cascader-menu" and @role="menu"]//ul[@class="el-scrollbar__view el-cascader-menu__list"]/li[contains(@class,"el-cascader-node is-selectable")]/span[text()="{product_class}"]/preceding-sibling::label[1]//span[@class="el-radio__inner"]',
                    timeout=self.timeout,
                )
                drop_select_radio.click()
        query_ele = waitForXpath(
            self.browser,
            '//div[@class="_button" and contains(text(),"查询")]',
            timeout=self.timeout,
        )
        ActionChains(self.browser).move_to_element(query_ele).click(query_ele).perform()
        # 暂停下，否则因为下面的页码信息获取太快而获取错误信息
        time.sleep(1.2)
        # 获取页码信息行
        pages_ele = waitForXpath(
            self.browser,
            "//div[@class='pagination-container text-right']",
            timeout=self.timeout,
        )
        product_num = waitForXpath(
            pages_ele,
            "./span[@class='list_total']",
            timeout=self.timeout,
        ).text
        product_num = re.search(r"\d+", product_num).group()
        page_num = int(product_num) // 10 + 1
        for i in range(page_num):
            # 把查询到内容，包括多页的全部装到product_names
            product_names.extend(self.get_products_single_page())
            # 翻页
            if page_num > 1 and i < page_num:
                waitForXpath(
                    pages_ele,
                    "//button[@class='btn-next']",
                    timeout=self.timeout,
                ).click()
        product_names.sort()
        return product_names

    def update_product(self, product_info: dict):
        # 一、查询子产品是否存在
        # 1、先产品名称搜索
        product_name = product_info["产品名称"]
        if product_name is None or len(product_name) == 0:
            print("产品名称必须填写")
            return -1
        search_content = waitForXpath(
            self.browser,
            '//div[@class="el-input el-input--mini"]/input[@type="text" and @autocomplete="off" and @placeholder="产品名称" and @class="el-input__inner"]',
            timeout=self.timeout,
        )
        search_content.clear()
        search_content.send_keys(product_name)
        # 2、产品分类搜索
        # 点击下拉菜单
        main_product_classes = product_info["产品分类"]
        if len(main_product_classes) > 0:
            product_departer_ele = waitForXpath(
                self.browser,
                f'//div[@class="nowrap font12 mr8" and @style="white-space: nowrap;" and contains(text(),"产品分类")]/following-sibling::div[1]//input[@type="text" and @readonly="readonly" and @autocomplete="off" and @placeholder="请选择" and @class="el-input__inner"]',
                timeout=self.timeout,
            )
            product_departer_ele.click()
            # 选择下拉菜单里的内容
            parent_drop_select = waitForXpath(
                self.browser,
                f'//div[@class="el-popper el-cascader__dropdown" and @x-placement="bottom-start"]',
                timeout=self.timeout,
            )
            for product_class in main_product_classes.split("/"):
                drop_select_radio = waitForXpath(
                    parent_drop_select,
                    f'//div[@class="el-scrollbar el-cascader-menu" and @role="menu"]//ul[@class="el-scrollbar__view el-cascader-menu__list"]/li[contains(@class,"el-cascader-node is-selectable")]/span[text()="{product_class.strip()}"]/preceding-sibling::label[1]//span[@class="el-radio__inner"]',
                    timeout=self.timeout,
                )
                drop_select_radio.click()
        query_ele = waitForXpath(
            self.browser,
            '//div[@class="_button" and contains(text(),"查询")]',
            timeout=self.timeout,
        )
        ActionChains(self.browser).move_to_element(query_ele).click(query_ele).perform()
        time.sleep(random.uniform(0.5, 1.5))
        title_eles = self.browser.find_elements(
            by=By.XPATH,
            value=f'//li[@class="listV2_row pointer"]/span[@class="listV2_cell ellipsis" and @name="productName" and @title="{product_name}"]',
        )
        # 没查到记录，所以不更新
        if len(title_eles) == 0:
            return 0
        elif len(title_eles) > 1:
            return 2
        # 查到多个记录，说明有多个名称一样的产品，只更新第一条记录
        # 打开详情,更新产品信息
        title_eles[0].click()
        time.sleep(random.uniform(0.5, 1.5))
        # 二、打开详情并更新信息
        for key, value in product_info.items():
            key = key.strip()
            value = value.strip()
            # 0)无需更新项
            if key in ("产品分类", "产品名称"):
                continue
            # 1）特殊更新项
            elif key == "新产品名称":
                product_name_ele = waitForXpath(
                    self.browser,
                    '//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"产品名称")]/following-sibling::div[1]//input[@type="text" and @autocomplete="off" and @class="el-input__inner"]',
                    timeout=self.timeout,
                )
                product_name_ele.clear()
                product_name_ele.send_keys(value)
            # n）以下为需要更新的信息
            else:
                # 首先判断当前要素是否为下拉菜单
                select_eles = self.browser.find_elements(
                    by=By.XPATH,
                    value=f'//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"{key}")]/following-sibling::div[1]//input[@type="text" and @readonly="readonly" and @autocomplete="off" and @placeholder="请选择" and @class="el-input__inner"]',
                )
                # 1）更新下拉框
                if len(select_eles) > 0:
                    # 触发下拉菜单生成
                    select_eles[0].click()
                    # 选择下拉菜单里的内容
                    waitForXpath(
                        self.browser,
                        f'//div[@class="el-select-dropdown el-popper" and @x-placement="bottom-start"]//ul[@class="el-scrollbar__view el-select-dropdown__list"]//span[text()="{value}"]/parent::li[contains(@class,"el-select-dropdown__item")]',
                        timeout=self.timeout,
                    ).click()
                # 2）更新输入框
                else:
                    parent_text_ele = waitForXpath(
                        self.browser,
                        f'//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"{key}")]/following-sibling::div[1]',
                        timeout=self.timeout,
                    )
                    text_ele = waitForXpath(
                        parent_text_ele,
                        './/input[@type="text" and @autocomplete="off" and @class="el-input__inner"]|.//textarea[@autocomplete="off" and @class="el-textarea__inner"]',
                        timeout=self.timeout,
                    )
                    text_ele.clear()
                    text_ele.send_keys(value)
        # 保存提交
        waitForXpath(
            self.browser,
            '//div[@class="productCard mtb20"]//div[@class="_button" and contains(text(),"提交")]',
            timeout=self.timeout,
        ).click()
        # 返回产品列表,上面保存时就会返回，但如果没有改变信息而保存会出现下面的提示信息，并保留在当前页面，故使用下面做下判断
        # message_content = waitForXpath(
        #             self.browser,
        #             f'//p[@class="el-message__content" and contains(text(),"您没有修改产品信息")]',
        #             timeout=self.timeout,
        #         )
        time.sleep(random.uniform(0.1, 0.5))
        if "您没有修改产品信息" in self.browser.page_source:
            waitForXpath(
                self.browser,
                '//div[@class="nav_item"]/img[@class="nav_item-icon pointer" and @title="返回上一页" and @alt="back"]',
                timeout=self.timeout,
            ).click()
        return 1

    # 增加产品信息
    def add_product(self, product_info: dict):
        # 主产品增加
        waitForXpath(
            self.browser,
            "//div[@class='_button' and contains(text(),'子产品新增')]",
            timeout=self.timeout,
        ).click()
        # 0、选择产品分类
        # 点击下拉菜单
        main_product_classes = product_info["产品分类"]
        waitForXpath(
            self.browser,
            '//label[@class="el-form-item__label" and contains(text(),"产品分类")]/following-sibling::div[1]//input[@type="text" and @readonly="readonly" and @autocomplete="off" and @placeholder="请选择" and @class="el-input__inner"]',
            timeout=self.timeout,
        ).click()
        # 选择下拉菜单里的内容
        for product_class in main_product_classes.split("/"):
            drop_select_radio = waitForXpath(
                self.browser,
                f'//div[@class="el-popper el-cascader__dropdown" and @x-placement="bottom-start"]//div[@class="el-scrollbar el-cascader-menu" and @role="menu"]//ul[@class="el-scrollbar__view el-cascader-menu__list"]/li[@class="el-cascader-node"]//span[text()="{product_class.strip()}"]/parent::li[@class="el-cascader-node"]',
                timeout=self.timeout,
            )
            drop_select_radio.click()
            # ActionChains(self.browser).move_to_element(drop_select_radio).click(drop_select_radio).perform()
        # 1、输入产品名称
        main_product_name = product_info["产品名称"]
        waitForXpath(
            self.browser,
            '//div[@class="el-form-item el-form-item--mini"]/label[contains(text(),"产品名称")]/following-sibling::div[1]//input[@type="text" and @valuekey="productName" and @autocomplete="off" and @class="el-input__inner" and @placeholder="请输入内容"]',
            timeout=self.timeout,
        ).click()
        time.sleep(random.uniform(0.1, 0.5))
        waitForXpath(
            self.browser,
            f'//div[@class="el-autocomplete-suggestion el-popper" and @x-placement="bottom-start"]//ul[@class="el-scrollbar__view el-autocomplete-suggestion__list" and @role="listbox"]/li[contains(@id,"el-autocomplete") and @role="option" and normalize-space(text())="{main_product_name.strip()}"]',
            timeout=self.timeout,
        ).click()
        # self.browser.switch_to.active_element.send_keys(Keys.ENTER)
        # 点击下一步
        waitForXpath(
            self.browser,
            '//div[@class="_button margin-auto" and contains(text(),"下一步")]',
            timeout=self.timeout,
        ).click()
        # 循环更新子产品信息
        for key, value in product_info.items():
            key = key.strip()
            value = value.strip()
            # 0)无需更新项
            if key in ("产品分类", "产品名称"):
                continue
            # 1）特殊更新项
            elif key == "子产品名称":
                product_name_ele = waitForXpath(
                    self.browser,
                    '//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"产品名称")]/following-sibling::div[1]//input[@type="text" and @autocomplete="off" and @class="el-input__inner"]',
                    timeout=self.timeout,
                )
                product_name_ele.clear()
                product_name_ele.send_keys(value)
            # n）以下为需要更新的信息
            else:
                # 首先判断当前要素是否为下拉菜单
                select_eles = self.browser.find_elements(
                    by=By.XPATH,
                    value=f'//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"{key}")]/following-sibling::div[1]//input[@type="text" and @readonly="readonly" and @autocomplete="off" and @placeholder="请选择" and @class="el-input__inner"]',
                )
                # 1）更新下拉框
                if len(select_eles) > 0:
                    # 触发下拉菜单生成
                    select_eles[0].click()
                    # 选择下拉菜单里的内容
                    waitForXpath(
                        self.browser,
                        f'//div[@class="el-select-dropdown el-popper" and @x-placement="bottom-start"]//ul[@class="el-scrollbar__view el-select-dropdown__list"]//span[text()="{value}"]/parent::li[contains(@class,"el-select-dropdown__item")]',
                        timeout=self.timeout,
                    ).click()
                # 2）更新输入框
                else:
                    parent_text_ele = waitForXpath(
                        self.browser,
                        f'//div[contains(@class,"font12 textRight mr8") and @style="white-space: nowrap; width: 130px;" and contains(text(),"{key}")]/following-sibling::div[1]',
                        timeout=self.timeout,
                    )
                    text_ele = waitForXpath(
                        parent_text_ele,
                        './/input[@type="text" and @autocomplete="off" and @class="el-input__inner"]|.//textarea[@autocomplete="off" and @class="el-textarea__inner"]',
                        timeout=self.timeout,
                    )
                    text_ele.clear()
                    text_ele.send_keys(value)
        # 6、保存提交
        waitForXpath(
            self.browser,
            '//div[@class="productCard mtb20"]//div[@class="_button" and contains(text(),"提交")]',
            timeout=self.timeout,
        ).click()

    # 通过产品分类和名称(模糊)查询 批量修改产品信息
    def batch_update_product_info(self, file_path):
        self.login()
        pro_items = load_json_table(file_path)
        for pro_item in pro_items:
            product_names = self.search_products(pro_item)
            for product_name in product_names:
                pro_item["子产品名称"] = product_name
                self.update_product(pro_item)
        self.wd.quit_driver()

    # # 根据json表中的子产品名称和分类搜索，修改完全匹配到的产品，如果不存在就添加
    # 要求产品名称完整，存在的话理论上只能搜索一条结果，不存在就新增，如果搜到多个，就打印出来做出提醒进行人工干预
    # 由于新增需要谨慎些，所以增加一个控制，即使搜索不到也不要新增
    def update_add_product_info(self, file_path, to_add=False):
        self.login()
        pro_items = load_json_table(file_path)
        for pro_item in pro_items:
            update_result = self.update_product(pro_item)
            # 产品名称存在且搜索不到情况下才允许新增
            if to_add and update_result == 0:
                print(f"{pro_item}--产品不存在，将新增处理")
                self.add_product(pro_item)
            elif update_result == 2:
                print(f"{pro_item}--产品已存在多个，请核实什么情况！")
        self.wd.quit_driver()


if __name__ == "__main__":
    # 添加子产品信息
    sm_child = ProductChildModify(userID="000216", passwd="abcd@1234")
    sm_child.update_add_product_info(
        file_path=r"D:\temp\retail_yinhangka_child_product_list.txt", to_add=True
    )
    # sm_child.batch_update_product_info()  # ProductChildModify  ProductMainModify
