import pytest

from surveys.reports import create_survey_output
from surveys.tests.factories import create_answered_survey

pytestmark = pytest.mark.django_db


def test_first_report():
    su = create_answered_survey()
    create_survey_output(su)
