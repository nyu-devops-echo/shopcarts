Feature: The shopcarts service back-end
    As a Shopcarts Owner
    I need a RESTful shopcarts service
    So that I can keep track of all the products in my Shopcart

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service"
    And I should not see "404 Not Found"

<<<<<<< HEAD
Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the "user_id" to "1"
    And I click the "Create" button
    Then I should see cart with id "1" in the All Shopcarts table


# Scenario: Create a Shopcart with Products
#     When I visit the "Home Page"
#     And I set the user_id to "1"
#     And I click
#     And I click the "Create" button
#     Then I should see the cart in the All Shopcarts table
=======
Scenario: Delete a Shopcart
    Given the following shopcarts
        | user_id |
        | 1     |
    When I visit the "Home Page"
    And I visit Shopcart "1"
    And I press the "Delete" button
    Then I should not see Shopcart "1" in the results
>>>>>>> 57286c6b945a243ea51c83135359ae5e3bc6e87f
