import unittest
import os
from app import app, db
from app.models.product import Product
from app.models.shopcart import Shopcart

if 'TRAVIS' in os.environ:
    DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root@localhost:3306/shopcarts_test')
else:
    DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost:3306/shopcarts_test')

class TestProduct(unittest.TestCase):
    """ Product Model Tests """

    @classmethod
    def setUpClass(cls):
        app.debug = False
        # Set up the test database
        if DATABASE_URI:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    def setUp(self):
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        product = Product(id=1, name="Test", price=1.0, description="Test Description")
        
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Test")
        self.assertEqual(product.price, 1.0)
        self.assertEqual(product.description, "Test Description")
    
    def test_seed_data(self):
        """ Test Product data can be seeded """
        self.assertEqual(len(Product.query.all()), 0)

        Product.seed_db()
        self.assertEqual(len(Product.query.all()), 5)
    
    def test_product_representation(self):
        """ Test the product is printed correctly """
        product = Product(name="Test")

        self.assertEqual(str(product), "<Name 'Test'>")
    
    def test_get_all_products(self):
        """ Test All products Can Be Retrieved """
        Product.seed_db()

        products = Product.all()

        self.assertEqual(len(products), 5)
    
    def test_serialize_a_product(self):
        product = Product(id=1, name="Test", price=1.0, description="Test Description")
        product = product.serialize()

        self.assertEqual(product['id'], 1)
        self.assertEqual(product['name'], "Test")
        self.assertEqual(product['price'], 1.0)
        self.assertEqual(product['description'], "Test Description")

if __name__ == '__main__':
    unittest.main()
