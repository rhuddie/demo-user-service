import pytest
import requests


@pytest.fixture(scope="module")
def request_session():
    return requests.Session()


def test_list_users(request_session):
    response = request_session.get('http://127.0.0.1:5000/api/list')
    assert response.ok
    print(response.json())
