import pytest
import os

from surveys.reports import create_survey_output, embellish_table
from surveys.tests.factories import create_answered_survey

pytestmark = pytest.mark.django_db


def test_first_report():
    su = create_answered_survey()
    create_survey_output(su)


def test_embellish():
    testdir = os.path.dirname(os.path.realpath(__file__))
    h = open(os.path.join(testdiryes
                          , 'report.html'), 'r').read()
    print(embellish_table(h))
