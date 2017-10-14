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

    def test_get_all_shopcarts(self):
        """ Test All Shopcarts Can Be Retrieved """
        # Add 3 shopcarts to memory and check that we can retrieve them all
        cart1 = Shopcart(1, [])
        cart2 = Shopcart(2, [])
        cart3 = Shopcart(3, [])
        cart1.save()
        cart2.save()
        cart3.save()

        # Invoke method and check the returned data
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 3)
        self.assertEqual(shopcarts[0].uid, 1)
        self.assertEqual(shopcarts[1].uid, 2)
        self.assertEqual(shopcarts[2].uid, 3)

    def test_delete_a_shopcart(self):
        """ Test A Shopcart Can Be Deleted """
        cart = Shopcart(1, {})
        cart.save()
        self.assertEqual( len(Shopcart.all()), 1)

        # Delete the shopcart and make sure it isn't in the database
        cart.delete()
        self.assertEqual( len(Shopcart.all()), 0)


if __name__ == '__main__':
    unittest.main()
