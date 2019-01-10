Feature: Hospitals
  As the administrator of correspondents information I want to list, create, edit, and delete hospitals

  Scenario: Add a first Hospital
    Given there are as yet no hospitals
    And I am logged in as admin
    When I login to admin ui
    And I select add-hospital
    And I submit the add-hospital form for "Hospital 1"
    Then I am returned to the correspondents page
    And I see one survey row
    And The title of the survey is "Hospital 1"



