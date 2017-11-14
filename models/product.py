import os
import json
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Local database credentials
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'localdb'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

# Get service credentials from Bluemix
if 'VCAP_SERVICES' in os.environ: 
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    creds = vcap['cleardb'][0]['credentials']

    HOSTNAME = creds['hostname']
    PORT = creds['port']
    USERNAME = creds['username']
    PASSWORD = creds['password']
    DATABASE = creds['name']
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db = SQLAlchemy(app)

# create database engineer
engine = create_engine(DB_URI)
# create_str = "CREATE DATABASE IF NOT EXISTS %s ;" % (DATABASE)
# engine.execute(create_str, echo=True)
conn = engine.connect()
conn.execute("commit")
conn.execute("create database if not exists localdb")
conn.close()

DEBUG = (os.getenv('DEBUG', 'True') == 'True')
PORT = os.getenv('PORT', '5000')

class Product(db.Model):
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

    # define the database table
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(140), unique=False, nullable=True)

    def __repre__(self):
        return '<Name %r>' % self.name

    def __init__(self, id=0, name='', price=0.0, description=None):
        """
        Initializing Product
        """
        self.id = int(id)
        self.name = name
        self.price = float(price)
        self.description = description


######################################################################
#  M y S Q L   D A T A B A S E   C O N N E C T I O N   M E T H O D S
######################################################################

    @staticmethod
    def init_db():
        """ Initilize the Product table in database"""
        db.create_all()
        p1 = Product(id=1,name='Apple',price=1.2,description='Fruit')
        p2 = Product(id=2,name='Pen',price=3.4,description='Stationery')
        p3 = Product(id=3,name='Pineapple',price=2.3,description='Fruit')
        p4 = Product(id=4,name='Beef',price=33.0,description='Meat')
        p5 = Product(id=5,name='Notebook',price=0.99,description='Stationery')
            
        # check exist before add
        if db.session.query(Product.id).filter(Product.id==1).count() == 0:
            db.session.add(p1)
        if db.session.query(Product.id).filter(Product.id==2).count() == 0:
            db.session.add(p2)
        if db.session.query(Product.id).filter(Product.id==3).count() == 0:
            db.session.add(p3)
        if db.session.query(Product.id).filter(Product.id==4).count() == 0:
            db.session.add(p4)
        if db.session.query(Product.id).filter(Product.id==5).count() == 0:
            db.session.add(p5)
        db.session.commit()
