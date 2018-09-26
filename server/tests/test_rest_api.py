import os
import pytest

from server.server import (
    configure_service,
    get_db_path,
    User,
)

TEST_USER = {'username': 'aa', 'email': 'bb', 'dob': 'cc', 'address': 'dd'}


def delete_test_user(session):
    with session.app.app_context():
        User.query.filter(**TEST_USER).delete()
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
def add_test_user_session(app_session):
    user = User(**TEST_USER)
    with app_session.app.app_context():
        app_session.db.session.add(user)
        app_session.db.session.commit()
        print('DONE')
    yield app_session
    delete_test_user(app_session)


def test_api_add_user(app_session):
    with app_session.api.app.test_client() as c:
        r = c.post('/api/add', data=TEST_USER)
        assert r.status_code == 200
        print(r.data)
        # TODO make this cleanup step
        delete_test_user(app_session)


def test_api_list_existing_user(add_test_user_session):
    with add_test_user_session.api.app.test_client() as c:
        r = c.get('/api/list')
        assert r.status_code == 200
        print(r.data)


def test_api_list_no_users(app_session):
    with app_session.api.app.test_client() as c:
        r = c.get('/api/list')
        assert r.status_code == 200
        print(r.data)


def test_list_users(app_session):
    with app_session.app.test_client() as c:
        # This works with html page not rest api
        r = c.get('/list-users')
        assert r.status_code == 200
        print(r.data)