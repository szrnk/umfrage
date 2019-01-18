from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, post_generation, Sequence
from ..models import Survey, Section, Question, Option


class SurveyFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Survey %03d" % n)

    class Meta:
        model = Survey


class SectionFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Section %03d" % n)
    title = Faker('sentence', nb_words=7)

    class Meta:
        model = Section


class QuestionFactory(DjangoModelFactory):

    code = Sequence(lambda n: "QCode%03d" % n)
    text = Faker('sentence', nb_words=30)
    order = Sequence(lambda n: n)

    class Meta:
        model = Question


class OptionFactory(DjangoModelFactory):

    code = Sequence(lambda n: "OCode%03d" % n)
    text = Faker('sentence', nb_words=30)
    order = Sequence(lambda n: n)

    class Meta:
        model = Option


def basic_structure():
    surveys = []
    for sui in range(2):
        su = SurveyFactory()
        for sei in range(4):
            se = SectionFactory(survey=su)
            for qui in range(4):
                qu = QuestionFactory(section=se)
                for opi in range(4):
                    _ = OptionFactory(question=qu)
        surveys.append(su)
    return surveys
