import os
from flask import Flask, jsonify, request, url_for, make_response
from flask_api import status
from models.shopcart import Shopcart

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
# DELETE A PRODUCT FROM A SHOPCART
######################################################################
@app.route('/shopcarts/<int:uid>/products/<int:pid>', methods=['DELETE'])
def delete_product(uid, pid):
    cart = Shopcart.find(uid)
    if cart:
        cart.delete_product(pid)
    return make_response('', status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
    # dummy data for server testing
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
