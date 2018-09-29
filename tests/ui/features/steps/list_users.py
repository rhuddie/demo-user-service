from behave import step

from tests.ui.features.pages.list_users import ListUsersPage


@step('I am on the list users form')
def navigate_to_new_user_form(context):
    context.base.open_url('/list-users')


@step('I see {count} users listed')
def add_user(context, count):
    ListUsersPage(context)
