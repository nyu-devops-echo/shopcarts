import unittest
import json
from flask_api import status
import server
from models.shopcart import Shopcart
from models.dataerror import DataValidationError

class TestServer(unittest.TestCase):
    """ Shopcarts Server Tests """
    def setUp(self):
        self.app = server.app.test_client()
        server.Shopcart(1).save()
        server.Shopcart(2).save()
        server.Shopcart().save()

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

    def test_create_an_existing_shopcart(self):
        """ Create an existing shopcart PUT request"""
        # Get an existing shopcart
        cart = Shopcart.find(1)
        self.assertIsNotNone(cart)
        # add this shopcart
        new_shopcart = {'uid': cart.uid }
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts/', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart(self):
        """ Create a shopcart PUT request"""
        #Check for exists
        cart = Shopcart.find(5)
        self.assertIsNone(cart)
        # add a new shopcart 
        new_shopcart = {'uid': 5 }
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts/', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['uid'], 5)

    def test_create_shopcart_prods(self):
        """ Create a shopcart with many products PUT request"""
        
        # add a new shopcart with many products
        new_shopcart = {'uid': 5 , 'products':{8:13,21:34}}
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts/', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json, json.loads(data))

    # def test_create_shopcart_one_prods(self):
    #     """ Create a shopcart with one product id PUT request"""
        
    #     # add a new shopcart with one products
    #     new_shopcart = {'uid': 5 , 'products':21}
    #     data = json.dumps(new_shopcart)
    #     resp = self.app.post('/shopcarts/', data=data, content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
    #     # Make sure location header is set
    #     location = resp.headers.get('Location', None)
    #     self.assertIsNotNone(location)

    #     # Check the data is correct
    #     new_json = json.loads(resp.data.decode('utf8'))
    #     data=json.loads( json.dumps( {'uid': 5 , 'products':{21:1} }) )
    #     self.assertEqual(new_json, data)

    # def test_create_shopcart_invalid_prods(self):
    #     """ Create a shopcart with invalid products PUT request"""
    #     # add a new shopcart with many products
    #     new_shopcart = {'uid': 5 , 'products':{'prod1':13}}
    #     data = json.dumps(new_shopcart)
    #     resp = self.app.post('/shopcarts/', data=data, content_type='application/json')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        


if __name__ == '__main__':
    unittest.main()
