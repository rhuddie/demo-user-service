from collections import namedtuple

from server.server import (
    User
)

UserData = namedtuple('UserData', ['username', 'email', 'dob', 'address'])

TEST_USER = {
    'username': 'bilbobaggins',
    'email': 'bilbo@baggins.com',
    'dob': '22/9/1954',
    'address': 'Bag End, Hobbiton'
}


def get_test_data_as_dict(data):
    return UserData(*data.split(', ', maxsplit=3))._asdict()


def delete_test_user(session):
    with session.app.app_context():
        User.query.filter_by(**TEST_USER).delete()
        session.db.session.commit()


def delete_all_users(session):
    with session.app.app_context():
        session.db.session.query(User).delete()
        session.db.session.commit()


def add_test_user(session):
    user = User(**TEST_USER)
    with session.app.app_context():
        session.db.session.query(User).delete()
        session.db.session.add(user)
        session.db.session.commit()
