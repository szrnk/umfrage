from factory import DjangoModelFactory, Faker, Sequence, SubFactory

from ..models import Survey, Section, Question, Option, DisplayByOptions, DisplayByValue


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
    parent_section = SubFactory(SectionFactory)
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


class DisplayByOptionsFactory(DjangoModelFactory):
    trigger_question = SubFactory(QuestionFactory)
    shown_element = SubFactory(QuestionFactory)

    class Meta:
        model = DisplayByOptions


class DisplayByValueFactory(DjangoModelFactory):
    trigger_question = SubFactory(QuestionFactory)
    shown_element = SubFactory(QuestionFactory)
    value = 0
    condition = '=='

    class Meta:
        model = DisplayByValue


def several_long_surveys(surveyname=None):
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
                qu = QuestionFactory(parent_section=se)
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


def several_tight_surveys(surveyname=None):
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
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Single Choice",
                qtype='SINGLECHOICE'

            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # second question
            qui = 1
            qu = QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Multiple Choice",
                qtype='MULTICHOICE'
            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # third question
            qui = 2
            qu = QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Select (Dropdown)",
                qtype='SELECT'
            )
            for opi in range(4):
                _ = OptionFactory(question=qu, text=f"text for option {opi}")

            # fourth question
            qui = 3
            QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Text input",
                qtype='TEXT'
            )

            # fifth question
            qui = 4
            QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Essay input",
                qtype='ESSAY'
            )

            # sixth question
            qui = 5
            QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Integer input",
                qtype='INTEGER'
            )

            # seventh question
            qui = 6
            QuestionFactory(
                parent_section=se,
                text=f"text for question {qui}, with original order {qui} - Email input",
                qtype='EMAIL'
            )

        surveys.append(su)
    return surveys


def pet_survey(surveyname=None):
    # allow a one-shot survey name
    if surveyname is not None:
        survey_kwargs = dict(name=surveyname)
    else:
        survey_kwargs = dict()
    su = SurveyFactory(**survey_kwargs)
    se = SectionFactory(survey=su, title=f"Pet Interest Questions")

    # interest in animals?
    int_in_animals = QuestionFactory(
        parent_section=se,
        text=f"Are you interested in animals?",
        qtype='SINGLECHOICE'
    )
    int_yes = OptionFactory(question=int_in_animals, text=f"Yes")
    OptionFactory(question=int_in_animals, text=f"No")

    # have pets?
    have_pets = QuestionFactory(
        parent_section=se,
        text=f"Do you have pets?",
        qtype='SINGLECHOICE'
    )
    have_pets_yes = OptionFactory(question=have_pets, text=f"Yes")
    OptionFactory(question=have_pets, text=f"No")

    # which pets?
    which_pets = QuestionFactory(
        parent_section=se,
        text=f"Which pets do you share your love with?",
        qtype='MULTICHOICE'
    )
    which_cat_option = OptionFactory(question=which_pets, text=f"One or more cats")
    OptionFactory(question=which_pets, text=f"One or more dogs")
    OptionFactory(question=which_pets, text=f"One or more goldfish")

    # how many cats?
    how_many_cats = QuestionFactory(
        parent_section=se,
        text=f"How many cats are your friends?",
        qtype='INTEGER'
    )

    # fewer than than 2
    happy_with_few = QuestionFactory(
        parent_section=se,
        text=f"Want more cats?",
        qtype='SINGLECHOICE'
    )
    OptionFactory(question=happy_with_few, text=f"Yes")
    OptionFactory(question=happy_with_few, text=f"No")

    # more than 5
    more_than_five = QuestionFactory(
        parent_section=se,
        text=f"Do you run a cat sanctuary?",
        qtype='SINGLECHOICE'
    )
    OptionFactory(question=more_than_five, text=f"Yes")
    OptionFactory(question=more_than_five, text=f"No")

    int_in_animals_to_have_pets =\
        DisplayByOptionsFactory(shown_element=have_pets, trigger_question=int_in_animals)
    int_in_animals_to_have_pets.options.add(int_yes)

    have_pets_to_which_pets =\
        DisplayByOptionsFactory(shown_element=which_pets, trigger_question=have_pets)
    have_pets_to_which_pets.options.add(have_pets_yes)

    which_pets_cats_to_how_many_cats =\
        DisplayByOptionsFactory(shown_element=how_many_cats, trigger_question=which_pets)
    which_pets_cats_to_how_many_cats.options.add(which_cat_option)

    DisplayByValueFactory(shown_element=happy_with_few, trigger_question=how_many_cats, value='2', condition="<=")
    DisplayByValueFactory(shown_element=more_than_five, trigger_question=how_many_cats, value='5', condition=">=")

    return su


