import os
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status
from models.shopcart import Shopcart
from models.dataerror import DataValidationError

app = Flask(__name__)
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
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
    
if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
