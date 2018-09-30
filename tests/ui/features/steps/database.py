from behave import step
from collections import namedtuple

from server.server import (
    User
)

TEST_USER = {
    'username': 'bilbobaggins',
    'email': 'bilbo@baggins.com',
    'dob': '22/9/54',
    'address': 'Bag End, Hobbiton'
}

UserData = namedtuple('UserData', ['username', 'email', 'dob', 'address'])


@step("I start with an empty database")
def start_empty_database(context):
    with context.session.app.app_context():
        context.session.db.session.query(User).delete()
        context.session.db.session.commit()


@step("I start with a database with test user already added")
def start_test_user_added_database(context):
    user = User(**TEST_USER)
    with context.session.app.app_context():
        context.session.db.session.query(User).delete()
        context.session.db.session.add(user)
        context.session.db.session.commit()


@step("there are {count} users in the database")
def assert_user_count(context, count):
    with context.session.app.app_context():
        users = context.session.db.session.query(User)
    obs_len = len(users.all())
    assert obs_len == int(count), f'Observed user count {obs_len} does not match expected {count}'


@step("user database contains {count} record matching: {data}")
def assert_user_exists(context, count, data):
    user_data = UserData(*data.split(', ', maxsplit=3))._asdict()
    with context.session.app.app_context():
        users = context.session.db.session.query(User).filter_by(**user_data).all()
    obs_len = len(users)
    assert obs_len == int(count), f'{count} record should exist for user, but observed {obs_len}!'
