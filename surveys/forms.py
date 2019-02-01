from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, MultipleChoiceField

from surveys.models import Option, Answer, Question


class FlexiForm(forms.Form):
    """
    Form for a single question, with single selection
    """

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop("question", None)
        self.department = kwargs.pop("department", None)
        self.survey = kwargs.pop("survey", None)
        super().__init__(*args, **kwargs)
        options = [(o.id, o.text) for o in self.question.options()]
        self.field_name = f"option"
        if self.question.qtype == "MULTI":
            self.single = False
            self.fields[self.field_name] = MultipleChoiceField(
                label=self.question.text,
                choices=options,
                widget=forms.CheckboxSelectMultiple(),
                required=False,
            )
        else:
            self.single = True
            self.fields[self.field_name] = ChoiceField(
                label=self.question.text,
                choices=options,
                widget=forms.RadioSelect(),
                required=False,
            )
        self.fields["qid"] = forms.CharField(
            label="qid", max_length=10, widget=forms.HiddenInput()
        )
        self.fields[self.field_name].help_text = self.question.help_text

    def get_initial_for_field(self, field, field_name):
        if field_name == "qid":
            return str(self.question.pk)
        answer = Answer.objects.filter(
            question_id=self.question.pk, department_id=self.department.pk
        ).first()
        if answer is not None:
            values = [str(o.id) for o in answer.options.all()]
            if self.single:
                if values:
                    return values[0]
                return ''
            return values
        return ''

    def clean(self):
        if not self.cleaned_data[self.field_name]:
            raise ValidationError("Missing option")

    def save(self):
        qid = int(self.cleaned_data["qid"])
        question = Question.objects.filter(pk=qid).first()
        option_ids = self.cleaned_data[self.field_name]
        if type(option_ids) == str:
            option_ids = [option_ids]
        option_ids = [int(oid) for oid in option_ids]
        options = Option.objects.filter(id__in=option_ids)
        earlier = Answer.objects.filter(
            question_id=qid, department_id=self.department.pk
        ).first()
        if earlier:
            earlier.delete()
        answer = Answer.objects.create(question=question, department=self.department)
        for option in options:
            answer.options.add(option)
