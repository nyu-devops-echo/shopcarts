from .dataerror import DataValidationError
class Shopcart(object):
    """
    This is model for the shop carts
    Assumptions:
        - In memory persistence
        - The fields of a shopcart include:
            - user id
            - Dictionary of products { product_id: quantity_of_product}
        - The total price of the shopcart will be dynamically calculated
    """
    __data = []
    __index = 0

    def __init__(self, uid=0, products=None):
        """
        :param uid: user id
        :param products: dict of products <products id, quantity of product>
        """
        self.uid = int(uid)
        self.products = self.__validate_products(products)

    def save(self):
        """ Saves a Shopcart in the database """
        Shopcart.__data.append(self)

    def add_product(self, pid, quant=1):
        """ Adds a tuple of product, quantity to the product dict """
        pq_tup = (pid,quant)
        self.products.update( self.__validate_products(pq_tup) )

    def delete(self):
        """ Deletes a Shopcart in the database """
        Shopcart.__data.remove(self)

    def serialize(self):
        """Serializes a shopcart to a dictionary"""
        return {'uid':self.uid, 'products': self.products}

    def deserialize(self, data):
        """ Deserializes a cart from a dictionary
        Args:
            data (dict): A dictionary containing the cart data
        """
        #data not dict
        if not isinstance(data, dict):
            raise DataValidationError('ERROR: Invalid shopcart.\nBody of request contained bad or no data')
        
        #Data is dict and has uid
        if data.has_key('uid'):
            self.uid = data['uid']
            self.products = self.__validate_products(data['products'])
        
        #Data is dict and is missing uid
        else:
            raise DataValidationError('ERROR: Invalid shopcart.\nBody of request is missing user id')
        return

    @staticmethod
    def all():
        """ Query that returns all Shopcarts """
        return Shopcart.__data

    @staticmethod
    def remove_all():
        """ Remove all Shopcarts from memory """
        Shopcart.__data = []

    @staticmethod
    def find(uid):
        """ Find a Shopcart by it's uid"""
        for cart in Shopcart.__data:
            if cart.uid == uid:
                return cart

        return None

    @staticmethod
    def __validate_products(products):
        """ Validates products or raises an error"""
        # Product is none so set an empty list
        if products is None:
            return {}

        #Not None
        # Tuple of product, quantity 
        if type(products) == tuple  and len(products)==2 and all(isinstance(pq,int) for pq in products): 
            return {products[0]:products[1]}

        # Just a Product id, set default quantity to 1
        if type(products) == int: 
            return {products:1}

        if type(products) != dict : 
            raise DataValidationError("ERROR: Data Validation error\nInvalid format for products")

        # Products is a dict of proper tuples
        if ( all( isinstance(pid,int) for pid in products.keys() ) and
             all( (isinstance(q,int) and (q > 0)) for q in products.values() ) ):
            return products

        #Products not valid
        raise DataValidationError("ERROR: Data Validation error\nInvalid format for products")
