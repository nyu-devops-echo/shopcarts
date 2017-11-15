import unittest
from app import app
from app.models import db
from app.models.product import Product

class TestProduct(unittest.TestCase):
    """ Product Model Tests """
    
    def setUp(self):
        # Push app context for flask-sqlalchemy
        ctx = app.app_context()
        ctx.push()

        # Start transaction for testing
        db.session.begin_nested()
        Product.query.delete()
    
    def tearDown(self):
        # Clean up after tests
        db.session.rollback()

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

if __name__ == '__main__':
    unittest.main()
