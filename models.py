
class Product(object):
    """This is the model for the products in the shopping carts
    Assumptions: (*** FOR SPRINT 0 ***)
        - In memory persistance 
        - Property includes:
            - product id
            - name
            - price 
            - description
        - Model should only initially include init method and product fields.
    """ 
    
    __data = []
    __index = 0

    def __init__(self, id=0, name='', price=0.0, description=None):
        """
        Initializing Product
        """
        self.id = int(id)
        self.name = name
        self.price = float(price)
        self.description = description