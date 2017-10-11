import unittest
from models.shopcart import Shopcart

class TestShopcart(unittest.TestCase):
    """ Shopcart Model Tests """

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        cart = Shopcart(1, [])
        
        self.assertEqual(cart.uid, 1)
        self.assertEqual(cart.products, [])

if __name__ == '__main__':
    unittest.main()
