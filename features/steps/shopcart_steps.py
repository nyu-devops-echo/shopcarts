"""
Pet Steps
Steps file for Pet.feature
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

# CREATE A SHOPCART
@when(u'I set the "{user_id}" to "{value}"')
def step_impl(context, user_id, value):
    element = context.driver.find_element_by_id(user_id)
    element.clear()
    element.send_keys(value)

@when(u'I click the "{create}" button')
def step_impl(context, create):
    button_id = 'shopcart-' + create.lower()
    context.driver.find_element_by_id(button_id).click()

# FIXME
@then(u'I should see cart with id "{id}" in the All Shopcarts table')
def step_impl(context, id):
    table = context.driver.find_element_by_id('shopcarts-table-list')
    print (table.text)
    assert id in table.text
