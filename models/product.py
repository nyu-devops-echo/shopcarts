import os
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:////tmp/echo.db'
db = SQLAlchemy(app)

class Product(db.Model):
    """This is the model for the products in the shopping carts
    Assumptions: (*** FOR SPRINT 0 ***)
        - In memory persistance 
        - Property includes:
            - product id
            - name
            - price 
            - description
        - Model should only initially include init method and product fields.
    """ 
    
    __data = []
    __index = 0

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, unique=False, nullable=False)
    description = db.Column(db.String(140), unique=False, nullable=True)

    def __repre__(self):
        return '<Name %r>' % self.name

    """no need to define the __init__ method for Product
    because SQLAlchemy adds an implicit constructor to all model classes 
    which accepts keyword arguments for all its columns and relationships"""
    def __init__(self, id=0, name='', price=0.0, description=None):
        """
        Initializing Product
        """
        self.id = int(id)
        self.name = name
        self.price = float(price)
        self.description = description


######################################################################
#  M y S Q L   D A T A B A S E   C O N N E C T I O N   M E T H O D S
######################################################################

