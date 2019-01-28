from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField

from surveys.models import Option, Answer, Question
from surveys.progress import Progress


class FlexiForm(forms.Form):
    """
    Form for a single question, with multiple options
    """

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop("question", None)
        self.department = kwargs.pop("department", None)
        self.survey = kwargs.pop("survey", None)
        super().__init__(*args, **kwargs)
        options = [(o.id, o.text) for o in self.question.options()]
        self.field_name = f"option"
        self.fields[self.field_name] = ChoiceField(
            label=self.question.text,
            choices=options,
            widget=forms.RadioSelect(),
            required=False,
        )
        self.fields["qid"] = forms.CharField(
            label="qid", max_length=10, widget=forms.HiddenInput()
        )

    def get_initial_for_field(self, field, field_name):
        if field_name == "qid":
            return str(self.question.pk)
        answer = Answer.objects.filter(
            question_id=self.question.pk, department_id=self.department.pk
        ).first()
        if answer is not None:
            return str(answer.option_id)
        return ""

    def clean(self):
        if not self.cleaned_data[self.field_name]:
            raise ValidationError("Missing option")

    def save(self, request):
        qid = int(self.cleaned_data["qid"])
        question = Question.objects.filter(pk=qid).first()
        option = Option.objects.filter(id=self.cleaned_data[self.field_name]).first()
        earlier = Answer.objects.filter(
            question_id=qid, department_id=self.department.pk
        ).first()
        if earlier:
            earlier.delete()
        Answer.objects.create(
            question=question, department=self.department, option=option
        )
        Progress(request, self.survey).advance(request)
