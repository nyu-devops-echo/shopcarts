import unittest
from models.shopcart import Shopcart

class TestShopcart(unittest.TestCase):
    """ Shopcart Model Tests """
    def setUp(self):
        Shopcart.remove_all()

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        cart = Shopcart(1,[])
        self.assertEqual(cart.uid, 1)
        self.assertEqual(cart.products, [])

    def test_it_can_be_saved(self):
        """ Test Model is Saved to Memory """
        items = Shopcart.all()
        self.assertEqual(len(items), 0)

        cart = Shopcart(1,[])
        cart.save()
        items = Shopcart.all()

        self.assertEqual(len(items), 1)

if __name__ == '__main__':
    unittest.main()
