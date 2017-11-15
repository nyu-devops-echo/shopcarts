import unittest
from app.models.product import Product

class TestProduct(unittest.TestCase):
    """ Product Model Tests """

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        product = Product(id=1, name="Test", price=1.0, description="Test Description")
        
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Test")
        self.assertEqual(product.price, 1.0)
        self.assertEqual(product.description, "Test Description")

if __name__ == '__main__':
    unittest.main()
