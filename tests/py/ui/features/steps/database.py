from behave import step

from server.server import (
    User
)
from tests.common import (
    add_test_user,
    delete_all_users,
    get_test_data_as_dict,
)


@step("I start with an empty database")
def start_empty_database(context):
    delete_all_users(context.session)


@step("I start with a database with test user already added")
def start_test_user_added_database(context):
    add_test_user(context.session)


@step("there are {count} users in the database")
def assert_user_count(context, count):
    with context.session.app.app_context():
        users = context.session.db.session.query(User)
    obs_len = len(users.all())
    assert obs_len == int(count), f'Observed user count {obs_len} does not match expected {count}'


@step("user database contains {count} record matching: {data}")
def assert_user_exists(context, count, data):
    user_data = get_test_data_as_dict(data)
    with context.session.app.app_context():
        users = context.session.db.session.query(User).filter_by(**user_data).all()
    obs_len = len(users)
    assert obs_len == int(count), f'{count} record should exist for user, but observed {obs_len}!'
