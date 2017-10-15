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
@app.route('/shopcarts/', methods=['POST'])
def create_shopcart():
    """
        Creates a shopcart and saves it to database
        POST Request accepts data as:
            - no id (Finds the first available and assigns it)
            - id 
            - id + one product id (Model sets quant to 1)
            - id + dictionary of {prod_id:quant}
    """
    dat= request.get_json()
    if Shopcart.find( dat['uid'] ):
        message = { 'ERROR' : 'Shopcart with id: %s is in Database' % str(id) }
        return make_response(jsonify(message), status.HTTP_400_BAD_REQUEST )
    
    try:
        prods ={}
        if 'products' in dat.keys():
            try:
                if type(dat['products']) == dict:
                    prods = { int(p):int(q) for (p,q) in dat['products'].items() }
                else:
                    prods = dat['products']
            except ValueError as e:
                raise DataValidationError('ERROR: %s has an invalid format for products'% dat['products'])

        if 'uid' in dat.keys():
            uid = dat['uid']
        else:
            uid = Shopcart().get_available_id()
        cart = Shopcart(uid, prods )
    except DataValidationError as e:
        return make_response( jsonify(e.args[0]) , status.HTTP_400_BAD_REQUEST )

    cart.save()
    message = cart.serialize()
    location_url = url_for('get_shopcarts', id=cart.uid, _external=True)
    return jsonify(message), status.HTTP_201_CREATED, {'Location': location_url}

if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
