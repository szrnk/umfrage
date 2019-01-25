from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField
from django.shortcuts import get_object_or_404

from correspondents.models import Department
from surveys.models import Option, Answer, Survey
from surveys.progress import Progress


class FlexiForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        options = [(o.id, o.text) for o in self.question.options()]
        field_name = f'option'
        self.fields[field_name] = ChoiceField(label=self.question.text, choices=options, widget=forms.RadioSelect(), required=False)

    def clean(self):
        if not self.cleaned_data['option']:
            raise ValidationError('Missing option')

    def save(self, request):

        option = Option.objects.filter(id=self.cleaned_data['option']).first()
        survey_id = request.session.get('survey_id')
        survey = get_object_or_404(Survey, pk=survey_id)

        department_id = request.session['department_id']
        department = Department.objects.filter(id=department_id).first()

        earlier = Answer.objects.filter(question_id=self.question.pk, department_id=department.pk).first()
        if earlier:
            earlier.delete()

        Answer.objects.create(question=self.question, department=department, option=option)

        Progress(request, survey).advance(request)
