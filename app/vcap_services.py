# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
VCAP Services module

This module initializes the database connection String
from VCAP_SERVICES in Bluemix if Found
"""
import os
import json

def get_database_uri():
    """
    Initialized MySQL database connection

    This method will work in the following conditions:
      1) In Bluemix with Redis bound through VCAP_SERVICES
      2) With MySQL running on the local server as with Travis CI
    """
    # Get the credentials from the Bluemix environment
    if 'VCAP_SERVICES' in os.environ:
        vcap_services = os.environ['VCAP_SERVICES']
        services = json.loads(vcap_services)
        creds = services['cleardb'][0]['credentials']
        #uri = creds["uri"]
        username = creds["username"]
        password = creds["password"]
        hostname = creds["hostname"]
        port = creds["port"]
        name = creds["name"]
    else:
        username = 'root'
        password = 'root'
        hostname = 'localhost'
        port = '3306'
        name = 'shopcarts'

    if 'TRAVIS' in os.environ:
        password = ''
    
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'
    return connect_string.format(username, password, hostname, port, name)
