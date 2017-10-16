import unittest
import json
from flask_api import status
import server
# from models.shopcart import Shopcart
# from models.dataerror import DataValidationError

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


    def test_create_shopcart(self):
        """ Create an empty shopcart POST on shopcarts"""
        # add a new shopcart 
        cart = {'uid':3}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        # data = json.loads(resp.data.decode('utf8'))
        # self.assertEqual(location, data['Location'] )

    def test_create_shopcart_invalid_data(self):
        """ Create a cart with invalid data"""
        # add a new shopcart 
        prods = [1]
        resp = self.app.post('/shopcarts', data=json.dumps(prods), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_shopcart_one_prods(self):
        """ Create a shopcart with one product id PUT request"""        
        # add a new shopcart with one product
        cart = {'products':21}
        data = json.dumps(cart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products'], {'21':1} )

    def test_create_shopcart_prods(self):
        """ Create a shopcart with many products PUT request"""
        
        # add a new shopcart with many products
        new_shopcart = { "products": { 8:13 , 21:34 } }
        data = json.dumps( new_shopcart )
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products'], {"8":13,"21":34})

    def test_create_shopcart_invalid_prods(self):
        """ Create a shopcart with invalid products PUT request"""
        # add a new shopcart with many products
        new_shopcart = { 'products': { 'prod1':'13'} }
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
if __name__ == '__main__':
    unittest.main()
