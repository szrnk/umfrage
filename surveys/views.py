from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from surveys.models import Survey


class IndexView(generic.ListView):
    model = Survey
    template_name = 'surveys/index.html'


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'

