import pytest
from django.conf import settings

from surveys.models import Question

pytestmark = pytest.mark.django_db


def test_option_parentage(option: Question):
    assert option.question is not None
    assert option.question.section is not None
    assert option.question.section.survey is not None
