"""
Shopcart Steps
Steps file for shopcarts.feature
"""
from os import getenv
import json
import requests
from behave import *
from app import server

BASE_URL = getenv('BASE_URL', 'http://localhost:5000/')

@when(u'I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}" in the name')
def step_impl(context, message):
    assert message in context.driver.find_element_by_tag_name('body').text

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.driver.find_element_by_tag_name('body').text

@when(u'I visit "{location}"')
def step_impl(context,location):
    """ Make a call to http://localhost:5000 + location"""
    context.driver.get(context.base_url +  location)

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.driver.find_element_by_tag_name('body').text
