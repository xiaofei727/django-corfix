from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup_post', views.signup_post, name='signup_post'),
    path('signin_post', views.signin_post, name='signin_post'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('projects', views.projects, name='projects'),
    path('<int:client_id>/company_profile', views.company_profile, name='company_profile'),
]