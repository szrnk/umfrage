from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from surveys.models import Survey, Section, Question, Option


class IndexView(generic.ListView):
    model = Survey
    template_name = 'surveys/index.html'


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'

    def sections(self):
        return Section.objects.filter(survey_id=self.object.id)

