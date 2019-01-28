import pytest
from django.conf import settings
from django.test import RequestFactory

from surveys.models import Question, Survey, Option
from surveys.tests.factories import QuestionFactory, SurveyFactory, OptionFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def survey() -> Survey:
    return SurveyFactory()


@pytest.fixture
def question() -> Question:
    return QuestionFactory()


@pytest.fixture
def option() -> Option:
    return OptionFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
