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
        self.assertEqual(data['name'], 'Shopcarts REST API Service')
        self.assertEqual(data['description'], 'This is the REST API Service for the shopcarts.')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_shopcart(self):
        """ Test Get a Shopcart """
        # Test for existing shopcarts
        resp = self.app.get('/shopcarts/1')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual (data['uid'], 1)
        self.assertEqual (data['products'], {})

        resp = self.app.get('/shopcarts/2')
        self.assertEqual( resp.status_code, HTTP_200_OK )
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual (data['uid'], 2)
        self.assertEqual (data['products'], {})

        # Test for non-existent shopcart
        resp = self.app.get('/shopcarts/3')
        self.assertEqual( resp.status_code, HTTP_404_NOT_FOUND )
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual (data['error'], 'Shopcart with id: 3 was not found')


if __name__ == '__main__':
    unittest.main()
