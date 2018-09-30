from behave import step

from server.server import (
    User
)

TEST_USER = {
    'username': 'bilbobaggins',
    'email': 'bilbo@baggins.com',
    'dob': '22/9/54',
    'address': 'Bag End, Hobbiton'
}


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
