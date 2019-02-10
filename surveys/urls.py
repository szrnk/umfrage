from django.urls import path

from . import views
from .models import Option, Question

app_name = "surveys"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("invite/<str:token>", views.InvitationView.as_view(), name="invite"),
    path("current/", views.CurrentSurveyView.as_view(), name="current"),
    path("myinvitations/", views.MyInvitationsView.as_view(), name="myinvitations"),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path('linked_options/', views.LinkedOptionsView.as_view(model=Option), name='linked_options'),
    path('trigger_questions/', views.TriggerQuestionView.as_view(model=Question), name='trigger_questions'),
]


