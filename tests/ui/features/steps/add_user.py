from behave import step

from tests.ui.features.pages.add_user import AddUserPage


@step("I enter {field} {value}")
def enter_field_value(context, field, value):
    AddUserPage(context).set_field('input-' + field, value)


@step(u'I am on the add new user form')
def navigate_to_new_user_form(context):
    context.base.open_url('/add-user')


@step(u'I press the Add button')
def add_user(context):
    AddUserPage(context).add_button.click()


@step(u'I see user is added successfully')
def validate_user_added(context):
    pass
