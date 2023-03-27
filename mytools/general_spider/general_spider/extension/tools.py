import functools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def waitForXpath(
    browser, select_arg, select_method=By.XPATH, timeout=2, is_elements=False
):
    """
    阻塞等待某个元素的出现直到timeout结束

    :param browser:浏览器实例
    :param select_method:所使用的选择器方法
    :param select_arg:选择器参数
    :param timeout:超时时间
    :return:
    """
    wait = WebDriverWait(browser, timeout)
    if is_elements:
        element = wait.until(
            EC.presence_of_all_elements_located((select_method, select_arg))
        )
    else:
        element = wait.until(
            EC.presence_of_element_located((select_method, select_arg))
        )
    return element


def waitNotForXpath(
    browser, select_arg, select_method=By.XPATH, timeout=2, is_elements=False
):
    """
    阻塞等待某个元素的出现直到timeout结束

    :param browser:浏览器实例
    :param select_method:所使用的选择器方法
    :param select_arg:选择器参数
    :param timeout:超时时间
    :return:
    """
    wait = WebDriverWait(browser, timeout)
    if is_elements:
        element = wait.until_not(
            EC.presence_of_all_elements_located((select_method, select_arg))
        )
    else:
        element = wait.until_not(
            EC.presence_of_element_located((select_method, select_arg))
        )
    return element
