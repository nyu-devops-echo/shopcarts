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
# RETRIEVE A Shopcart 
######################################################################
@app.route('/shopcarts/<int:user_id>', methods=['GET'])
def get_shopcarts(uid):
    """
    Retrieve a single shopcart
    This endpoint will return a shopcart based on it's user id
    """
    shopcart = Shopcart.find(uid)
    if not shopcart:
        raise Exception("Shopcart with id '{}' was not found.".format(uid))
    return make_response(jsonify(shopcart.serialize()), status.HTTP_200_OK)

######################################################################
# ADD A NEW CART
######################################################################
@app.route('/shopcarts', methods=['POST'])
def create_shopcart():
    """
    Creates a shopcart
    This endpoint will create a shopcart based the data in the body that is posted
    """
    shopcart = Shopcart()
    shopcart.deserialize(request.get_json())
    shopcart.save()
    message = shopcart.serialize()
    location_url = url_for('get_shopcarts', shopcart_id=shopcart.uid, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
