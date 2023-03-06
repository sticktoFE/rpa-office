import os
import pickle
import random

# 导入显示等待类

# 导入期望场景类

# 导入By类
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from pathlib import Path
from myutils.sele_driver import web_driver_manager


class SeleMail:
    def __init__(self, userID, passwd, down_path):
        self.cookies_path = Path("D:/tmp/db_cookie_1")
        self.userID = userID
        self.passwd = passwd
        # 下面两个都行 # driver = WebDriverManager().get_driver_Chromeexe()
        self.driver = web_driver_manager.get_driver_ChromeDriver(
            SetHeadless=False, down_file_save_path=down_path
        )
        self.driver.implicitly_wait(15)
        # 最大化窗口
        self.driver.maximize_window()

    # 保存cookies
    def save_cookies(self, driver):
        cookies = driver.get_cookies()
        with open(self.cookies_path, "wb") as f:
            pickle.dump(cookies, f)

    # 加载cookies
    def load_cookies(self, driver):
        # 清理cookies
        driver.delete_all_cookies()
        with open(self.cookies_path, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        # 本网站密码并没有保存，所以手动增加进去，而且短信验证后选中信任本机不要再短信验证，但也没有保留到cookie中
        # 所以利用cookie来自动登录对此网站无法使用
        # driver.add_cookie({"name": "fakePassword", "value": "abcd@1234"}) 找不到 输入密码的input之name，所以无效
        # 加载完cookies后再访问
        driver.refresh()  # .get("https://email.zybank.com.cn/coremail")

    """
    邮箱登录，现在是模拟输入登录，并利用浏览器的cookies下次自动登录
    后面改造成交互输入用户密码，增强安全性
    """

    def login(self):
        self.driver.get("https://email.zybank.com.cn/coremail")
        # 登陆
        # 用户名
        user_name = self.driver.find_element(by=By.XPATH, value='//input[@name="uid"]')
        if not user_name.get_attribute("value"):
            user_name.clear()
            user_name.send_keys(self.userID)
        # 密码
        pass_word = self.driver.find_element(
            by=By.XPATH,
            value='//*[@class="u-input" and @type="password" and @id="fakePassword"]',
        )
        if not pass_word.get_attribute("value"):
            pass_word.clear()
            pass_word.send_keys(self.passwd)
        # 登录
        login_button = self.driver.find_element(
            by=By.XPATH, value='//*[@class="u-btn u-btn-primary submit j-submit"]'
        )
        login_button.click()
        # time.sleep(random.randint(4, 8))
        # 如果需要验证码区域,短信验证码
        try:
            verify_code = self.driver.find_element(
                by=By.XPATH,
                value='//*[@class="u-input j-code" and @type="text"]',
            )
            verify_code.send_keys(input())
            # 重新发送获取验证码按钮，一般不需要
            # again_send_verifycode_button = self.driver.find_element(
            #     by=By.XPATH, value='//*[@class="u-btn u-btn-default send-code-btn j-send"]'
            # )
            # again_send_verifycode_button.click()
            # 选中信任本机，下次不要再要求输入短信验证码
            trust_thismachine_checkbox = self.driver.find_element(
                by=By.XPATH,
                value='//i[@class="checkbox"]',
            )
            hover = ActionChains(self.driver).move_to_element(
                trust_thismachine_checkbox
            )
            hover.perform()  # 悬停
            # 也可 .send_keys(Keys.SPACE)  checkbox radio都是这样选中或者反选
            trust_thismachine_checkbox.click()
            # time.sleep(random.randint(1, 3))
            # 确认并登录按钮
            confirm_login_button = self.driver.find_element(
                by=By.XPATH, value='//*[@class="u-btn u-btn-primary j-confirm"]'
            )
            confirm_login_button.click()
        except NoSuchElementException:
            print("不需要验证码")
        self.driver.switch_to.default_content()

    # 针对存在的草稿，上传附件并保存
    def upload_through_draft(self, get_file=None):
        get_file = os.fspath(get_file)
        # 登录邮箱
        self.login()
        # 等着退出按钮显示出来（webdriver提供的显示等待，元素级别的等待），此处显示等待不启用，使用隐式等待
        # wait = WebDriverWait(driver, timeout=30, poll_frequency=0.2)
        # presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。所以性能更快
        # visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
        # wait.until(
        #     EC.visibility_of_element_located((By.XPATH, "//a[(text(),'退出')]"))
        # )
        # 类似sleep的是强制等待，即等待这个时间后再执行下面的内容,整体用self.driver.implicitly_wait(10)代替，要不
        # 一则太多sleep,二则强制等待那么长时间不灵活
        # time.sleep(random.randint(3, 6))
        self.driver.find_element(by=By.XPATH, value='//div[text()="草稿箱"]').click()
        # time.sleep(random.randint(3, 6))
        self.driver.find_element(
            by=By.XPATH, value='//span[@class="subject" and @title="虚拟桌面申请表格"]'
        ).click()
        # time.sleep(random.randint(3, 6))
        # 找下有没有附件
        element_to_hover_overs = self.driver.find_elements(
            by=By.XPATH,
            value='//div[@class="name j-name"]',
        )
        # 删除存量邮件
        for element in element_to_hover_overs:
            # 附件的删除按钮只有鼠标悬停在相应元素上才能显示
            hover = ActionChains(self.driver).move_to_element(element)  # 找到元素
            hover.perform()  # 悬停
            # 删除一个附件
            self.driver.find_element(
                by=By.XPATH, value='//a[@class="link j-delete" and text()="删除"]'
            ).click()
            time.sleep(random.randint(3, 6))
        # 上传附件
        self.driver.find_element(
            by=By.XPATH,
            value='//input[@type="file" and @name="attachments" and @id="attachments"]',
        ).send_keys(get_file)
        # 上传成功绿色对勾出现
        self.driver.find_element(by=By.XPATH, value='//div[@class="info j-info"]')
        # 保存草稿
        self.driver.find_element(by=By.XPATH, value='//span[text()="存草稿"]').click()
        time.sleep(random.uniform(0.5, 2))
        assert "保存草稿成功" in self.driver.page_source
        logout_link = self.driver.find_element(by=By.XPATH, value="//a[text()='退出']")
        logout_link.click()
        time.sleep(random.uniform(1, 3))
        # assert "登录" in self.driver.page_source
        self.driver.quit()

    # 针对存在的草稿，下载附件并保存
    def download_through_draft(self):
        # 登录邮箱
        self.login()
        # 等着退出按钮显示出来（webdriver提供的显示等待，元素级别的等待），此处显示等待不启用，使用隐式等待
        # wait = WebDriverWait(driver, timeout=30, poll_frequency=0.2)
        # presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。所以性能更快
        # visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
        # wait.until(
        #     EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'退出')]"))
        # )
        # 类似sleep的是强制等待，即等待这个时间后再执行下面的内容,整体用self.driver.implicitly_wait(10)代替，要不
        # 一则太多sleep,二则强制等待那么长时间不灵活
        # time.sleep(random.randint(3, 6))
        self.driver.find_element(by=By.XPATH, value='//div[text()="草稿箱"]').click()
        # time.sleep(random.randint(3, 6))
        self.driver.find_element(
            by=By.XPATH, value='//span[@class="subject" and @title="虚拟桌面申请表格"]'
        ).click()
        # 找下有没有附件
        element_to_hover_overs = self.driver.find_elements(
            by=By.XPATH,
            value='//div[@class="name j-name"]',
        )
        # 下载存量邮件
        for element in element_to_hover_overs:
            # 附件的删除或下载按钮只有鼠标悬停在相应元素上才能显示
            hover = ActionChains(self.driver).move_to_element(element)  # 找到元素
            hover.perform()  # 悬停
            # 下载附件
            self.driver.find_element(
                by=By.XPATH, value='//a[@class="link j-download" and text()="下载"]'
            ).click()
            # time.sleep(random.randint(3, 6))
        logout_link = self.driver.find_element(by=By.XPATH, value="//a[text()='退出']")
        logout_link.click()
        time.sleep(random.uniform(1, 3))
        # assert "登录" in self.driver.page_source
        self.driver.quit()

    # 发送邮件，包括收件人 主题 内容及附件
    def send_mail(self, to_who, mail_title, content, get_file):
        # time.sleep(random.randint(3, 6))
        self.driver.find_element(
            by=By.XPATH,
            value='//button[@class="u-btn u-btn-default u-btn-large btn-compose j-mlsb"]//span[text()="写 信"]',
        ).click()
        # 1、收件人
        toMail = self.driver.find_element(
            by=By.XPATH, value='//a[@class="link" and @contact="to" and text()="收件人"]'
        )
        toMail.click()
        # 搜索联系人
        toMail_search_click = self.driver.find_element(
            by=By.XPATH,
            value='//div[@class="u-dialog-content"]//span[@class="u-input-container u-input-round"]',
        )
        toMail_search_click.click()
        # toMail_search = toMail_search_click.find_element(
        #     by=By.XPATH, value='//input[@class="u-input-1" and @placeholder="搜索联系人"]')
        toMail_search = self.driver.switch_to.active_element
        toMail_search.send_keys(to_who)
        # 选中联系人
        # time.sleep(random.uniform(1, 5))  # 还是等待下，要不操作太快
        toMail_select = self.driver.find_element(
            by=By.XPATH,
            value=f'//tr[@email="mengtianxiang@zybank.com.cn" and @name="{to_who}"]//i[@class="checkbox"]',
        )
        toMail_select.click()
        # 确定
        toMail_confirm = self.driver.find_element(
            by=By.XPATH,
            value='//div[@class="u-dialog-btns"]/button[@class="u-btn u-btn-primary" and @data-role="confirm" and text()="确定"]',
        )
        toMail_confirm.click()
        # 2、主题
        title = self.driver.find_element(
            by=By.XPATH, value='//input[@class="input" and @name="subject"]'
        )
        title.send_keys(mail_title)
        # 3、上传附件
        self.driver.find_element(
            by=By.XPATH,
            value='//input[@type="file" and @name="attachments" and @id="attachments"]',
        ).send_keys(os.fspath(get_file))
        # 上传成功绿色对勾出现
        self.driver.find_element(by=By.XPATH, value='//div[@class="info j-info"]')
        # 4、邮件内容
        # 切换到iframe
        self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME, "iframe")[1])
        self.driver.find_element(
            by=By.XPATH,
            value='//body[@class="ke-content"]/textarea[@class="ke-edit-textarea"]',
        ).click()
        toMail_content = self.driver.switch_to.active_element
        toMail_content.send_keys(content)
        time.sleep(random.uniform(1, 10))
        # 5、发送
        # 切换回主文档
        self.driver.switch_to.default_content()
        # 先保存下草稿
        self.driver.find_element(by=By.XPATH, value='//span[text()="存草稿"]').click()
        time.sleep(random.uniform(0.5, 2))
        assert "保存草稿成功" in self.driver.page_source
        # 发送
        self.driver.find_element(
            by=By.XPATH, value='//div[@class="toolbar j-toolbar"]/span[text()="发 送"]'
        ).click()
        time.sleep(random.uniform(0.5, 2))
        # 关闭发送信后的tab页
        self.driver.find_element(
            by=By.XPATH,
            value='//div[@class="tab-body"]/span[@class="iconfont icontabclose close" and @title="关闭"]',
        ).click()

    # 批量发送文件
    def send_mails(self, dict_list):
        # 登录邮箱
        self.login()
        for item in dict_list:
            attach_save_path = item.get("attach_save_path")
            self.send_mail(
                "孟天祥", "关于XXX的需求说明文档", "老师，请审核此需求", get_file=attach_save_path
            )
            time.sleep(random.uniform(1, 5))
        logout_link = self.driver.find_element(by=By.XPATH, value="//a[text()='退出']")
        logout_link.click()
        self.driver.quit()

    def clear_mail(self):
        pass


if __name__ == "__main__":
    sm = SeleMail()
    # sm.uploadOrDownload_through_draft(type=1)
    sm.send_mail()
