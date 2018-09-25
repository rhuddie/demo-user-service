import requests
import unittest


class RestApiTests(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.session = requests.Session()

    def test_list_users(self):
        response = self.session.get('http://127.0.0.1:5000/api/list')
        assert response.ok
        print(response.json())


if __name__ == '__main__':
    unittest.main()
