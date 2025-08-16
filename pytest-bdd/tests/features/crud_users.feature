Feature: Create/Update/Delete user

  Scenario: Create user
    When I POST "/api/users" with json:
      | name | morpheus |
      | job  | leader   |
    Then the response status code should be 201
    And the response should match the schema "create_user_schema.json"

  Scenario: Full update user (PUT)
    When I PUT "/api/users/2" with json:
      | name | morpheus        |
      | job  | zion resident   |
    Then the response status code should be 200
    And the response should match the schema "update_user_schema.json"

  Scenario: Partial update user (PATCH)
    When I PATCH "/api/users/2" with json:
      | job  | architect   |
    Then the response status code should be 200
    And the response should match the schema "update_user_schema.json"

  Scenario: Delete user
    When I DELETE "/api/users/2"
    Then the response status code should be 204
