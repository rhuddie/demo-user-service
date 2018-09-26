import pytest

from server.server import (
    configure_service,
    get_db_path,
)


@pytest.fixture(scope="module")
def app_session():
    return configure_service(get_db_path('testing.db'))


def test_api_list(app_session):
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