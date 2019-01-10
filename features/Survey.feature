Feature: Surveys
  As the administrator of surveys I want to list, create, edit, and delete surveys

  Scenario: Add a first survey
    Given there are as yet no surveys
    And I am logged in as admin
    When I login to admin ui
    And I select add-survey
    And I submit the add-survey form for "survey1"
    Then I am returned to the surveys page
    And I see one survey row
    And The title of the survey is "survey1"


