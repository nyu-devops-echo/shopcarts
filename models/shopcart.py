class Shopcart(object):

    """
    This is model for the shop carts
    Assumptions:
        - In memory persistence
        - The fields of a shopcart include:
            - user id
            - list of products (product id, quantity of product )
        - The total price of the shopcart will be dynamically calculated
        - Model should only initially include `init` method and shopcart fields

    """

    __data = []
    __index = 0

    __products = dict()

    def __init__(self, uid=0, products=None):
        """
        :param uid: user id
        :param products: dict of products <products id, quantity of product>
        """

        self.uid = int(uid)
        self.products = products if products else []

    def save(self):
        """ Saves a Shopcart in the database """
        Shopcart.__data.append(self)

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
