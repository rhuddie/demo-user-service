from collections import namedtuple


UserData = namedtuple('UserData', ['username', 'email', 'dob', 'address'])

TEST_USER = {
    'username': 'bilbobaggins',
    'email': 'bilbo@baggins.com',
    'dob': '22/9/1954',
    'address': 'Bag End, Hobbiton'
}


def get_test_data_as_dict(data):
    return UserData(*data.split(', ', maxsplit=3))._asdict()
