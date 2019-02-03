import pytest
from django.conf import settings
from core.conftest import user

from core.users.forms import UserCreationForm
from core.users.tests.factories import UserFactory
from correspondents.models import Department
from surveys.forms import FlexiForm
from surveys.tests.factories import OptionFactory
from surveys.models import Question, Option, Survey, Answer

pytestmark = pytest.mark.django_db


class TestFlexiForm:
    def test_single_choice(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):

        department.user_set.add(user)
        [question.option_set.add(OptionFactory()) for i in range(3)]
        question.qtype = "SINGLECHOICE"
        first_option = question.option_set.first()
        form = FlexiForm(
            data={"option": str(first_option.id), "qid": str(question.id)},
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        assert form.cleaned_data["option"] == str(form.question.option_set.first().id)
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opt = ans.options.first()
        assert opt.pk == first_option.pk
        assert form.as_p().count('radio') >= 3

    def test_multiple_choice(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        [question.option_set.add(OptionFactory()) for _ in range(3)]
        question.qtype = "MULTICHOICE"
        first_option = question.option_set.all()[0]
        second_option = question.option_set.all()[1]
        form = FlexiForm(
            data={
                "option": [str(first_option.id), str(second_option.id)],
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        assert form.cleaned_data["option"] == [
            str(first_option.id),
            str(second_option.id),
        ]
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 2
        assert form.as_p().count('checkbox') >= 3

    def test_select(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        [question.option_set.add(OptionFactory()) for _ in range(3)]
        question.qtype = "SELECT"
        first_option = question.option_set.all()[0]
        form = FlexiForm(
            data={
                "option": str(first_option.id),
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        str(form.question.option_set.first().id)
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 1
        assert form.as_p().count('option') >= 3

    def test_text(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "TEXT"
        TEST_TEXT = 'something here'
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 0
        assert ans.value.text == TEST_TEXT

    def test_essay(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "ESSAY"
        TEST_TEXT = """something here
        and there"""
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 0
        assert ans.value.text == TEST_TEXT

    def test_integer_compliant(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "INTEGER"
        TEST_TEXT = '123'
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 0
        assert ans.value.text == TEST_TEXT

    def test_integer_non_compliant(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "INTEGER"
        TEST_TEXT = '123ABC'
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert not form.is_valid()

    def test_email_compliant(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "EMAIL"
        TEST_TEXT = 'abc@gmail.com'
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert form.is_valid()
        form.save()
        ans = Answer.objects.filter(department__pk=department.pk).first()
        opts = ans.options.all()
        assert len(opts) == 0
        assert ans.value.text == TEST_TEXT

    def test_email_non_compliant(
        self,
        user: settings.AUTH_USER_MODEL,
        survey: Survey,
        department: Department,
        question: Question,
    ):
        department.user_set.add(user)
        question.qtype = "EMAIL"
        TEST_TEXT = 'gmail.com'
        form = FlexiForm(
            data={
                "option": TEST_TEXT,
                "qid": str(question.id),
            },
            survey=survey,
            department=department,
            question=question,
        )
        assert not form.is_valid()


def test_explore_question_form(
    user: settings.AUTH_USER_MODEL,
    survey: Survey,
    department: Department,
    question: Question,
):
    department.user_set.add(user)
    [question.option_set.add(OptionFactory()) for _ in range(3)]
    form = FlexiForm(survey=survey, department=department, question=question)
    ff = form.as_p()
    assert 'type="radio"' in ff
