import os
import pickle
import random

# 导入显示等待类
from selenium.webdriver.support.ui import WebDriverWait

# 导入期望场景类
from selenium.webdriver.support import expected_conditions as EC

# 导入By类
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.action_chains import ActionChains
import time
from pathlib import Path
from myutils import web_driver_manager
from myutils.info_out_manager import get_temp_folder
cookies_path = Path("D:/tmp/db_cookie_1")

# 保存cookies


def save_cookies(driver):
    cookies = driver.get_cookies()
    with open(cookies_path, "wb") as f:
        pickle.dump(cookies, f)

# 加载cookies


def load_cookies(driver):
    # 清理cookies
    driver.delete_all_cookies()
    with open(cookies_path, "rb") as f:
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


def login():
    # 下面两个都行
    driver = web_driver_manager.get_driver_ChromeDriver()
    #
    # driver = WebDriverManager().get_driver_Chromeexe()
    driver.get("https://email.zybank.com.cn/coremail")
    # 最大化窗口
    driver.maximize_window()
    # 登陆
    # 用户名
    user_name = driver.find_element(by=By.XPATH, value='//input[@name="uid"]')
    if not user_name.get_attribute("value"):
        user_name.clear()
        user_name.send_keys("loubenlei@zybank.com.cn")
    # 密码
    pass_word = driver.find_element(
        by=By.XPATH,
        value='//*[@class="u-input" and @type="password" and @id="fakePassword"]',
    )
    if not pass_word.get_attribute("value"):
        pass_word.clear()
        pass_word.send_keys("******")
    # 登录
    login_button = driver.find_element(
        by=By.XPATH, value='//*[@class="u-btn u-btn-primary submit j-submit"]'
    )
    login_button.click()
    # time.sleep(random.randint(4, 8))
    # 如果需要验证码区域,短信验证码
    try:
        verify_code = driver.find_element(
            by=By.XPATH,
            value='//*[@class="u-input j-code" and @type="text"]',
        )
        verify_code.send_keys(input())
        # 重新发送获取验证码按钮，一般不需要
        # again_send_verifycode_button = driver.find_element(
        #     by=By.XPATH, value='//*[@class="u-btn u-btn-default send-code-btn j-send"]'
        # )
        # again_send_verifycode_button.click()
        # 选中信任本机，下次不要再要求输入短信验证码
        trust_thismachine_checkbox = driver.find_element(
            by=By.XPATH,
            value='//i[@class="checkbox"]',
        )
        hover = ActionChains(driver).move_to_element(
            trust_thismachine_checkbox)
        hover.perform()  # 悬停
        # 也可 .send_keys(Keys.SPACE)  checkbox radio都是这样选中或者反选
        trust_thismachine_checkbox.click()
        # time.sleep(random.randint(1, 3))
        # 确认并登录按钮
        confirm_login_button = driver.find_element(
            by=By.XPATH, value='//*[@class="u-btn u-btn-primary j-confirm"]'
        )
        confirm_login_button.click()
    except NoSuchElementException:
        print("不需要验证码")
    driver.switch_to.default_content()
    return driver


# 针对存在的草稿，上传附件并保存
def uploadOrDownload_through_draft(type=0):
    # 登录邮箱
    driver = login()
    # 等着退出按钮显示出来（webdriver提供的显示等待，元素级别的等待），此处显示等待不启用，使用隐式等待
    # wait = WebDriverWait(driver, timeout=30, poll_frequency=0.2)
    # presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。所以性能更快
    # visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
    # wait.until(
    #     EC.visibility_of_element_located((By.XPATH, "//a[contains(text(),'退出')]"))
    # )
    # 类似sleep的是强制等待，即等待这个时间后再执行下面的内容,整体用driver.implicitly_wait(10)代替，要不
    # 一则太多sleep,二则强制等待那么长时间不灵活
    # time.sleep(random.randint(3, 6))
    driver.find_element(by=By.XPATH, value='//div[text()="草稿箱"]').click()
    # time.sleep(random.randint(3, 6))
    driver.find_element(
        by=By.XPATH, value='//span[@class="subject" and @title="虚拟桌面申请表格"]'
    ).click()
    # time.sleep(random.randint(3, 6))
    # 找下有没有附件
    element_to_hover_overs = driver.find_elements(
        by=By.XPATH,
        value='//div[@class="name j-name"]',
    )
    # 上传附件到草稿箱
    if type == 0:
        out_folder = get_temp_folder(
            des_folder_name='spiders_out', is_clear_folder=False)
        out_finished = f"{out_folder}/PingDingGov_finished.txt"
        while not Path(out_finished).exists():
            time.sleep(1)
        # 删除存量邮件
        for element in element_to_hover_overs:
            # 附件的删除按钮只有鼠标悬停在相应元素上才能显示
            hover = ActionChains(driver).move_to_element(element)  # 找到元素
            hover.perform()  # 悬停
            # 删除一个附件
            driver.find_element(
                by=By.XPATH, value='//a[@class="link j-delete" and text()="删除"]'
            ).click()
            time.sleep(random.randint(3, 6))
        # 上传附件
        driver.find_element(
            by=By.XPATH,
            value='//input[@type="file" and @name="attachments" and @id="attachments"]',
        ).send_keys(str(out_finished))
        # 上传成功绿色对勾出现
        driver.find_element(
            by=By.XPATH, value='//div[@class="info j-info"]')
        # 保存草稿
        driver.find_element(
            by=By.XPATH, value='//span[text()="存草稿"]').click()
        time.sleep(random.uniform(0.5, 2))
        assert "保存草稿成功" in driver.page_source
        # # 判断文件是否存在，删除已上传的文件
        if os.path.exists(out_finished):
            # 存在，则删除文件
            os.remove(out_finished)
    elif type == 1:
        # 下载存量邮件
        for element in element_to_hover_overs:
            # 附件的删除或下载按钮只有鼠标悬停在相应元素上才能显示
            hover = ActionChains(driver).move_to_element(element)  # 找到元素
            hover.perform()  # 悬停
            # 下载附件
            driver.find_element(
                by=By.XPATH, value='//a[@class="link j-download" and text()="下载"]'
            ).click()
            time.sleep(random.randint(3, 6))
    logout_link = driver.find_element(by=By.XPATH, value="//a[text()='退出']")
    logout_link.click()
    time.sleep(random.uniform(1, 3))
    # assert "登录" in driver.page_source
    driver.quit()
