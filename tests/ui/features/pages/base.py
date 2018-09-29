import logging
import os

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait


def find_custom_element(root, cls, by, selector, timeout):
    element = WebDriverWait(root, timeout).until(
        lambda driver: root.find_element(by, selector),
        message="Could not find object using selector: {}".format(selector))
    element.__class__ = cls
    return element


class WebdriverBase:

    def __init__(self, context, scenario, driver):
        self.context = context
        self.scenario = scenario
        self.driver = driver
        self.logger = logging.getLogger("behave")
        port = os.getenv('SERVER_PORT', '5000')
        self.base_url = f'http://127.0.0.1:{port}'

    def open_url(self, url):
        self.driver.get(self.base_url + url)
        self.driver.maximize_window()

    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')

    def get_wait(self, timeout):
        return WebDriverWait(self.driver, timeout)

    def find_custom_element(self, cls, by, selector, timeout=0):
        return find_custom_element(self.driver, cls, by, selector, timeout)


class CustomElement(WebElement):

    def get_wait(self, timeout):
        return WebDriverWait(self.parent, timeout)

    def find_custom_element(self, cls, by, selector, timeout=0):
        return find_custom_element(self, cls, by, selector, timeout)
