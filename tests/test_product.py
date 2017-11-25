import unittest
from app import app
from app.models import db
from app.models.product import Product
from app.models.shopcart import Shopcart

class TestProduct(unittest.TestCase):
    """ Product Model Tests """
    
    def setUp(self):
        # Push app context for flask-sqlalchemy
        ctx = app.app_context()
        ctx.push()

        # Start transaction for testing
        self.connection = db.engine.connect()
        self.trans = self.connection.begin()
        db.session.configure(bind=self.connection, binds={})

        Shopcart.remove_all()
        Product.query.delete()

    def tearDown(self):
        # Clean up after tests
        self.trans.rollback()
        self.connection.close()
        db.session.remove()

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
