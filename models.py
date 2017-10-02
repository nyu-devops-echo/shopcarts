
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
    def __init__(self, id, name, price, description=None):
        self.id = int(id)
        self.name = name
        self.price = float(price)
        self.description = description