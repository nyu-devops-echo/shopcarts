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

    def add_product(self, pq_tup):
        """ Adds a tuple of product, quantity to the product dict """
        self.products.update( self.__validate_products(pq_tup) )

    @staticmethod
    def all():
        """ Query that returns all Shopcarts """
        return Shopcart.__data

    @staticmethod
    def remove_all():
        """ Remove all Shopcarts from memory """
        Shopcart.__data = []

    @staticmethod
    def __validate_products(products):
        """ Validates products or raises an error"""
        try:
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
                raise DataValidationError() 
            
            # Products is a dict of proper tuples
            if ( all( isinstance(pid,int) for pid in products.keys() ) and
                 all( (isinstance(q,int) and (q > 0)) for q in products.values() ) ):
                return products

            #Products not valid
            raise DataValidationError() 

        except DataValidationError as e:
            print(type(e)) 
            print('ERROR: Products were not added to shopcart.')
            return {}