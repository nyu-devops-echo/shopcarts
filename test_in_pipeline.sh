#!/bin/bash

#DONT FORGET TO ADD ENVIORMENT VARIABLES VCAPS_SERVICE AND DATABASE_URI

sudo pip install virtualenv
virtualenv -p /usr/bin/python3 .
source bin/activate
pip3 install -r requirements.txt
pip3 install nose==1.3.7
nosetests-3.4