Feature: List user form

  @testcase
  Scenario: List users of an empty database
    Given I start with an empty database
    And I am on the list users form
    Then I see 0 users listed
