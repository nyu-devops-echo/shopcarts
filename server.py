import os
import json
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
from models.shopcart import Shopcart
from models.dataerror import DataValidationError

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
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Root URL response """
    return jsonify(name='Shopcarts REST API Service',
                   version='1.0',
                   description= 'This is the REST API Service for the shopcarts.'), status.HTTP_200_OK

######################################################################
# RETRIEVE A SHOPCART
######################################################################
@app.route('/shopcarts/<int:id>', methods=['GET'])
def get_shopcarts(id):
    cart = Shopcart.find(id)
    if cart:
        message = { 'uid': cart.uid, 'products': cart.products }
        rc = status.HTTP_200_OK
    else:
        message = { 'error' : 'Shopcart with id: %s was not found' % str(id) }
        rc = status.HTTP_404_NOT_FOUND

    return jsonify(message), rc

######################################################################
# DELETE A SHOPCART
######################################################################
@app.route('/shopcarts/<int:id>', methods=['DELETE'])
def delete_shopcarts(id):
    """
    Delete a Shopcart
    This endpoint will delete a Shopcart based on the id specified in the path
    """
    cart = Shopcart.find(id)

    if cart:
        cart.delete()

    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# Create a Shopcart
######################################################################
@app.route('/shopcarts', methods=['POST'])
def create_shopcart():
    """Creates a shopcart and saves it to database"""
    data = request.get_json()
    try :
        id = data['uid']
    except KeyError :
        message = { 'error': 'POST needs a user id' }
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    cart = Shopcart.find(id)
    if cart:
        message = jsonify({ 'error' : 'Shopcart for user %s already exits' % str(id) })
        rc = status.HTTP_409_CONFLICT
        return make_response(message,rc)

    # Create the Cart
    cart = Shopcart(id)
    #Validate correct data
    try:
        cart.deserialize(  data )
    except DataValidationError as e:
        message = { 'error': e.args[0] }
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    # If correct save it and return object
    cart.save()
    message = cart.serialize()
    location_url = url_for('get_shopcarts', id = int( cart.uid ), _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, { 'Location': location_url })
    
######################################################################
# UPDATE AN EXISTING Shopcart product
######################################################################
@app.route('/shopcarts/<int:uid>/products/<int:pid>', methods=['PUT'])
def update_shopcart(uid,pid):
    """
    Update a Shopcart
    This endpoint will update a Shopcart based the body that is posted
    """
    check_content_type('application/json')
    cart = Shopcart.find(uid)
    if not cart:
        message = { 'error' : 'Shopcart with id: %d was not found' % uid }
        rc = status.HTTP_404_NOT_FOUND
        return make_response(jsonify(message),rc)

    prods_cart= cart.serialize()['products']
    if not pid in prods_cart.keys():
        message = { 'error' : 'Product %d is not on shopcart %d' % (pid,uid) }
        rc = status.HTTP_404_NOT_FOUND
        return make_response(jsonify(message),rc)

    cart.deserialize( request.get_json() )
    cart.save()
    return make_response(jsonify(cart.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A PRODUCT TO A SHOPCART
######################################################################
@app.route('/shopcarts/<int:uid>/products', methods=['POST'])
def add_product(uid):
    """Add a product to the shopcart with the given uid"""
    cart = Shopcart.find(uid)

    if not cart:
        return jsonify("Cart with id '{}' was not found.".format(uid)), status.HTTP_404_NOT_FOUND

    try:
        cart.add_products(request.get_json())
        cart.save()
    except DataValidationError as e:
        message = { 'error': e.args[0] }
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    return make_response(jsonify(cart.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A PRODUCT FROM A SHOPCART
######################################################################
@app.route('/shopcarts/<int:uid>/products/<int:pid>', methods=['DELETE'])
def delete_product(uid, pid):
    cart = Shopcart.find(uid)
    if cart:
        cart.delete_product(pid)
    return make_response('', status.HTTP_204_NO_CONTENT)



######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    #app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))

@app.before_first_request
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


######################################################################
# List all Shopcarts
######################################################################
@app.route('/shopcarts', methods=['GET'])
def get_all_shopcarts():
    pid = request.args.get('pid')
    if pid:
        carts = Shopcart.find_by_product( int(pid) )
    else:
        carts = Shopcart.all()
    message = [cart.serialize() for cart in carts]
    rc = status.HTTP_200_OK
    return jsonify(message), rc

######################################################################
# Prune empty Shopcarts
######################################################################
@app.route('/shopcarts/prune', methods=['DELETE'])
def prune_empty_shopcarts():
    Shopcart.prune()
    return make_response('', status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
