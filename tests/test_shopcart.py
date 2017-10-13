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
        # Check that there are no shopcarts
        items = Shopcart.all()
        self.assertEqual(len(items), 0)

        # Save a shopcart and check it was added to memory
        cart = Shopcart(1,[])
        cart.save()
        items = Shopcart.all()
        self.assertEqual(len(items), 1)

        # Check that the saved item is actually the one we saved
        fetched = items[0]
        self.assertEqual(fetched.uid,1)
        self.assertEqual(fetched.products,[])

if __name__ == '__main__':
    unittest.main()
