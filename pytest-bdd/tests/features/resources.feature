Feature: Resources (unknown)

  Scenario: Get resource list
    When I GET "/api/unknown"
    Then the response status code should be 200
    And the response should match the schema "resource_list_schema.json"

  Scenario: Get single resource (id=2)
    When I GET "/api/unknown/2"
    Then the response status code should be 200
    And the response should match the schema "resource_single_schema.json"

  Scenario: Get missing resource (id=23) -> 404
    When I GET "/api/unknown/23"
    Then the response status code should be 404
