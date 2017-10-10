import os
from flask import Flask, jsonify
from flask_api import status

app = Flask(__name__)

DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

@app.route("/")
def home():
    return jsonify("Home"), status.HTTP_200_OK


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
