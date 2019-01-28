import pytest
from django.conf import settings

from surveys.models import Question, Option

pytestmark = pytest.mark.django_db


def test_option_parentage(option: Option):
    assert option.question is not None
    assert option.question.section is not None
    assert option.question.section.survey is not None


# def test_explore_question_form(question: Question):
#
