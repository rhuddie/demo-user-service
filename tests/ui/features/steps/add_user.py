from behave import step

from tests.ui.features.pages.add_user import AddUserPage


@step("I enter {field} {value}")
def enter_field_value(context, field, value):
    AddUserPage(context).set_field('input-' + field, value)


@step('I am on the add new user form')
def navigate_to_new_user_form(context):
    context.base.open_url('/add-user')


@step('I press the Add button')
def add_user(context):
    AddUserPage(context).add_user()


@step('I see user is added successfully')
def validate_user_added(context):
    page = AddUserPage(context)
    status = page.status
    msg = status.message
    assert status.is_success() and msg == "User successfully added!", (
        f'User was not added successfully :: Message type: "{status.message_type}" :: "{msg}"')


@step("I see user was not added successfully")
def validate_user_add_error(context):
    page = AddUserPage(context)
    status = page.status
    msg = status.message
    assert status.is_error() and msg.startswith("Error adding user:"), (
        f'User was not added successfully :: Message type: "{status.message_type}" :: "{msg}"')

