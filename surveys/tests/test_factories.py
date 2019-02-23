import pytest

from surveys.tests.factories import pet_survey, several_long_surveys, several_tight_surveys, create_answered_survey

pytestmark = pytest.mark.django_db


class TestSurveyCreationAndDeletion:

    def test_creation_and_deletion_pet_survey(self):
        psu = pet_survey(f"Pet Survey 1")
        psu.delete()

    def test_creation_and_deletion_basic_survey(self):
        surveys = several_long_surveys(f"Survey Basic")
        for survey in surveys:
            survey.delete()

    def test_creation_and_deletion_tight_surveys(self):
        surveys = several_tight_surveys(f"Survey Tight")
        for survey in surveys:
            survey.delete()

    def test_create_answered_survey(self):
        surveys = []
        for i in range(3):
            surveys.append(create_answered_survey())
        for s in surveys:
            s.delete()
        # TODO : check that the database population has not changed
        #  answers, questions, sections, options, etc.



