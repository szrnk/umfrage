from django.views import generic

from .models import Hospital


class IndexView(generic.ListView):
    model = Hospital
    template_name = 'correspondents/index.html'


class DetailView(generic.DetailView):
    model = Hospital
    template_name = 'correspondents/detail.html'

    # def questions(self):
    #     return Hospital.objects.filter(survey_id=self.object.id)

