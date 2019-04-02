from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup_post', views.signup_post, name='signup_post'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('projects', views.projects, name='projects'),
]