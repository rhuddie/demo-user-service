Feature: Add user form

  Scenario: Add a new user to the system
    Given I am on the add new user form
    And I enter username bilbobaggins
    And I enter email address bilbo@baggins.com
    And I enter dob 22/9/54
    And I enter address Bag End, Hobbiton
    When I press the Add button
    Then I see user is added successfully
