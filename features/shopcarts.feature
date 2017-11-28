Feature: The shopcarts service back-end
    As a Shopcarts Owner
    I need a RESTful shopcarts service
    So that I can keep track of all the products in my Shopcart

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service"
    And I should not see "404 Not Found"

Scenario: List all shopcarts
    When I visit "/shopcarts"
    Then I should see "[]"
    And I should not see "404 Not Found"

Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the Shopcart "user_id" to "1"
    And I click the "Add Products" button
    And I add "1" "Apple" to the cart
    And I click the "Create" button
    Then I should see Shopcart "1" in the results

Scenario: Delete a Shopcart
    Given the following shopcarts
        | user_id |
        | 1     |
    When I visit the "Home Page"
    And I visit Shopcart "1"
    And I press the "Delete" button
    Then I should not see Shopcart "1" in the results

