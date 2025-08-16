Feature: Auth endpoints

  Scenario: Register successful
    When I POST "/api/register" with json:
      | email    | eve.holt@reqres.in |
      | password | pistol             |
    Then the response status code should be 200
    And the response should match the schema "register_success_schema.json"

  Scenario: Register missing password -> 400
    When I POST "/api/register" with json:
      | email | sydney@fife |
    Then the response status code should be 400
    And the response should match the schema "register_error_schema.json"

  Scenario: Login successful
    When I POST "/api/login" with json:
      | email | eve.holt@reqres.in |
      | password | cityslicka      |
    Then the response status code should be 200
    And the response should match the schema "login_success_schema.json"

  Scenario: Login missing password -> 400
    When I POST "/api/login" with json:
      | email | peter@klaven |
    Then the response status code should be 400
