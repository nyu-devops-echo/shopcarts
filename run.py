"""
Shopcart Service Runner

Start the Shopcart Service
"""

import os
from app import app, server

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print("*************************************************")
    print(" S H O P C A R T   S E R V I C E   R U N N I N G ")
    print("*************************************************")
    server.init_db()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
