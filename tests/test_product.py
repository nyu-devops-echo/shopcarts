import unittest
from models.product import Product

class TestProduct(unittest.TestCase):
    """ Product Model Tests """

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        product = Product(1, "Test", 1.0, "Test Description")
        
        self.assertEqual(product.id, 1)
        self.assertEqual(product.name, "Test")
        self.assertEqual(product.price, 1.0)
        self.assertEqual(product.description, "Test Description")

if __name__ == '__main__':
    unittest.main()
