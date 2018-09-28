import logging
import os


from pathlib import Path
from behave.log_capture import capture
from selenium import webdriver

from server.tests.ui.features.pages.base import WebdriverBase


repo_base = Path(__file__).parent.parent.absolute()
logger = logging.getLogger()


def before_all(context):
    context.driver = None
    os.makedirs(os.path.join(str(repo_base), 'features', 'testresults'), exist_ok=True)
    context.repo_base = str(repo_base)


def before_scenario(context, scenario):
    desired_cap = {'chromeOptions': {'excludeSwitches': ['disable-popup-blocking']}}
    driver = webdriver.Chrome(desired_capabilities=desired_cap)
    logger.info('Webdriver version: {}'.format(driver.capabilities['version']))
    logger.info('Chromedriver version: {}'.format(
        driver.capabilities['chrome']['chromedriverVersion']))
    context.base = WebdriverBase(context, scenario, driver)


@capture
def after_scenario(context, scenario):
    if context.driver:
        context.driver.quit()
    del context.base


def after_step(context, step):
    pass


def after_all(context):
    context.driver = None
    if hasattr(context, 'display'):
        context.display.stop()
