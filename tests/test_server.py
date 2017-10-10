import unittest
import json
from flask_api import status
import server

class TestServer(unittest.TestCase):
    """ Shopcarts Server Tests """

    def setUp(self):
        self.app = server.app.test_client()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')

        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data, 'Home')

if __name__ == '__main__':
    unittest.main()
