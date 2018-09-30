from collections import namedtuple


UserData = namedtuple('UserData', ['username', 'email', 'dob', 'address'])


def get_test_data_as_dict(data):
    return UserData(*data.split(', ', maxsplit=3))._asdict()
