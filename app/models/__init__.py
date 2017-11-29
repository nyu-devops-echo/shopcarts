import os
import json
import warnings
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, migrate_db=True):
    # Get service credentials from Bluemix
    if 'VCAP_SERVICES' in os.environ:
        vcap = json.loads(os.environ['VCAP_SERVICES'])
        creds = vcap['cleardb'][0]['credentials']
        db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            creds['username'], creds['password'], creds['hostname'], creds['port'], creds['name'])
    else:
        db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            'root', 'root', '127.0.0.1', '3306', 'shopcarts')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3600
    db.init_app(app)

    if not migrate_db:
        return

    with app.app_context():
        from .shopcart import Shopcart
        from .product import Product
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            db.create_all()
