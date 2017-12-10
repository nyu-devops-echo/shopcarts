#!/bin/bash

#Nosetests
#DONT FORGET TO ADD ENVIORMENT VARIABLES VCAPS_SERVICE AND DATABASE_URI

sudo pip install virtualenv
virtualenv -p /usr/bin/python3 .
source bin/activate
pip3 install -r requirements.txt
pip3 install nose==1.3.7
nosetests-3.4



#Integration tests
#DONT FORGET TO ADD BASE_URL to the env pointing to the dev app in bluemix.

# Install Chrome and chromedriver for Selenium browser support
sudo apt-get update
sudo apt-get install -y unzip libgconf-2-4 libnss3-dev
sudo apt-get install -y chromium-browser
wget -N http://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d bin
export PATH=$(pwd)/bin:$PATH

echo "chromium installed?"
which chromium-browser
chromium-browser --no-sandbox -version

echo "chromedriver installed?"
which chromedriver

echo "PATH"
echo $PATH
 
# Setup python app
sudo pip install virtualenv
virtualenv -p /usr/bin/python3.4 .
source bin/activate
pip3 install -r requirements.txt

# Run integration tests
behave