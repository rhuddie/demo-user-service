from behave import step

from tests.ui.features.pages.list_users import ListUsersPage
from tests.ui.features.steps.common import get_test_data_as_dict


@step('I am on the list users form')
def navigate_to_new_user_form(context):
    context.base.open_url('/list-users')


@step('I see {count} users listed')
def add_user(context, count):
    obs_count = ListUsersPage(context).row_count()
    assert obs_count == int(count), f'Expected count {count} does not match observed count {obs_count}!'


@step(u'I see a record with values: {data}')
def step_impl(context, data):
    user_dict = get_test_data_as_dict(data)
    exists = ListUsersPage(context).row_exists(**user_dict)
    assert exists, f'Row does not exist with expected data: {data}'
