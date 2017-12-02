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
