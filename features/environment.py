"""
Environment for Behave Testing
"""
import os
from behave import *
from selenium import webdriver

BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

def before_all(context):
    """ Executed once before all tests """
    # Set Headless Chrome as driver
    options = webdriver.ChromeOptions()
    options.set_headless()
    context.driver = webdriver.Chrome(chrome_options=options)

    # Polls the DOM if an element is not immediately available
    context.driver.implicitly_wait(5)

    context.base_url = BASE_URL
