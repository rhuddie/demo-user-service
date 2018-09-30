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

    def row_exists(self, **kwargs):
        return bool(self.table.get_row_with_values(**kwargs))


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

    def get_row_with_values(self, **kwargs):
        col_selector = 'td[@col-id="{}" and text()="{}"]'
        col_selectors = [col_selector.format(key, value) for key, value in kwargs.items()]
        row_selector = 'descendant::tr[' + ' and '.join(col_selectors) + ']'
        try:
            return self.find_custom_element(
                UserTableRow,
                By.XPATH,
                row_selector
            )
        except TimeoutException:
            return None


class UserTableRow(CustomElement):

    def get_value(self, col_id):
        return self.find_custom_element(
            CustomElement,
            f'td[col-id="{col_id}"]'
        ).get_attribute('value')