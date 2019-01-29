import pytest

from surveys.models import Option

pytestmark = pytest.mark.django_db


def test_option_parentage(option: Option):
    assert option.question is not None
    assert option.question.section is not None
    assert option.question.section.survey is not None
