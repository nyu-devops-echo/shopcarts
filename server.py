import os
from flask import Flask, jsonify
from flask_api import status

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
