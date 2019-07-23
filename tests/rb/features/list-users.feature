Feature: List user form

  Scenario: List users of an empty database
    Given I start with an empty database
    And I am on the list users form
    Then I see 0 users listed

    Scenario: List users of a populated database
    Given I start with a database with test user already added
    And I am on the list users form
    Then I see 1 users listed
    And I see a record with values: bilbobaggins, bilbo@baggins.com, 22/9/1954, Bag End, Hobbiton
