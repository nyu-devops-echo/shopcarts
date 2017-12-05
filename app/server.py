import os
from flask import jsonify, request, url_for, make_response, abort
from flask_api import status
from .models.shopcart import Shopcart
from .models.product import Product
from .models.dataerror import DataValidationError
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """
    User interface
    ---
    tags:
      - Shopcarts
    description: The Shopcarts endpoint allows you to query shopcarts
    """
    return app.send_static_file('index.html')

######################################################################
# RETRIEVE A SHOPCART
######################################################################
@app.route('/shopcarts/<int:id>', methods=['GET'])
def get_shopcarts(id):
    cart = Shopcart.find(id)
    if cart:
        message = cart.serialize()
        rc = status.HTTP_200_OK
    else:
        message = {'error' : 'Shopcart with id: %s was not found' % str(id)}
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
    try:
        user_id = data['user_id']
    except KeyError:
        message = {'error': 'POST needs a user id'}
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    cart = Shopcart.find(user_id)
    if cart:
        message = jsonify({'error' : 'Shopcart for user %s already exits' % str(user_id)})
        rc = status.HTTP_409_CONFLICT
        return make_response(message, rc)

    # Create the Cart
    products = data['products'] if 'products' in data else None
    try:
        cart = Shopcart(user_id, products)
    except DataValidationError as e:
        message = {'error': e.args[0]}
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    # If correct save it and return object
    cart.save()
    message = cart.serialize()
    location_url = url_for('get_shopcarts', id=int(cart.user_id), _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {'Location': location_url})

######################################################################
# UPDATE AN EXISTING Shopcart product
######################################################################
@app.route('/shopcarts/<int:user_id>/products/<int:pid>', methods=['PUT'])
def update_shopcart(user_id, pid):
    """
    Update a Shopcart
    This endpoint will update a Shopcart based the body that is posted
    """
    check_content_type('application/json')
    cart = Shopcart.find(user_id)

    if not cart:
        message = {'error' : 'Shopcart with id: %d was not found' % user_id}
        rc = status.HTTP_404_NOT_FOUND
        return make_response(jsonify(message), rc)

    prods_cart = cart.serialize()['products']
    if not pid in prods_cart.keys():
        message = {'error' : 'Product %d is not on shopcart %d' % (pid, user_id)}
        rc = status.HTTP_404_NOT_FOUND
        return make_response(jsonify(message), rc)

    data = request.get_json()
    try:
        quantity = data['quantity']
    except KeyError:
        message = {'error': 'Update product needs a quantity'}
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    if not isinstance(quantity, int):
        message = {'error': 'Update product needs a valid quantity'}
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    cart.update_product(pid, quantity)
    cart.save()

    return make_response(jsonify(cart.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A PRODUCT TO A SHOPCART
######################################################################
@app.route('/shopcarts/<int:user_id>/products', methods=['POST'])
def add_product(user_id):
    """Add a product to the shopcart with the given user_id"""
    cart = Shopcart.find(user_id)

    if not cart:
        return jsonify("Cart with id '{}' was not found.".format(user_id)), status.HTTP_404_NOT_FOUND

    try:
        cart.add_products(request.get_json())
        cart.save()
    except DataValidationError as e:
        message = {'error': e.args[0]}
        return jsonify(message), status.HTTP_400_BAD_REQUEST

    return make_response(jsonify(cart.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE A PRODUCT FROM A SHOPCART
######################################################################
@app.route('/shopcarts/<int:user_id>/products/<int:pid>', methods=['DELETE'])
def delete_product(user_id, pid):
    cart = Shopcart.find(user_id)
    if cart:
        cart.delete_product(pid)
    return make_response('', status.HTTP_204_NO_CONTENT)

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

######################################################################
# Get all available Products
######################################################################
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.all()
    message = [product.serialize() for product in products]

    return jsonify(message), status.HTTP_200_OK

######################################################################
# DELETE ALL SHOPCART DATA (for testing only)
######################################################################
@app.route('/shopcarts/reset', methods=['DELETE'])
def shopcarts_reset():
    """ Removes all shopcarts from the database """
    Shopcart.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """ Checks that the media type is correct """
    if content_type in request.headers['Content-Type']:
        return
    #app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, 'Content-Type must be {}'.format(content_type))

def init_db():
    """ Initializes the SQLAlchemy app """
    Shopcart.init_db()
    Product.seed_db()
