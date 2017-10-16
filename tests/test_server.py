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


    def test_create_shopcart(self):
        """ Create an empty shopcart POST on shopcarts"""
        # add a new shopcart 
        n_cart = len(server.Shopcart.all())
        cart = {'uid':3 }
        resp = self.app.put('/shopcarts/3', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        data = json.loads(resp.data.decode('utf8'))
        self.assertIn('/shopcarts/3',location  )
        #Actually saved
        self.assertEqual(len(server.Shopcart.all()),n_cart+1 )

    def test_create_shopcart_invalid_data(self):
        """ Create a cart with invalid data"""
        # add a new shopcart 
        new = {'uid':'one'}
        resp = self.app.put('/shopcarts/3', data=json.dumps(new), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_shopcart_invalid_prod_data(self):
        """ Create a cart with invalid  product data"""
        # add a new shopcart 
        prods = 3
        resp = self.app.put('/shopcarts/3', data=json.dumps(prods), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_shopcart_one_prods(self):
        """ Create a shopcart with one product id POST request"""        
        # add a new shopcart with one product
        n_cart = len(server.Shopcart.all())
        cart = {'uid':3, 'products':21}
        data = json.dumps(cart)
        resp = self.app.put('/shopcarts/1', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        self.assertIn('/shopcarts/3',location  )
        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products'], {'21':1} )
        #Actually saved
        self.assertEqual(len(server.Shopcart.all()),n_cart+1 )


    def test_create_shopcart_prods(self):
        """ Create a shopcart with many products POST request"""
        n_cart = len(server.Shopcart.all())
        # add a new shopcart with many products
        new_shopcart = { 'uid':3, "products": { 8:13 , 21:34 } }
        data = json.dumps( new_shopcart )
        resp = self.app.put('/shopcarts/3', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        self.assertIn('/shopcarts/3',location  )

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products'], {"8":13,"21":34})
        self.assertEqual(len(server.Shopcart.all()),n_cart+1 )


    def test_create_shopcart_invalid_prods(self):
        """ Create a shopcart with invalid products POST request"""
        # add a new shopcart with many products
        new_shopcart = { 'uid':3, 'products': { 'prod1':'13'} }
        data = json.dumps(new_shopcart)
        resp = self.app.put('/shopcarts/3', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
