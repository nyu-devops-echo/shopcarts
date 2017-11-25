import unittest
from sqlalchemy.orm.collections import InstrumentedList
from app import app
from app.models import db
from app.models.shopcart import Shopcart
from app.models.product import Product
from app.models.dataerror import DataValidationError

class TestShopcart(unittest.TestCase):
    """ Shopcart Model Tests """
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
        Product.seed_db()

    def tearDown(self):
        # Clean up after tests
        self.trans.rollback()
        self.connection.close()
        db.session.remove()

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        cart = Shopcart(1)

        self.assertEqual(cart.user_id, 1)
        self.assertEqual(cart.products, [])

    def test_shopcart_representation(self):
        """ Test the shopcart is printed correctly """
        cart = Shopcart(1)

        self.assertEqual(str(cart), "<UserId 1 - 0 Products>")

    def test_it_can_be_saved(self):
        """ Test Model is Saved to database """
        # Check that there are no shopcarts
        items = Shopcart.all()
        self.assertEqual(len(items), 0)

        # Save a shopcart and check it was added to memory
        cart = Shopcart(1)
        cart.save()
        items = Shopcart.all()
        self.assertEqual(len(items), 1)

        # Check that the saved item is actually the one we saved
        fetched = items[0]
        self.assertEqual(fetched.user_id, 1)
        self.assertEqual(fetched.products, [])

    def test_string_is_invalid_product(self):
        """Test that strings are not accepted as products"""
        # Passing a string
        with self.assertRaises(DataValidationError):
            Shopcart(1, 'product1')

    def test_float_is_invalid_product(self):
        """Test that floats are not accepted as products"""
        # Passing a double
        with self.assertRaises(DataValidationError):
            Shopcart(1, 2.0)

    def test_set_is_invalid_product(self):
        """Test for not allowing sets in products"""
        # Passing a set
        with self.assertRaises(DataValidationError):
            Shopcart(1, {1})

    def test_invalid_dict_is_invalid_product(self):
        """Test that invalid dict are not accepted as products"""
        # Passing a double
        with self.assertRaises(DataValidationError):
            Shopcart(1, {1: "many"})

    def test_that_products_are_always_a_list(self):
        """Test that the shopcart model has products as a list"""
        # Initializing just an id without product
        shopcart = Shopcart(1)
        self.assertEqual(type(shopcart.products), InstrumentedList)

        # initializing None as products
        shopcart = Shopcart(1, None)
        self.assertEqual(type(shopcart.products), InstrumentedList)

        # initializing empty dict
        shopcart = Shopcart(1, {})
        self.assertEqual(type(shopcart.products), InstrumentedList)

        # Passing just a product id
        shopcart = Shopcart(1, 5)
        self.assertEqual(type(shopcart.products), InstrumentedList)

        # A dictionary of products
        shopcart = Shopcart(1, {1:3, 2:8, 3:21})
        self.assertEqual(type(shopcart.products), InstrumentedList)

    def test_initializing_with_products(self):
        """Testing initializing a cart with products """
        # Create a new shopcart without a product
        shopcart = Shopcart(0)
        self.assertTrue(len(shopcart.products) == 0)

        # Create a new shopcart with a product
        shopcart = Shopcart(0, 5)
        self.assertEqual(len(shopcart.products), 1)
        self.assertEqual(shopcart.products[0].quantity, 1)

        # Creating a valid dictionary
        shopcart = Shopcart(0, {1:7, 2:21, 3:55})
        self.assertEqual(len(shopcart.products), 3)
        self.assertEqual(shopcart.products[0].quantity, 7)
        self.assertEqual(shopcart.products[1].quantity, 21)
        self.assertEqual(shopcart.products[2].quantity, 55)

        # Saving products
        shopcart.save()
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 1)

        #C orrect Type
        s = shopcarts[0]
        self.assertEqual(type(s.products), InstrumentedList)

        # Correct Length
        self.assertEqual(len(s.products) ,3)

    def test_adding_with_a_product(self):
        """ Test to add a product to an exiting shopcart"""
        shopcart = Shopcart(7)
        shopcart.save()
        shopcarts = shopcart.all()

        s = shopcarts[0]
        self.assertEqual(s.user_id, 7)
        self.assertEqual(len(s.products), 0)

        # Adding product 1 with quant 34
        s.add_product(1, 34)
        #There's only one product
        self.assertEqual(len(s.products), 1)
        # It's the correct one with correct quant
        self.assertEqual(s.products[0].quantity, 34)

        # Adding a second
        s.add_product(2, 55)
        # #There's two  products
        self.assertEqual(len(s.products), 2)
        # # It's the correct one with correct quant
        self.assertEqual(s.products[1].quantity, 55)

    def test_adding_a_product_that_already_exists(self):
        """ Test to add a product that exists in a cart """
        shopcart = Shopcart(7, {1: 5})
        shopcart.save()

        shopcart.add_product(1, 5)

        self.assertEqual(shopcart.products[0].quantity, 10)

    def test_adding_an_invalid_product(self):
        """ Test to add invalid product"""
        shopcart = Shopcart(21)
        shopcart.save()
        shopcarts = shopcart.all()

        s = shopcarts[0]
        self.assertEqual(s.user_id, 21)
        self.assertEqual(len(s.products), 0)

        # Adding product 21.5
        with self.assertRaises(DataValidationError):
            s.add_product(21.5)

        # Adding a second error
        with self.assertRaises(DataValidationError):
            s.add_product(1, 0.5)

    def test_get_all_shopcarts(self):
        """ Test All Shopcarts Can Be Retrieved """
        # Add 3 shopcarts to memory and check that we can retrieve them all
        cart1 = Shopcart(1)
        cart2 = Shopcart(2)
        cart3 = Shopcart(3)
        cart1.save()
        cart2.save()
        cart3.save()

        # Invoke method and check the returned data
        shopcarts = Shopcart.all()
        self.assertEqual(len(shopcarts), 3)
        self.assertEqual(shopcarts[0].user_id, 1)
        self.assertEqual(shopcarts[1].user_id, 2)
        self.assertEqual(shopcarts[2].user_id, 3)

    def test_find_a_shopcart(self):
        """ Find a shopcart by uid """
        Shopcart(2).save()
        Shopcart(5).save()

        cart = Shopcart.find(5)

        self.assertEqual(cart.user_id, 5)
        self.assertEqual(len(cart.products), 0)

    def test_find_shopcart_that_doesnt_exist(self):
        """ Try to find a non-existant Shopcart """
        Shopcart(2).save()

        cart = Shopcart.find(5)

        self.assertIsNone(cart)

    def test_delete_a_shopcart(self):
        """ Test A Shopcart Can Be Deleted """
        cart = Shopcart(1, 1)
        cart.save()
        self.assertEqual(len(Shopcart.all()), 1)

        # Delete the shopcart and make sure it isn't in the database
        cart.delete()
        self.assertEqual(len(Shopcart.all()), 0)

    def test_delete_products_from_shopcart(self):
        """ Test a product in a shopcart can be deleted """
        cart = Shopcart(1, {1: 2, 5: 7})
        cart.save()
        cart.delete_product(5)
        self.assertEqual(len(cart.products), 1)

    def test_shopcarts_are_pruned(self):
        """ Test empty shopcarts are pruned """
        Shopcart(1).save()
        Shopcart(2).save()
        Shopcart(3, {5 : 7}).save()

        Shopcart.prune()

        self.assertEqual(len(Shopcart.all()), 1)

    def test_get_shopcarts_with_a_specific_product(self):
        Shopcart(1, {1: 7, 2: 5}).save()
        Shopcart(2, {3: 1}).save()
        Shopcart(3, {4: 1, 5: 4, 1: 3}).save()

        self.assertEqual(len(Shopcart.all()), 3)

        self.assertEqual(len(Shopcart.find_by_product(1)), 2)
        self.assertEqual(len(Shopcart.find_by_product(5)), 1)
        self.assertEqual(len(Shopcart.find_by_product(6)), 0)

    def test_add_multiple_products(self):
        """ Add multiple products to an existing cart """
        cart = Shopcart(1, {1: 1})
        cart.save()

        cart.add_products({1: 2, 2: 4})

        self.assertEqual(len(cart.products), 2)
        self.assertEqual(cart.products[0].quantity, 3)
        self.assertEqual(cart.products[1].quantity, 4)

    def test_add_products_with_invalid_type(self):
        """ Try to add multiple products not as a dict """
        cart = Shopcart(1)
        with self.assertRaises(DataValidationError):
            cart.add_products([(1, 2), (2, 4)])

    def test_create_product_helper_function_with_invalid_pid(self):
        """ Try to create a product association to a non-existant product """
        with self.assertRaises(DataValidationError):
            Shopcart.create_product(10)
    
    def test_shopcart_serialization(self):
        """ Test serializing a shopcart """
        cart = Shopcart(1, {1: 2, 2: 1})
        cart = cart.serialize()

        self.assertEqual(cart['user_id'], 1)
        self.assertEqual(cart['products'][1]["name"], "Apple")
        self.assertEqual(cart['products'][1]["quantity"], 2)

        self.assertEqual(cart['products'][2]["name"], "Pen")
        self.assertEqual(cart['products'][2]["quantity"], 1)

if __name__ == '__main__':
    unittest.main()
