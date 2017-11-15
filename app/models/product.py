from . import db

class Product(db.Model):
    # define the database table
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(140), unique=False, nullable=True)

    def __repr__(self):
        return '<Name %r>' % self.name

    @staticmethod
    def seed_db():
        """ Initilize the Products in database"""
        p1 = Product(id=1, name='Apple', price=1.2, description='Fruit')
        p2 = Product(id=2, name='Pen', price=3.4, description='Stationery')
        p3 = Product(id=3, name='Pineapple', price=2.3, description='Fruit')
        p4 = Product(id=4, name='Beef', price=33.0, description='Meat')
        p5 = Product(id=5, name='Notebook', price=0.99, description='Stationery')

        # check exist before add
        if not Product.query.get(1):
            db.session.add(p1)
        if not Product.query.get(1):
            db.session.add(p2)
        if not Product.query.get(3):
            db.session.add(p3)
        if not Product.query.get(4):
            db.session.add(p4)
        if not Product.query.get(5):
            db.session.add(p5)

        db.session.commit()
