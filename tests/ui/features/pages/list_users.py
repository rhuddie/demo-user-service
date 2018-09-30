from selenium.common.exceptions import TimeoutException
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

    def row_count(self):
        return len(self.table)


class UserTable(CustomElement):

    def __len__(self):
        return len(self.rows)

    @property
    def rows(self):
        try:
            return self.find_custom_elements(
                UserTableRow,
                By.CSS_SELECTOR,
                'tr[id="row-data"]'
            )
        except TimeoutException:
            return []


class UserTableRow(CustomElement):

    def get_value(self, col_id):
        return self.find_custom_element(
            CustomElement,
            f'td[col-id="{col_id}"]'
        ).get_attribute('value')