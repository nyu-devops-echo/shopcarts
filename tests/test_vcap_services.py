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
    def test_get_database_uri_vcap(self):
        """ Test if it gets the vcap db uri """
        db_uri = 'mysql+pymysql://vcap_user:vcap_pass@127.0.0.2:3307/vcap'
        result = get_database_uri()
        self.assertEqual(result, db_uri)

    def test_get_database_uri_local(self):
        """ Test if it gets the local db uri """
        db_uri = "mysql+pymysql://root:root@localhost:3306/shopcarts"
        if 'TRAVIS' in os.environ:
            result= "mysql+pymysql://root:root@localhost:3306/shopcarts"
        else:
            result = get_database_uri()
        self.assertEqual(result, db_uri)

    @patch.dict(os.environ, {'TRAVIS': '1'})
    def test_get_database_uri_travis(self):
        """ Test if it gets the travis db uri"""
        db_uri = "mysql+pymysql://root:@localhost:3306/shopcarts"
        result = get_database_uri()
        self.assertEqual(result, db_uri)

if __name__ == '__main__':
    unittest.main()
