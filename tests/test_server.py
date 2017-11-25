import unittest
import json
from flask_api import status
from app import server
from app.models import db

class TestServer(unittest.TestCase):
    """ Shopcarts Server Tests """
    def setUp(self):
        self.app = server.app.test_client()
        server.app.debug = True
        server.app.app_context().push()

        # Start transaction for testing
        self.connection = db.engine.connect()
        self.trans = self.connection.begin()
        db.session.configure(bind=self.connection, binds={})

        server.Shopcart.remove_all()
        server.Product.query.delete()
        server.Product.seed_db()

        server.Shopcart(1).save()
        server.Shopcart(2).save()
        # uid 3 is used in test_get_nonexistent_shopcart
        server.Shopcart(4, {1: 7, 2: 21, 3: 55}).save()

    def tearDown(self):
        # Clean up after tests
        self.trans.rollback()
        self.connection.close()
        db.session.remove()

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_shopcart(self):
        """ Test Get a Shopcart """
        # Test for existing shopcarts
        resp = self.app.get('/shopcarts/1')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['products'], {})

    def test_get_nonexistent_shopcart(self):
        """ Test Get a Non-Existent Shopcart """
        resp = self.app.get('/shopcarts/3')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual(data['error'], 'Shopcart with id: 3 was not found')

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

    def test_create_shopcart(self):
        """ Create an empty shopcart POST on shopcarts"""
        # add a new shopcart
        n_cart = len(server.Shopcart.all())
        cart = {'user_id': 3}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        data = json.loads(resp.data.decode('utf8'))
        self.assertIn('/shopcarts/3', location)
        # Actually saved
        self.assertEqual(len(server.Shopcart.all()), n_cart+1)

    def test_create_shopcart_invalid_data(self):
        """ Create a cart with invalid data"""
        cart = {'user_id': 3, "products": 'prod1'}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        cart = {'user_id': 3, "products": -12}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        cart = {'user_id': 3, 'products': []}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shopcart_with_a_prod(self):
        """ Create a cart uid 3 with a product id 5"""
        n_cart = len(server.Shopcart.all())
        cart = {'user_id': 3, "products": 5}
        resp = self.app.post('/shopcarts', data=json.dumps(cart), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        data = json.loads(resp.data.decode('utf8'))
        self.assertIn('/shopcarts/3', location)
        self.assertDictContainsSubset({"quantity": 1}, data['products']['5'])
        self.assertEqual(len(server.Shopcart.all()), n_cart+1)

    def test_create_shopcart_prods(self):
        """ Create a shopcart with many products"""
        n_cart = len(server.Shopcart.all())
        # add a new shopcart with many products
        new_shopcart = {"user_id": 3, "products": {1: 13, 2: 34}}
        data = json.dumps(new_shopcart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertIsNotNone(location)
        self.assertIn('/shopcarts', location)

        # Check the data is correct
        new_json = json.loads(resp.data.decode('utf8'))

        self.assertDictContainsSubset({"quantity": 13}, new_json['products']['1'])
        self.assertDictContainsSubset({"quantity": 34}, new_json['products']['2'])
        self.assertEqual(len(server.Shopcart.all()), n_cart+1)

    def test_create_shopcart_invalid_prods(self):
        """ Create a shopcart with invalid products """
        new_shopcart = {'uid': 3, 'products': {'prod1': '13'}}
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
        self.assertEqual(n_cart, len(server.Shopcart.all()))

    def test_create_without_uid(self):
        """ Create a shopcart without id"""
        n_cart = len(server.Shopcart.all())
        cart = {}
        data = json.dumps(cart)
        resp = self.app.post('/shopcarts', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(n_cart, len(server.Shopcart.all()))

    def test_update_product(self):
        """Updating a product"""
        cart = server.Shopcart.find(2)

        self.assertIsNotNone(cart)
        cart.add_product(pid=2, quant=3)
        cart.add_product(pid=3, quant=5)

        prods_in_cart = cart.serialize()['products']
        self.assertDictContainsSubset({"quantity": 3}, prods_in_cart[2])
        self.assertDictContainsSubset({"quantity": 5}, prods_in_cart[3])

        data = json.dumps({'quantity': 2})

        resp = self.app.put('/shopcarts/2/products/3', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        new_json = json.loads(resp.data.decode('utf8'))
        self.assertDictContainsSubset({"quantity": 2}, new_json['products']["3"])

    def test_update_product_without_quantity(self):
        """ Updating a product and not sending quantity """
        cart = server.Shopcart.find(2)
        cart.add_product(pid=3, quant=3)

        resp = self.app.put('/shopcarts/2/products/3', data=json.dumps({}), content_type='application/json')

        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual(data['error'], 'Update product needs a quantity')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_with_invalid_quantity(self):
        """ Updating a product with an invalid quantity """
        cart = server.Shopcart.find(2)
        cart.add_product(pid=3, quant=3)

        data = json.dumps({'quantity': 'a'})

        resp = self.app.put('/shopcarts/2/products/3', data=data, content_type='application/json')

        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual(data['error'], 'Update product needs a valid quantity')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_to_0(self):
        """Updating a product to 0"""
        cart = server.Shopcart.find(2)

        self.assertIsNotNone(cart)
        cart.add_product(pid=2, quant=3)
        cart.add_product(pid=3, quant=5)

        prods_in_cart = cart.serialize()['products']
        self.assertDictContainsSubset({"quantity": 3}, prods_in_cart[2])
        self.assertDictContainsSubset({"quantity": 5}, prods_in_cart[3])

        data = json.dumps({'quantity': 0})

        resp = self.app.put('/shopcarts/2/products/3', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        new_json = json.loads(resp.data.decode('utf8'))
        self.assertNotIn("3", new_json['products'])

    def test_update_product_not_existing_shopcart(self):
        """Updating a product of an unexistent shopcart"""
        self.assertIsNone(server.Shopcart.find(3))

        data = json.dumps({'quantity': 2})

        resp = self.app.put('/shopcarts/3/products/3', data=data, content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_not_existing_before(self):
        """Updating a product of an unexiting product in an existing cart"""
        cart = server.Shopcart.find(2)
        self.assertIsNotNone(cart)
        prods_in_cart = cart.serialize()['products']
        self.assertEqual(prods_in_cart, {})

        self.assertNotIn(1, prods_in_cart.keys())

        data = json.dumps({'quantity': 7})
        resp = self.app.put('/shopcarts/2/products/1',
                            data=data, content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_content_type_media_error(self):
        """Not supported media"""
        data = '6'
        resp = self.app.put('/shopcarts/3/products/1',
                            data=data, content_type='application/text')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_delete_a_product_from_shopcart(self):
        """ Test Delete a Product From A Shopcart """
        # Delete products with ID of 5 from cart 1
        cart = server.Shopcart.find(1)
        cart.add_product(5)
        cart.save()

        resp = self.app.delete('/shopcarts/1/products/5')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        cart = server.Shopcart.find(1)
        self.assertEqual(len(cart.products), 0)

    def test_delete_nonexistent_product_from_shopcart(self):
        """ Test Delete a Nonexistent Product From A Shopcart """
        resp = self.app.delete('/shopcarts/1/products/5')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

        cart = server.Shopcart.find(1)
        self.assertEqual(len(cart.products), 0)

    def test_add_new_product_to_cart(self):
        """ Add a new product to the cart """
        product_count = len(server.Shopcart.find(2).products)
        data = {1: 2}

        resp = self.app.post('/shopcarts/2/products', data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['products']), product_count + 1)
        self.assertDictContainsSubset({"quantity": 2}, data['products']['1'])

    def test_add_multiple_new_products_to_cart(self):
        """ Add multiple new products to the cart """
        product_count = len(server.Shopcart.find(2).products)
        data = {1: 2, 2: 4}

        resp = self.app.post('/shopcarts/2/products', data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['products']), product_count + 2)
        self.assertDictContainsSubset({"quantity": 2}, data['products']['1'])
        self.assertDictContainsSubset({"quantity": 4}, data['products']['2'])

    def test_add_existing_product_to_cart(self):
        """ Add an existing product to the cart """
        product_count = len(server.Shopcart.find(4).products)
        data = {1: 2}

        resp = self.app.post('/shopcarts/4/products', data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['products']), product_count)
        self.assertDictContainsSubset({"quantity": 9}, data['products']['1'])

    def test_add_multiple_existing_products_to_cart(self):
        """ Add multiple existing products to the cart """
        product_count = len(server.Shopcart.find(4).products)
        data = {1: 2, 2: 2}

        resp = self.app.post('/shopcarts/4/products', data=json.dumps(data), content_type='application/json')
        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['products']), product_count)
        self.assertDictContainsSubset({"quantity": 9}, data['products']['1'])
        self.assertDictContainsSubset({"quantity": 23}, data['products']['2'])

    def test_add_products_in_bad_format_to_cart(self):
        """ Try to add malformed products to cart """
        data = [(1, 2), (2, 4)]
        resp = self.app.post('/shopcarts/2/products', data=json.dumps(data), content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(server.Shopcart.find(2).products), 0)

    def test_add_product_to_nonexistent_cart(self):
        """ Add a product to a nonexistent cart """
        data = {1: 2}

        resp = self.app.post('/shopcarts/100/products', data=json.dumps(data), content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_shopcart(self):
        """ List All Shopcarts """
        resp = self.app.get('/shopcarts')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        carts = json.loads(resp.data.decode('utf8'))
        self.assertEqual(len(carts), 3)

    def test_prune_empty_shopcarts(self):
        """ Prune empty shopcarts """
        resp = self.app.delete('/shopcarts/prune')

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(server.Shopcart.all()), 1)

    def test_query_product(self):
        """ Query for shopcarts by product id """
        cart = server.Shopcart.find(1)
        cart.add_product(1)
        cart.add_product(2)
        cart.save()

        cart = server.Shopcart.find(2)
        cart.add_product(2)
        cart.save()

        #count for 1 should have cart 1, 4
        resp = self.app.get('/shopcarts', query_string='pid=1')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual({1, 4}, {c['user_id'] for c in data})

    def test_query_nonexintent_product(self):
        """ Query a product that does not exists"""
        self.assertEqual(len(server.Shopcart.find_by_product(123)), 0)
        resp = self.app.get('/shopcarts', query_string='pid=123')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data.decode('utf8'))
        self.assertEqual(data, [])

    def test_get_all_products(self):
        """ Get a list of all products """
        resp = self.app.get('/products')

        data = json.loads(resp.data.decode('utf8'))

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 5)

if __name__ == '__main__':
    unittest.main()
