import unittest
import json
from flask_api import status
import server

class TestServer(unittest.TestCase):
    """ Shopcarts Server Tests """
    def setUp(self):
        self.app = server.app.test_client()
        server.Shopcart(1).save()
        server.Shopcart(2).save()

    def tearDown(self):
        server.Shopcart.remove_all()

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
        self.assertEqual( resp.status_code, status.HTTP_200_OK )
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual (data['uid'], 1)
        self.assertEqual (data['products'], {})

    def test_get_nonexistent_shopcart(self):
        """ Test Get a Non-Existent Shopcart """
        resp = self.app.get('/shopcarts/3')
        self.assertEqual( resp.status_code, status.HTTP_404_NOT_FOUND )
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual (data['error'], 'Shopcart with id: 3 was not found')
    
    def test_delete_shopcart(self):
        """ Delete a Shopcart that exists """
        cart_count = len(server.Shopcart.all())
        resp = self.app.delete('/shopcarts/1')

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        self.assertEqual(len(server.Shopcart.all()), cart_count - 1)
    
    def test_delete_nonexistent_shopcart(self):
        """ Delete a Shopcart that doesn't exist """
        cart_count = len(server.Shopcart.all())
        resp = self.app.delete('/shopcarts/5')

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        self.assertEqual(len(server.Shopcart.all()), cart_count)

if __name__ == '__main__':
    unittest.main()
