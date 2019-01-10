Feature: Hospitals
  As the administrator of correspondents information I want to list, create, edit, and delete hospitals

  Scenario: Add a first Hospital
    Given there are as yet no hospitals
    And I am logged in as admin
    When I login to admin ui
    And I select add-hospital
    And I submit the add-hospital form for "Hospital 1"
    Then I am returned to the hospitals list
    And I see one hospital row
    And The title of the hospital is "Hospital 1"


  Scenario: Add a department to a Hospital
    Given that a hospital "Hospital 1" is defined in the system
    And no departments exist
    And I am logged in as admin
    When I login to admin ui
    And I select add-department
    And I submit the add-department form for "emergency dept" to hospital "Hospital 1"
    Then I am returned to the department list
    And I see one department row
    And the name of the department is "emergency dept"
