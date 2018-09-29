from selenium.webdriver.common.by import By

from tests.ui.features.pages.base import CustomElement


class ListUsersPage:

    def __init__(self, context):
        self.base = context.base

    @property
    def table(self):
        return self.base.find_custom_element(
            UserTable,
            By.CSS_SELECTOR,
            'table[id="table-users"]'
        )


class UserTable(CustomElement):

    @property
    def rows(self):
        # TODO: add rows with find custom elements