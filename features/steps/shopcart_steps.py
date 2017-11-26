"""
Pet Steps
Steps file for Pet.feature
"""

import json
import requests
from behave import *

@when(u'I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in context.driver.find_element_by_id('app-js').text

@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in context.driver.find_element_by_id('app-js').text

@given(u'the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/shopcarts/reset', headers=headers)
    assert context.resp.status_code == 204
    create_url = context.base_url + '/shopcarts'
    for row in context.table:
        data = {"user_id": row['user_id']}
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        assert context.resp.status_code == 201

@when(u'I visit Shopcart "{user_id}"')
def step_impl(context, user_id):
    button_id = 'view-shopcart-' + user_id
    context.driver.find_element_by_id(button_id).click()

@when(u'I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then(u'I should not see Shopcart "{user_id}" in the results')
def step_impl(context, user_id):
    element = context.driver.find_element_by_id('shopcarts-table-list')
    assert not element.find_elements_by_id('shopcart-' + user_id + '-row')
