import unittest
from models.shopcart import Shopcart
from models.dataerror import DataValidationError

class TestShopcart(unittest.TestCase):
    """ Shopcart Model Tests """
    def setUp(self):
        Shopcart.remove_all()

    def test_it_can_be_instantiated(self):
        """ Test Instantiation """
        cart = Shopcart(1)
        self.assertEqual(cart.uid, 1)
        self.assertEqual(cart.products,{})

    def test_it_can_be_saved(self):
        """ Test Model is Saved to Memory """
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
        self.assertEqual(fetched.uid,1)
        self.assertEqual(fetched.products,{})

    def test_string_is_invalid_product(self):
        """Test that strings are not accepted as products"""
        # Passing a string
        with self.assertRaises(DataValidationError):
            shopcart = Shopcart(1,'product1')

    def test_float_is_invalid_product(self):
        """Test that floats are not accepted as products"""
        # Passing a double
        with self.assertRaises(DataValidationError):
            shopcart = Shopcart(1,2.0)

    def test_set_is_invalid_product(self):
        """Test for not allowing sets in products"""
        # Passing a set
        with self.assertRaises(DataValidationError):
            shopcart = Shopcart(1,{1})

    def test_that_products_are_always_a_dict(self):
        """Test that the shopcart model has products as a dict"""
        # Initializing just an id without product
        shopcart = Shopcart(1)
        self.assertTrue( type(shopcart.products) == dict )

        # initializing None as products
        shopcart = Shopcart(1,None)
        self.assertTrue(type(shopcart.products) == dict )

        # initializing empty dict
        shopcart = Shopcart(1,{})
        self.assertTrue(type(shopcart.products) == dict )

        # Passing just a product id
        shopcart = Shopcart(1,5)
        self.assertTrue(type(shopcart.products) == dict )

        # A dictionary of products
        shopcart = Shopcart(1,{2:3,5:8,13:21})
        self.assertTrue(type(shopcart.products) == dict )

    def test_initializing_with_products(self):
        """Testing initializing a cart with products """
        # Create a new shopcart without a product
        shopcart = Shopcart(0)
        self.assertTrue( len(shopcart.products) == 0)

        # Create a new shopcart with a product
        shopcart = Shopcart(0,5)
        self.assertTrue( len(shopcart.products) > 0)
        self.assertEqual( shopcart.products , {5:1} )

        # Creating a valid dictionary
        shopcart = Shopcart(0, {5:7,13:21,34:55 } )
        self.assertEqual( shopcart.products , {5:7,13:21,34:55 } )

        # Saving products
        shopcart.save()
        shopcarts = Shopcart.all()
        self.assertTrue( len(shopcarts) > 0)

        #Correct Type
        s = shopcarts[0]
        self.assertTrue( type(s.products) == dict)

        #Correct Length
        self.assertEqual( len(s.products) , 3)

    def test_adding_with_a_product(self):
        """ Test to add a product to an exiting shopcart"""
        shopcart = Shopcart(7)
        shopcart.save()
        shopcarts = shopcart.all()
        s=shopcarts[0]
        self.assertEqual( s.uid ,7 )
        self.assertEqual( len(s.products) , 0 )

        # Adding product 21 with quant 34
        s.add_product( 21,34 )
        #There's only one product
        self.assertEqual( len(s.products) ,1 )
        # It's the correct one with correct quant
        self.assertEqual( s.products[21] , 34 )

        # Adding a second
        s.add_product( 34, 55 )
        #There's two  products
        self.assertEqual( len(s.products) ,2 )
        # It's the correct one with correct quant
        self.assertEqual( s.products[34] , 55 )
    
    def test_adding_a_product_that_already_exists(self):
        """ Test to add a product that exists in a cart """
        shopcart = Shopcart(7, {1: 5})
        shopcart.save()

        shopcart.add_product(1, 5)

        self.assertEqual(shopcart.products[1], 10)

    def test_adding_an_invalid_product(self):
        """ Test to add invalid product"""
        shopcart = Shopcart(21)
        shopcart.save()
        shopcarts = shopcart.all()
        s=shopcarts[0]
        self.assertEqual( s.uid ,21 )
        self.assertEqual( len(s.products) , 0 )

        # Adding product 21.5
        with self.assertRaises(DataValidationError):
            s.add_product( 21.5 )

        # Adding a second error
        with self.assertRaises(DataValidationError):
            s.add_product( 34, 0.5 )

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
        self.assertEqual(shopcarts[0].uid, 1)
        self.assertEqual(shopcarts[1].uid, 2)
        self.assertEqual(shopcarts[2].uid, 3)

    def test_find_a_shopcart(self):
        """ Find a shopcart by uid """
        Shopcart(2).save()
        Shopcart(5).save()

        cart = Shopcart.find(5)

        self.assertEqual(cart.uid, 5)
        self.assertEqual(len(cart.products), 0)

    def test_find_shopcart_that_doesnt_exist(self):
        """ Try to find a non-existant Shopcart """
        Shopcart(2).save()

        cart = Shopcart.find(5)

        self.assertIsNone(cart)

    def test_delete_a_shopcart(self):
        """ Test A Shopcart Can Be Deleted """
        cart = Shopcart(1, {})
        cart.save()
        self.assertEqual( len(Shopcart.all()), 1)

        # Delete the shopcart and make sure it isn't in the database
        cart.delete()
        self.assertEqual( len(Shopcart.all()), 0)

    def test_delete_products_from_shopcart(self):
        cart = Shopcart(1, { 5 : 7})
        cart.save()
        cart.delete_product(5)
        self.assertEqual( len(cart.products), 0 )     

    def test_shopcarts_are_pruned(self):
        """ Test empty shopcarts are pruned """
        Shopcart(1).save()
        Shopcart(2).save()
        Shopcart(3, { 5 : 7}).save()

        Shopcart.prune()
        
        self.assertEqual(len(Shopcart.all()), 1)

    def test_desirialize_error(self):
        """Test deserialize error"""
        cart = Shopcart()
        with self.assertRaises( DataValidationError ):
            cart.deserialize(5)

    def test_Get_shopcarts_with_a_specific_product(self):
        Shopcart(1, { 5 : 7 , 3:5}).save()
        Shopcart(2, { 6 : 1 }).save()
        Shopcart(3, { 5 : 1, 6:4, 7:3 }).save()
        self.assertEqual(len(Shopcart.all()), 3)
        self.assertEqual(len(Shopcart.find_by_product(5)), 2)
        self.assertEqual(len(Shopcart.find_by_product(6)), 2)
        self.assertEqual(len(Shopcart.find_by_product(7)), 1)
        self.assertEqual(len(Shopcart.find_by_product(1)), 0)   
    
    def test_add_multiple_products(self):
        """ Add multiple products to an existing cart """
        cart = Shopcart(1, {1: 1})
        cart.save()

        cart.add_products({1: 2, 2: 4})

        self.assertEqual(len(cart.products), 2)
        self.assertEqual(cart.products[1], 3)
        self.assertEqual(cart.products[2], 4)

    def test_add_products_with_invalid_type(self):
        """ Try to add multiple products not as a dict """
        cart = Shopcart(1)
        with self.assertRaises(DataValidationError):
            cart.add_products([(1, 2), (2, 4)])

if __name__ == '__main__':
    unittest.main()
