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
    text = Faker("sentence", nb_words=10)
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

        # Make the last question in the last section a multi, for later tests
        for section in su.sections():
            for question in section.questions():
                pass
        lastq = question
        lastq.qtype = 'MULTICHOICE'
        lastq.save()

        surveys.append(su)
    return surveys


# def tight_survey_structure(surveyname=None):
#     # allow a one-shot survey name
#     if surveyname is not None:
#         survey_kwargs = dict(name=surveyname)
#     else:
#         survey_kwargs = dict()
#
#     surveys = []
#     for sui in range(2):
#         su = SurveyFactory(**survey_kwargs)
#         survey_kwargs = dict()
#         for sei in range(4):
#             se = SectionFactory(survey=su, title=f"this is section {sei}")
#             for qui in range(4):
#                 qu = QuestionFactory(
#                     section=se,
#                     text=f"text for question {qui}, with original order {qui}",
#                 )
#                 for opi in range(4):
#                     _ = OptionFactory(question=qu, text=f"text for option {opi}")
#
#         # Make the second question in the first section a multi, for later tests
#         section = su.section_set.first()
#         second = section.question_set.all()[1]
#         second.qtype = 'MULTICHOICE'
#         second.save()
#
#         surveys.append(su)
#     return surveys


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

            # first question
            qui = 0
            qu = QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Single Choice",
                qtype='SINGLECHOICE'

            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # second question
            qui = 1
            qu = QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Multiple Choice",
                qtype='MULTICHOICE'
            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # third question
            qui = 2
            qu = QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Select (Dropdown)",
                qtype='SELECT'
            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # fourth question
            qui = 3
            QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Text input",
                qtype='TEXT'
            )

            # fifth question
            qui = 4
            QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Essay input",
                qtype='ESSAY'
            )

            # sixth question
            qui = 5
            QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Integer input",
                qtype='INTEGER'
            )

            # seventh question
            qui = 6
            QuestionFactory(
                section=se,
                text=f"text for question {qui}, with original order {qui} - Email input",
                qtype='EMAIL'
            )

        surveys.append(su)
    return surveys
