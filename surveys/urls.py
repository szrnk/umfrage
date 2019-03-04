from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .models import Option, Question

SR = staff_member_required
LR = login_required

app_name = "surveys"
urlpatterns = [
    #path("", views.IndexView.as_view(), name="index"),
    #path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/as_table", SR(views.SurveyTableView.as_view()), name="table"),
    path("<int:pk>/as_csv", SR(views.survey_csv_file_view), name="csvfile"),
    path("<int:pk>/as_xlsx", SR(views.survey_xlsx_file_view), name="xlsxfile"),

    path("invite/<str:token>", views.InvitationView.as_view(), name="invite"),
    path("current/", views.CurrentSurveyView.as_view(), name="current"),
    path("myinvitations/", LR(views.MyInvitationsView.as_view()), name="myinvitations"),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('linked_options/', LR(views.LinkedOptionsView.as_view(model=Option)), name='linked_options'),
    path('trigger_questions_options/', LR(views.TriggerQuestionView.as_view(model=Question)), name='trigger_questions', kwargs=dict(type='options')),
    path('trigger_questions_value/', LR(views.TriggerQuestionView.as_view(model=Question)), name='trigger_questions', kwargs=dict(type='value')),
]


