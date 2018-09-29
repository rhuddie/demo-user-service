from selenium.webdriver.common.by import By

from tests.ui.features.pages.base import CustomElement


class AddUserPage:
    """MFA Registration Page."""

    def __init__(self, context):
        self.base = context.base

    @property
    def form(self):
        return self.base.find_custom_element(
            AddUserForm,
            By.CSS_SELECTOR,
            'form[id="form-user-input"]'
        )

    @property
    def add_button(self):
        return self.base.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            'input[id="btn-add"]'
        )

    def set_field(self, field_id, value):
        self.form.get_field(field_id).send_keys(value)


class AddUserForm(CustomElement):

    def get_field(self, field_id):
        return self.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            f'input[id="{field_id}"]'
        )
