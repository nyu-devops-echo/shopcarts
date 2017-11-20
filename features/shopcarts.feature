Feature: The shopcarts service back-end
    As a Shopcarts Owner
    I need a RESTful shopcarts service
    So that I can keep track of all the products in my Shopcart

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Shopcarts REST API Service" in the name
    And I should not see "404 Not Found"

Scenario: List all shopcarts
    When I visit "/shopcarts"
    Then I should see "[]"
    And I should not see "404 Not Found"

