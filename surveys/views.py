from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from surveys.models import Survey, Question, Option


class IndexView(generic.ListView):
    model = Survey
    template_name = 'surveys/index.html'


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'

    def questions(self):
        return Question.objects.filter(survey_id=self.object.id)

