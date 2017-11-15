"""
Microservice module

This module contains the microservice code for
    server
    models
"""
from flask import Flask

# Create the Flask aoo
app = Flask(__name__)

from .models import init_db
init_db(app)

# Server needs app so must be placed after app is created
from . import server
