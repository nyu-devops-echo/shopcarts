import warnings
from app import db
from .product import Product
from .dataerror import DataValidationError

# Association object to represent look-up table between products and shopcarts
class ProductShopcart(db.Model):
    __tablename__ = 'product_shopcart'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('shopcarts.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    shopcart = db.relationship('Shopcart', backref=db.backref("products", passive_deletes='all'))
    product = db.relationship('Product')

    def __init__(self, product=None, quantity=0, shopcart=None):
        self.product = product
        self.quantity = quantity
        self.shopcart = shopcart

class Shopcart(db.Model):
    __tablename__ = 'shopcarts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True, unique=True, nullable=False)

    def __init__(self, user_id, products=None):
        """
        :param user_id: user id
        :param products: list of products <products id, quantity of product>
        """
        self.user_id = int(user_id)
        self.products = self.__validate_products(products)

    def __repr__(self):
        return '<UserId %d - %d Products>' % (self.user_id, len(self.products))

    def save(self):
        """ Saves a Shopcart in the database """
        db.session.add(self)
        db.session.commit()

    def add_products(self, products):
        if type(products) != dict:
            raise DataValidationError('Invalid products: body of request contained bad or no data')

        for pid, quantity in products.items():
            self.add_product(int(pid), quantity)

    def add_product(self, pid, quant=1):
        """ Adds a tuple of product, quantity to the product dict """
        for product in self.products:
            if product.product_id != pid:
                continue

            product.quantity += quant
            return

        pq_tup = (pid, quant)
        self.products.append(self.__validate_products(pq_tup)[0])

    def delete(self):
        """ Deletes a Shopcart in the database """
        for product in self.products:
            db.session.delete(product)

        db.session.delete(self)
        db.session.commit()
    
    def update_product(self, pid, quantity):
        """ Updates a product quantity """
        if not quantity:
            self.delete_product(pid)
            return

        for product in self.products:
            if product.product_id != pid:
                continue

            product.quantity = quantity
            return

    def delete_product(self, pid):
        """ Removes a Product entirely from a Shopcart """
        for product in self.products:
            if product.product_id != pid:
                continue

            db.session.delete(product)
            db.session.commit()
            return

    def serialize(self):
        """ Serializes a shopcart into a dictionary """
        u_dict = {"user_id": self.user_id,}
        prods = {"products": {} }
        for p in self.products:
            p_dict = { p.product.id: p.product.serialize() }
            p_dict[p.product.id].update( {"quantity": p.quantity } )
            prods['products'].update(p_dict)
        if prods:
            u_dict.update(prods)
        
        return u_dict

    @staticmethod
    def init_db():
        """ Initializes the database session """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            db.create_all() # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Query that returns all Shopcarts """
        return Shopcart.query.all()

    @staticmethod
    def remove_all():
        """ Remove all Shopcarts from database """
        ProductShopcart.query.delete()
        Shopcart.query.delete()
        db.session.commit()

    @staticmethod
    def find(user_id):
        """ Find a Shopcart by it's user_id"""
        return Shopcart.query.filter_by(user_id=user_id).first()

    @staticmethod
    def prune():
        """ Delete empty shopcarts """
        for cart in Shopcart.query.filter(~Shopcart.products.any()):
            db.session.delete(cart)

        db.session.commit()

    @staticmethod
    def __validate_products(products):
        """ Validates products or raises an error """
        # Product is none so set an empty list
        if products is None:
            return []

        # Not None
        # Tuple of product, quantity
        if isinstance(products, tuple) and len(products) == 2 and all(isinstance(pq, int) for pq in products):
            return [Shopcart.create_product(products[0], products[1])]

        # Just a Product id, set default quantity to 1
        if isinstance(products, int) and products >= 0:
            return [Shopcart.create_product(products, 1)]

        if not isinstance(products, dict):
            raise DataValidationError("ERROR: Data Validation error\nInvalid format for products")

        # Products is a dict of proper tuples
        if all((isinstance(q, int) and (q > 0)) for q in products.values()):
            return [Shopcart.create_product(product, quantity) for product, quantity in products.items()]

        raise DataValidationError("ERROR: Data Validation error\nInvalid format for products")

    @staticmethod
    def find_by_product(pid):
        """ Returns all of the Shopcarts that have a specific id
        Args:
            pid (int): product id to query
        """
        return Shopcart.query.filter(Shopcart.products.any(product_id=pid)).all()

    @staticmethod
    def create_product(product_id, quantity=0):
        """ Searches for valid product and creates a ProductShopcart class if found """
        product = Product.query.get(product_id)
        if not product:
            raise DataValidationError("ERROR: Data Validation error\nInvalid product: %d" % product_id)

        return ProductShopcart(product, quantity)
