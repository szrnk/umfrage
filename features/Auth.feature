# Created by russ at 2019-01-03
Feature: Auth
  Preliminary authentication

  Scenario: Unauthenticated user can't access the page
    Given I am not authenticated
    When I access the page
    Then Status code is 200
    # TODO  Make this prove that an unauthenticated user can do nothing dangerour


