import json
import os
import unittest
from unittest.mock import patch
from app.vcap_services import get_database_uri

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

class TestVcapServices(unittest.TestCase):
    """ VCAP Services Tests """

    @patch.dict(os.environ, {'VCAP_SERVICES': json.dumps(VCAP_SERVICES)})
    @patch.dict(os.environ, {'DATABASE_URI': 'mysql+pymysql://vcap_user:vcap_pass@127.0.0.2:3307/vcap' })
    def test_get_database_uri_vcap(self):
        """ Test if it gets the vcap db uri """
        db_uri = os.getenv('DATABASE_URI')
        result = get_database_uri()
        self.assertEqual(result, db_uri)

    def test_get_database_uri_local(self):
        """ Test if it gets the local db uri """
        db_uri = os.getenv('DATABASE_URI', "mysql+pymysql://root:@localhost:3306/shopcarts")
        result = get_database_uri()
        self.assertEqual(result, db_uri)

if __name__ == '__main__':
    unittest.main()
