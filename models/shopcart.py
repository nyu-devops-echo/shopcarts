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
    
    def add_products(self, products):
        if type(products) != dict :
            raise DataValidationError('Invalid products: body of request contained bad or no data')
        
        for pid, quantity in products.items():
            self.add_product(int(pid), quantity)

    def add_product(self, pid, quant=1):
        """ Adds a tuple of product, quantity to the product dict """
        if pid in self.products:
            quant += self.products[pid]

        pq_tup = (pid, quant)
        self.products.update( self.__validate_products(pq_tup) )

    def delete(self):
        """ Deletes a Shopcart in the database """
        Shopcart.__data.remove(self)

    def delete_product(self, pid):
        """ Removes a Product entirely from a Shopcart """
        self.products.pop(pid, None)

    def serialize(self):
        """ Serializes a shopcart into a dictionary """
        return {"uid": self.uid, "products": self.products }

    def deserialize(self,data):
        """ Deserializes a shopcart from a dictionary """

        # A {'products': {'prod':quant} } ** JSON.DUMP MAKES KEYS TO STR
        if type( data ) != dict :
            raise DataValidationError('Invalid shopcart: body of request contained bad or no data')

        if "products" in data.keys():
            try:
                if type( data['products'] ) == dict:
                    # ** JSON.DUMP MAKES KEYS TO STR
                    # See if needs to delete a product 
                    prods ={}
                    for (pid,quant) in data['products'].items():
                        if int(quant) == 0:
                            self.delete_product( int(pid) )
                        else:
                            prods.update( {int(pid):int(quant)} )
                else:
                    prods = int( data['products'] )
                self.products.update( self.__validate_products( prods ) )
            except ValueError :
                raise DataValidationError('ERROR: %s has an invalid format for products'% data['products'])
            except TypeError :
                raise DataValidationError('ERROR: %s has an invalid format for products'% data['products'])

       
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
    def prune():
        """ Delete empty shopcarts """
        Shopcart.__data = [cart for cart in Shopcart.__data if cart.products]

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
        if type(products) == int and products >= 0:
            return {products:1}

        if type(products) != dict :
            raise DataValidationError("ERROR: Data Validation error\nInvalid format for products")

        # Products is a dict of proper tuples
        if ( all( isinstance(pid,int) for pid in products.keys() ) and
             all( (isinstance(q,int) and (q > 0)) for q in products.values() ) ):
            return products

    @staticmethod
    def find_by_product(pid):
        """ Returns all of the Shopcarts that have a specific id
        Args:
            pid (int): product id to query
        """
        return [cart for cart in Shopcart.__data if pid in cart.products.keys()  ]

