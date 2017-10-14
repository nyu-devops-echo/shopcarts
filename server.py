import os
from flask import Flask, jsonify
from flask_api import status
from models.shopcart import Shopcart

app = Flask(__name__)

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

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
        rc = HTTP_200_OK
    else:
        message = { 'error' : 'Shopcart with id: %s was not found' % str(id) }
        rc = HTTP_404_NOT_FOUND

    return jsonify(message), rc


if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
