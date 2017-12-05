"""
Microservice module

This module contains the microservice code for
    server
    models
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the Flask aoo
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app import server, models
from flasgger import Swagger

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Shopcarts REST API Service",
            "description":"This is the Shopcart API",
            "endpoint": 'v1_spec',
            "route": '/v1/spec',
            "basePath": '/'
        }
    ],
}

# Initialize Swagger after configuring it
Swagger(app)
