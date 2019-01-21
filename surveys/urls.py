from django.urls import path

from . import views

app_name = 'surveys'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('invite/<str:token>', views.InvitationView.as_view(), name='invite'),
    path('current/', views.CurrentSurveyView.as_view(), name='current'),
    path('mysurveys/', views.MySurveysView.as_view(), name='mysurveys'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
