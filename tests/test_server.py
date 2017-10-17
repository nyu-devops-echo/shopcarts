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
        cart = {'uid': 3 }
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
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
        cart = {'uid': 3 , "products":'prod1'}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        cart= {'uid': 3 , "products":-12}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        cart= {'uid': 3 , 'products':[]}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_shopcart_with_a_prod(self):
        """ Create a cart uid 3 with a product id 5"""
        n_cart = len(server.Shopcart.all())
        cart= {'uid': 3 , "products":5}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        data = json.loads(resp.data.decode('utf8'))
        self.assertIn('/shopcarts/3',location  )
        self.assertEqual( data['products'] , {'5':1} )
        self.assertEqual(len(server.Shopcart.all()),n_cart+1 )

    def test_create_shopcart_prods(self):
        """ Create a shopcart with many products"""
        n_cart = len(server.Shopcart.all())
        # add a new shopcart with many products
        new_shopcart = {"uid":3 , "products": { 8:13 , 21:34 } }
        data = json.dumps( new_shopcart )
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        self.assertIn('/shopcarts',location  )

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products'], {"8":13,"21":34})
        self.assertEqual(len(server.Shopcart.all()),n_cart+1 )

    def test_create_shopcart_invalid_prods(self):
        """ Create a shopcart with invalid products """
        new_shopcart = {'uid':3, 'products': { 'prod1':'13'} }
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart_that_exists(self):
        """ Create a shopcart that exists"""
        n_cart = len(server.Shopcart.all())
        cart = server.Shopcart.find(1)
        self.assertIsNotNone(cart)
        data = json.dumps(cart.serialize())
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(n_cart, len(server.Shopcart.all()) )

    def test_create_without_uid(self):
        """ Create a shopcart without id"""
        n_cart = len(server.Shopcart.all())
        cart = {}
        data = json.dumps(cart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(n_cart, len(server.Shopcart.all()) )

    def test_update_product(self):
        """Updating a product"""
        cart = server.Shopcart.find(2)

        self.assertIsNotNone(cart)
        cart.add_product(pid=2,quant=3)
        cart.add_product( pid = 3, quant= 5 )
        
        prods_in_cart = cart.serialize()['products']
        self.assertEqual(prods_in_cart, {2:3,3:5} )
        
        pid_to_update= 3
        quant_to_update= 2
        data = json.dumps( {'products': {pid_to_update:quant_to_update} } )
        
        resp = self.app.put('/shopcarts/2/products/' + str(pid_to_update), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        new_json = json.loads(resp.data.decode('utf8'))
        self.assertEqual(new_json['products']["3"], 2 )

    def test_update_product_not_existing_shopcart(self):
        """Updating a product of an unexistent shopcart"""
        self.assertIsNone(server.Shopcart.find(3) )
        pid_to_update= 3
        quant_to_update= 2
        data = json.dumps( {'products': {pid_to_update:quant_to_update} } )
        
        resp = self.app.put('/shopcarts/3/products/' + str(pid_to_update), data=data, content_type='application/json')
        
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_not_existing_before(self):
        """Updating a product of an unexiting product in an existing cart"""
        cart = server.Shopcart.find(2)
        self.assertIsNotNone(cart)        
        prods_in_cart = cart.serialize()['products']
        self.assertEqual(prods_in_cart, {} )
        
        pid_to_update = 1
        quant_to_update = 7
        self.assertNotIn( pid_to_update, prods_in_cart.keys() )
        
        data = json.dumps( {'products': {pid_to_update:quant_to_update} } )
        resp = self.app.put('/shopcarts/2/products/' + str(pid_to_update), 
                            data=data, content_type='application/json')
        
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_content_type_media_error(self):
        """Not supported media"""    
        data = '6'    
        resp = self.app.put('/shopcarts/3/products/' + str(1), 
                            data=data, content_type='application/text')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE )





if __name__ == '__main__':
    unittest.main()
