import logging

from selenium.webdriver.support.ui import WebDriverWait


class WebdriverBase:

    def __init__(self, context, scenario, driver):
        self.context = context
        self.scenario = scenario
        self.driver = driver
        self.logger = logging.getLogger("behave")

    def open_url(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
        self.wait_for_page_loaded()

    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')

    def get_wait(self, timeout):
        return WebDriverWait(self.driver, timeout)