# 发送邮件，包括收件人 主题 内容及附件


def send_mail(type=0):
    # 登录邮箱
    driver = login()
    # time.sleep(random.randint(3, 6))
    driver.find_element(
        by=By.XPATH, value='//button[@class="u-btn u-btn-default u-btn-large btn-compose j-mlsb"]//span[text()="写 信"]').click()
    # 1、收件人
    toMail = driver.find_element(
        by=By.XPATH, value='//a[@class="link" and @contact="to" and text()="收件人"]')
    toMail.click()
    # 搜索联系人
    toMail_search_click = driver.find_element(
        by=By.XPATH, value='//div[@class="u-dialog-content"]//span[@class="u-input-container u-input-round"]')
    toMail_search_click.click()
    # toMail_search = toMail_search_click.find_element(
    #     by=By.XPATH, value='//input[@class="u-input-1" and @placeholder="搜索联系人"]')
    toMail_search = driver.switch_to.active_element
    toMail_search.send_keys("孟天祥")
    # 选中联系人
    toMail_select = driver.find_element(
        by=By.XPATH, value='//tr[@email="mengtianxiang@zybank.com.cn" and @name="孟天祥"]')
    toMail_select.click()
    # 确定
    toMail_confirm = driver.find_element(
        by=By.XPATH, value='//div[@class="u-dialog-btns"]/button[@class="u-btn u-btn-primary" and @data-role="confirm" and text()="确定"]')
    toMail_confirm.click()
    # 2、主题
    title = driver.find_element(
        by=By.XPATH, value='//input[@class="input" and @name="subject"]')
    title.send_keys("需求审核文档")
    # 3、上传附件
    # 找下有没有附件
    element_to_hover_overs = driver.find_elements(
        by=By.XPATH,
        value='//div[@class="name j-name"]',
    )
    # 上传附件到草稿箱
    out_folder = get_temp_folder(
        des_folder_name='spiders_out', is_clear_folder=False)
    out_finished = f"{out_folder}/新建 DOCX 文档.docx"
    while not Path(out_finished).exists():
        time.sleep(1)
    # 删除存量邮件
    for element in element_to_hover_overs:
        # 附件的删除按钮只有鼠标悬停在相应元素上才能显示
        hover = ActionChains(driver).move_to_element(element)  # 找到元素
        hover.perform()  # 悬停
        # 删除一个附件
        driver.find_element(
            by=By.XPATH, value='//a[@class="link j-delete" and text()="删除"]'
        ).click()
        time.sleep(random.randint(3, 6))
    # 上传附件
    driver.find_element(
        by=By.XPATH,
        value='//input[@type="file" and @name="attachments" and @id="attachments"]',
    ).send_keys(str(out_finished))
    # 上传成功绿色对勾出现
    driver.find_element(
        by=By.XPATH, value='//div[@class="info j-info"]')
    # 保存草稿
    driver.find_element(
        by=By.XPATH, value='//span[text()="存草稿"]').click()
    time.sleep(random.uniform(0.5, 2))
    assert "保存草稿成功" in driver.page_source
    # 4、邮件内容
    # 切换到iframe
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])
    content_body = driver.find_element(
        by=By.XPATH, value='//body[@class="ke-content"]').click()
    toMail_content = driver.switch_to.active_element
    toMail_content.send_keys("你好，天祥，请审核！")
    # 5、发送
    # 切换回主文档
    driver.switch_to.default_content()
    driver.find_element(
        by=By.XPATH, value='//div[@class="toolbar j-toolbar"]/span[text()="发 送"]').click()
    # # 判断文件是否存在，删除已上传的文件
    # if os.path.exists(out_finished):
    #     # 存在，则删除文件
    #     os.remove(out_finished)
    logout_link = driver.find_element(by=By.XPATH, value="//a[text()='退出']")
    logout_link.click()
    time.sleep(random.uniform(1, 3))
    # assert "登录" in driver.page_source
    driver.quit()


if __name__ == "__main__":
    # uploadOrDownload_through_draft(type=1)
    send_mail()
