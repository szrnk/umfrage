from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic

from surveys.models import Survey, Section, Invitation


class IndexView(generic.ListView):
    model = Survey
    template_name = 'surveys/index.html'


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/detail.html'

    def sections(self):
        return Section.objects.filter(survey_id=self.object.id)


class InvitationView(generic.RedirectView):
    model = Invitation

    def get(self, request, token):
        """
        Lookup the token, and store the key info in the session
        :param request:
        :param token:
        :return:
        """
        invitation = Invitation.objects.filter(token=token).first()
        request.session['department_id'] = invitation.department.id
        request.session['survey_id'] = invitation.survey.id
        request.session['invitation_token'] = token
        messages.add_message(request, messages.INFO, 'Thank you for coming. Please login, or create a new login.')
        return HttpResponseRedirect('/accounts/login')


class CurrentSurveyView(generic.DetailView):
    template_name = 'surveys/current.html'

    def get_object(self):
        survey_id = self.request.session.get('survey_id')
        survey = get_object_or_404(Survey, pk=survey_id)
        return survey


class MySurveysView(generic.ListView):
    template_name = 'surveys/mysurveys.html'

    def get_queryset(self):
        return self.request.user.surveys.all()

