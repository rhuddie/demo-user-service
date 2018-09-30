Feature: Add user form

  Scenario: Add a new user to the system
    Given I start with an empty database
    And I am on the add new user form
    And I enter username bilbobaggins
    And I enter email bilbo@baggins.com
    And I enter dob 22/9/54
    And I enter address Bag End, Hobbiton
    When I press the Add button
    Then I see user was added successfully
    And there are 1 users in the database
    And user database contains 1 record matching: bilbobaggins, bilbo@baggins.com, 22/9/54, Bag End, Hobbiton

  Scenario: Attempt to add a duplicate user to the system
    Given I start with a database with test user already added
    And I am on the add new user form
    And I enter username bilbobaggins
    And I enter email bilbo@baggins.com
    And I enter dob 22/9/54
    And I enter address Bag End, Hobbiton
    When I press the Add button
    Then I see user was not added successfully
    And there are 1 users in the database
    And user database contains 1 record matching: bilbobaggins, bilbo@baggins.com, 22/9/54, Bag End, Hobbiton

  Scenario: Add a new user to the system with existing user
    Given I start with a database with test user already added
    And I am on the add new user form
    And I enter username frodobaggins
    And I enter email frodo@baggins.com
    And I enter dob 7/5/73
    And I enter address 2b Bag End, Hobbiton
    When I press the Add button
    Then I see user was added successfully
    And there are 2 users in the database
    And user database contains 1 record matching: bilbobaggins, bilbo@baggins.com, 22/9/54, Bag End, Hobbiton
    And user database contains 1 record matching: frodobaggins, frodo@baggins.com, 7/5/73, 2b Bag End, Hobbiton
