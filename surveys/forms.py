from django import forms
from django.core.exceptions import ValidationError
from django.forms import ChoiceField


class FlexiForm(forms.Form):

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        options = [(o.id, o.text) for o in question.options()]
        field_name = f'option'
        self.fields[field_name] = ChoiceField(label=question.text, choices=options, widget=forms.RadioSelect(), required=False)

    def clean(self):
        if not self.cleaned_data['option']:
            raise ValidationError('Missing option')
       #  options = set()
       #  i = 0
       #  field_name = 'interest_%s' % (i,)
       #  while self.cleaned_data.get(field_name):
       #     interest = self.cleaned_data[field_name]
       #     # if interest in interests:
       #     #     self.add_error(field_name, 'Duplicate')
       #     # else:
       #     #     interests.add(interest)
       #     i += 1
       #     field_name = 'interest_%s' % (i,)
       # #self.cleaned_data[“interests”] = interests

    def save(self):
        question = self.instance
        pass

"""

    def save(self):
        profile = self.instance
        profile.first_name = self.cleaned_data[“first_name”]
        profile.last_name = self.cleaned_data[“last_name”]

        profile.interest_set.all().delete()
        for interest in self.cleaned_data[“interests”]:
           ProfileInterest.objects.create(
               profile=profile,
               interest=interest,
           )
           """


"""


TODO

Add a form POST url


"""
