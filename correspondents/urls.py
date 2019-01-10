from django.urls import path

from . import views

urlpatterns = [

    # ex: /correspondents
    path('', views.IndexView.as_view(), name='hospitalindex'),

    # ex: /correspondents/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

]
