from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from correspondents.models import Department
from surveys.forms import FlexiForm
from surveys.models import Survey, Section, Invitation, Option, Answer

from .progress import Progress


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


class CurrentSurveyView(LoginRequiredMixin, generic.DetailView):
    template_name = 'surveys/current.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = None

    def get_object(self):
        survey_id = self.request.session.get('survey_id')
        survey = Survey.objects.filter(pk=survey_id).first()
        if survey is not None:
            # This has the side effect of ensuring session tracking for question and section
            self.progress = Progress(self.request, survey)
        return survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['object'] is None:
            # We could not get a current survey, skip
            return context
        survey = context['object']
        context['progress'] = self.progress

        department_id = self.request.session.get('department_id')
        department = get_object_or_404(Department, pk=department_id)
        context['department'] = department

        section_index = self.progress.get_data()[str(survey.id)]['section_index']
        section = survey.sections()[section_index]
        question_index = self.progress.get_data()[str(survey.id)]['question_index']
        question = section.question_set.all()[question_index]

        form = FlexiForm(question=question)
        context['form'] = form

        context['progress'] = self.progress.get_data()[str(survey.id)]
        return context


def post_current(request):
    survey_id = request.session.get('survey_id')
    progress = request.session.get('progress')
    survey = get_object_or_404(Survey, pk=survey_id)
    department_id = request.session['department_id']
    department = Department.objects.filter(id=department_id).first()

    # TODO refac
    section_index = progress[str(survey.id)]['section_index']
    section = survey.sections()[section_index]
    question_index = progress[str(survey.id)]['question_index']
    question = section.question_set.all()[question_index]

    #TODO: check the user is in the department of the invite

    if request.method == "POST":
        form = FlexiForm(request.POST, question=question)
        if form.is_valid():
            option = Option.objects.filter(id=form.cleaned_data['option']).first()

            earlier = Answer.objects.filter(question_id=question.pk, department_id=department.pk).first()
            if earlier:
                earlier.delete()

            Answer.objects.create(question=question, department=department, option=option)

            Progress(request, survey).advance(request)

            return HttpResponseRedirect(reverse('surveys:current'))
        # else:
        #     form = FlexiForm(question=question)

        return render(request, 'surveys/current.html', {'form': form, 'survey': survey, 'department': department})
    else:
        return HttpResponseRedirect(reverse('surveys:current'))


class MySurveysView(generic.ListView):
    template_name = 'surveys/mysurveys.html'

    def get_queryset(self):
        return self.request.user.surveys.all()


class SurveySequence(object):

    def __init__(self, survey):
        self.survey = survey
        self.sequence = self.build()

    def build(self):
        ret = []
        return ret
        # for section in self.survey.section_set:
        #     for question in section.question_set:
