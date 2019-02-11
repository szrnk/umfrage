from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField, MultipleChoiceField, CharField, IntegerField, EmailField

from surveys.models import Option, Answer, Question, Value


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
        self.option_field = False
        if self.question.qtype == "MULTICHOICE":
            self.single = False
            self.option_field = True
            self.fields[self.field_name] = MultipleChoiceField(
                label=self.question.text,
                choices=options,
                widget=forms.CheckboxSelectMultiple(),
                required=False,
            )
        elif self.question.qtype == "SINGLECHOICE":
            self.single = True
            self.option_field = True
            self.fields[self.field_name] = ChoiceField(
                label=self.question.text,
                choices=options,
                widget=forms.RadioSelect(),
                required=False,
            )
        elif self.question.qtype == "SELECT":
            self.single = True
            self.option_field = True
            self.fields[self.field_name] = ChoiceField(
                label=self.question.text,
                choices=options,
                required=False,
            )
        elif self.question.qtype == "TEXT":
            self.single = True
            self.fields[self.field_name] = CharField(
                label=self.question.text,
                required=False,
            )
        elif self.question.qtype == "ESSAY":
            self.single = True
            self.fields[self.field_name] = CharField(
                label=self.question.text,
                widget=forms.Textarea,
                required=False,
            )
        elif self.question.qtype == "INTEGER":
            self.single = True
            self.fields[self.field_name] = IntegerField(
                label=self.question.text,
                required=False,
            )
        elif self.question.qtype == "EMAIL":
            self.single = True
            self.fields[self.field_name] = EmailField(
                label=self.question.text,
                required=False,
            )
        else:
            raise AttributeError("Bad field type")
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
            if self.option_field:
                values = [str(o.id) for o in answer.options.all()]
                if self.single:
                    if values:
                        return values[0]
                    return ''
                return values
            else:
                return answer.value.text
        return ''

    def save(self):
        qid = int(self.cleaned_data["qid"])
        question = Question.objects.filter(pk=qid).first()

        if self.option_field:
            option_ids = self.cleaned_data[self.field_name]
            if type(option_ids) == str:
                if bool(option_ids):
                    option_ids = [option_ids]
                else:
                    option_ids = []
            option_ids = [int(oid) for oid in option_ids]
            options = Option.objects.filter(id__in=option_ids)
        else:
            val = self.cleaned_data[self.field_name]
            val = Value.objects.create(text=val)

        earlier = Answer.objects.filter(
            question_id=qid, department_id=self.department.pk
        ).first()
        if earlier:
            earlier.delete()

        answer = Answer.objects.create(question=question, department=self.department)
        if self.option_field:
            for option in options:
                answer.options.add(option)
        else:
            answer.value = val
            answer.save()
