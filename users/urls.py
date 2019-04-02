from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('projects', views.projects, name='projects'),
]