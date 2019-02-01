Feature: Surveys
  As the administrator of surveys I want to list, create, edit, and delete surveys

  Scenario: Add a first survey in the admin dashboard
    Given there are as yet no surveys
    And I am logged in as admin
    When I login to admin ui
    And I select add-survey
    And I submit the add-survey form for "survey1"
    Then I am returned to the surveys page
    And I see one survey row
    And The title of the survey is "survey1"

  Scenario: User responds to Invitation by creating login, confirming email, and seeing the survey
    Given there is a basic_survey called "My Basic Survey"
    And a typical_hospital exists called "Typical Hospital" with department "Emergency Department"
    And an invitation for "My Basic Survey" has been extended to "Emergency Department" of "Typical Hospital"
    When I visit the link from the invitation
    And I create a user account for "zina", "zina@example.com", "zina-the-tricky"
    And I confirm the email address
    And I login as "zina", "zina-the-tricky"
    Then the relevant ids are in my session
    And I can see the invitation to "My Basic Survey" in my "zina" profile list of invitations
    # And The session has a progress structure for "My Basic Survey" and both section and question indices are 0
    And There is section, question, and option text for each level of "My Basic Survey"
    And The final question of "My Basic Survey" is multichoice
