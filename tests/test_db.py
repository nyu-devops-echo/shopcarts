import json
import os
import unittest
from unittest.mock import patch
from flask import Flask
from app.models import init_db

VCAP_SERVICES = {
    'cleardb': [
        {
            'credentials': {
                'username': 'vcap_user',
                'password': 'vcap_pass',
                'hostname': '127.0.0.2',
                'port': '3307',
                'name': 'vcap'
            }
        }
    ]
}

class TestDb(unittest.TestCase):
    """ Database Tests """

    @patch.dict(os.environ, {'VCAP_SERVICES': json.dumps(VCAP_SERVICES)})
    def test_vcap_services(self):
        """ Test if VCAP_SERVICES works """
        app = Flask(__name__)
        init_db(app, migrate_db=False)

        db_uri = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            'vcap_user', 'vcap_pass', '127.0.0.2', '3307', 'vcap')

        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], db_uri)

if __name__ == '__main__':
    unittest.main()
