import pytest

from correspondents.tests.factories import DepartmentFactory
from surveys.models import Option, Survey, DisplayByOptions, Answer, Value
from surveys.tests.factories import SurveyFactory, SectionFactory, QuestionFactory, OptionFactory, DisplayByOptionsFactory, \
    DisplayByValueFactory

pytestmark = pytest.mark.django_db


def test_option_parentage(option: Option):
    assert option.question is not None
    assert option.question.section is not None
    assert option.question.section.survey is not None


class TestDisplayLogic:

    def test_display_by_options(self):
        dep = DepartmentFactory()
        su = SurveyFactory()
        se = SectionFactory(survey=su)
        trigger_question = QuestionFactory(section=se, text='trigger')
        last_option = None
        first_option = None
        for opi in range(4):
            last_option = OptionFactory(question=trigger_question)
            if not first_option:
                first_option = last_option
        shown_question = QuestionFactory(section=se, text='show')
        dl = DisplayByOptionsFactory(trigger_question=trigger_question, shown_question=shown_question)
        dl.options.add(last_option)

        # not yet triggered - no answer
        assert(not shown_question.triggered())

        ans = Answer.objects.create(question=trigger_question, department=dep)
        ans.options.add(last_option)

        # now there is an answer including the option, so the shown_question is triggered
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different option, and the Q is again not triggered
        dl.options.clear()
        dl.options.add(first_option)
        assert(not shown_question.triggered())

    def test_display_by_value_conditions(self):
        dep = DepartmentFactory()
        su = SurveyFactory()
        se = SectionFactory(survey=su)
        trigger_question = QuestionFactory(section=se, text='trigger')
        shown_question = QuestionFactory(section=se, text='show')
        dl = DisplayByValueFactory(trigger_question=trigger_question, shown_question=shown_question, value='42', condition='==')

        # not yet triggered - no answer
        assert(not shown_question.triggered())

        ans = Answer.objects.create(question=trigger_question, department=dep)
        ans.value = Value.objects.create(text='42')
        ans.save()

        # now there is an answer including the option, so the shown_question is triggered
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different value, and the Q is again not triggered
        dl.value = '43'
        dl.save()
        assert(not shown_question.triggered())

        # now let's change the dl, to trigger on a different condition
        dl.condition = '<='
        dl.save()
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different condition
        dl.condition = '>='
        dl.save()
        ans.value = Value.objects.create(text='44')
        ans.save()
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different condition
        dl.condition = 'contains'
        dl.value = '4'
        dl.save()
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different condition
        dl.condition = 'containsNoCase'
        dl.value = 'abc'
        dl.save()
        ans.value = Value.objects.create(text='XXYABCDEFG')
        ans.save()
        assert(shown_question.triggered())

        # now let's change the dl, to trigger on a different condition
        dl.condition = 'containsNoCase'
        dl.value = 'abc'
        dl.save()
        ans.value = Value.objects.create(text='PPPPPP')
        ans.save()
        assert(not shown_question.triggered())



        
        




