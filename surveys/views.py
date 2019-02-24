from dal_select2.views import Select2QuerySetView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView

from correspondents.models import Department
from surveys.forms import FlexiForm
from surveys.models import Survey, Section, Invitation, Option, Answer, Question, Element, OPTION_CHOICES, VALUE_CHOICES
from surveys.reports import create_survey_output, create_survey_html_output, create_survey_csv
from pyquery import PyQuery as pq

from .progress import Progress


class IndexView(generic.ListView):
    model = Survey
    template_name = "surveys/index.html"


class DetailView(generic.DetailView):
    model = Survey
    template_name = "surveys/detail.html"

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
        request.session["department_id"] = invitation.department.id
        request.session["survey_id"] = invitation.survey.id
        request.session["invitation_token"] = token
        if request.user.is_authenticated:
            user = request.user
            # user.surveys.add(invitation.survey)
            user.invitations.add(invitation)
            user.save()

            messages.add_message(
                request,
                messages.INFO,
                f"Your current Survey and Department are now:: "
                f"Survey: {invitation.survey}, Department: {invitation.department}",
            )
            return HttpResponseRedirect(reverse("surveys:current"))
        messages.add_message(
            request,
            messages.INFO,
            "Thank you for coming. Please login, or create a new login.",
        )
        return HttpResponseRedirect("/accounts/login")


class CurrentSurveyView(LoginRequiredMixin, generic.DetailView):
    template_name = "surveys/current.html"
    # FormMixin
    form_class = FlexiForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.progress = None
        self.object = None

    def get_success_url(self):
        # TODO: branch at end of survey
        return reverse("surveys:current")

    def get_object(self):
        survey_id = self.request.session.get("survey_id")
        survey = Survey.objects.filter(pk=survey_id).first()
        self.survey = survey
        # if survey is not None:
        #     # This has the side effect of ensuring session tracking for question and section
        #     self.progress = Progress(self.request, survey)
        return survey

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["object"] is None:
            # We could not get a current survey, skip
            return context
        survey = context["object"]
        context["progress"] = self.progress
        department_id = self.request.session.get("department_id")
        department = get_object_or_404(Department, pk=department_id)
        context["department"] = department
        # context['progress'] = self.progress.get_data()[str(survey.id)]
        return context

    def get_form_kwargs(self):
        # kwargs = super().get_form_kwargs()
        kwargs = {}
        request = self.request
        survey_id = request.session.get("survey_id")
        #progress = request.session.get("progress")
        survey = get_object_or_404(Survey, pk=survey_id)
        department_id = request.session["department_id"]
        department = Department.objects.filter(id=department_id).first()
        if 0:
            section_index = progress[str(survey.id)]["section_index"]
            section = survey.sections()[section_index]
            question_index = progress[str(survey.id)]["question_index"]
            question = section.question_set.all()[question_index]
        else:
            qid = self.request.POST["qid"]
            question = Question.objects.filter(pk=qid).first()

        kwargs["question"] = question
        kwargs["department"] = department
        kwargs["survey"] = survey

        if self.request.method in ("POST", "PUT"):
            kwargs.update({"data": self.request.POST, "files": self.request.FILES})

        return kwargs

    def get_form(self):
        kwargs = self.get_form_kwargs()
        return FlexiForm(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            # TODO - find a way to get errors on the question
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class MyInvitationsView(generic.ListView):
    template_name = "surveys/myinvitations.html"

    def get_queryset(self):
        return self.request.user.invitations.all()


class LinkedOptionsView(Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Option.objects.none()
        trigger_question = self.forwarded.get('trigger_question', None)
        qs = Option.objects.all()
        if trigger_question:
            qs = qs.filter(question_id=trigger_question)
        return qs


class TriggerQuestionView(Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_staff:
            return Question.objects.none()
        shown_element = self.forwarded.get('shown_element', None)
        qs = Element.objects.none()
        if shown_element:
            shown_element = int(shown_element)
            question = Question.objects.filter(id=shown_element).first()
            if question is not None:
                survey = question.parent_section.survey
            else:
                section = Section.objects.filter(id=shown_element).first()
                survey = section.survey
            question_type = self.kwargs.get('type', None)
            qs = Question.objects.filter(parent_section__survey__exact=survey.id)
            if question_type == 'options':
                qs = qs.filter(qtype__in=OPTION_CHOICES)
            elif question_type == 'value':
                qs = qs.filter(qtype__in=VALUE_CHOICES)
            qs.exclude(id__in=[shown_element])
            if self.q:
                qs = qs.filter(text__istartswith=self.q)
        return qs


class SurveyTableView(TemplateView):
    template_name = "surveys/survey_summary_table.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = get_object_or_404(Survey, pk=kwargs['pk'])
        table = create_survey_html_output(survey)
        context['survey'] = survey
        context['table'] = table
        return context


def survey_csv_file_view(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    csv = create_survey_csv(survey)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{survey.name}.csv"'
    response.write(csv)
    return response
