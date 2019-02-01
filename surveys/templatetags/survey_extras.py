# survey_extras.py file
from django import template
from ..forms import FlexiForm

register = template.Library()


@register.simple_tag
def get_survey_question_form(survey, department, question):
    return FlexiForm(survey=survey, department=department, question=question)
