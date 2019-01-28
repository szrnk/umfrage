from factory import DjangoModelFactory, Faker, Sequence, SubFactory

from ..models import Survey, Section, Question, Option


class SurveyFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Survey %03d" % n)

    class Meta:
        model = Survey


class SectionFactory(DjangoModelFactory):

    survey = SubFactory(SurveyFactory)
    name = Sequence(lambda n: "Section %03d" % n)
    title = Faker("sentence", nb_words=7)
    order = Sequence(lambda n: n)

    class Meta:
        model = Section


class QuestionFactory(DjangoModelFactory):
    section = SubFactory(SectionFactory)
    code = Sequence(lambda n: "QCode%03d" % n)
    text = Faker("sentence", nb_words=30)
    order = Sequence(lambda n: n)

    class Meta:
        model = Question


class OptionFactory(DjangoModelFactory):
    question = SubFactory(QuestionFactory)
    code = Sequence(lambda n: "OCode%03d" % n)
    text = Faker("sentence", nb_words=30)
    order = Sequence(lambda n: n)

    class Meta:
        model = Option


def basic_survey_structure(surveyname=None):
    # allow a one-shot survey name
    if surveyname is not None:
        survey_kwargs = dict(name=surveyname)
    else:
        survey_kwargs = dict()

    surveys = []
    for sui in range(2):
        su = SurveyFactory(**survey_kwargs)
        survey_kwargs = dict()
        for sei in range(4):
            se = SectionFactory(survey=su)
            for qui in range(4):
                qu = QuestionFactory(section=se)
                for opi in range(4):
                    _ = OptionFactory(question=qu)
        surveys.append(su)
    return surveys


def tight_survey_structure(surveyname=None):
    # allow a one-shot survey name
    if surveyname is not None:
        survey_kwargs = dict(name=surveyname)
    else:
        survey_kwargs = dict()

    surveys = []
    for sui in range(2):
        su = SurveyFactory(**survey_kwargs)
        survey_kwargs = dict()
        for sei in range(4):
            se = SectionFactory(survey=su, title=f"this is section {sei}")
            for qui in range(4):
                qu = QuestionFactory(
                    section=se,
                    text=f"text for question {qui}, with original order {qui}",
                )
                for opi in range(4):
                    _ = OptionFactory(question=qu, text=f"text for option {opi}")
        surveys.append(su)
    return surveys
