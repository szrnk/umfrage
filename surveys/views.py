from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from correspondents.models import Department
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
        if request.user.is_authenticated:
            user = request.user
            user.department_id = invitation.department.id
            user.surveys.add(invitation.survey)

            messages.add_message(request, messages.INFO, f'Your current Survey and Department are now:: '
                                 f'Survey: {invitation.survey}, Department: {invitation.department}')
            return HttpResponseRedirect(reverse('surveys:current'))
        messages.add_message(request, messages.INFO, 'Thank you for coming. Please login, or create a new login.')
        return HttpResponseRedirect('/accounts/login')


class CurrentSurveyView(generic.DetailView):
    template_name = 'surveys/current.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.this_section = None
        self.this_question = None

    def get_object(self):
        survey_id = self.request.session.get('survey_id')
        survey = get_object_or_404(Survey, pk=survey_id)
        self.this_section = survey.section_set.first()
        self.this_question = survey.section_set.first().question_set.first()
        return survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_sections'] = ['Section First', 'Section Second']
        context['this_section'] = self.this_section
        context['this_question'] = self.this_question
        context['future_sections'] = ['Section Later', 'Section Last']
        department_id = self.request.session.get('department_id')
        department = get_object_or_404(Department, pk=department_id)
        context['department'] = department
        return context


class MySurveysView(generic.ListView):
    template_name = 'surveys/mysurveys.html'

    def get_queryset(self):
        return self.request.user.surveys.all()
