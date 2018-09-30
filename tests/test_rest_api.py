import os
import pytest

from server.server import (
    configure_service,
    get_db_path,
    User,
)
from tests.common import TEST_USER


def delete_test_user(session):
    with session.app.app_context():
        User.query.filter_by(**TEST_USER).delete()
        session.db.session.commit()


def delete_all_users(session):
    with session.app.app_context():
        session.db.session.query(User).delete()
        session.db.session.commit()


@pytest.fixture(scope="module")
def app_session(request):
    db_path = get_db_path('testing.db')
    srv = configure_service(db_path)

    def delete_db():
        os.unlink(db_path)
    request.addfinalizer(delete_db)
    return srv


@pytest.fixture(scope="function")
def populated_database(app_session):
    user = User(**TEST_USER)
    with app_session.app.app_context():
        app_session.db.session.add(user)
        app_session.db.session.commit()
    yield app_session
    delete_test_user(app_session)


@pytest.fixture(scope="function")
def empty_database(app_session):
    delete_all_users(app_session)
    yield app_session
    delete_all_users(app_session)


def test_api_add_user(empty_database):
    with empty_database.api.app.test_client() as c:
        r = c.post('/api/add', data=TEST_USER)
        assert r.status_code == 200


def test_api_add_user_invalid_email(empty_database):
    user = TEST_USER
    user['email'] = 'invalidemail.com'
    with empty_database.api.app.test_client() as c:
        r = c.post('/api/add', data=user)
        assert r.status_code == 500


def test_api_add_user_invalid_dob(empty_database):
    user = TEST_USER
    user['dob'] = 'invaliddate'
    with empty_database.api.app.test_client() as c:
        r = c.post('/api/add', data=user)
        assert r.status_code == 500


def test_api_add_user_incomplete_data(empty_database):
    user = TEST_USER.copy()
    user.pop('address')
    with empty_database.api.app.test_client() as c:
        r = c.post('/api/add', data=user)
        assert r.status_code == 500


def test_api_add_duplicate_user(populated_database):
    with populated_database.api.app.test_client() as c:
        r = c.post('/api/add', data=TEST_USER)
        assert r.status_code == 500


def test_api_list_existing_user(populated_database):
    with populated_database.api.app.test_client() as c:
        r = c.get('/api/list')
        assert r.status_code == 200


def test_api_list_no_users(empty_database):
    with empty_database.api.app.test_client() as c:
        r = c.get('/api/list')
        assert r.status_code == 200
