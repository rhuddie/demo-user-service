import logging
import os


from pathlib import Path
from behave.log_capture import capture
from selenium import webdriver

from tests.ui.features.pages.base import WebdriverBase


repo_base = Path(__file__).parent.parent.absolute()
logger = logging.getLogger()


def before_all(context):
    context.base = None
    os.makedirs(os.path.join(str(repo_base), 'features', 'testresults'), exist_ok=True)
    context.repo_base = str(repo_base)


def before_scenario(context, scenario):
    desired_cap = {'chromeOptions': {'excludeSwitches': ['disable-popup-blocking']}}
    opt = webdriver.ChromeOptions()
    if os.getenv('HEADLESS', False) == '1':
        opt.add_argument('--headless')
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=opt,
                              service_args=[
                                  "--verbose",
                                  "--log-path=chromedriver.log"
                              ],
                              desired_capabilities=desired_cap)
    logger.info('Webdriver version: {}'.format(driver.capabilities['version']))
    logger.info('Chromedriver version: {}'.format(
        driver.capabilities['chrome']['chromedriverVersion']))
    context.base = WebdriverBase(context, scenario, driver)


@capture
def after_scenario(context, scenario):
    if context.base:
        context.base.driver.quit()
        del context.base.driver


def after_step(context, step):
    pass


def after_all(context):
    if hasattr(context, 'display'):
        context.display.stop()
