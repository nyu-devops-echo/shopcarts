import os
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
from models.shopcart import Shopcart
from models.dataerror import DataValidationError

app = Flask(__name__)
DEBUG = (os.getenv('DEBUG', 'True') == 'True')
PORT = os.getenv('PORT', '5000')

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
