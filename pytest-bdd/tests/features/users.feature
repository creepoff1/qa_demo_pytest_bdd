Feature: Users endpoints
  As a client of ReqRes
  I want to work with users collection and items

  Scenario Outline: Get users list returns 200 and valid payload
    When I GET "/api/users" with query params:
      | page | <page> |
    Then the response status code should be 200
    And the response should match the schema "users_list_schema.json"
    And the field "data" should be an array with at least 1 item

    Examples:
      | page |
      | 1    |
      | 2    |

  Scenario: Get single existing user (id=2)
    When I GET "/api/users/2"
    Then the response status code should be 200
    And the response should match the schema "user_single_schema.json"

  Scenario: Get single missing user (id=23) -> 404
    When I GET "/api/users/23"
    Then the response status code should be 404

  Scenario: Delayed response (3s)
    When I GET "/api/users" with query params:
      | delay | 3 |
    Then the response status code should be 200
    And the response should match the schema "users_list_schema.json"
