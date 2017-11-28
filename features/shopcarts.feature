Feature: The shopcarts service back-end
    As a Shopcarts Owner
    I need a RESTful shopcarts service
    So that I can keep track of all the products in my Shopcart

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service"
    And I should not see "404 Not Found"

Scenario: List all shopcarts
    Given the following shopcarts
        | user_id   |
        | 2         |
        | 3         |
        | 4         |
    When I visit the "Home Page"
    Then I should see "2" in the results
    And I should see "3" in the results
    And I should see "4" in the results

Scenario: Create a Shopcart
    When I visit the "Home Page"
    And I set the Shopcart "user_id" to "1"
    And I click the "Add Products" button
    And I add "1" "Apple" to the cart
    And I click the "Create" button
    Then I should see Shopcart "1" in the results
    And I should not see "Status Code: 409. Shopcart for user 1 already exits" in the form

Scenario: Delete a Shopcart
    Given the following shopcarts
        | user_id |
        | 1     |
    When I visit the "Home Page"
    And I visit Shopcart "1"
    And I click the "Delete" button
    Then I should not see Shopcart "1" in the results

Scenario: Delete a Product from a Shopcart
    Given the following shopcarts
        | user_id | product_id | quantity |
        | 1       | 2          | 5        |
    When I visit the "Home Page"
    And I visit Shopcart "1"
    And I delete product "2" from the cart
    Then I should see "No products in this shopcart"