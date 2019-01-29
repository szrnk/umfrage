import pytest
from django.test import RequestFactory

from correspondents.models import Department, Hospital
from correspondents.tests.factories import DepartmentFactory, HospitalFactory
from surveys.models import Question, Survey, Option
from surveys.tests.factories import QuestionFactory, SurveyFactory, OptionFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


# MODELS ##########################


@pytest.fixture
def department() -> Department:
    return DepartmentFactory()


@pytest.fixture
def option() -> Option:
    return OptionFactory()


@pytest.fixture
def hospital() -> Hospital:
    return HospitalFactory()


@pytest.fixture
def question() -> Question:
    return QuestionFactory()


@pytest.fixture
def survey() -> Survey:
    return SurveyFactory()


# FORMS #########################


# MISC #########################


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
