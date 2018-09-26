import pytest
import requests

from server.server import (
    configure_service,
    get_db_path,
)


@pytest.fixture(scope="module")
def request_session():
    return requests.Session()


@pytest.fixture(scope="module")
def application():
    return configure_service(get_db_path('testing.db'))[0]


@pytest.fixture(scope="module")
def api():
    return configure_service(get_db_path('testing.db'))[1]


def test_api_list(api):
    with api.app.test_client() as c:
        r = c.get('/api/list')
        assert r.status_code == 200
        print(r.data)


def test_list_users(application):
    with application.test_client() as c:
        # This works with html page not rest api
        r = c.get('/list-users')
        assert r.status_code == 200
        print(r.data)