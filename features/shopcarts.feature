Feature: The shopcarts service back-end
    As a Shopcarts Owner
    I need a RESTful shopcarts service
    So that I can keep track of all the products in my Shopcart

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service" in the name
    And I should not see "404 Not Found"

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