def interest_survey(surveyname=None):
    # allow a one-shot survey name
    if surveyname is not None:
        survey_kwargs = dict(name=surveyname)
    else:
        survey_kwargs = dict()

    su = SurveyFactory(**survey_kwargs)

    # Overview Section ----------------
    se_ov = SectionFactory(survey=su, title=f"Overview")

    # interest in animals?
    int_in_animals = QuestionFactory(
        parent_section=se_ov,
        text=f"What interests you more?",
        qtype='SINGLECHOICE'
    )
    int_yes = OptionFactory(question=int_in_animals, text=f"Animals")
    int_no = OptionFactory(question=int_in_animals, text=f"Motorsport")

    # Pet Section ----------------
    se_pe = SectionFactory(survey=su, title=f"Pet Questions")

    # have pets?
    have_pets = QuestionFactory(
        parent_section=se_pe,
        text=f"Do you have pets?",
        qtype='SINGLECHOICE'
    )
    have_pets_yes = OptionFactory(question=have_pets, text=f"Yes")
    OptionFactory(question=have_pets, text=f"No")

    # which pets?
    which_pets = QuestionFactory(
        parent_section=se_pe,
        text=f"Which pets do you share your love with?",
        qtype='MULTICHOICE'
    )
    which_cat_option = OptionFactory(question=which_pets, text=f"One or more cats")
    OptionFactory(question=which_pets, text=f"One or more dogs")
    OptionFactory(question=which_pets, text=f"One or more goldfish")

    # how many cats?
    how_many_cats = QuestionFactory(
        parent_section=se_pe,
        text=f"How many cats are your friends?",
        qtype='INTEGER'
    )

    # fewer than than 2
    happy_with_few = QuestionFactory(
        parent_section=se_pe,
        text=f"Want more cats?",
        qtype='SINGLECHOICE'
    )
    OptionFactory(question=happy_with_few, text=f"Yes")
    OptionFactory(question=happy_with_few, text=f"No")

    # more than 5
    more_than_five = QuestionFactory(
        parent_section=se_pe,
        text=f"Do you run a cat sanctuary?",
        qtype='SINGLECHOICE'
    )
    OptionFactory(question=more_than_five, text=f"Yes")
    OptionFactory(question=more_than_five, text=f"No")

    # MS Section ----------------
    se_ms = SectionFactory(survey=su, title=f"Motorsport Questions")

    interested_in_ferrari = QuestionFactory(
        parent_section=se_ms,
        text=f"Do you like the Ferrari team?",
        qtype='SINGLECHOICE'
    )
    OptionFactory(question=interested_in_ferrari, text=f"Yes")
    OptionFactory(question=interested_in_ferrari, text=f"No")

    # Logic
    int_in_animals_to_have_pets =\
        DisplayByOptionsFactory(shown_element=se_pe, trigger_question=int_in_animals)
    int_in_animals_to_have_pets.options.add(int_yes)

    have_pets_to_which_pets =\
        DisplayByOptionsFactory(shown_element=which_pets, trigger_question=have_pets)
    have_pets_to_which_pets.options.add(have_pets_yes)

    which_pets_cats_to_how_many_cats =\
        DisplayByOptionsFactory(shown_element=how_many_cats, trigger_question=which_pets)
    which_pets_cats_to_how_many_cats.options.add(which_cat_option)

    DisplayByValueFactory(shown_element=happy_with_few, trigger_question=how_many_cats, value='2', condition="<=")
    DisplayByValueFactory(shown_element=more_than_five, trigger_question=how_many_cats, value='5', condition=">=")

    int_in_animals_to_ms_section =\
        DisplayByOptionsFactory(shown_element=se_ms, trigger_question=int_in_animals)
    int_in_animals_to_ms_section.options.add(int_no)

    return su




