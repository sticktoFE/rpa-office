import functools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def waitFor(browser, select_arg, select_method, timeout=2):
    """
    阻塞等待某个元素的出现直到timeout结束
    
    :param browser:浏览器实例
    :param select_method:所使用的选择器方法
    :param select_arg:选择器参数
    :param timeout:超时时间
    :return:
    """
    element = WebDriverWait(browser, timeout).until(
        EC.presence_of_element_located((select_method, select_arg))
    )
    return element
    
# 用xpath选择器等待元素
waitForXpath = functools.partial(waitFor, select_method=By.XPATH)

# 用css选择器等待元素
waitForCss = functools.partial(waitFor, select_method=By.CSS_SELECTOR)