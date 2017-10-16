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
@app.route('/shopcarts/<int:id>', methods=['PUT'])
def create_shopcart(id):
    """Creates a shopcart and saves it to database
        POST Request accepts data as: 
        - id + prod id (sets default to 1)
        - id + {prod:quant}
    """
    # if cart = Shopcart.find(id):
        # Not clear on what to do here
    #     return 
    cart = Shopcart()
    try:
        cart.deserialize(  request.get_json() )
    except DataValidationError as e:
        message = {'error': e.args[0]}
        return jsonify(message), status.HTTP_400_BAD_REQUEST
    cart.save()
    message = cart.serialize()
    location_url = url_for('get_shopcarts', id = int( cart.uid ), _external=True)    
    return make_response(jsonify(message), status.HTTP_201_CREATED, { 'Location': location_url })
    
if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
