from selenium.webdriver.common.by import By

from tests.ui.features.pages.base import CustomElement


class AddUserPage:

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
    def status(self):
        return self.base.find_custom_element(
            AddUserStatus,
            By.CSS_SELECTOR,
            'p[id="status-text"]'
        )

    def set_field(self, field_id, value):
        self.form.get_field(field_id).send_keys(value)

    def reset_form(self):
        self.form.reset_button.click()

    def go_to_list_view(self):
        self.form.list_button.click()

    def add_user(self):
        self.form.add_button.click()
        self.status.wait_until_visible()


class AddUserForm(CustomElement):

    @property
    def add_button(self):
        return self.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            'input[id="btn-add"]'
        )

    @property
    def list_button(self):
        return self.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            'input[id="btn-list"]'
        )

    @property
    def reset_button(self):
        return self.base.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            'input[id="btn-reset"]'
        )

    def get_field(self, field_id):
        return self.find_custom_element(
            CustomElement,
            By.CSS_SELECTOR,
            f'input[id="{field_id}"]'
        )


class AddUserStatus(CustomElement):

    @property
    def message(self):
        return self.text

    @property
    def message_type(self):
        return self.get_attribute('type')

    def is_success(self):
        return self.get_attribute('type') == 'success'

    def is_error(self):
        return self.get_attribute('type') == 'error'

    def wait_until_visible(self):
        self.get_wait(10).until(lambda driver: self.message_type != 'hidden')
